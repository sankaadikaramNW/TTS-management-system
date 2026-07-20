from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.academic import Course, Subject, Lesson, LessonPlan, Timetable, AcademicAttendance, Exam, ExamMark
from app.models.student import Student
from app.models.user import User
from app.repositories.base import BaseRepository

class CourseRepository(BaseRepository[Course]):
    def get_all(self, db: Session) -> List[Course]:
        return db.query(Course).filter(Course.deleted_at == None).all()

class SubjectRepository(BaseRepository[Subject]):
    def get_by_course(self, db: Session, course_id: str) -> List[Subject]:
        return db.query(Subject).filter(Subject.course_id == course_id, Subject.deleted_at == None).all()

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

course_repo = CourseRepository(Course)
subject_repo = SubjectRepository(Subject)
lesson_repo = LessonRepository(Lesson)
lesson_plan_repo = LessonPlanRepository(LessonPlan)
timetable_repo = TimetableRepository(Timetable)
attendance_repo = AttendanceRepository(AcademicAttendance)
exam_repo = ExamRepository(Exam)
exam_mark_repo = ExamMarkRepository(ExamMark)
