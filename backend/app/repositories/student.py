from typing import Optional, List, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.academic import Course
from app.repositories.base import BaseRepository

class StudentRepository(BaseRepository[Student]):
    def get_by_service_number(self, db: Session, service_number: str) -> Optional[Student]:
        return db.query(Student).filter(Student.service_number == service_number, Student.deleted_at == None).first()

    def get_by_nic(self, db: Session, nic: str) -> Optional[Student]:
        return db.query(Student).filter(Student.nic == nic, Student.deleted_at == None).first()

    def search_students(
        self, 
        db: Session, 
        *, 
        search_query: Optional[str] = None, 
        rank: Optional[str] = None,
        trade: Optional[str] = None,
        course_id: Optional[str] = None,
        status: Optional[str] = None,
        squadron: Optional[str] = None,
        skip: int = 0, 
        limit: int = 20
    ) -> Tuple[int, List[Student]]:
        query = db.query(Student).filter(Student.deleted_at == None)

        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter(
                or_(
                    Student.service_number.like(search_pattern),
                    Student.full_name.like(search_pattern),
                    Student.initials.like(search_pattern),
                    Student.nic.like(search_pattern)
                )
            )

        if rank:
            query = query.filter(Student.rank == rank)
        if trade:
            query = query.filter(Student.trade == trade)
        if course_id:
            query = query.filter(Student.course_id == course_id)
        if status:
            query = query.filter(Student.status == status)
        if squadron:
            query = query.filter(Student.squadron == squadron)

        total = query.count()
        results = query.offset(skip).limit(limit).all()
        
        # Load course details for response output matching
        for student in results:
            if student.course_id:
                course = db.query(Course).filter(Course.id == student.course_id).first()
                student.course_name = course.name if course else None
            else:
                student.course_name = None

        return total, results

student_repo = StudentRepository(Student)
