from datetime import date
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.academic import Course, Timetable, AcademicAttendance, Exam, ExamMark
from app.models.student import Trade, ParadeSubmission
from app.repositories.academic import timetable_repo, attendance_repo, exam_repo, exam_mark_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.academic import TimetableCreate, TimetableAttendanceUpdateRequest, ExamMarkUpdateRequest

class AcademicService:
    def create_timetable_entry(self, db: Session, tt_in: TimetableCreate, user_id: str, ip: str, ua: str) -> Timetable:
        # Check if period is already booked for this course on this date
        existing = db.query(Timetable).filter(
            Timetable.course_id == tt_in.course_id,
            Timetable.date == tt_in.date,
            Timetable.period_number == tt_in.period_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Timetable period {tt_in.period_number} is already scheduled for this course on {tt_in.date}"
            )

        db_tt = Timetable(
            course_id=tt_in.course_id,
            date=tt_in.date,
            period_number=tt_in.period_number,
            subject_id=tt_in.subject_id,
            lesson_id=tt_in.lesson_id,
            instructor_id=tt_in.instructor_id,
            location=tt_in.location
        )
        created_tt = timetable_repo.create(db, obj_in=db_tt)
        audit_repo.create_log(
            db, user_id, "TIMETABLE_CREATED", ip, ua,
            f"Scheduled course {tt_in.course_id} on {tt_in.date} period {tt_in.period_number}"
        )
        return created_tt

    def update_timetable_attendance(self, db: Session, request: TimetableAttendanceUpdateRequest, user_id: str, ip: str, ua: str) -> List[AcademicAttendance]:
        tt = timetable_repo.get(db, request.timetable_id)
        if not tt:
            raise HTTPException(status_code=404, detail="Timetable session slot not found")

        # Verify Parade State Approval for course trade and date
        course = db.query(Course).filter(Course.id == tt.course_id).first()
        trade_obj = db.query(Trade).filter(Trade.id == course.trade_id).first() if course and course.trade_id else None
        trade_label = trade_obj.label if trade_obj else (course.trade_name if course else 'General')

        ps_sub = None
        if trade_label:
            ps_sub = db.query(ParadeSubmission).filter(
                ParadeSubmission.date == tt.date,
                ParadeSubmission.trade == trade_label
            ).first()
            if not ps_sub and trade_obj:
                ps_sub = db.query(ParadeSubmission).filter(
                    ParadeSubmission.date == tt.date,
                    ParadeSubmission.trade == trade_obj.code
                ).first()

        if not ps_sub or ps_sub.status != 'APPROVED':
            raise HTTPException(
                status_code=400,
                detail="Today's Parade State has not been approved. Classroom attendance cannot be finalized until the Parade State is approved."
            )

        valid_statuses = {'PRESENT', 'ABSENT', 'LATE', 'SICK_REPORT', 'COURSE_VISIT', 'LEAVE', 'HOSPITAL', 'EXCUSED'}

        updated_records = []
        try:
            for record in request.records:
                student = student_repo.get(db, record.student_id)
                if not student:
                    continue

                raw_status = (record.status or 'PRESENT').strip().upper()
                norm_status = raw_status if raw_status in valid_statuses else 'PRESENT'

                att = db.query(AcademicAttendance).filter(
                    AcademicAttendance.timetable_id == request.timetable_id,
                    AcademicAttendance.student_id == record.student_id
                ).first()

                if att:
                    att.status = norm_status
                    att.remarks = record.remarks
                else:
                    att = AcademicAttendance(
                        timetable_id=request.timetable_id,
                        student_id=record.student_id,
                        status=norm_status,
                        remarks=record.remarks
                    )
                    db.add(att)
                updated_records.append(att)

            db.commit()
            audit_repo.create_log(
                db, user_id, "TIMETABLE_ATTENDANCE_UPDATED", ip, ua,
                f"Updated classroom attendance registry for timetable session ID {request.timetable_id} ({len(updated_records)} trainees)"
            )
            return updated_records
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save bulk classroom attendance: {str(e)}")

    def enter_exam_marks(self, db: Session, request: ExamMarkUpdateRequest, user_id: str, ip: str, ua: str) -> List[ExamMark]:
        exam = exam_repo.get(db, request.exam_id)
        if not exam or exam.deleted_at:
            raise HTTPException(status_code=404, detail="Examination slot not found")

        results = []
        for record in request.records:
            student = student_repo.get(db, record.student_id)
            if not student:
                continue

            status = "Absent"
            if record.marks_obtained >= 0:
                status = "Pass" if record.marks_obtained >= exam.pass_marks else "Fail"

            db_mark = db.query(ExamMark).filter(
                ExamMark.exam_id == request.exam_id,
                ExamMark.student_id == record.student_id
            ).first()

            if db_mark:
                db_mark.marks_obtained = record.marks_obtained
                db_mark.status = status
                db_mark.remarks = record.remarks
                db_mark.entered_by = user_id
            else:
                db_mark = ExamMark(
                    exam_id=request.exam_id,
                    student_id=record.student_id,
                    marks_obtained=record.marks_obtained,
                    status=status,
                    remarks=record.remarks,
                    entered_by=user_id
                )
                db.add(db_mark)
            results.append(db_mark)

        db.commit()
        audit_repo.create_log(
            db, user_id, "EXAM_MARKS_UPDATED", ip, ua,
            f"Entered/updated grades for exam ID {request.exam_id} for {len(results)} trainees"
        )
        return results

academic_service = AcademicService()
