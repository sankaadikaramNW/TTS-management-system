from datetime import date, datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc, asc

from app.models.student import Student, Rank, Trade, StudentStatusType, ParadeState, ParadeSubmission, ParadeStatusType, PersonalOccurrence
from app.models.academic import Course, Subject, Batch, Exam, ExamMark, AcademicAttendance, CourseCalendar, Classroom, Timetable, Lesson
from app.models.accommodation import AccommodationBillet, AccommodationBunkBed, BedPosition, AccommodationAllocation, AccommodationBuilding
from app.models.user import User


class ReportRepository:

    # ─────────────────────────────────────────────────────────────
    # 1. Student Dossier Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_student_dossier_data(
        db: Session,
        trade: Optional[str] = None,
        course_id: Optional[str] = None,
        batch: Optional[str] = None,
        status: Optional[str] = None,
        rank: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        query = db.query(
            Student.id,
            Student.service_number,
            Student.rank,
            Student.full_name,
            Student.initials,
            Student.nic,
            Student.trade,
            Student.batch,
            Student.status,
            Student.blood_group,
            Student.phone.label("contact_number"),
            Student.joining_date.label("intake_date"),
            Course.name.label("course_name"),
            Course.code.label("course_code")
        ).outerjoin(Course, Student.course_id == Course.id)

        if trade:
            query = query.filter(Student.trade == trade)
        if course_id:
            query = query.filter(Student.course_id == course_id)
        if batch:
            query = query.filter(Student.batch == batch)
        if status:
            query = query.filter(Student.status == status)
        if rank:
            query = query.filter(Student.rank == rank)
        if search:
            q = f"%{search.strip()}%"
            query = query.filter(or_(
                Student.service_number.ilike(q),
                Student.full_name.ilike(q),
                Student.nic.ilike(q)
            ))

        students = query.order_by(Student.service_number.asc()).all()

        rows = []
        status_counts: Dict[str, int] = {}
        trade_counts: Dict[str, int] = {}

        for idx, s in enumerate(students, 1):
            st_label = s.status or "Active"
            tr_label = s.trade or "Unassigned"
            status_counts[st_label] = status_counts.get(st_label, 0) + 1
            trade_counts[tr_label] = trade_counts.get(tr_label, 0) + 1

            rows.append({
                "s_no": idx,
                "service_number": s.service_number,
                "rank": s.rank or "LAC",
                "full_name": f"{s.rank or ''} {s.initials or ''} {s.full_name}".strip(),
                "trade": s.trade or "General",
                "course": f"{s.course_name} ({s.course_code})" if s.course_name else "N/A",
                "batch": s.batch or "N/A",
                "status": st_label,
                "nic": s.nic or "N/A",
                "blood_group": s.blood_group or "N/A",
                "intake_date": str(s.intake_date) if s.intake_date else "N/A"
            })

        summary = {
            "total_trainees": len(students),
            "status_breakdown": status_counts,
            "trade_breakdown": trade_counts
        }

        return rows, summary

    # ─────────────────────────────────────────────────────────────
    # 2. Parade State Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_parade_state_data(
        db: Session,
        parade_date: Optional[date] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        trade: Optional[str] = None,
        status: Optional[str] = None,
        approval_status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Optional[Dict[str, Any]]]:
        target_date = parade_date or (date_from if date_from else date.today())
        
        query = db.query(
            ParadeState.id,
            ParadeState.date,
            ParadeState.status,
            ParadeState.remarks,
            ParadeState.created_at,
            Student.id.label("student_id"),
            Student.service_number,
            Student.rank,
            Student.full_name,
            Student.trade,
            Student.batch,
            ParadeSubmission.status.label("submission_status"),
            ParadeSubmission.submitted_at,
            ParadeSubmission.reviewed_at,
            User.full_name.label("approving_officer_name")
        ).join(Student, ParadeState.student_id == Student.id
        ).outerjoin(ParadeSubmission, ParadeState.submission_id == ParadeSubmission.id
        ).outerjoin(User, ParadeSubmission.approving_officer_id == User.id)

        if date_from and date_to:
            query = query.filter(ParadeState.date.between(date_from, date_to))
        else:
            query = query.filter(ParadeState.date == target_date)

        if trade:
            query = query.filter(Student.trade == trade)
        if status:
            query = query.filter(ParadeState.status == status)
        if approval_status:
            query = query.filter(ParadeSubmission.status == approval_status)

        records = query.order_by(ParadeState.date.desc(), Student.service_number.asc()).all()

        rows = []
        present_cnt = 0
        leave_cnt = 0
        hosp_cnt = 0
        awol_cnt = 0
        cvisit_cnt = 0
        sick_cnt = 0
        tduty_cnt = 0
        other_cnt = 0

        for idx, r in enumerate(records, 1):
            st = (r.status or "Present").upper()
            if "PRESENT" in st:
                present_cnt += 1
            elif "LEAVE" in st:
                leave_cnt += 1
            elif "HOSPITAL" in st:
                hosp_cnt += 1
            elif "AWOL" in st:
                awol_cnt += 1
            elif "COURSE" in st or "VISIT" in st:
                cvisit_cnt += 1
            elif "SICK" in st:
                sick_cnt += 1
            elif "TEMPORARY" in st or "DUTY" in st:
                tduty_cnt += 1
            else:
                other_cnt += 1

            rows.append({
                "s_no": idx,
                "date": str(r.date),
                "service_number": r.service_number,
                "rank": r.rank or "LAC",
                "full_name": f"{r.rank or ''} {r.full_name}".strip(),
                "trade": r.trade or "General",
                "batch": r.batch or "N/A",
                "parade_status": r.status or "Present",
                "approval_status": r.submission_status or "DRAFT",
                "remarks": r.remarks or "—"
            })

        total = len(records)
        eff_pct = round((present_cnt / total * 100), 1) if total > 0 else 0.0

        # Check submission details for header/summary
        submission_info = None
        if records:
            first_rec = records[0]
            submission_info = {
                "submission_status": first_rec.submission_status or "DRAFT",
                "is_approved": first_rec.submission_status == "APPROVED",
                "approving_officer": first_rec.approving_officer_name or "Not Approved",
                "approved_at": str(first_rec.reviewed_at) if first_rec.reviewed_at else None
            }

        summary = {
            "total_strength": total,
            "present_count": present_cnt,
            "leave_count": leave_cnt,
            "hospital_count": hosp_cnt,
            "awol_count": awol_cnt,
            "course_visit_count": cvisit_cnt,
            "sick_report_count": sick_cnt,
            "temp_duty_count": tduty_cnt,
            "other_count": other_cnt,
            "effective_strength_pct": eff_pct
        }

        return rows, summary, submission_info

    # ─────────────────────────────────────────────────────────────
    # 3. Academic Results & Marksheet Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_academic_results_data(
        db: Session,
        exam_id: Optional[str] = None,
        course_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        batch: Optional[str] = None,
        result_status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
        # If no specific exam_id given, get the most recent or matching exam
        exam = None
        if exam_id:
            exam = db.query(Exam).filter(Exam.id == exam_id).first()
        elif course_id:
            q = db.query(Exam).filter(Exam.course_id == course_id)
            if subject_id:
                q = q.filter(Exam.subject_id == subject_id)
            exam = q.order_by(Exam.date.desc()).first()
        else:
            exam = db.query(Exam).order_by(Exam.date.desc()).first()

        if not exam:
            return [], {}, {}

        course = db.query(Course).filter(Course.id == exam.course_id).first()
        subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()

        # Get result sheet items using standard exam repository logic
        from app.repositories.academic import exam_repo
        result_sheet = exam_repo.get_result_sheet(db, exam.id)

        rows = []
        marks_list = []
        pass_cnt = 0
        fail_cnt = 0

        for idx, st in enumerate(result_sheet.get("students", []), 1):
            if result_status and result_status != "ALL":
                if st.get("result_status") != result_status:
                    continue

            marks_val = st.get("marks_obtained")
            if marks_val is not None:
                marks_list.append(float(marks_val))
                if float(marks_val) >= exam.pass_marks:
                    pass_cnt += 1
                else:
                    fail_cnt += 1

            rows.append({
                "s_no": idx,
                "service_number": st.get("service_number"),
                "rank": st.get("rank") or "LAC",
                "full_name": f"{st.get('rank') or ''} {st.get('student_name')}".strip(),
                "trade": st.get("trade") or "General",
                "batch": st.get("batch") or "N/A",
                "parade_status": st.get("parade_state_status") or "Present",
                "can_sit_exam": "Yes" if st.get("can_sit_exam") else "No",
                "is_overridden": "Yes" if st.get("is_overridden") else "No",
                "marks_obtained": f"{st.get('marks_obtained'):.1f}" if st.get("marks_obtained") is not None else "--",
                "result_status": st.get("result_status") or "ELIGIBLE",
                "remarks": st.get("remarks") or (f"Override: {st.get('override_reason')}" if st.get("is_overridden") else "—")
            })

        avg_marks = round(sum(marks_list) / len(marks_list), 1) if marks_list else 0.0
        max_m = max(marks_list) if marks_list else 0.0
        min_m = min(marks_list) if marks_list else 0.0
        sat_count = len(marks_list)
        pass_pct = round((pass_cnt / sat_count * 100), 1) if sat_count > 0 else 0.0

        exam_meta = {
            "exam_id": exam.id,
            "exam_type": exam.type,
            "exam_date": str(exam.date),
            "max_marks": exam.max_marks,
            "pass_marks": exam.pass_marks,
            "course_name": course.name if course else "N/A",
            "course_code": course.code if course else "N/A",
            "subject_name": subject.name if subject else "N/A",
            "subject_code": subject.code if subject else "N/A",
            "is_parade_approved": result_sheet.get("is_parade_approved", False)
        }

        res_summary = result_sheet.get("summary", {})
        summary = {
            "total_trainees": res_summary.get("total_trainees", len(rows)),
            "eligible_count": res_summary.get("eligible_count", 0),
            "sat_exam_count": sat_count,
            "did_not_sit_count": res_summary.get("did_not_sit_count", 0),
            "pass_count": pass_cnt,
            "fail_count": fail_cnt,
            "pass_percentage": pass_pct,
            "average_marks": avg_marks,
            "highest_marks": max_m,
            "lowest_marks": min_m,
            "leave_count": res_summary.get("leave_count", 0),
            "hospital_count": res_summary.get("hospital_count", 0),
            "awol_count": res_summary.get("awol_count", 0),
            "course_visit_count": res_summary.get("course_visit_count", 0),
            "overridden_count": res_summary.get("overridden_count", 0)
        }

        return rows, summary, exam_meta

    # ─────────────────────────────────────────────────────────────
    # 4. Classroom Attendance Register Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_attendance_register_data(
        db: Session,
        course_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        batch: Optional[str] = None,
        instructor_id: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        query = db.query(
            AcademicAttendance.id,
            Timetable.date,
            Timetable.period_number.label("period"),
            AcademicAttendance.status,
            AcademicAttendance.remarks,
            Student.service_number,
            Student.rank,
            Student.full_name,
            Student.trade,
            Student.batch,
            Subject.name.label("subject_name"),
            Subject.code.label("subject_code"),
            Course.name.label("course_name"),
            User.full_name.label("instructor_name")
        ).join(Timetable, AcademicAttendance.timetable_id == Timetable.id
        ).join(Student, AcademicAttendance.student_id == Student.id
        ).outerjoin(Subject, Timetable.subject_id == Subject.id
        ).outerjoin(Course, Timetable.course_id == Course.id
        ).outerjoin(User, Timetable.instructor_id == User.id)

        if course_id:
            query = query.filter(Timetable.course_id == course_id)
        if subject_id:
            query = query.filter(Timetable.subject_id == subject_id)
        if batch:
            query = query.filter(Student.batch == batch)
        if instructor_id:
            query = query.filter(Timetable.instructor_id == instructor_id)
        if date_from and date_to:
            query = query.filter(Timetable.date.between(date_from, date_to))
        elif date_from:
            query = query.filter(Timetable.date >= date_from)

        if status:
            query = query.filter(AcademicAttendance.status == status)

        records = query.order_by(Timetable.date.desc(), Timetable.period_number.asc(), Student.service_number.asc()).all()

        rows = []
        present_cnt = 0
        absent_cnt = 0
        late_cnt = 0
        excused_cnt = 0

        for idx, r in enumerate(records, 1):
            st = (r.status or "Present").upper()
            if "PRESENT" in st:
                present_cnt += 1
            elif "ABSENT" in st:
                absent_cnt += 1
            elif "LATE" in st:
                late_cnt += 1
            else:
                excused_cnt += 1

            rows.append({
                "s_no": idx,
                "date": str(r.date),
                "period": f"Period {r.period}" if r.period else "—",
                "service_number": r.service_number,
                "rank": r.rank or "LAC",
                "full_name": f"{r.rank or ''} {r.full_name}".strip(),
                "trade": r.trade or "General",
                "batch": r.batch or "N/A",
                "subject": f"{r.subject_name} ({r.subject_code})" if r.subject_name else "N/A",
                "instructor": r.instructor_name or "N/A",
                "status": r.status or "Present",
                "remarks": r.remarks or "—"
            })

        total = len(records)
        att_rate = round((present_cnt / total * 100), 1) if total > 0 else 0.0

        summary = {
            "total_records": total,
            "present_count": present_cnt,
            "absent_count": absent_cnt,
            "late_count": late_cnt,
            "excused_count": excused_cnt,
            "attendance_rate_pct": att_rate
        }

        return rows, summary

    # ─────────────────────────────────────────────────────────────
    # 5. Accommodation & Bunk Bed Billeting Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_accommodation_data(
        db: Session,
        building_id: Optional[str] = None,
        billet_id: Optional[str] = None,
        status: Optional[str] = None,
        bunk_level: Optional[str] = None,
        trade: Optional[str] = None,
        batch: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        # Query bed positions with bunker, billet, and active allocation details
        query = db.query(
            BedPosition.id.label("position_id"),
            BedPosition.position_type,  # TOP / BOTTOM
            BedPosition.status.label("bed_status"),
            AccommodationBunkBed.bunk_no.label("bunk_number"),
            AccommodationBillet.name.label("billet_name"),
            AccommodationBuilding.name.label("building_name"),
            AccommodationAllocation.allocated_at,
            Student.service_number,
            Student.rank,
            Student.full_name,
            Student.trade,
            Student.batch
        ).join(AccommodationBunkBed, BedPosition.bunk_bed_id == AccommodationBunkBed.id
        ).join(AccommodationBillet, AccommodationBunkBed.billet_id == AccommodationBillet.id
        ).outerjoin(AccommodationBuilding, AccommodationBillet.building_id == AccommodationBuilding.id
        ).outerjoin(AccommodationAllocation, and_(
            AccommodationAllocation.bed_position_id == BedPosition.id,
            AccommodationAllocation.vacated_at == None
        )).outerjoin(Student, AccommodationAllocation.student_id == Student.id)

        if building_id:
            query = query.filter(AccommodationBillet.building_id == building_id)
        if billet_id:
            query = query.filter(AccommodationBillet.id == billet_id)
        if status:
            query = query.filter(BedPosition.status == status)
        if bunk_level:
            query = query.filter(BedPosition.position_type == bunk_level.upper())
        if trade:
            query = query.filter(Student.trade == trade)
        if batch:
            query = query.filter(Student.batch == batch)

        records = query.order_by(
            AccommodationBuilding.name.asc(),
            AccommodationBillet.name.asc(),
            AccommodationBunkBed.bunk_no.asc(),
            BedPosition.position_type.desc()
        ).all()

        rows = []
        occupied_cnt = 0
        available_cnt = 0
        maint_cnt = 0

        for idx, r in enumerate(records, 1):
            st = (r.bed_status or "Available").capitalize()
            if st == "Occupied":
                occupied_cnt += 1
            elif st == "Maintenance":
                maint_cnt += 1
            else:
                available_cnt += 1

            rows.append({
                "s_no": idx,
                "building": r.building_name or "Main Complex",
                "billet_name": r.billet_name,
                "bunk_number": f"Bunk {r.bunk_number}" if r.bunk_number else "—",
                "bunk_level": r.position_type or "TOP",
                "bed_status": st,
                "service_number": r.service_number or "—",
                "trainee_name": f"{r.rank or ''} {r.full_name}".strip() if r.full_name else "Vacant / Available",
                "trade": r.trade or "—",
                "batch": r.batch or "—",
                "allocated_date": str(r.allocated_at.date()) if r.allocated_at else "—"
            })

        total = len(records)
        occ_rate = round((occupied_cnt / total * 100), 1) if total > 0 else 0.0

        summary = {
            "total_bed_positions": total,
            "occupied_count": occupied_cnt,
            "available_count": available_cnt,
            "maintenance_count": maint_cnt,
            "occupancy_rate_pct": occ_rate,
            "vacancy_rate_pct": round(100.0 - occ_rate, 1)
        }

        return rows, summary

    # ─────────────────────────────────────────────────────────────
    # 6. Course Calendar & Training Schedule Report
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_course_calendar_schedule_data(
        db: Session,
        course_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        phase: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any], Optional[Dict[str, Any]]]:
        # If no course specified, pick first active course
        course = None
        if course_id:
            course = db.query(Course).filter(Course.id == course_id).first()
        else:
            course = db.query(Course).filter(Course.is_active == True).first()

        if not course:
            return [], {}, None

        query = db.query(
            CourseCalendar.id,
            CourseCalendar.serial_number,
            CourseCalendar.commencement_date,
            CourseCalendar.completion_date,
            CourseCalendar.phase_name,
            CourseCalendar.working_days,
            CourseCalendar.theory_periods,
            CourseCalendar.practical_periods,
            CourseCalendar.total_periods,
            CourseCalendar.remarks,
            Subject.name.label("subject_name"),
            Subject.code.label("subject_code"),
            User.full_name.label("instructor_name")
        ).outerjoin(Subject, CourseCalendar.subject_id == Subject.id
        ).outerjoin(User, CourseCalendar.instructor_id == User.id
        ).filter(CourseCalendar.course_id == course.id)

        if phase:
            query = query.filter(CourseCalendar.phase_name == phase)
        if date_from and date_to:
            query = query.filter(CourseCalendar.commencement_date.between(date_from, date_to))
        elif date_from:
            query = query.filter(CourseCalendar.commencement_date >= date_from)

        entries = query.order_by(CourseCalendar.serial_number.asc(), CourseCalendar.commencement_date.asc()).all()

        rows = []
        tot_theory = 0
        tot_practical = 0
        tot_periods = 0
        phases_set = set()

        for idx, e in enumerate(entries, 1):
            t_p = e.theory_periods or 0
            p_p = e.practical_periods or 0
            tot_p = e.total_periods or (t_p + p_p)

            tot_theory += t_p
            tot_practical += p_p
            tot_periods += tot_p
            if e.phase_name:
                phases_set.add(e.phase_name)

            rows.append({
                "s_no": idx,
                "serial_no": e.serial_number,
                "date": f"{e.commencement_date} to {e.completion_date}" if e.commencement_date and e.completion_date else str(e.commencement_date or "—"),
                "working_days": f"{e.working_days} Days" if e.working_days else "—",
                "phase": e.phase_name or "Phase 1",
                "subject": f"{e.subject_name} ({e.subject_code})" if e.subject_name else "—",
                "theory_periods": t_p,
                "practical_periods": p_p,
                "total_periods": tot_p,
                "instructor": e.instructor_name or "Assigned Instructor",
                "remarks": e.remarks or "—"
            })

        course_meta = {
            "course_id": course.id,
            "course_name": course.name,
            "course_code": course.code,
            "trade_name": course.trade.label if course.trade else "General",
            "duration_weeks": course.duration_weeks,
            "intake_capacity": course.intake_capacity
        }

        summary = {
            "total_calendar_entries": len(entries),
            "total_phases": len(phases_set),
            "total_theory_periods": tot_theory,
            "total_practical_periods": tot_practical,
            "total_periods": tot_periods,
            "start_date": str(entries[0].commencement_date) if entries and entries[0].commencement_date else "N/A",
            "completion_date": str(entries[-1].completion_date) if entries and entries[-1].completion_date else "N/A"
        }

        return rows, summary, course_meta

    # ─────────────────────────────────────────────────────────────
    # 7. Personal Occurrence Reporting (Achievements & Misconduct)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_occurrence_data(
        db: Session,
        trainee_id: Optional[str] = None,
        occurrence_type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        trade: Optional[str] = None,
        batch: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        query = db.query(
            PersonalOccurrence.id,
            PersonalOccurrence.occurrence_date,
            PersonalOccurrence.occurrence_type,
            PersonalOccurrence.title,
            PersonalOccurrence.description,
            PersonalOccurrence.remarks,
            PersonalOccurrence.status,
            Student.service_number,
            Student.rank,
            Student.full_name,
            Student.trade,
            Student.batch,
            User.full_name.label('creator_name')
        ).join(
            Student, PersonalOccurrence.trainee_id == Student.id
        ).outerjoin(
            User, PersonalOccurrence.created_by == User.id
        ).filter(
            PersonalOccurrence.deleted_at.is_(None)
        )


        if trainee_id:
            query = query.filter(PersonalOccurrence.trainee_id == trainee_id)
        if occurrence_type and occurrence_type.upper() != 'ALL':
            query = query.filter(PersonalOccurrence.occurrence_type == occurrence_type)
        if date_from:
            query = query.filter(PersonalOccurrence.occurrence_date >= date_from)
        if date_to:
            query = query.filter(PersonalOccurrence.occurrence_date <= date_to)
        if trade:
            query = query.filter(Student.trade == trade)
        if batch:
            query = query.filter(Student.batch == batch)
        if search:
            s_term = f"%{search}%"
            query = query.filter(
                or_(
                    Student.service_number.ilike(s_term),
                    Student.full_name.ilike(s_term),
                    PersonalOccurrence.title.ilike(s_term),
                    PersonalOccurrence.description.ilike(s_term)
                )
            )

        records = query.order_by(PersonalOccurrence.occurrence_date.desc(), Student.service_number.asc()).all()

        rows = []
        total_occurrences = len(records)
        achievements_count = 0
        misconduct_count = 0

        for idx, rec in enumerate(records, start=1):
            occ_type = rec.occurrence_type
            if occ_type == 'ACHIEVEMENT':
                achievements_count += 1
                type_display = 'ACHIEVEMENT / COMMENDATION'
            elif occ_type == 'MISCONDUCT_OFFENSE':
                misconduct_count += 1
                type_display = 'MISCONDUCT / OFFENSE'
            else:
                type_display = str(occ_type).replace('_', ' ').upper()

            rows.append({
                "s_no": idx,
                "occurrence_date": str(rec.occurrence_date) if rec.occurrence_date else "—",
                "service_number": rec.service_number or "—",
                "rank": rec.rank or "—",
                "trainee_name": rec.full_name or "—",
                "trade": rec.trade or "—",
                "batch": rec.batch or "—",
                "occurrence_type": type_display,
                "title": rec.title or "—",
                "description": rec.description or "—",
                "recorded_by": rec.creator_name or "Authorized Officer",

                "remarks": rec.remarks or "—"
            })


        summary = {
            "total_occurrences": total_occurrences,
            "achievements_count": achievements_count,
            "misconduct_count": misconduct_count,
            "disciplinary_rate": f"{(misconduct_count / total_occurrences * 100):.1f}%" if total_occurrences > 0 else "0.0%"
        }

        return rows, summary

    # ─────────────────────────────────────────────────────────────
    # 8. Filter Dropdown Metadata
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def get_filter_metadata(db: Session) -> Dict[str, Any]:
        trades = db.query(Trade).filter(Trade.is_active == True).order_by(Trade.label.asc()).all()
        courses = db.query(Course).filter(Course.is_active == True).order_by(Course.name.asc()).all()
        batches = db.query(Batch).filter(Batch.status == 'Active').order_by(Batch.name.asc()).all()
        ranks = db.query(Rank).filter(Rank.is_active == True).order_by(Rank.id.asc()).all()
        student_statuses = db.query(StudentStatusType).filter(StudentStatusType.is_active == True).all()
        parade_statuses = db.query(ParadeStatusType).filter(ParadeStatusType.is_active == True).all()
        billets = db.query(AccommodationBillet).filter(AccommodationBillet.status == 'Active').all()
        subjects = db.query(Subject).order_by(Subject.name.asc()).all()

        return {
            "trades": [{"value": t.label, "label": f"{t.label} ({t.code})"} for t in trades],
            "courses": [{"value": c.id, "label": f"{c.name} ({c.code})"} for c in courses],
            "batches": [{"value": b.name, "label": b.name} for b in batches],
            "ranks": [{"value": r.code, "label": f"{r.label} ({r.code})"} for r in ranks],
            "student_statuses": [{"value": s.label, "label": s.label} for s in student_statuses],
            "parade_statuses": [{"value": p.label, "label": p.label} for p in parade_statuses],
            "billets": [{"value": b.id, "label": b.name} for b in billets],
            "subjects": [{"value": s.id, "label": f"{s.name} ({s.code})"} for s in subjects]
        }


report_repo = ReportRepository()
