from datetime import date
from typing import Optional, List, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.student import Student, PersonalOccurrence
from app.models.academic import Course
from app.models.user import User
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


class PersonalOccurrenceRepository(BaseRepository[PersonalOccurrence]):
    def _enrich(self, db: Session, occurrence: PersonalOccurrence) -> PersonalOccurrence:
        """Attach joined trainee and recorder details."""
        if occurrence.trainee_id:
            trainee = db.query(Student).filter(Student.id == occurrence.trainee_id).first()
            if trainee:
                occurrence.trainee_service_number = trainee.service_number
                occurrence.trainee_rank = trainee.rank
                occurrence.trainee_full_name = trainee.full_name
                occurrence.trainee_trade = trainee.trade
                occurrence.trainee_batch = trainee.batch

        if occurrence.created_by:
            creator = db.query(User).filter(User.id == occurrence.created_by).first()
            if creator:
                rank = creator.rank or ""
                name = creator.full_name or creator.username
                occurrence.creator_name = f"{rank} {name}".strip()
        else:
            occurrence.creator_name = None

        return occurrence

    def get_by_id(self, db: Session, occurrence_id: str) -> Optional[PersonalOccurrence]:
        occ = db.query(PersonalOccurrence).filter(
            PersonalOccurrence.id == occurrence_id,
            PersonalOccurrence.deleted_at == None
        ).first()
        if occ:
            self._enrich(db, occ)
        return occ

    def get_by_trainee(
        self,
        db: Session,
        trainee_id: str,
        occurrence_type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[PersonalOccurrence]:
        query = db.query(PersonalOccurrence).filter(
            PersonalOccurrence.trainee_id == trainee_id,
            PersonalOccurrence.deleted_at == None
        )
        if occurrence_type and occurrence_type.upper() != 'ALL':
            query = query.filter(PersonalOccurrence.occurrence_type == occurrence_type.upper())
        if date_from:
            query = query.filter(PersonalOccurrence.occurrence_date >= date_from)
        if date_to:
            query = query.filter(PersonalOccurrence.occurrence_date <= date_to)

        results = query.order_by(
            PersonalOccurrence.occurrence_date.desc(),
            PersonalOccurrence.created_at.desc()
        ).all()
        for occ in results:
            self._enrich(db, occ)
        return results

    def search_occurrences(
        self,
        db: Session,
        *,
        search_query: Optional[str] = None,
        trainee_id: Optional[str] = None,
        occurrence_type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[int, List[PersonalOccurrence]]:
        query = db.query(PersonalOccurrence).join(Student, PersonalOccurrence.trainee_id == Student.id).filter(
            PersonalOccurrence.deleted_at == None
        )

        if trainee_id:
            query = query.filter(PersonalOccurrence.trainee_id == trainee_id)

        if occurrence_type and occurrence_type.upper() != 'ALL':
            query = query.filter(PersonalOccurrence.occurrence_type == occurrence_type.upper())

        if date_from:
            query = query.filter(PersonalOccurrence.occurrence_date >= date_from)

        if date_to:
            query = query.filter(PersonalOccurrence.occurrence_date <= date_to)

        if search_query:
            term = f"%{search_query}%"
            query = query.filter(
                or_(
                    PersonalOccurrence.title.like(term),
                    PersonalOccurrence.description.like(term),
                    Student.service_number.like(term),
                    Student.full_name.like(term)
                )
            )

        total = query.count()
        results = query.order_by(
            PersonalOccurrence.occurrence_date.desc(),
            PersonalOccurrence.created_at.desc()
        ).offset(skip).limit(limit).all()

        for occ in results:
            self._enrich(db, occ)

        return total, results

personal_occurrence_repo = PersonalOccurrenceRepository(PersonalOccurrence)

