from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Text, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

class Student(Base, TimeStampedModelMixin):
    __tablename__ = 'students'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_number = Column(String(30), unique=True, nullable=False, index=True)
    initials = Column(String(30), nullable=True, default='')
    full_name = Column(String(255), nullable=False)
    nic = Column(String(20), unique=True, nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True, default='Male')
    rank = Column(String(50), nullable=True, default='Aircraftman')
    trade = Column(String(50), nullable=True, default='Airframe')
    course_id = Column(String(36), ForeignKey('courses.id', ondelete='SET NULL'), nullable=True)
    batch = Column(String(30), nullable=True, default='N/A')
    squadron = Column(String(50), default='Training Squadron')
    unit = Column(String(50), default='SLAF TTS Ekala')
    posting = Column(String(100), nullable=True)
    joining_date = Column(Date, nullable=True)
    passing_out_date = Column(Date, nullable=True)
    status = Column(String(30), default='Active')  # Active, Sick, Leave, Detached, AWOL, Passed Out
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    blood_group = Column(String(10), nullable=True, default='O+')
    medical_category = Column(String(50), default='A4G4')
    religion = Column(String(30), nullable=True, default='Buddhist')
    nationality = Column(String(30), default='Sri Lankan')
    permanent_address = Column(Text, nullable=True)
    temporary_address = Column(Text, nullable=True)
    profile_photo_path = Column(String(255), nullable=True)
    qr_code_data = Column(Text, nullable=True)

    # Relationships
    course = relationship("Course", back_populates="students")
    parade_states = relationship("ParadeState", back_populates="student", cascade="all, delete-orphan")
    allocations = relationship("AccommodationAllocation", back_populates="student", cascade="all, delete-orphan")
    attendance = relationship("AcademicAttendance", back_populates="student", cascade="all, delete-orphan")
    exam_marks = relationship("ExamMark", back_populates="student", cascade="all, delete-orphan")
    occurrences = relationship("PersonalOccurrence", back_populates="trainee", cascade="all, delete-orphan")

class ParadeState(Base):
    __tablename__ = 'parade_states'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(30), nullable=False)  # Present, Sick Report, Hospital, Leave, Temporary Duty, Course Visit, Detached Duty, AWOL
    remarks = Column(Text, nullable=True)
    updated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    submission_id = Column(String(36), ForeignKey('parade_submissions.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="parade_states")
    updater = relationship("User")
    submission = relationship("ParadeSubmission", back_populates="parade_states")

class ParadeStatusType(Base):
    __tablename__ = 'parade_status_types'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StudentStatusType(Base):
    __tablename__ = 'student_status_types'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Rank(Base):
    __tablename__ = 'ranks'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False)
    label = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ParadeSubmission(Base):
    """Tracks the full two-stage workflow lifecycle for a daily parade per trade."""
    __tablename__ = 'parade_submissions'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    date = Column(Date, nullable=False, index=True)
    trade = Column(String(50), nullable=False)  # Trade name that this submission covers
    submitted_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    approving_officer_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status = Column(
        Enum('DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED', name='parade_submission_status'),
        nullable=False, default='DRAFT'
    )
    submitter_remarks = Column(Text, nullable=True)   # Remarks from NCO on submission
    approver_remarks = Column(Text, nullable=True)    # Remarks from Officer I/C on approval
    rejection_reason = Column(Text, nullable=True)    # Reason given on rejection
    submitted_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    submitter = relationship("User", foreign_keys=[submitted_by])
    approving_officer = relationship("User", foreign_keys=[approving_officer_id])
    parade_states = relationship("ParadeState", back_populates="submission")


class OfficerInCharge(Base):
    """Stores Officer I/C appointments per trade for the approval routing."""
    __tablename__ = 'officer_in_charge'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    trade = Column(String(50), nullable=False, index=True)    # Trade this officer is I/C of
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    appointed_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    is_active = Column(Boolean, default=True)
    appointed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    officer = relationship("User", foreign_keys=[user_id])
    appointed_by_user = relationship("User", foreign_keys=[appointed_by])


class PersonalOccurrence(Base, TimeStampedModelMixin):
    """Tracks significant personal occurrences (Achievements & Misconduct/Offenses) for trainees."""
    __tablename__ = 'personal_occurrences'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    trainee_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False, index=True)
    occurrence_type = Column(String(30), nullable=False, index=True)  # ACHIEVEMENT or MISCONDUCT_OFFENSE
    occurrence_date = Column(Date, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    remarks = Column(Text, nullable=True)
    status = Column(String(30), default='Active', index=True)
    created_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    trainee = relationship("Student", back_populates="occurrences")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])

    __table_args__ = (
        Index('idx_trainee_occ_date', 'trainee_id', 'occurrence_date'),
    )
