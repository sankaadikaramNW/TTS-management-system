from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

class Student(Base, TimeStampedModelMixin):
    __tablename__ = 'students'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_number = Column(String(30), unique=True, nullable=False, index=True)
    initials = Column(String(30), nullable=False)
    full_name = Column(String(255), nullable=False)
    nic = Column(String(20), unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    rank = Column(String(50), nullable=False)
    trade = Column(String(50), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.id', ondelete='SET NULL'), nullable=True)
    batch = Column(String(30), nullable=False)
    squadron = Column(String(50), default='Training Squadron')
    unit = Column(String(50), default='SLAF TTS Ekala')
    posting = Column(String(100), nullable=True)
    joining_date = Column(Date, nullable=False)
    passing_out_date = Column(Date, nullable=True)
    status = Column(String(30), default='Active')  # Active, Sick, Leave, Detached, AWOL, Passed Out
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(100), nullable=False)
    emergency_contact_phone = Column(String(20), nullable=False)
    blood_group = Column(String(10), nullable=False)
    medical_category = Column(String(50), default='A4G4')
    religion = Column(String(30), nullable=False)
    nationality = Column(String(30), default='Sri Lankan')
    permanent_address = Column(Text, nullable=False)
    temporary_address = Column(Text, nullable=True)
    profile_photo_path = Column(String(255), nullable=True)
    qr_code_data = Column(Text, nullable=True)

    # Relationships
    course = relationship("Course", back_populates="students")
    parade_states = relationship("ParadeState", back_populates="student", cascade="all, delete-orphan")
    allocations = relationship("AccommodationAllocation", back_populates="student", cascade="all, delete-orphan")
    attendance = relationship("AcademicAttendance", back_populates="student", cascade="all, delete-orphan")
    exam_marks = relationship("ExamMark", back_populates="student", cascade="all, delete-orphan")

class ParadeState(Base):
    __tablename__ = 'parade_states'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(30), nullable=False)  # Present, Sick Report, Hospital, Leave, Temporary Duty, Course Visit, Detached Duty, AWOL
    remarks = Column(Text, nullable=True)
    updated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="parade_states")
    updater = relationship("User")
