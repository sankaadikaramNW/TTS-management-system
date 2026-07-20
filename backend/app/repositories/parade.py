from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student, ParadeState
from app.models.user import User

class ParadeStateRepository:
    def get_by_student_and_date(self, db: Session, student_id: str, parade_date: date) -> Optional[ParadeState]:
        return db.query(ParadeState).filter(ParadeState.student_id == student_id, ParadeState.date == parade_date).first()

    def get_parade_states_by_date(self, db: Session, parade_date: date) -> List[ParadeState]:
        results = db.query(ParadeState).filter(ParadeState.date == parade_date).all()
        for p in results:
            student = db.query(Student).filter(Student.id == p.student_id).first()
            if student:
                p.student_name = student.full_name
                p.student_service_number = student.service_number
                p.student_rank = student.rank
        return results

    def create_or_update(self, db: Session, *, student_id: str, parade_date: date, status: str, remarks: Optional[str] = None, user_id: Optional[str] = None) -> ParadeState:
        db_obj = self.get_by_student_and_date(db, student_id, parade_date)
        if db_obj:
            db_obj.status = status
            db_obj.remarks = remarks
            db_obj.updated_by = user_id
        else:
            db_obj = ParadeState(
                student_id=student_id,
                date=parade_date,
                status=status,
                remarks=remarks,
                updated_by=user_id
            )
            db.add(db_obj)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_summary(self, db: Session, parade_date: date) -> dict:
        total_enrolled = db.query(Student).filter(Student.deleted_at == None, Student.status != "Passed Out").count()
        states = db.query(ParadeState).filter(ParadeState.date == parade_date).all()
        
        summary = {
            "date": parade_date,
            "total_strength": total_enrolled,
            "present": 0,
            "sick_report": 0,
            "hospital": 0,
            "leave": 0,
            "temp_duty": 0,
            "course_visit": 0,
            "detached_duty": 0,
            "awol": 0
        }

        # Status counts mapping
        status_map = {
            "Present": "present",
            "Sick Report": "sick_report",
            "Hospital": "hospital",
            "Leave": "leave",
            "Temporary Duty": "temp_duty",
            "Course Visit": "course_visit",
            "Detached Duty": "detached_duty",
            "AWOL": "awol"
        }

        logged_student_ids = set()
        for state in states:
            logged_student_ids.add(state.student_id)
            key = status_map.get(state.status)
            if key:
                summary[key] += 1

        # Students with no recorded status for today are assumed "Present" by default in reports
        unrecorded_count = total_enrolled - len(logged_student_ids)
        if unrecorded_count > 0:
            summary["present"] += unrecorded_count

        return summary

parade_repo = ParadeStateRepository()
