from datetime import date, datetime
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.academic import Course, Timetable, AcademicAttendance, Exam, ExamMark
from app.models.student import Trade, ParadeSubmission, ParadeState
from app.repositories.academic import timetable_repo, attendance_repo, exam_repo, exam_mark_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.academic import TimetableCreate, TimetableAttendanceUpdateRequest, ExamMarkUpdateRequest, ExamEligibilityOverrideRequest

class AcademicService:
    def create_timetable_entry(self, db: Session, tt_in: TimetableCreate, user_id: str, ip: str, ua: str) -> Timetable:
        # Check if course exists and date is within configured course start and end dates
        course = db.query(Course).filter(Course.id == tt_in.course_id).first()
        if course:
            if course.start_date and tt_in.date < course.start_date:
                raise HTTPException(
                    status_code=400,
                    detail=f"Timetable date ({tt_in.date.strftime('%d.%m.%Y')}) cannot be earlier than course start date ({course.start_date.strftime('%d.%m.%Y')})."
                )
            if course.end_date and tt_in.date > course.end_date:
                raise HTTPException(
                    status_code=400,
                    detail=f"Timetable date ({tt_in.date.strftime('%d.%m.%Y')}) cannot be later than course end date ({course.end_date.strftime('%d.%m.%Y')})."
                )

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

    def get_exam_result_sheet(self, db: Session, exam_id: str) -> Dict[str, Any]:
        sheet = exam_repo.get_result_sheet(db, exam_id)
        if not sheet:
            raise HTTPException(status_code=404, detail="Examination slot not found")
        return sheet

    def override_exam_eligibility(
        self, db: Session, exam_id: str, request: ExamEligibilityOverrideRequest,
        user_id: str, ip: str, ua: str
    ) -> Dict[str, Any]:
        exam = exam_repo.get(db, exam_id)
        if not exam or exam.deleted_at:
            raise HTTPException(status_code=404, detail="Examination slot not found")

        student = student_repo.get(db, request.student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        if not request.reason or not request.reason.strip():
            raise HTTPException(status_code=400, detail="A valid override justification reason is mandatory")

        p_state = db.query(ParadeState).filter(
            ParadeState.student_id == student.id,
            ParadeState.date == exam.date
        ).first()
        orig_status = p_state.status if p_state else 'Unknown'

        db_mark = db.query(ExamMark).filter(
            ExamMark.exam_id == exam_id,
            ExamMark.student_id == student.id
        ).first()

        if db_mark:
            db_mark.is_overridden = True
            db_mark.override_reason = request.reason.strip()
            db_mark.overridden_by = user_id
            db_mark.overridden_at = datetime.utcnow()
            db_mark.original_parade_status = orig_status
            if request.remarks:
                db_mark.remarks = request.remarks.strip()
        else:
            db_mark = ExamMark(
                exam_id=exam_id,
                student_id=student.id,
                marks_obtained=0.0,
                status="Pending",
                remarks=request.remarks.strip() if request.remarks else None,
                entered_by=user_id,
                is_overridden=True,
                override_reason=request.reason.strip(),
                overridden_by=user_id,
                overridden_at=datetime.utcnow(),
                original_parade_status=orig_status
            )
            db.add(db_mark)

        db.commit()
        audit_repo.create_log(
            db, user_id, "EXAM_ELIGIBILITY_OVERRIDDEN", ip, ua,
            f"Authorized override for trainee {student.service_number} ({student.full_name}) for exam {exam_id}. Reason: {request.reason.strip()}"
        )

        return self.get_exam_result_sheet(db, exam_id)

    def enter_exam_marks(self, db: Session, request: ExamMarkUpdateRequest, user_id: str, ip: str, ua: str) -> List[ExamMark]:
        exam = exam_repo.get(db, request.exam_id)
        if not exam or exam.deleted_at:
            raise HTTPException(status_code=404, detail="Examination slot not found")

        # Load course and trade
        course = db.query(Course).filter(Course.id == exam.course_id).first()
        trade_obj = db.query(Trade).filter(Trade.id == course.trade_id).first() if course and course.trade_id else None
        trade_label = trade_obj.label if trade_obj else (getattr(course, 'trade_name', None))

        # Check trade parade submission status for exam date
        ps_sub = None
        if trade_label:
            ps_sub = db.query(ParadeSubmission).filter(
                ParadeSubmission.date == exam.date,
                ParadeSubmission.trade == trade_label
            ).first()
            if not ps_sub and trade_obj:
                ps_sub = db.query(ParadeSubmission).filter(
                    ParadeSubmission.date == exam.date,
                    ParadeSubmission.trade == trade_obj.code
                ).first()

        is_trade_parade_approved = (ps_sub.status == 'APPROVED') if ps_sub else False
        ineligible_keywords = ['LEAVE', 'HOSPITAL', 'AWOL', 'COURSE', 'SICK', 'DETACHED']

        results = []
        for record in request.records:
            student = student_repo.get(db, record.student_id)
            if not student:
                continue

            # Check existing mark & override state
            db_mark = db.query(ExamMark).filter(
                ExamMark.exam_id == request.exam_id,
                ExamMark.student_id == record.student_id
            ).first()

            is_overridden = bool(db_mark and db_mark.is_overridden)

            # Check trainee parade state for exam date
            p_state = db.query(ParadeState).filter(
                ParadeState.student_id == student.id,
                ParadeState.date == exam.date
            ).first()

            is_p_approved = False
            if p_state:
                if p_state.submission_id:
                    sub = db.query(ParadeSubmission).filter(ParadeSubmission.id == p_state.submission_id).first()
                    if sub:
                        is_p_approved = (sub.status == 'APPROVED')
                elif is_trade_parade_approved:
                    is_p_approved = True
            elif is_trade_parade_approved:
                is_p_approved = True

            raw_status = p_state.status if p_state else 'Present'
            norm_status_upper = raw_status.strip().upper()
            is_status_ineligible = any(kw in norm_status_upper for kw in ineligible_keywords)

            # Enforce eligibility validation on mark submission:
            if is_p_approved and is_status_ineligible and not is_overridden:
                # If attempting to submit marks for an ineligible trainee without an override:
                if record.marks_obtained is not None and record.marks_obtained >= 0:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Cannot submit marks for trainee {student.service_number} ({student.full_name}): Trainee is on approved {raw_status} for examination date {exam.date}. Authorized officer override required."
                    )
                else:
                    # Ineligible without marks, skip or maintain absent/parade status
                    continue

            marks_val = record.marks_obtained if (record.marks_obtained is not None and record.marks_obtained >= 0) else None
            status = "Absent"
            if marks_val is not None:
                status = "Pass" if marks_val >= exam.pass_marks else "Fail"

            if db_mark:
                if marks_val is not None:
                    db_mark.marks_obtained = marks_val
                    db_mark.status = status
                db_mark.remarks = record.remarks
                db_mark.entered_by = user_id
            else:
                db_mark = ExamMark(
                    exam_id=request.exam_id,
                    student_id=record.student_id,
                    marks_obtained=marks_val if marks_val is not None else 0.0,
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
