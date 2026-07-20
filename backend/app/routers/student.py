import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.repositories.student import student_repo
from app.services.student import student_service
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse

router = APIRouter(prefix="/students", tags=["Student Management"])

@router.get("", response_model=StudentListResponse)
def list_students(
    search: Optional[str] = None,
    rank: Optional[str] = None,
    trade: Optional[str] = None,
    course_id: Optional[str] = None,
    status: Optional[str] = None,
    squadron: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:read"))
):
    total, items = student_repo.search_students(
        db, 
        search_query=search, 
        rank=rank, 
        trade=trade, 
        course_id=course_id, 
        status=status,
        squadron=squadron,
        skip=skip, 
        limit=limit
    )
    return {"total": total, "items": items}

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_details(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:read"))
):
    student = student_repo.get(db, student_id)
    if not student or student.deleted_at:
        raise HTTPException(status_code=404, detail="Student record not found")
    
    # Inject course name
    if student.course:
        student.course_name = student.course.name
    return student

@router.post("", response_model=StudentResponse)
def add_new_student(
    request: Request,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return student_service.create_student(db, student_data, current_user.id, ip, ua)

@router.put("/{student_id}", response_model=StudentResponse)
def edit_student_profile(
    student_id: str,
    request: Request,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return student_service.update_student(db, student_id, student_data, current_user.id, ip, ua)

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student_record(
    student_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return student_service.delete_student(db, student_id, current_user.id, ip, ua)

@router.post("/{student_id}/photo")
def upload_student_photo(
    student_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("student:write"))
):
    student = student_repo.get(db, student_id)
    if not student or student.deleted_at:
        raise HTTPException(status_code=404, detail="Student record not found")

    # Verify standard image type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image")

    # Setup directories
    file_ext = os.path.splitext(file.filename)[1]
    photo_name = f"{student.service_number.replace('/', '_')}{file_ext}"
    photo_dir = os.path.join(settings.UPLOAD_DIR, "photos")
    os.makedirs(photo_dir, exist_ok=True)
    
    file_path = os.path.join(photo_dir, photo_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    student.profile_photo_path = f"/static/uploads/photos/{photo_name}"
    db.commit()
    
    return {"photo_url": student.profile_photo_path}
