from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

# --- Course ---
class CourseBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    duration_weeks: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: str
    created_at: datetime
    
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
