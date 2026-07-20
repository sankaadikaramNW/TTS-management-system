from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Double, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

class Course(Base, TimeStampedModelMixin):
    __tablename__ = 'courses'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    duration_weeks = Column(Integer, nullable=False)

    # Relationships
    students = relationship("Student", back_populates="course")
    subjects = relationship("Subject", back_populates="course", cascade="all, delete-orphan")
    timetables = relationship("Timetable", back_populates="course", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="course", cascade="all, delete-orphan")

class Subject(Base, TimeStampedModelMixin):
    __tablename__ = 'subjects'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    code = Column(String(30), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    periods = Column(Integer, default=40, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="subjects")
    lessons = relationship("Lesson", back_populates="subject", cascade="all, delete-orphan")
    timetables = relationship("Timetable", back_populates="subject", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="subject", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    subject_id = Column(String(36), ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subject = relationship("Subject", back_populates="lessons")
    lesson_plans = relationship("LessonPlan", back_populates="lesson", cascade="all, delete-orphan")
    timetables = relationship("Timetable", back_populates="lesson")

class LessonPlan(Base):
    __tablename__ = 'lesson_plans'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    lesson_id = Column(String(36), ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    instructor_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    duration_minutes = Column(Integer, default=45)
    objectives = Column(Text, nullable=True)
    training_aids = Column(Text, nullable=True)
    references_used = Column(Text, nullable=True)
    plan_doc_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lesson = relationship("Lesson", back_populates="lesson_plans")
    instructor = relationship("User")

class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    period_number = Column(Integer, nullable=False)  # 1, 2, 3, 4, 5, 6, 7, 8
    subject_id = Column(String(36), ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(String(36), ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False)
    instructor_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    location = Column(String(100), default='Main Lecture Hall')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="timetables")
    subject = relationship("Subject", back_populates="timetables")
    lesson = relationship("Lesson", back_populates="timetables")
    instructor = relationship("User")
    attendance = relationship("AcademicAttendance", back_populates="timetable", cascade="all, delete-orphan")

class AcademicAttendance(Base):
    __tablename__ = 'academic_attendance'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timetable_id = Column(String(36), ForeignKey('timetables.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(20), default='Present')  # Present, Absent, Excused
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    timetable = relationship("Timetable", back_populates="attendance")
    student = relationship("Student", back_populates="attendance")

class Exam(Base, TimeStampedModelMixin):
    __tablename__ = 'exams'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(String(36), ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(30), nullable=False)  # Phase Test, Final Exam
    date = Column(Date, nullable=False)
    max_marks = Column(Double, default=100.0)
    pass_marks = Column(Double, default=50.0)

    # Relationships
    course = relationship("Course", back_populates="exams")
    subject = relationship("Subject", back_populates="exams")
    marks = relationship("ExamMark", back_populates="exam", cascade="all, delete-orphan")

class ExamMark(Base):
    __tablename__ = 'exam_marks'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    exam_id = Column(String(36), ForeignKey('exams.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    marks_obtained = Column(Double, nullable=False)
    status = Column(String(20), nullable=False)  # Pass, Fail, Absent
    remarks = Column(Text, nullable=True)
    entered_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exam = relationship("Exam", back_populates="marks")
    student = relationship("Student", back_populates="exam_marks")
    recorder = relationship("User")
