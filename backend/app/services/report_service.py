from datetime import datetime, date
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User, AuditLog
from app.repositories.reports import report_repo
from app.schemas.reports import (
    StandardReportResponse, ReportHeaderInfo, ReportSummaryStatItem,
    ReportTableColumn, ReportFilterMetaResponse
)
from app.services.report_export_service import report_export_service


class ReportService:

    @staticmethod
    def _log_report_audit(db: Session, user_id: str, report_type: str, params: Dict[str, Any], ip: str = "127.0.0.1", ua: str = "Unknown"):
        """Record audit entry whenever an official report is compiled or exported."""
        try:
            param_summary = ", ".join([f"{k}={v}" for k, v in params.items() if v])
            audit = AuditLog(
                user_id=user_id,
                module="Enterprise Reports",
                action="REPORT_GENERATED",
                details=f"Generated {report_type.upper()} report with parameters: [{param_summary}]",
                ip_address=ip,
                user_agent=ua
            )
            db.add(audit)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[Audit Error] Failed to log report generation: {e}")

    # ─────────────────────────────────────────────────────────────
    # 1. Student Dossier Report
    # ─────────────────────────────────────────────────────────────
    def get_student_report(
        self,
        db: Session,
        current_user: User,
        trade: Optional[str] = None,
        course_id: Optional[str] = None,
        batch: Optional[str] = None,
        status: Optional[str] = None,
        rank: Optional[str] = None,
        search: Optional[str] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary = report_repo.get_student_dossier_data(
            db, trade=trade, course_id=course_id, batch=batch,
            status=status, rank=rank, search=search
        )

        params = {
            "trade": trade, "course_id": course_id, "batch": batch,
            "status": status, "rank": rank, "search": search
        }
        self._log_report_audit(db, current_user.id, "student_dossier", params, ip, ua)

        # Header
        header = ReportHeaderInfo(
            title="TRAINEE PERSONAL DOSSIERS & STATUS DIRECTORY",
            subtitle="Official Sri Lanka Air Force Trade Training School Student Master Register",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        # Summary Metrics
        stat_items = [
            ReportSummaryStatItem(label="Total Trainees", value=summary["total_trainees"], category="primary"),
        ]
        for st_name, count in summary.get("status_breakdown", {}).items():
            cat = "success" if st_name.upper() == "ACTIVE" else ("danger" if st_name.upper() in ["AWOL", "SUSPENDED"] else "warning")
            pct = round((count / summary["total_trainees"] * 100), 1) if summary["total_trainees"] > 0 else 0.0
            stat_items.append(ReportSummaryStatItem(
                label=st_name,
                value=count,
                percentage=pct,
                category=cat
            ))

        # Columns
        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", is_monospace=True, min_width="100px"),
            ReportTableColumn(field="full_name", label="Rank & Trainee Full Name", align="left", min_width="220px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="140px"),
            ReportTableColumn(field="course", label="Course Assigned", align="left", min_width="180px"),
            ReportTableColumn(field="batch", label="Batch", align="center", min_width="90px"),
            ReportTableColumn(field="status", label="Status", align="center", is_badge=True, min_width="110px"),
            ReportTableColumn(field="blood_group", label="Blood Grp", align="center", min_width="90px"),
            ReportTableColumn(field="intake_date", label="Intake Date", align="center", min_width="110px")
        ]

        return StandardReportResponse(
            report_type="student",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 2. Parade State Report
    # ─────────────────────────────────────────────────────────────
    def get_parade_report(
        self,
        db: Session,
        current_user: User,
        parade_date: Optional[date] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        trade: Optional[str] = None,
        status: Optional[str] = None,
        approval_status: Optional[str] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary, sub_info = report_repo.get_parade_state_data(
            db, parade_date=parade_date, date_from=date_from, date_to=date_to,
            trade=trade, status=status, approval_status=approval_status
        )

        params = {
            "parade_date": str(parade_date) if parade_date else None,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None,
            "trade": trade,
            "status": status,
            "approval_status": approval_status
        }
        self._log_report_audit(db, current_user.id, "parade_state", params, ip, ua)

        appr_status_txt = sub_info.get("submission_status", "DRAFT") if sub_info else "DRAFT"
        appr_officer_txt = sub_info.get("approving_officer", "Pending") if sub_info else "Pending"

        header = ReportHeaderInfo(
            title="DAILY TRADE PARADE STATE & STRENGTH REGISTER",
            subtitle=f"Official Attendance & Strength Accounting Record • Approval: {appr_status_txt} (Officer I/C: {appr_officer_txt})",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        tot = summary["total_strength"]
        stat_items = [
            ReportSummaryStatItem(label="Total Strength", value=tot, category="primary"),
            ReportSummaryStatItem(label="Present Strength", value=summary["present_count"], percentage=summary["effective_strength_pct"], category="success"),
            ReportSummaryStatItem(label="On Leave", value=summary["leave_count"], category="warning"),
            ReportSummaryStatItem(label="In Hospital", value=summary["hospital_count"], category="danger"),
            ReportSummaryStatItem(label="AWOL", value=summary["awol_count"], category="danger"),
            ReportSummaryStatItem(label="Course Visit", value=summary["course_visit_count"], category="info"),
            ReportSummaryStatItem(label="Sick Report", value=summary["sick_report_count"], category="warning")
        ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="date", label="Parade Date", align="center", min_width="100px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", is_monospace=True, min_width="100px"),
            ReportTableColumn(field="full_name", label="Rank & Trainee Full Name", align="left", min_width="220px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="140px"),
            ReportTableColumn(field="batch", label="Batch", align="center", min_width="90px"),
            ReportTableColumn(field="parade_status", label="Parade Status", align="center", is_badge=True, min_width="130px"),
            ReportTableColumn(field="approval_status", label="Approval State", align="center", is_badge=True, min_width="120px"),
            ReportTableColumn(field="remarks", label="Remarks / Notes", align="left", min_width="180px")
        ]

        return StandardReportResponse(
            report_type="parade",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 3. Academic Results & Marksheet Report
    # ─────────────────────────────────────────────────────────────
    def get_academic_results_report(
        self,
        db: Session,
        current_user: User,
        exam_id: Optional[str] = None,
        course_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        batch: Optional[str] = None,
        result_status: Optional[str] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary, exam_meta = report_repo.get_academic_results_data(
            db, exam_id=exam_id, course_id=course_id, subject_id=subject_id,
            batch=batch, result_status=result_status
        )

        params = {
            "exam_id": exam_id,
            "course": exam_meta.get("course_name") if exam_meta else None,
            "subject": exam_meta.get("subject_name") if exam_meta else None,
            "exam_type": exam_meta.get("exam_type") if exam_meta else None,
            "exam_date": exam_meta.get("exam_date") if exam_meta else None,
            "result_status": result_status
        }
        self._log_report_audit(db, current_user.id, "academic_results", params, ip, ua)

        sub_title = f"{exam_meta.get('course_name', 'Course')} • {exam_meta.get('subject_name', 'Subject')} ({exam_meta.get('exam_type', 'Exam')} on {exam_meta.get('exam_date', 'N/A')})" if exam_meta else "Examination Performance & Official Marksheet"

        header = ReportHeaderInfo(
            title="OFFICIAL EXAMINATION MARKSHEET & ASSESSMENT REPORT",
            subtitle=sub_title,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        stat_items = []
        if summary:
            stat_items = [
                ReportSummaryStatItem(label="Total Trainees", value=summary.get("total_trainees", 0), category="secondary"),
                ReportSummaryStatItem(label="Eligible to Sit", value=summary.get("eligible_count", 0), category="success"),
                ReportSummaryStatItem(label="Sat Examination", value=summary.get("sat_exam_count", 0), category="primary"),
                ReportSummaryStatItem(label="Did Not Sit (Parade)", value=summary.get("did_not_sit_count", 0), category="danger"),
                ReportSummaryStatItem(label="Passed", value=summary.get("pass_count", 0), percentage=summary.get("pass_percentage", 0), category="success"),
                ReportSummaryStatItem(label="Failed", value=summary.get("fail_count", 0), category="danger"),
                ReportSummaryStatItem(label="Average Marks", value=f"{summary.get('average_marks', 0):.1f}", category="info"),
                ReportSummaryStatItem(label="Highest Marks", value=f"{summary.get('highest_marks', 0):.1f}", category="info"),
                ReportSummaryStatItem(label="Lowest Marks", value=f"{summary.get('lowest_marks', 0):.1f}", category="warning")
            ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", is_monospace=True, min_width="100px"),
            ReportTableColumn(field="full_name", label="Rank & Trainee Full Name", align="left", min_width="220px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="140px"),
            ReportTableColumn(field="batch", label="Batch", align="center", min_width="90px"),
            ReportTableColumn(field="parade_status", label="Parade State (Exam Date)", align="center", is_badge=True, min_width="160px"),
            ReportTableColumn(field="can_sit_exam", label="Eligible", align="center", min_width="80px"),
            ReportTableColumn(field="marks_obtained", label="Marks Obtained", align="center", is_monospace=True, min_width="120px"),
            ReportTableColumn(field="result_status", label="Result Status", align="center", is_badge=True, min_width="130px"),
            ReportTableColumn(field="remarks", label="Remarks / Override Note", align="left", min_width="180px")
        ]

        return StandardReportResponse(
            report_type="academic_results",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 4. Classroom Attendance Register Report
    # ─────────────────────────────────────────────────────────────
    def get_attendance_report(
        self,
        db: Session,
        current_user: User,
        course_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        batch: Optional[str] = None,
        instructor_id: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary = report_repo.get_attendance_register_data(
            db, course_id=course_id, subject_id=subject_id, batch=batch,
            instructor_id=instructor_id, date_from=date_from, date_to=date_to, status=status
        )

        params = {
            "course_id": course_id, "subject_id": subject_id, "batch": batch,
            "instructor_id": instructor_id, "date_range": f"{date_from} to {date_to}" if date_from and date_to else None,
            "status": status
        }
        self._log_report_audit(db, current_user.id, "attendance_register", params, ip, ua)

        header = ReportHeaderInfo(
            title="CLASSROOM ATTENDANCE & PERIOD PARTICIPATION REGISTER",
            subtitle="Official Academic Session Attendance Records • Sri Lanka Air Force TTS Ekala",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        stat_items = [
            ReportSummaryStatItem(label="Total Logged Records", value=summary["total_records"], category="primary"),
            ReportSummaryStatItem(label="Present", value=summary["present_count"], percentage=summary["attendance_rate_pct"], category="success"),
            ReportSummaryStatItem(label="Absent", value=summary["absent_count"], category="danger"),
            ReportSummaryStatItem(label="Late", value=summary["late_count"], category="warning"),
            ReportSummaryStatItem(label="Excused", value=summary["excused_count"], category="info"),
            ReportSummaryStatItem(label="Overall Attendance Rate", value=f"{summary['attendance_rate_pct']}%", category="success")
        ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="date", label="Date", align="center", min_width="100px"),
            ReportTableColumn(field="period", label="Period", align="center", min_width="90px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", is_monospace=True, min_width="100px"),
            ReportTableColumn(field="full_name", label="Rank & Trainee Full Name", align="left", min_width="220px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="130px"),
            ReportTableColumn(field="subject", label="Subject / Module", align="left", min_width="180px"),
            ReportTableColumn(field="instructor", label="Instructor", align="left", min_width="160px"),
            ReportTableColumn(field="status", label="Attendance Status", align="center", is_badge=True, min_width="130px"),
            ReportTableColumn(field="remarks", label="Remarks", align="left", min_width="140px")
        ]

        return StandardReportResponse(
            report_type="attendance",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 5. Accommodation & Billeting Report
    # ─────────────────────────────────────────────────────────────
    def get_accommodation_report(
        self,
        db: Session,
        current_user: User,
        building_id: Optional[str] = None,
        billet_id: Optional[str] = None,
        status: Optional[str] = None,
        bunk_level: Optional[str] = None,
        trade: Optional[str] = None,
        batch: Optional[str] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary = report_repo.get_accommodation_data(
            db, building_id=building_id, billet_id=billet_id, status=status,
            bunk_level=bunk_level, trade=trade, batch=batch
        )

        params = {
            "building_id": building_id, "billet_id": billet_id, "status": status,
            "bunk_level": bunk_level, "trade": trade, "batch": batch
        }
        self._log_report_audit(db, current_user.id, "accommodation_billet", params, ip, ua)

        header = ReportHeaderInfo(
            title="TRAINEE BILLETING & BUNK BED ACCOMMODATION REPORT",
            subtitle="Official Billet Roster, Bunk Allocations & Capacity Audit • Housing Module",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        stat_items = [
            ReportSummaryStatItem(label="Total Bed Positions", value=summary["total_bed_positions"], category="primary"),
            ReportSummaryStatItem(label="Occupied Positions", value=summary["occupied_count"], percentage=summary["occupancy_rate_pct"], category="success"),
            ReportSummaryStatItem(label="Available Vacancies", value=summary["available_count"], percentage=summary["vacancy_rate_pct"], category="info"),
            ReportSummaryStatItem(label="Under Maintenance", value=summary["maintenance_count"], category="warning"),
            ReportSummaryStatItem(label="Billet Occupancy Rate", value=f"{summary['occupancy_rate_pct']}%", category="success")
        ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="building", label="Building Complex", align="left", min_width="140px"),
            ReportTableColumn(field="billet_name", label="Billet Name", align="left", min_width="140px"),
            ReportTableColumn(field="bunk_number", label="Bunk ID", align="center", min_width="90px"),
            ReportTableColumn(field="bunk_level", label="Level (Top/Bottom)", align="center", is_badge=True, min_width="120px"),
            ReportTableColumn(field="bed_status", label="Status", align="center", is_badge=True, min_width="110px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", is_monospace=True, min_width="100px"),
            ReportTableColumn(field="trainee_name", label="Allocated Trainee", align="left", min_width="220px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="130px"),
            ReportTableColumn(field="batch", label="Batch", align="center", min_width="90px"),
            ReportTableColumn(field="allocated_date", label="Allocated Date", align="center", min_width="110px")
        ]

        return StandardReportResponse(
            report_type="accommodation",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 6. Course Calendar & Training Schedule Report
    # ─────────────────────────────────────────────────────────────
    def get_course_calendar_report(
        self,
        db: Session,
        current_user: User,
        course_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        phase: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        ip: str = "127.0.0.1",
        ua: str = "Unknown"
    ) -> StandardReportResponse:
        rows, summary, course_meta = report_repo.get_course_calendar_schedule_data(
            db, course_id=course_id, batch_id=batch_id, phase=phase,
            date_from=date_from, date_to=date_to
        )

        params = {
            "course": course_meta.get("course_name") if course_meta else None,
            "phase": phase,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
        self._log_report_audit(db, current_user.id, "course_calendar", params, ip, ua)

        sub_title = f"{course_meta.get('course_name', 'Course')} ({course_meta.get('course_code', 'CODE')}) • Duration: {course_meta.get('duration_weeks', 0)} Weeks" if course_meta else "Course Curriculum & Phase Training Schedule"

        header = ReportHeaderInfo(
            title="OFFICIAL COURSE TRAINING CALENDAR & SCHEDULE REPORT",
            subtitle=sub_title,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        stat_items = []
        if summary:
            stat_items = [
                ReportSummaryStatItem(label="Total Scheduled Days", value=summary.get("total_working_days", 0), category="primary"),
                ReportSummaryStatItem(label="Curriculum Phases", value=summary.get("total_phases", 0), category="info"),
                ReportSummaryStatItem(label="Theory Periods", value=summary.get("total_theory_periods", 0), category="secondary"),
                ReportSummaryStatItem(label="Practical Periods", value=summary.get("total_practical_periods", 0), category="secondary"),
                ReportSummaryStatItem(label="Total Scheduled Periods", value=summary.get("total_periods", 0), category="success"),
                ReportSummaryStatItem(label="Course Start Date", value=summary.get("start_date", "N/A"), category="info"),
                ReportSummaryStatItem(label="Completion Date", value=summary.get("completion_date", "N/A"), category="success")
            ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="60px"),
            ReportTableColumn(field="date", label="Date", align="center", min_width="100px"),
            ReportTableColumn(field="day_no", label="Working Day", align="center", min_width="90px"),
            ReportTableColumn(field="phase", label="Phase", align="center", is_badge=True, min_width="100px"),
            ReportTableColumn(field="subject", label="Subject / Module", align="left", min_width="160px"),
            ReportTableColumn(field="activity", label="Topic / Practical Activity", align="left", min_width="220px"),
            ReportTableColumn(field="theory_periods", label="Theory (P)", align="center", min_width="80px"),
            ReportTableColumn(field="practical_periods", label="Practical (P)", align="center", min_width="80px"),
            ReportTableColumn(field="total_periods", label="Total (P)", align="center", min_width="80px"),
            ReportTableColumn(field="instructor", label="Instructor", align="left", min_width="160px")
        ]

        return StandardReportResponse(
            report_type="course_calendar",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 7. Personal Occurrence Report (Achievements & Misconduct)
    # ─────────────────────────────────────────────────────────────
    def get_occurrence_report(
        self,
        db: Session,
        current_user: User,
        trainee_id: Optional[str] = None,
        occurrence_type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        trade: Optional[str] = None,
        batch: Optional[str] = None,
        search: Optional[str] = None,
        client_ip: str = "127.0.0.1",
        user_agent: str = "Unknown"
    ) -> StandardReportResponse:
        params = {
            "trainee_id": trainee_id,
            "occurrence_type": occurrence_type or "ALL",
            "date_from": str(date_from) if date_from else None,
            "date_to": str(date_to) if date_to else None,
            "trade": trade,
            "batch": batch,
            "search": search
        }
        self._log_report_audit(db, current_user.id, "occurrences", params, client_ip, user_agent)

        rows, summary = report_repo.get_occurrence_data(
            db,
            trainee_id=trainee_id,
            occurrence_type=occurrence_type,
            date_from=date_from,
            date_to=date_to,
            trade=trade,
            batch=batch,
            search=search
        )

        header = ReportHeaderInfo(
            title="TRAINEE PERSONAL OCCURRENCE & CONDUCT DOSSIER",
            subtitle="Official Register of Commendations, Achievements, Disciplinary Actions & Misconduct",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            generated_by=f"{current_user.full_name} ({current_user.username})",
            parameters=params
        )

        stat_items = []
        if summary:
            stat_items = [
                ReportSummaryStatItem(label="Total Occurrences Logged", value=summary.get("total_occurrences", 0), category="primary"),
                ReportSummaryStatItem(label="Achievements / Commendations", value=summary.get("achievements_count", 0), category="success"),
                ReportSummaryStatItem(label="Misconduct / Offenses", value=summary.get("misconduct_count", 0), category="danger"),
                ReportSummaryStatItem(label="Disciplinary Rate", value=summary.get("disciplinary_rate", "0.0%"), category="warning")
            ]

        columns = [
            ReportTableColumn(field="s_no", label="S/No", align="center", min_width="50px"),
            ReportTableColumn(field="occurrence_date", label="Date", align="center", min_width="95px"),
            ReportTableColumn(field="service_number", label="Service No", align="center", min_width="95px"),
            ReportTableColumn(field="rank", label="Rank", align="center", min_width="70px"),
            ReportTableColumn(field="trainee_name", label="Trainee Name", align="left", min_width="160px"),
            ReportTableColumn(field="trade", label="Trade", align="left", min_width="110px"),
            ReportTableColumn(field="batch", label="Batch", align="center", min_width="75px"),
            ReportTableColumn(field="occurrence_type", label="Occurrence Category", align="center", is_badge=True, min_width="160px"),
            ReportTableColumn(field="title", label="Title / Incident Summary", align="left", min_width="170px"),
            ReportTableColumn(field="description", label="Detailed Description", align="left", min_width="220px"),
            ReportTableColumn(field="recorded_by", label="Recorded By", align="left", min_width="130px"),
            ReportTableColumn(field="remarks", label="Remarks", align="left", min_width="130px")
        ]

        return StandardReportResponse(
            report_type="occurrences",
            header=header,
            summary_stats=stat_items,
            columns=columns,
            rows=rows,
            total_records=len(rows)
        )

    # ─────────────────────────────────────────────────────────────
    # 8. Metadata Dropdowns
    # ─────────────────────────────────────────────────────────────
    def get_filter_metadata(self, db: Session) -> ReportFilterMetaResponse:
        return ReportFilterMetaResponse(**report_repo.get_filter_metadata(db))

    # ─────────────────────────────────────────────────────────────
    # 8. Export Dispatchers
    # ─────────────────────────────────────────────────────────────
    def export_report_excel(self, title: str, header: Dict[str, Any], summary: Optional[Dict[str, Any]], columns: List[Dict[str, Any]], rows: List[Dict[str, Any]]) -> bytes:
        return report_export_service.generate_excel_workbook(
            report_title=title,
            header_info=header,
            summary_data=summary,
            columns=columns,
            rows=rows
        )

    def export_report_pdf(self, title: str, header: Dict[str, Any], summary: Optional[Dict[str, Any]], columns: List[Dict[str, Any]], rows: List[Dict[str, Any]]) -> bytes:
        return report_export_service.generate_pdf_document(
            report_title=title,
            header_info=header,
            summary_data=summary,
            columns=columns,
            rows=rows
        )


report_service = ReportService()
