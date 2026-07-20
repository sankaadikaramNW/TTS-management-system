from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.repositories.academic import (
    course_repo, subject_repo, lesson_repo, timetable_repo, attendance_repo, exam_repo, exam_mark_repo
)
from app.services.academic import academic_service
from app.schemas.academic import (
    CourseResponse, CourseCreate, SubjectResponse, SubjectCreate, LessonResponse, LessonCreate,
    TimetableResponse, TimetableCreate, TimetableAttendanceUpdateRequest, AttendanceResponse,
    ExamResponse, ExamCreate, ExamMarkUpdateRequest, ExamMarkResponse
)

router = APIRouter(prefix="/academic", tags=["Academic Activities"])

# --- Courses ---
@router.get("/courses", response_model=List[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return course_repo.get_all(db)

@router.post("/courses", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Course
    db_course = Course(**course_data.model_dump())
    return course_repo.create(db, obj_in=db_course)

# --- Subjects ---
@router.get("/subjects/{course_id}", response_model=List[SubjectResponse])
def get_subjects(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return subject_repo.get_by_course(db, course_id)

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Subject
    db_subject = Subject(**subject_data.model_dump())
    return subject_repo.create(db, obj_in=db_subject)

# --- Lessons ---
@router.get("/lessons/{subject_id}", response_model=List[LessonResponse])
def get_lessons(
    subject_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return lesson_repo.get_by_subject(db, subject_id)

@router.post("/lessons", response_model=LessonResponse)
def create_lesson(
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Lesson
    db_lesson = Lesson(**lesson_data.model_dump())
    return lesson_repo.create(db, obj_in=db_lesson)

# --- Timetables ---
@router.get("/timetables", response_model=List[TimetableResponse])
def get_timetables(
    course_id: str,
    timetable_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    t_date = timetable_date or date.today()
    return timetable_repo.get_schedule(db, course_id, t_date)

@router.post("/timetables", response_model=TimetableResponse)
def create_timetable_slot(
    request: Request,
    timetable_data: TimetableCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return academic_service.create_timetable_entry(db, timetable_data, current_user.id, ip, ua)

# --- Attendance ---
@router.get("/attendance/{timetable_id}", response_model=List[AttendanceResponse])
def get_class_attendance(
    timetable_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return attendance_repo.get_by_timetable(db, timetable_id)

@router.post("/attendance", response_model=List[AttendanceResponse])
def record_class_attendance(
    request: Request,
    attendance_data: TimetableAttendanceUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return academic_service.update_timetable_attendance(db, attendance_data, current_user.id, ip, ua)

# --- Exams ---
@router.get("/exams/{course_id}", response_model=List[ExamResponse])
def get_exams(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return exam_repo.get_by_course(db, course_id)

@router.post("/exams", response_model=ExamResponse)
def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Exam
    db_exam = Exam(**exam_data.model_dump())
    return exam_repo.create(db, obj_in=db_exam)

# --- Exam Marks ---
@router.get("/exam-marks/{exam_id}", response_model=List[ExamMarkResponse])
def get_exam_grades(
    exam_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return exam_mark_repo.get_by_exam(db, exam_id)

@router.post("/exam-marks", response_model=List[ExamMarkResponse])
def record_exam_grades(
    request: Request,
    marks_data: ExamMarkUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return academic_service.enter_exam_marks(db, marks_data, current_user.id, ip, ua)
