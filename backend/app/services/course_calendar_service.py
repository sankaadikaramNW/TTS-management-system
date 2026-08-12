"""
Course Calendar Service
Business logic for managing course phases, theory/practical periods, working days, and dates validation.
"""
from datetime import date
from typing import List, Optional
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
        """Enforce validation rules for dates and period numbers."""
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

    def validate_instructor(self, db: Session, instructor_id: Optional[str]) -> Optional[User]:
        """Ensure assigned instructor exists and is active."""
        if not instructor_id:
            return None
        instructor = db.query(User).filter(User.id == instructor_id, User.is_active == True).first()
        if not instructor:
            raise HTTPException(
                status_code=400,
                detail="Selected instructor is invalid or inactive."
            )
        return instructor

    def get_active_instructors(self, db: Session) -> List[dict]:
        """Fetch list of active users available for instructor assignment."""
        users = db.query(User).filter(User.is_active == True).order_by(User.full_name.asc()).all()
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
        remarks: Optional[str] = None,
        user_id: Optional[str] = None,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> CourseCalendar:
        """Create a new course calendar phase entry."""
        # 1. Check course existence
        course = course_repo.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Selected course does not exist.")

        # 2. Validate inputs
        self.validate_dates_and_periods(commencement_date, completion_date, theory_periods, practical_periods, working_days)
        self.validate_instructor(db, instructor_id)

        # 3. Determine serial number
        if serial_number is None or serial_number <= 0:
            serial_number = course_calendar_repo.get_next_serial_number(db, course_id)

        total_periods = theory_periods + practical_periods

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
            instructor_id=instructor_id if instructor_id and instructor_id.strip() else None,
            remarks=remarks.strip() if remarks else None,
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
                details=f"Added calendar phase '{entry.phase_name}' (S/No: {entry.serial_number}) for course '{course.name}'",
                ip_address=ip,
                user_agent=ua
            )

        return course_calendar_repo._enrich(db, entry)

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
        new_instructor_id = instructor_id if instructor_id is not None else entry.instructor_id

        # Validate updated fields
        self.validate_dates_and_periods(new_commencement, new_completion, new_theory, new_practical, new_working_days)
        if instructor_id is not None:
            self.validate_instructor(db, new_instructor_id)

        old_details = f"Phase: {entry.phase_name}, S/No: {entry.serial_number}, Theory: {entry.theory_periods}, Practical: {entry.practical_periods}"

        entry.phase_name = new_phase_name
        entry.commencement_date = new_commencement
        entry.completion_date = new_completion
        entry.theory_periods = new_theory
        entry.practical_periods = new_practical
        entry.total_periods = new_theory + new_practical
        entry.working_days = new_working_days
        if serial_number is not None and serial_number > 0:
            entry.serial_number = serial_number
        if instructor_id is not None:
            entry.instructor_id = instructor_id if instructor_id.strip() else None
        if remarks is not None:
            entry.remarks = remarks.strip() if remarks else None
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
                details=f"Updated calendar phase '{entry.phase_name}'. Previous: [{old_details}]",
                ip_address=ip,
                user_agent=ua
            )

        return course_calendar_repo._enrich(db, entry)

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


course_calendar_service = CourseCalendarService()
