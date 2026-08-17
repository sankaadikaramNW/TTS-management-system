from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

# --- Trade Schemas ---
class TradeBase(BaseModel):
    code: str
    label: str
    description: Optional[str] = None
    is_active: bool = True

class TradeCreate(TradeBase):
    pass

class TradeUpdate(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class TradeResponse(TradeBase):
    id: str
    courses_count: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Course Schemas ---
class CourseBase(BaseModel):
    code: str
    name: str
    trade_id: Optional[str] = None
    course_type: Optional[str] = "Basic"  # Basic, Advance, Special
    duration_weeks: int = 24
    intake_capacity: Optional[int] = 30
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    is_active: bool = True

    @field_validator('start_date', 'end_date', 'trade_id', 'description', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    trade_id: Optional[str] = None
    course_type: Optional[str] = None
    duration_weeks: Optional[int] = None
    intake_capacity: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('start_date', 'end_date', 'trade_id', 'description', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class CourseResponse(CourseBase):
    id: str
    trade_name: Optional[str] = None
    batches_count: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True

# --- Classroom Schemas ---
class ClassroomBase(BaseModel):
    code: str
    name: str
    block: Optional[str] = None
    building: Optional[str] = None
    capacity: int = 30
    description: Optional[str] = None
    is_active: bool = True

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    block: Optional[str] = None
    building: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ClassroomResponse(ClassroomBase):
    id: str
    is_occupied: Optional[bool] = False
    assigned_batch_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Batch Schemas ---
class BatchBase(BaseModel):
    name: str
    course_id: str
    trade_id: Optional[str] = None
    intake_date: Optional[date] = None
    passing_out_date: Optional[date] = None
    capacity: int = 30
    classroom_id: Optional[str] = None
    instructor_id: Optional[str] = None
    status: str = "Active"  # Active, Passed Out, Archived

    @field_validator('intake_date', 'passing_out_date', 'trade_id', 'classroom_id', 'instructor_id', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    name: Optional[str] = None
    course_id: Optional[str] = None
    trade_id: Optional[str] = None
    intake_date: Optional[date] = None
    passing_out_date: Optional[date] = None
    capacity: Optional[int] = None
    classroom_id: Optional[str] = None
    instructor_id: Optional[str] = None
    status: Optional[str] = None

    @field_validator('intake_date', 'passing_out_date', 'trade_id', 'classroom_id', 'instructor_id', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class BatchResponse(BatchBase):
    id: str
    course_name: Optional[str] = None
    trade_name: Optional[str] = None
    classroom_name: Optional[str] = None
    instructor_name: Optional[str] = None
    instructor_service_number: Optional[str] = None
    instructor_rank: Optional[str] = None
    student_count: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True

# --- Instructor Schema (SSOT from Users table) ---
class InstructorResponse(BaseModel):
    id: str
    username: str
    full_name: str
    service_number: Optional[str] = None
    rank: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    assigned_batches_count: Optional[int] = 0

    class Config:
        from_attributes = True

# --- Subject ---
class SubjectBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    periods: int = 40

class SubjectCreate(SubjectBase):
    course_id: str

class SubjectResponse(SubjectBase):
    id: str
    course_id: str
    course_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Lesson ---
class LessonBase(BaseModel):
    name: str
    description: Optional[str] = None

class LessonCreate(LessonBase):
    subject_id: str

class LessonResponse(LessonBase):
    id: str
    subject_id: str

    class Config:
        from_attributes = True

# --- Lesson Plan ---
class LessonPlanCreate(BaseModel):
    lesson_id: str
    instructor_id: str
    duration_minutes: int = 45
    objectives: Optional[str] = None
    training_aids: Optional[str] = None
    references_used: Optional[str] = None

class LessonPlanResponse(BaseModel):
    id: str
    lesson_id: str
    lesson_name: Optional[str] = None
    instructor_id: str
    instructor_name: Optional[str] = None
    duration_minutes: int
    objectives: Optional[str] = None
    training_aids: Optional[str] = None
    references_used: Optional[str] = None
    plan_doc_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Timetable ---
class TimetableBase(BaseModel):
    course_id: str
    date: date
    period_number: int  # 1..8
    subject_id: str
    lesson_id: str
    instructor_id: str
    location: Optional[str] = "Main Lecture Hall"

class TimetableCreate(TimetableBase):
    pass

class TimetableResponse(TimetableBase):
    id: str
    course_name: Optional[str] = None
    subject_name: Optional[str] = None
    lesson_name: Optional[str] = None
    instructor_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Attendance ---
class AttendanceRecord(BaseModel):
    student_id: str
    status: str  # Present, Absent, Excused
    remarks: Optional[str] = None

class TimetableAttendanceUpdateRequest(BaseModel):
    timetable_id: str
    records: List[AttendanceRecord]

class AttendanceResponse(BaseModel):
    id: str
    timetable_id: str
    student_id: str
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    status: str
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

# --- Exam ---
class ExamBase(BaseModel):
    course_id: str
    subject_id: str
    type: str  # Phase Test, Final Exam
    date: date
    max_marks: float = 100.0
    pass_marks: float = 50.0

class ExamCreate(ExamBase):
    pass

class ExamResponse(ExamBase):
    id: str
    course_name: Optional[str] = None
    subject_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Exam Mark ---
class ExamMarkRecord(BaseModel):
    student_id: str
    marks_obtained: float
    remarks: Optional[str] = None

class ExamMarkUpdateRequest(BaseModel):
    exam_id: str
    records: List[ExamMarkRecord]

class ExamMarkResponse(BaseModel):
    id: str
    exam_id: str
    student_id: str
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    marks_obtained: float
    status: str  # Pass, Fail, Absent
    remarks: Optional[str] = None
    entered_by: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Academic Dashboard Summary Schema ---
class AcademicDashboardSummary(BaseModel):
    total_trades: int
    total_courses: int
    active_batches: int
    active_instructors: int
    active_students: int
    available_classrooms: int
    pending_instructor_assignments: int = 0
    upcoming_phase_tests: int
    upcoming_final_exams: int
    classroom_utilization_rate: float
    batch_distribution_by_trade: List[Dict[str, Any]]
    recent_batches: List[Dict[str, Any]]
    upcoming_academic_activities: List[Dict[str, Any]]

# --- Lesson Plan Document Schemas ---
class LessonPlanDocumentCreate(BaseModel):
    """Fields received from the multipart upload form (metadata portion)."""
    course_id: str
    title: str
    lesson_id: Optional[str] = None
    subject_name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    academic_year: Optional[str] = None
    remarks: Optional[str] = None

    @field_validator('lesson_id', 'subject_name', 'version', 'description', 'academic_year', 'remarks', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class LessonPlanDocumentUpdate(BaseModel):
    """Partial metadata update (no file re-upload)."""
    title: Optional[str] = None
    description: Optional[str] = None
    subject_name: Optional[str] = None
    version: Optional[str] = None
    academic_year: Optional[str] = None
    remarks: Optional[str] = None
    lesson_id: Optional[str] = None

    @field_validator('lesson_id', 'subject_name', 'version', 'description', 'academic_year', 'remarks', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class LessonPlanDocumentResponse(BaseModel):
    id: str
    course_id: str
    lesson_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    subject_name: Optional[str] = None
    version: Optional[str] = None
    academic_year: Optional[str] = None
    remarks: Optional[str] = None
    original_file_name: str
    cloudinary_url: str
    resource_type: Optional[str] = 'raw'
    file_size: int
    mime_type: Optional[str] = 'application/pdf'
    uploaded_by: Optional[str] = None
    status: str = 'Active'
    uploaded_at: datetime
    updated_at: Optional[datetime] = None

    # Joined fields
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    trade_name: Optional[str] = None
    trade_id: Optional[str] = None
    uploader_name: Optional[str] = None
    uploader_service_number: Optional[str] = None
    lesson_name: Optional[str] = None

    class Config:
        from_attributes = True


# --- Course Calendar Schemas ---
class CourseCalendarCreate(BaseModel):
    serial_number: Optional[int] = Field(None, description="Order / Serial Number. Auto-assigned if omitted.")
    phase_name: str = Field(..., min_length=1, max_length=255, description="Name of the course phase/activity")
    subject_id: Optional[str] = Field(None, description="Linked subject ID from subjects table")
    theory_periods: int = Field(0, ge=0, description="Number of theory periods")
    practical_periods: int = Field(0, ge=0, description="Number of practical periods")
    working_days: int = Field(0, ge=0, description="Number of working days")
    commencement_date: date = Field(..., description="Commencement date")
    completion_date: date = Field(..., description="Completion date")
    instructor_id: Optional[str] = Field(None, description="Assigned instructor user ID")
    instructor_status: Optional[str] = Field("NOT_ASSIGNED", description="ASSIGNED or NOT_ASSIGNED")
    remarks: Optional[str] = Field(None, description="Optional remarks")

    @field_validator('instructor_id', 'subject_id', 'remarks', 'instructor_status', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class CourseCalendarUpdate(BaseModel):
    serial_number: Optional[int] = Field(None, ge=1)
    phase_name: Optional[str] = Field(None, min_length=1, max_length=255)
    subject_id: Optional[str] = Field(None, description="Linked subject ID from subjects table")
    theory_periods: Optional[int] = Field(None, ge=0)
    practical_periods: Optional[int] = Field(None, ge=0)
    working_days: Optional[int] = Field(None, ge=0)
    commencement_date: Optional[date] = None
    completion_date: Optional[date] = None
    instructor_id: Optional[str] = None
    instructor_status: Optional[str] = Field(None, description="ASSIGNED or NOT_ASSIGNED")
    remarks: Optional[str] = None
    status: Optional[str] = Field(None, description="Active, Archived")

    @field_validator('instructor_id', 'subject_id', 'remarks', 'instructor_status', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

class CourseCalendarResponse(BaseModel):
    id: str
    course_id: str
    subject_id: Optional[str] = None
    serial_number: int
    phase_name: str
    theory_periods: int
    practical_periods: int
    total_periods: int
    working_days: int
    commencement_date: date
    completion_date: date
    instructor_id: Optional[str] = None
    instructor_status: str = "NOT_ASSIGNED"
    remarks: Optional[str] = None
    status: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Joined fields
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    trade_name: Optional[str] = None
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    instructor_name: Optional[str] = None
    instructor_service_number: Optional[str] = None

    class Config:
        from_attributes = True

class CourseCalendarSummaryResponse(BaseModel):
    course_id: str
    course_name: str
    course_code: str
    trade_id: Optional[str] = None
    trade_name: Optional[str] = None
    total_phases: int
    total_theory_periods: int
    total_practical_periods: int
    total_periods: int
    total_working_days: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    lead_instructor_name: Optional[str] = None

class ReorderCalendarEntriesRequest(BaseModel):
    ordered_ids: List[str] = Field(..., description="List of CourseCalendar IDs in desired display order")

class AcademicCalendarEventItem(BaseModel):
    id: str
    course_id: str
    course_name: str
    course_code: str
    trade_id: Optional[str] = None
    trade_name: Optional[str] = None
    batch_name: Optional[str] = None
    activity: str
    serial_number: int
    start_date: date
    end_date: date
    instructor_id: Optional[str] = None
    instructor_name: Optional[str] = None
    instructor_status: str = "NOT_ASSIGNED"
    theory_periods: int = 0
    practical_periods: int = 0
    total_periods: int = 0
    working_days: int = 0
    remarks: Optional[str] = None

    class Config:
        from_attributes = True

class AcademicDashboardCalendarResponse(BaseModel):
    start_date: date
    end_date: date
    events: List[AcademicCalendarEventItem]

