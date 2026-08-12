from datetime import date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.academic import Classroom, Course, Batch, Subject, Lesson, LessonPlan, Timetable, AcademicAttendance, Exam, ExamMark, LessonPlanDocument
from app.models.student import Student, Trade
from app.models.user import User, Role
from app.repositories.base import BaseRepository

class TradeRepository(BaseRepository[Trade]):
    def get_all(self, db: Session, include_inactive: bool = False) -> List[Trade]:
        query = db.query(Trade)
        if not include_inactive:
            query = query.filter(Trade.is_active == True)
        results = query.all()
        for t in results:
            t.courses_count = db.query(Course).filter(Course.trade_id == t.id).count()
        return results

    def get_by_code(self, db: Session, code: str) -> Optional[Trade]:
        return db.query(Trade).filter(Trade.code == code).first()

class ClassroomRepository(BaseRepository[Classroom]):
    def get_all(self, db: Session, include_inactive: bool = False) -> List[Classroom]:
        query = db.query(Classroom)
        if not include_inactive:
            query = query.filter(Classroom.is_active == True)
        results = query.all()
        for c in results:
            assigned_batch = db.query(Batch).filter(Batch.classroom_id == c.id, Batch.status == 'Active').first()
            c.is_occupied = assigned_batch is not None
            c.assigned_batch_name = assigned_batch.name if assigned_batch else None
        return results

    def get_by_code(self, db: Session, code: str) -> Optional[Classroom]:
        return db.query(Classroom).filter(Classroom.code == code).first()

class CourseRepository(BaseRepository[Course]):
    def get_all(self, db: Session) -> List[Course]:
        results = db.query(Course).filter(Course.deleted_at == None).all()
        for c in results:
            trade = db.query(Trade).filter(Trade.id == c.trade_id).first() if c.trade_id else None
            c.trade_name = trade.label if trade else "General"
            c.batches_count = db.query(Batch).filter(Batch.course_id == c.id).count()
        return results

    def get_by_trade(self, db: Session, trade_id: str) -> List[Course]:
        results = db.query(Course).filter(Course.trade_id == trade_id, Course.deleted_at == None).all()
        for c in results:
            trade = db.query(Trade).filter(Trade.id == c.trade_id).first() if c.trade_id else None
            c.trade_name = trade.label if trade else "General"
            c.batches_count = db.query(Batch).filter(Batch.course_id == c.id).count()
        return results

class BatchRepository(BaseRepository[Batch]):
    def get_all(self, db: Session) -> List[Batch]:
        results = db.query(Batch).order_by(Batch.created_at.desc()).all()
        for b in results:
            course = db.query(Course).filter(Course.id == b.course_id).first()
            trade = db.query(Trade).filter(Trade.id == b.trade_id).first() if b.trade_id else None
            classroom = db.query(Classroom).filter(Classroom.id == b.classroom_id).first() if b.classroom_id else None
            instructor = db.query(User).filter(User.id == b.instructor_id).first() if b.instructor_id else None
            
            b.course_name = course.name if course else "N/A"
            b.trade_name = trade.label if trade else "N/A"
            b.classroom_name = classroom.name if classroom else "Unassigned"
            b.instructor_name = instructor.full_name if instructor else "Unassigned"
            b.instructor_service_number = instructor.service_number if instructor else None
            b.instructor_rank = instructor.rank if instructor else None
            b.student_count = db.query(Student).filter(Student.course_id == b.course_id).count()
        return results

class InstructorRepository:
    def get_instructors(self, db: Session) -> List[Dict[str, Any]]:
        """
        Retrieves active instructors from the User Management Module (SSOT).
        Queries users with role 'Instructor' or designation containing Instructor.
        """
        query = db.query(User).join(Role, User.role_id == Role.id, isouter=True)\
                  .filter(User.deleted_at == None, User.is_active == True)
        
        users = query.all()
        instructors = []
        for u in users:
            is_inst = (u.role and u.role.name == 'Instructor') or \
                      (u.designation and 'instructor' in u.designation.lower()) or \
                      (u.assigned_module and 'academic' in u.assigned_module.lower())
            if is_inst:
                assigned_count = db.query(Batch).filter(Batch.instructor_id == u.id, Batch.status == 'Active').count()
                instructors.append({
                    "id": u.id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "service_number": u.service_number,
                    "rank": u.rank,
                    "department": u.department,
                    "designation": u.designation,
                    "email": u.email,
                    "mobile_number": u.mobile_number,
                    "assigned_batches_count": assigned_count
                })
        
        # Fallback if no specific role set: return all active staff/officers
        if not instructors:
            all_users = db.query(User).filter(User.deleted_at == None, User.is_active == True).limit(20).all()
            for u in all_users:
                assigned_count = db.query(Batch).filter(Batch.instructor_id == u.id, Batch.status == 'Active').count()
                instructors.append({
                    "id": u.id,
                    "username": u.username,
                    "full_name": u.full_name,
                    "service_number": u.service_number,
                    "rank": u.rank,
                    "department": u.department,
                    "designation": u.designation,
                    "email": u.email,
                    "mobile_number": u.mobile_number,
                    "assigned_batches_count": assigned_count
                })
        return instructors

class SubjectRepository(BaseRepository[Subject]):
    def get_by_course(self, db: Session, course_id: str) -> List[Subject]:
        results = db.query(Subject).filter(Subject.course_id == course_id, Subject.deleted_at == None).all()
        for s in results:
            c = db.query(Course).filter(Course.id == s.course_id).first()
            s.course_name = c.name if c else None
        return results

class LessonRepository(BaseRepository[Lesson]):
    def get_by_subject(self, db: Session, subject_id: str) -> List[Lesson]:
        return db.query(Lesson).filter(Lesson.subject_id == subject_id).all()

class LessonPlanRepository(BaseRepository[LessonPlan]):
    def get_by_lesson(self, db: Session, lesson_id: str) -> Optional[LessonPlan]:
        plan = db.query(LessonPlan).filter(LessonPlan.lesson_id == lesson_id).first()
        if plan:
            lesson = db.query(Lesson).filter(Lesson.id == plan.lesson_id).first()
            instructor = db.query(User).filter(User.id == plan.instructor_id).first()
            plan.lesson_name = lesson.name if lesson else None
            plan.instructor_name = instructor.full_name if instructor else None
        return plan

class TimetableRepository(BaseRepository[Timetable]):
    def get_schedule(self, db: Session, course_id: str, schedule_date: date) -> List[Timetable]:
        results = db.query(Timetable).filter(
            Timetable.course_id == course_id,
            Timetable.date == schedule_date
        ).order_by(Timetable.period_number).all()
        
        for t in results:
            course = db.query(Course).filter(Course.id == t.course_id).first()
            subject = db.query(Subject).filter(Subject.id == t.subject_id).first()
            lesson = db.query(Lesson).filter(Lesson.id == t.lesson_id).first()
            instructor = db.query(User).filter(User.id == t.instructor_id).first()
            
            t.course_name = course.name if course else None
            t.subject_name = subject.name if subject else None
            t.lesson_name = lesson.name if lesson else None
            t.instructor_name = instructor.full_name if instructor else None
            
        return results

class AttendanceRepository(BaseRepository[AcademicAttendance]):
    def get_by_timetable(self, db: Session, timetable_id: str) -> List[AcademicAttendance]:
        results = db.query(AcademicAttendance).filter(AcademicAttendance.timetable_id == timetable_id).all()
        for att in results:
            student = db.query(Student).filter(Student.id == att.student_id).first()
            if student:
                att.student_name = student.full_name
                att.student_service_number = student.service_number
        return results

class ExamRepository(BaseRepository[Exam]):
    def get_by_course(self, db: Session, course_id: str) -> List[Exam]:
        results = db.query(Exam).filter(Exam.course_id == course_id, Exam.deleted_at == None).all()
        for ex in results:
            course = db.query(Course).filter(Course.id == ex.course_id).first()
            subj = db.query(Subject).filter(Subject.id == ex.subject_id).first()
            ex.course_name = course.name if course else None
            ex.subject_name = subj.name if subj else None
        return results

class ExamMarkRepository(BaseRepository[ExamMark]):
    def get_by_exam(self, db: Session, exam_id: str) -> List[ExamMark]:
        results = db.query(ExamMark).filter(ExamMark.exam_id == exam_id).all()
        for em in results:
            student = db.query(Student).filter(Student.id == em.student_id).first()
            if student:
                em.student_name = student.full_name
                em.student_service_number = student.service_number
        return results

class LessonPlanDocumentRepository(BaseRepository[LessonPlanDocument]):
    def _enrich(self, db: Session, doc: LessonPlanDocument) -> LessonPlanDocument:
        """Attach joined fields to a LessonPlanDocument instance."""
        course = db.query(Course).filter(Course.id == doc.course_id).first() if doc.course_id else None
        trade = None
        if course and course.trade_id:
            trade = db.query(Trade).filter(Trade.id == course.trade_id).first()
        uploader = db.query(User).filter(User.id == doc.uploaded_by).first() if doc.uploaded_by else None
        lesson = db.query(Lesson).filter(Lesson.id == doc.lesson_id).first() if doc.lesson_id else None

        doc.course_name = course.name if course else None
        doc.course_code = course.code if course else None
        doc.trade_name = trade.label if trade else None
        doc.trade_id = trade.id if trade else None
        doc.uploader_name = uploader.full_name if uploader else None
        doc.uploader_service_number = uploader.service_number if uploader else None
        doc.lesson_name = lesson.name if lesson else None
        return doc

    def get_by_id(self, db: Session, doc_id: str) -> Optional[LessonPlanDocument]:
        doc = db.query(LessonPlanDocument).filter(LessonPlanDocument.id == doc_id).first()
        if doc:
            self._enrich(db, doc)
        return doc

    def get_by_course(self, db: Session, course_id: str, status: str = 'Active') -> List[LessonPlanDocument]:
        query = db.query(LessonPlanDocument).filter(LessonPlanDocument.course_id == course_id)
        if status and status != 'All':
            query = query.filter(LessonPlanDocument.status == status)
        results = query.order_by(LessonPlanDocument.uploaded_at.desc()).all()
        for doc in results:
            self._enrich(db, doc)
        return results

    def search(
        self,
        db: Session,
        search: Optional[str] = None,
        course_id: Optional[str] = None,
        trade_id: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[LessonPlanDocument]:
        query = db.query(LessonPlanDocument)

        if status and status != 'All':
            query = query.filter(LessonPlanDocument.status == status)
        else:
            # Default: show Active only
            query = query.filter(LessonPlanDocument.status == 'Active')

        if course_id:
            query = query.filter(LessonPlanDocument.course_id == course_id)

        if trade_id:
            # Join through courses to filter by trade
            course_ids = [c.id for c in db.query(Course).filter(Course.trade_id == trade_id).all()]
            query = query.filter(LessonPlanDocument.course_id.in_(course_ids))

        if search:
            search_term = f"%{search}%"
            from sqlalchemy import or_
            query = query.filter(
                or_(
                    LessonPlanDocument.title.ilike(search_term),
                    LessonPlanDocument.original_file_name.ilike(search_term),
                    LessonPlanDocument.subject_name.ilike(search_term),
                    LessonPlanDocument.description.ilike(search_term)
                )
            )

        results = query.order_by(LessonPlanDocument.uploaded_at.desc()).offset(skip).limit(limit).all()
        for doc in results:
            self._enrich(db, doc)
        return results

trade_repo = TradeRepository(Trade)
classroom_repo = ClassroomRepository(Classroom)
course_repo = CourseRepository(Course)
batch_repo = BatchRepository(Batch)
instructor_repo = InstructorRepository()
subject_repo = SubjectRepository(Subject)
lesson_repo = LessonRepository(Lesson)
lesson_plan_repo = LessonPlanRepository(LessonPlan)
lesson_plan_doc_repo = LessonPlanDocumentRepository(LessonPlanDocument)
timetable_repo = TimetableRepository(Timetable)
attendance_repo = AttendanceRepository(AcademicAttendance)
exam_repo = ExamRepository(Exam)
exam_mark_repo = ExamMarkRepository(ExamMark)

