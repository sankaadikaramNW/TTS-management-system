from datetime import date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.models.student import Student, Trade
from app.repositories.academic import (
    trade_repo, classroom_repo, course_repo, batch_repo, instructor_repo,
    subject_repo, lesson_repo, timetable_repo, attendance_repo, exam_repo, exam_mark_repo,
    lesson_plan_doc_repo, course_calendar_repo
)
from app.services.academic import academic_service
from app.services.lesson_plan_service import lesson_plan_service
from app.services.course_calendar_service import course_calendar_service
from app.schemas.academic import (
    TradeResponse, TradeCreate, TradeUpdate,
    CourseResponse, CourseCreate, CourseUpdate,
    ClassroomResponse, ClassroomCreate, ClassroomUpdate,
    BatchResponse, BatchCreate, BatchUpdate,
    InstructorResponse, AcademicDashboardSummary,
    SubjectResponse, SubjectCreate, LessonResponse, LessonCreate,
    TimetableResponse, TimetableCreate, TimetableAttendanceUpdateRequest, AttendanceResponse,
    ExamResponse, ExamCreate, ExamMarkUpdateRequest, ExamMarkResponse,
    LessonPlanDocumentResponse, LessonPlanDocumentUpdate,
    CourseCalendarCreate, CourseCalendarUpdate, CourseCalendarResponse,
    CourseCalendarSummaryResponse, ReorderCalendarEntriesRequest
)

router = APIRouter(prefix="/academic", tags=["Academic Activities Management Module"])

# --- 1. Academic Dashboard Summary ---
@router.get("/dashboard-summary", response_model=AcademicDashboardSummary)
def get_academic_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    from app.models.student import Student, Trade
    from app.models.academic import Course, Batch, Classroom, Exam, Timetable

    total_trades = db.query(Trade).filter(Trade.is_active == True).count()
    total_courses = db.query(Course).filter(Course.deleted_at == None).count()
    active_batches = db.query(Batch).filter(Batch.status == 'Active').count()
    
    # Active Instructors count from SSOT Users
    instructors = instructor_repo.get_instructors(db)
    active_instructors = len(instructors)
    
    active_students = db.query(Student).filter(Student.status == 'Active').count()
    
    total_classrooms = db.query(Classroom).filter(Classroom.is_active == True).count()
    occupied_classrooms = db.query(Batch).filter(Batch.classroom_id != None, Batch.status == 'Active').count()
    available_classrooms = max(0, total_classrooms - occupied_classrooms)
    utilization_rate = round((occupied_classrooms / total_classrooms * 100), 1) if total_classrooms > 0 else 0.0

    today = date.today()
    upcoming_phase_tests = db.query(Exam).filter(Exam.type == 'Phase Test', Exam.date >= today).count()
    upcoming_final_exams = db.query(Exam).filter(Exam.type == 'Final Exam', Exam.date >= today).count()

    # Batch distribution by trade
    trades_list = db.query(Trade).filter(Trade.is_active == True).all()
    batch_distribution = []
    for t in trades_list:
        cnt = db.query(Batch).filter(Batch.trade_id == t.id, Batch.status == 'Active').count()
        batch_distribution.append({
            "trade": t.label,
            "code": t.code,
            "active_batches": cnt
        })

    # Recent batches
    recent_batches_db = db.query(Batch).order_by(Batch.created_at.desc()).limit(5).all()
    recent_batches = []
    for b in recent_batches_db:
        c = db.query(Course).filter(Course.id == b.course_id).first()
        cl = db.query(Classroom).filter(Classroom.id == b.classroom_id).first() if b.classroom_id else None
        inst = db.query(User).filter(User.id == b.instructor_id).first() if b.instructor_id else None
        recent_batches.append({
            "id": b.id,
            "name": b.name,
            "course_name": c.name if c else "N/A",
            "classroom": cl.name if cl else "Unassigned",
            "instructor": inst.full_name if inst else "Unassigned",
            "status": b.status,
            "intake_date": str(b.intake_date) if b.intake_date else "N/A"
        })

    # Upcoming activities
    upcoming_activities = [
        {"title": "Phase Test 01 - Computer Tech 26/1", "type": "Exam", "date": "Tomorrow, 09:00 AM", "location": "E-01 Lab"},
        {"title": "Avionics System Overview Lecture", "type": "Lecture", "date": "10 Aug 2026", "location": "H-02 Hall"},
        {"title": "Final Trade Examination", "type": "Final Exam", "date": "15 Aug 2026", "location": "Main Examination Hall"},
        {"title": "Instructor Evaluation & Briefing", "type": "Meeting", "date": "18 Aug 2026", "location": "Academic Board Room"}
    ]

    return {
        "total_trades": total_trades,
        "total_courses": total_courses,
        "active_batches": active_batches,
        "active_instructors": active_instructors,
        "active_students": active_students,
        "available_classrooms": available_classrooms,
        "upcoming_phase_tests": upcoming_phase_tests,
        "upcoming_final_exams": upcoming_final_exams,
        "classroom_utilization_rate": utilization_rate,
        "batch_distribution_by_trade": batch_distribution,
        "recent_batches": recent_batches,
        "upcoming_academic_activities": upcoming_activities
    }


# --- 2. Trade Management ---
@router.get("/trades", response_model=List[TradeResponse])
def get_trades(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return trade_repo.get_all(db, include_inactive)

@router.post("/trades", response_model=TradeResponse)
def create_trade(
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.student import Trade
    existing_code = db.query(Trade).filter(Trade.code == trade_in.code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail=f"Trade code '{trade_in.code}' already exists")
    existing_name = db.query(Trade).filter(Trade.label == trade_in.label).first()
    if existing_name:
        raise HTTPException(status_code=400, detail=f"Trade name '{trade_in.label}' already exists")

    db_trade = Trade(
        code=trade_in.code.upper(),
        label=trade_in.label,
        description=trade_in.description,
        is_active=trade_in.is_active
    )
    return trade_repo.create(db, obj_in=db_trade)

@router.put("/trades/{trade_id}", response_model=TradeResponse)
def update_trade(
    trade_id: str,
    trade_in: TradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    t = trade_repo.get(db, trade_id)
    if not t:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    if trade_in.code and trade_in.code != t.code:
        dup = db.query(Trade).filter(Trade.code == trade_in.code, Trade.id != trade_id).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"Trade code '{trade_in.code}' already exists")
        t.code = trade_in.code.upper()
    if trade_in.label:
        t.label = trade_in.label
    if trade_in.description is not None:
        t.description = trade_in.description
    if trade_in.is_active is not None:
        t.is_active = trade_in.is_active

    db.commit()
    db.refresh(t)
    return t


# --- 3. Course Management ---
@router.get("/courses", response_model=List[CourseResponse])
def get_courses(
    trade_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    if trade_id and trade_id.strip():
        return course_repo.get_by_trade(db, trade_id.strip())
    return course_repo.get_all(db)

@router.post("/courses", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Course
    existing = db.query(Course).filter(Course.code == course_data.code, Course.deleted_at == None).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Course code/number '{course_data.code}' already exists")
    
    db_course = Course(**course_data.model_dump())
    return course_repo.create(db, obj_in=db_course)

@router.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: str,
    course_in: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Course
    c = course_repo.get(db, course_id)
    if not c or c.deleted_at:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(c, field, val)

    db.commit()
    db.refresh(c)
    return c


# --- 4. Classroom Management ---
@router.get("/classrooms", response_model=List[ClassroomResponse])
def get_classrooms(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return classroom_repo.get_all(db, include_inactive)

@router.post("/classrooms", response_model=ClassroomResponse)
def create_classroom(
    cls_in: ClassroomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Classroom
    existing = db.query(Classroom).filter(Classroom.code == cls_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Classroom ID '{cls_in.code}' already exists")
    if cls_in.capacity <= 0:
        raise HTTPException(status_code=400, detail="Classroom capacity must be greater than zero")

    db_cls = Classroom(**cls_in.model_dump())
    return classroom_repo.create(db, obj_in=db_cls)

@router.put("/classrooms/{classroom_id}", response_model=ClassroomResponse)
def update_classroom(
    classroom_id: str,
    cls_in: ClassroomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Classroom
    c = classroom_repo.get(db, classroom_id)
    if not c:
        raise HTTPException(status_code=404, detail="Classroom not found")

    update_data = cls_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(c, field, val)

    db.commit()
    db.refresh(c)
    return c


# --- 5. Batch Management ---
@router.get("/batches", response_model=List[BatchResponse])
def get_batches(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    return batch_repo.get_all(db)

@router.post("/batches", response_model=BatchResponse)
def create_batch(
    batch_in: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Batch, Course, Classroom
    course = db.query(Course).filter(Course.id == batch_in.course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="Selected course does not exist")
    
    if batch_in.classroom_id:
        classroom = db.query(Classroom).filter(Classroom.id == batch_in.classroom_id).first()
        if not classroom or not classroom.is_active:
            raise HTTPException(status_code=400, detail="Assigned classroom is not active or invalid")

    db_batch = Batch(**batch_in.model_dump())
    return batch_repo.create(db, obj_in=db_batch)

@router.put("/batches/{batch_id}", response_model=BatchResponse)
def update_batch(
    batch_id: str,
    batch_in: BatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    from app.models.academic import Batch
    b = batch_repo.get(db, batch_id)
    if not b:
        raise HTTPException(status_code=404, detail="Batch not found")

    update_data = batch_in.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(b, field, val)

    db.commit()
    db.refresh(b)
    return b


# --- 6. Instructor Retrieval (SSOT User Management Integration) ---
@router.get("/instructors", response_model=List[InstructorResponse])
def get_instructors_from_user_management(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """
    Business Rule Requirement:
    Retrieves instructors directly from the User Management Module (SSOT).
    Filters active users assigned the 'Instructor' role.
    """
    return instructor_repo.get_instructors(db)


# --- 7. Subjects & Lessons ---
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


# --- 8. Timetables & Attendance ---
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


# --- 9. Exams & Results ---
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


# --- 10. Academic Reports Endpoint ---
@router.get("/reports/{report_type}")
def get_academic_report(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    if report_type == "trade":
        trades = trade_repo.get_all(db, True)
        return [{"trade_code": t.code, "trade_name": t.label, "description": t.description, "courses": t.courses_count, "status": "Active" if t.is_active else "Inactive"} for t in trades]
    
    elif report_type == "course":
        courses = course_repo.get_all(db)
        return [{"code": c.code, "name": c.name, "trade": c.trade_name, "type": c.course_type, "duration": f"{c.duration_weeks} Wks", "capacity": c.intake_capacity, "status": "Active" if c.is_active else "Inactive"} for c in courses]

    elif report_type == "batch":
        batches = batch_repo.get_all(db)
        return [{"batch_name": b.name, "course": b.course_name, "trade": b.trade_name, "classroom": b.classroom_name, "instructor": b.instructor_name, "status": b.status} for b in batches]

    elif report_type == "classroom":
        classrooms = classroom_repo.get_all(db, True)
        return [{"classroom_code": c.code, "name": c.name, "block": c.block or "Main", "capacity": c.capacity, "status": "Occupied" if c.is_occupied else "Available", "assigned_batch": c.assigned_batch_name or "None"} for c in classrooms]

    elif report_type == "instructor":
        instructors = instructor_repo.get_instructors(db)
        return [{"service_no": i["service_number"] or "N/A", "rank": i["rank"] or "N/A", "name": i["full_name"], "department": i["department"] or "Academic", "assigned_batches": i["assigned_batches_count"]} for i in instructors]

    else:
        raise HTTPException(status_code=400, detail="Invalid report type specified")


# --- 11. Lesson Plan Document Management ---
@router.get("/lesson-plans", response_model=List[LessonPlanDocumentResponse])
def list_lesson_plans(
    course_id: Optional[str] = Query(None),
    trade_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """List lesson plan documents with optional filters."""
    return lesson_plan_doc_repo.search(
        db, search=search, course_id=course_id,
        trade_id=trade_id, status=status, skip=skip, limit=limit
    )

@router.get("/lesson-plans/{doc_id}", response_model=LessonPlanDocumentResponse)
def get_lesson_plan(
    doc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Get a single lesson plan document by ID."""
    doc = lesson_plan_doc_repo.get_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Lesson plan document not found.")
    return doc

@router.get("/lesson-plans/{doc_id}/file")
def stream_lesson_plan_file(
    doc_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Stream raw PDF file bytes for inline preview or download."""
    file_bytes, filename, mime_type = lesson_plan_service.download_document_bytes(db, doc_id)
    return Response(
        content=file_bytes,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Content-Type": mime_type,
            "Cache-Control": "public, max-age=3600"
        }
    )

@router.post("/lesson-plans", response_model=LessonPlanDocumentResponse)
def upload_lesson_plan(
    request: Request,
    file: UploadFile = File(...),
    course_id: str = Form(...),
    title: str = Form(...),
    lesson_id: Optional[str] = Form(None),
    subject_name: Optional[str] = Form(None),
    version: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    remarks: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Upload a new lesson plan PDF document."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")

    created_doc = lesson_plan_service.create_document(
        db=db,
        file=file,
        course_id=course_id,
        title=title,
        user_id=current_user.id,
        lesson_id=lesson_id if lesson_id and lesson_id.strip() else None,
        subject_name=subject_name if subject_name and subject_name.strip() else None,
        version=version if version and version.strip() else None,
        description=description if description and description.strip() else None,
        academic_year=academic_year if academic_year and academic_year.strip() else None,
        remarks=remarks if remarks and remarks.strip() else None,
        ip=ip,
        ua=ua
    )
    # Re-fetch with enriched fields
    return lesson_plan_doc_repo.get_by_id(db, created_doc.id)

@router.put("/lesson-plans/{doc_id}", response_model=LessonPlanDocumentResponse)
def update_lesson_plan_metadata(
    doc_id: str,
    update_in: LessonPlanDocumentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Update lesson plan metadata (no file re-upload)."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    update_data = update_in.model_dump(exclude_unset=True)
    return lesson_plan_service.update_metadata(db, doc_id, update_data, current_user.id, ip, ua)

@router.post("/lesson-plans/{doc_id}/replace", response_model=LessonPlanDocumentResponse)
def replace_lesson_plan_file(
    doc_id: str,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Replace the PDF file for an existing lesson plan document."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return lesson_plan_service.replace_document(db, doc_id, file, current_user.id, ip, ua)

@router.patch("/lesson-plans/{doc_id}/archive", response_model=LessonPlanDocumentResponse)
def archive_lesson_plan(
    doc_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Archive (soft-delete) a lesson plan document."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return lesson_plan_service.archive_document(db, doc_id, current_user.id, ip, ua)

@router.delete("/lesson-plans/{doc_id}")
def delete_lesson_plan(
    doc_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Permanently delete a lesson plan document (admin-level)."""
    # Extra authorization check: only Super Admin / System Admin can permanently delete
    if current_user.role.name not in ["Super Administrator", "System Administrator"] and \
       current_user.role_id not in ["role-super-admin", "role-sys-admin"]:
        raise HTTPException(status_code=403, detail="Only administrators can permanently delete lesson plan documents.")

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return lesson_plan_service.delete_document(db, doc_id, current_user.id, ip, ua)

@router.get("/courses/{course_id}/lesson-plans", response_model=List[LessonPlanDocumentResponse])
def get_course_lesson_plans(
    course_id: str,
    status: Optional[str] = Query('Active'),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Get all lesson plan documents for a specific course."""
    return lesson_plan_doc_repo.get_by_course(db, course_id, status=status or 'Active')


# --- 12. Course Calendar Management ---
@router.get("/instructors/active")
def get_active_instructors(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Fetch active instructors available for course calendar phase assignment."""
    return course_calendar_service.get_active_instructors(db)

@router.get("/course-calendars", response_model=List[CourseCalendarSummaryResponse])
def list_course_calendars(
    trade_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """List summary of active course calendars."""
    courses = course_repo.get_all(db)
    if trade_id:
        courses = [c for c in courses if c.trade_id == trade_id]

    summaries = []
    for c in courses:
        entries = course_calendar_repo.get_by_course(db, c.id)
        if entries:
            total_theory = sum(e.theory_periods for e in entries)
            total_prac = sum(e.practical_periods for e in entries)
            total_periods = sum(e.total_periods for e in entries)
            total_days = sum(e.working_days for e in entries)
            first_comm = min((e.commencement_date for e in entries), default=c.start_date)
            last_comp = max((e.completion_date for e in entries), default=c.end_date)
            lead_inst = next((e.instructor_name for e in entries if e.instructor_name), None)

            summaries.append(CourseCalendarSummaryResponse(
                course_id=c.id,
                course_name=c.name,
                course_code=c.code,
                trade_id=c.trade_id,
                trade_name=c.trade.label if c.trade else None,
                total_phases=len(entries),
                total_theory_periods=total_theory,
                total_practical_periods=total_prac,
                total_periods=total_periods,
                total_working_days=total_days,
                start_date=first_comm,
                end_date=last_comp,
                lead_instructor_name=lead_inst
            ))
    return summaries

@router.get("/courses/{course_id}/calendar", response_model=List[CourseCalendarResponse])
def get_course_calendar(
    course_id: str,
    status: Optional[str] = Query('Active'),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Get complete ordered course calendar phases for a specific course."""
    course = course_repo.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return course_calendar_repo.get_by_course(db, course_id, status=status or 'Active')

@router.post("/courses/{course_id}/calendar", response_model=CourseCalendarResponse)
def create_course_calendar_entry(
    course_id: str,
    payload: CourseCalendarCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Add a new calendar phase entry to a course calendar."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return course_calendar_service.create_entry(
        db=db,
        course_id=course_id,
        phase_name=payload.phase_name,
        commencement_date=payload.commencement_date,
        completion_date=payload.completion_date,
        theory_periods=payload.theory_periods,
        practical_periods=payload.practical_periods,
        working_days=payload.working_days,
        serial_number=payload.serial_number,
        instructor_id=payload.instructor_id,
        remarks=payload.remarks,
        user_id=current_user.id,
        ip=ip,
        ua=ua
    )

@router.get("/course-calendar/{calendar_id}", response_model=CourseCalendarResponse)
def get_course_calendar_entry(
    calendar_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:read"))
):
    """Get single course calendar phase entry by ID."""
    entry = course_calendar_repo.get_by_id(db, calendar_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Course calendar entry not found.")
    return entry

@router.put("/course-calendar/{calendar_id}", response_model=CourseCalendarResponse)
def update_course_calendar_entry(
    calendar_id: str,
    payload: CourseCalendarUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Update a course calendar phase entry."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return course_calendar_service.update_entry(
        db=db,
        calendar_id=calendar_id,
        phase_name=payload.phase_name,
        commencement_date=payload.commencement_date,
        completion_date=payload.completion_date,
        theory_periods=payload.theory_periods,
        practical_periods=payload.practical_periods,
        working_days=payload.working_days,
        serial_number=payload.serial_number,
        instructor_id=payload.instructor_id,
        remarks=payload.remarks,
        status=payload.status,
        user_id=current_user.id,
        ip=ip,
        ua=ua
    )

@router.delete("/course-calendar/{calendar_id}")
def delete_course_calendar_entry(
    calendar_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Delete a course calendar phase entry."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    course_calendar_service.delete_entry(db, calendar_id, current_user.id, ip, ua)
    return {"message": "Course calendar entry deleted successfully."}

@router.post("/courses/{course_id}/calendar/reorder", response_model=List[CourseCalendarResponse])
def reorder_course_calendar_entries(
    course_id: str,
    payload: ReorderCalendarEntriesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    """Reorder phase entries for a course calendar."""
    return course_calendar_repo.reorder_entries(db, course_id, payload.ordered_ids)

