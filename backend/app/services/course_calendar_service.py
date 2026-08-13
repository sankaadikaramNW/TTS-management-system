"""
Course Calendar Service
Business logic for managing course phases, theory/practical periods, working days, dates validation,
date conflict checking (HTTP 409), and instructor assignment rules (ASSIGNED vs NOT_ASSIGNED).
"""
from datetime import date
from typing import List, Optional, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.academic import Course, CourseCalendar
from app.models.user import User, Role
from app.repositories.academic import course_calendar_repo, course_repo
from app.repositories.user import audit_repo


class CourseCalendarService:

    def validate_dates_and_periods(
        self,
        commencement_date: date,
        completion_date: date,
        theory_periods: int,
        practical_periods: int,
        working_days: int
    ) -> None:
        """Enforce basic validation rules for dates and period numbers."""
        if completion_date < commencement_date:
            raise HTTPException(
                status_code=400,
                detail=f"Completion date ({completion_date.strftime('%d.%m.%Y')}) cannot be earlier than commencement date ({commencement_date.strftime('%d.%m.%Y')})."
            )
        if theory_periods < 0:
            raise HTTPException(status_code=400, detail="Theory periods cannot be negative.")
        if practical_periods < 0:
            raise HTTPException(status_code=400, detail="Practical periods cannot be negative.")
        if working_days < 0:
            raise HTTPException(status_code=400, detail="Working days cannot be negative.")

    def check_date_overlap(
        self,
        db: Session,
        course_id: str,
        commencement_date: date,
        completion_date: date,
        exclude_id: Optional[str] = None
    ) -> None:
        """
        Prevents duplicate and overlapping dates for the SAME COURSE.
        Logic:
          existing_commencement_date <= new_completion_date
          AND existing_completion_date >= new_commencement_date
          AND existing_course_id = new_course_id
          AND existing_status = 'Active'
          AND existing_id != current_id (on update)
        Returns HTTP 409 Conflict if overlap is detected.
        """
        query = db.query(CourseCalendar).filter(
            CourseCalendar.course_id == course_id,
            CourseCalendar.status == 'Active',
            CourseCalendar.commencement_date <= completion_date,
            CourseCalendar.completion_date >= commencement_date
        )
        if exclude_id:
            query = query.filter(CourseCalendar.id != exclude_id)

        conflict = query.first()
        if conflict:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Course Calendar date conflict.",
                    "conflicting_activity": conflict.phase_name,
                    "conflicting_start_date": str(conflict.commencement_date),
                    "conflicting_end_date": str(conflict.completion_date)
                }
            )

    def validate_instructor(self, db: Session, instructor_id: str) -> User:
        """Ensure assigned instructor exists and is active."""
        instructor = db.query(User).filter(User.id == instructor_id, User.is_active == True, User.deleted_at == None).first()
        if not instructor:
            raise HTTPException(
                status_code=400,
                detail="Selected instructor is invalid or inactive."
            )
        return instructor

    def validate_instructor_assignment(
        self,
        db: Session,
        instructor_id: Optional[str],
        instructor_status: Optional[str],
        remarks: Optional[str]
    ) -> Tuple[Optional[str], str, Optional[str]]:
        """
        Enforces Instructor Assignment Rules:
        - If instructor_status == 'ASSIGNED' or valid instructor_id provided:
          - instructor_id is required & must be active.
          - instructor_status = 'ASSIGNED'.
        - If instructor_status == 'NOT_ASSIGNED' or instructor_id is None/empty:
          - instructor_id = NULL (None).
          - instructor_status = 'NOT_ASSIGNED'.
          - remarks is MANDATORY.
        """
        cleaned_inst_id = instructor_id.strip() if instructor_id and instructor_id.strip() else None
        cleaned_remarks = remarks.strip() if remarks and remarks.strip() else None
        
        target_status = instructor_status.upper().strip() if instructor_status else None
        if not target_status:
            target_status = 'ASSIGNED' if cleaned_inst_id else 'NOT_ASSIGNED'

        if target_status == 'ASSIGNED':
            if not cleaned_inst_id:
                raise HTTPException(status_code=400, detail="Instructor selection is required when instructor status is set to ASSIGNED.")
            self.validate_instructor(db, cleaned_inst_id)
            return cleaned_inst_id, 'ASSIGNED', cleaned_remarks
        else:
            # NOT_ASSIGNED
            if not cleaned_remarks:
                raise HTTPException(
                    status_code=400,
                    detail="Remarks are required when instructor is NOT ASSIGNED. Please specify instructor nomination status and responsible person."
                )
            return None, 'NOT_ASSIGNED', cleaned_remarks

    def get_active_instructors(self, db: Session) -> List[dict]:
        """Fetch list of active users available for instructor assignment."""
        users = db.query(User).filter(User.is_active == True, User.deleted_at == None).order_by(User.full_name.asc()).all()
        instructors = []
        for u in users:
            rank = u.rank or ""
            name = u.full_name or u.username or ""
            service_no = u.service_number or ""
            display = f"{rank} {name}".strip()
            if service_no:
                display += f" ({service_no})"
            instructors.append({
                "id": u.id,
                "service_number": u.service_number,
                "rank": u.rank,
                "name": u.full_name,
                "display_name": display
            })
        return instructors

    def create_entry(
        self,
        db: Session,
        course_id: str,
        phase_name: str,
        commencement_date: date,
        completion_date: date,
        theory_periods: int = 0,
        practical_periods: int = 0,
        working_days: int = 0,
        serial_number: Optional[int] = None,
        instructor_id: Optional[str] = None,
        instructor_status: Optional[str] = None,
        remarks: Optional[str] = None,
        user_id: Optional[str] = None,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> CourseCalendar:
        """Create a new course calendar phase entry with transaction safety and overlap check."""
        # 1. Check course existence
        course = course_repo.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Selected course does not exist.")

        # 2. Validate dates and periods
        self.validate_dates_and_periods(commencement_date, completion_date, theory_periods, practical_periods, working_days)

        # 3. Prevent duplicate and overlapping dates for the SAME course (HTTP 409)
        self.check_date_overlap(db, course_id, commencement_date, completion_date)

        # 4. Validate instructor assignment & remarks
        final_inst_id, final_inst_status, final_remarks = self.validate_instructor_assignment(
            db, instructor_id, instructor_status, remarks
        )

        # 5. Determine serial number
        if serial_number is None or serial_number <= 0:
            serial_number = course_calendar_repo.get_next_serial_number(db, course_id)

        total_periods = theory_periods + practical_periods

        try:
            entry = CourseCalendar(
                course_id=course_id,
                serial_number=serial_number,
                phase_name=phase_name.strip(),
                theory_periods=theory_periods,
                practical_periods=practical_periods,
                total_periods=total_periods,
                working_days=working_days,
                commencement_date=commencement_date,
                completion_date=completion_date,
                instructor_id=final_inst_id,
                instructor_status=final_inst_status,
                remarks=final_remarks,
                status='Active',
                created_by=user_id
            )

            db.add(entry)
            db.commit()
            db.refresh(entry)

            # Audit Log
            if user_id:
                audit_repo.create_log(
                    db=db,
                    user_id=user_id,
                    action="CREATE_COURSE_CALENDAR_ENTRY",
                    module="Academic Management",
                    details=f"Added calendar phase '{entry.phase_name}' (S/No: {entry.serial_number}, Instructor Status: {final_inst_status}) for course '{course.name}'",
                    ip_address=ip,
                    user_agent=ua
                )

            return course_calendar_repo._enrich(db, entry)
        except Exception:
            db.rollback()
            raise

    def update_entry(
        self,
        db: Session,
        calendar_id: str,
        phase_name: Optional[str] = None,
        commencement_date: Optional[date] = None,
        completion_date: Optional[date] = None,
        theory_periods: Optional[int] = None,
        practical_periods: Optional[int] = None,
        working_days: Optional[int] = None,
        serial_number: Optional[int] = None,
        instructor_id: Optional[str] = None,
        instructor_status: Optional[str] = None,
        remarks: Optional[str] = None,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> CourseCalendar:
        """Update an existing course calendar phase entry."""
        entry = course_calendar_repo.get_by_id(db, calendar_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Course calendar entry not found.")

        # Determine effective updated values
        new_phase_name = phase_name.strip() if phase_name is not None else entry.phase_name
        new_commencement = commencement_date if commencement_date is not None else entry.commencement_date
        new_completion = completion_date if completion_date is not None else entry.completion_date
        new_theory = theory_periods if theory_periods is not None else entry.theory_periods
        new_practical = practical_periods if practical_periods is not None else entry.practical_periods
        new_working_days = working_days if working_days is not None else entry.working_days

        # Validate updated fields
        self.validate_dates_and_periods(new_commencement, new_completion, new_theory, new_practical, new_working_days)

        # Check date overlap (exclude current entry)
        self.check_date_overlap(db, entry.course_id, new_commencement, new_completion, exclude_id=calendar_id)

        # Determine effective instructor state
        req_inst_id = instructor_id if instructor_id is not None else entry.instructor_id
        req_inst_status = instructor_status if instructor_status is not None else getattr(entry, 'instructor_status', None)
        req_remarks = remarks if remarks is not None else entry.remarks

        final_inst_id, final_inst_status, final_remarks = self.validate_instructor_assignment(
            db, req_inst_id, req_inst_status, req_remarks
        )

        old_status_info = f"Instructor Status: {getattr(entry, 'instructor_status', 'N/A')}, Inst ID: {entry.instructor_id}"
        new_status_info = f"Instructor Status: {final_inst_status}, Inst ID: {final_inst_id}"

        try:
            entry.phase_name = new_phase_name
            entry.commencement_date = new_commencement
            entry.completion_date = new_completion
            entry.theory_periods = new_theory
            entry.practical_periods = new_practical
            entry.total_periods = new_theory + new_practical
            entry.working_days = new_working_days
            if serial_number is not None and serial_number > 0:
                entry.serial_number = serial_number
            
            entry.instructor_id = final_inst_id
            entry.instructor_status = final_inst_status
            entry.remarks = final_remarks

            if status is not None:
                entry.status = status

            db.commit()
            db.refresh(entry)

            # Audit Log
            if user_id:
                audit_repo.create_log(
                    db=db,
                    user_id=user_id,
                    action="UPDATE_COURSE_CALENDAR_ENTRY",
                    module="Academic Management",
                    details=f"Updated calendar phase '{entry.phase_name}'. Previous: [{old_status_info}] -> New: [{new_status_info}]",
                    ip_address=ip,
                    user_agent=ua
                )

            return course_calendar_repo._enrich(db, entry)
        except Exception:
            db.rollback()
            raise

    def delete_entry(
        self,
        db: Session,
        calendar_id: str,
        user_id: Optional[str] = None,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> bool:
        """Delete a course calendar entry."""
        entry = course_calendar_repo.get_by_id(db, calendar_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Course calendar entry not found.")

        phase_title = entry.phase_name
        c_id = entry.course_id

        try:
            db.delete(entry)
            db.commit()

            # Audit Log
            if user_id:
                audit_repo.create_log(
                    db=db,
                    user_id=user_id,
                    action="DELETE_COURSE_CALENDAR_ENTRY",
                    module="Academic Management",
                    details=f"Deleted calendar phase '{phase_title}' from course ID {c_id}",
                    ip_address=ip,
                    user_agent=ua
                )

            return True
        except Exception:
            db.rollback()
            raise


course_calendar_service = CourseCalendarService()
