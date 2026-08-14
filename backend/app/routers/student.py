import os
import shutil
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.repositories.student import student_repo, personal_occurrence_repo
from app.services.student import student_service
from app.services.personal_occurrence_service import personal_occurrence_service
from app.schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse, StudentListResponse, StudentStatusTypeResponse,
    RankResponse, TradeResponse, TradeCreate, TradeUpdate, RankCreate, RankUpdate,
    PersonalOccurrenceCreate, PersonalOccurrenceUpdate, PersonalOccurrenceResponse, PersonalOccurrenceListResponse
)
from app.models.student import Student, StudentStatusType, Rank, Trade, PersonalOccurrence

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


@router.get("/statuses", response_model=List[StudentStatusTypeResponse])
def get_student_statuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(StudentStatusType).filter(StudentStatusType.is_active == True).all()


@router.get("/ranks", response_model=List[RankResponse])
def get_student_ranks(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Rank)
    if not include_inactive:
        query = query.filter(Rank.is_active == True)
    return query.all()


@router.post("/ranks", response_model=RankResponse)
def create_student_rank(
    rank_in: RankCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    # Check duplicate code
    if db.query(Rank).filter(Rank.code == rank_in.code).first():
        raise HTTPException(status_code=400, detail=f"Rank with code '{rank_in.code}' already exists")
        
    db_rank = Rank(
        id=f"rank-{rank_in.code.lower().replace('_', '-')}",
        code=rank_in.code.upper(),
        label=rank_in.label,
        is_active=rank_in.is_active
    )
    db.add(db_rank)
    db.commit()
    db.refresh(db_rank)
    return db_rank


@router.put("/ranks/{rank_id}", response_model=RankResponse)
def update_student_rank(
    rank_id: str,
    rank_in: RankUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if not db_rank:
        raise HTTPException(status_code=404, detail="Rank not found")
        
    if rank_in.code is not None:
        # Check duplicate code
        dup = db.query(Rank).filter(Rank.code == rank_in.code, Rank.id != rank_id).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"Rank with code '{rank_in.code}' already exists")
        db_rank.code = rank_in.code.upper()
        
    if rank_in.label is not None:
        db_rank.label = rank_in.label
        
    if rank_in.is_active is not None:
        db_rank.is_active = rank_in.is_active
        
    db.commit()
    db.refresh(db_rank)
    return db_rank


@router.delete("/ranks/{rank_id}")
def delete_student_rank(
    rank_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    db_rank = db.query(Rank).filter(Rank.id == rank_id).first()
    if not db_rank:
        raise HTTPException(status_code=404, detail="Rank not found")
        
    # Check if there are active students assigned to this rank (by matching label)
    student_count = db.query(Student).filter(Student.rank == db_rank.label, Student.deleted_at == None).count()
    if student_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete Rank because there are {student_count} trainees assigned to it. Deactivate it instead."
        )
        
    db.delete(db_rank)
    db.commit()
    return {"message": "Rank deleted successfully"}


@router.get("/trades", response_model=List[TradeResponse])
def get_student_trades(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Trade)
    if not include_inactive:
        query = query.filter(Trade.is_active == True)
    return query.all()


@router.post("/trades", response_model=TradeResponse)
def create_student_trade(
    trade_in: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    # Check duplicate code
    if db.query(Trade).filter(Trade.code == trade_in.code).first():
        raise HTTPException(status_code=400, detail=f"Trade with code '{trade_in.code}' already exists")
        
    db_trade = Trade(
        id=f"trade-{trade_in.code.lower().replace('_', '-')}",
        code=trade_in.code.upper(),
        label=trade_in.label,
        is_active=trade_in.is_active
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@router.put("/trades/{trade_id}", response_model=TradeResponse)
def update_student_trade(
    trade_id: str,
    trade_in: TradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
        
    if trade_in.code is not None:
        # Check duplicate code
        dup = db.query(Trade).filter(Trade.code == trade_in.code, Trade.id != trade_id).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"Trade with code '{trade_in.code}' already exists")
        db_trade.code = trade_in.code.upper()
        
    if trade_in.label is not None:
        db_trade.label = trade_in.label
        
    if trade_in.is_active is not None:
        db_trade.is_active = trade_in.is_active
        
    db.commit()
    db.refresh(db_trade)
    return db_trade


@router.delete("/trades/{trade_id}")
def delete_student_trade(
    trade_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("academic:write"))
):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not db_trade:
        raise HTTPException(status_code=404, detail="Trade not found")
        
    # Check if there are active students assigned to this trade (by matching label)
    student_count = db.query(Student).filter(Student.trade == db_trade.label, Student.deleted_at == None).count()
    if student_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete Trade because there are {student_count} trainees assigned to it. Deactivate it instead."
        )
        
    db.delete(db_trade)
    db.commit()
    return {"message": "Trade deleted successfully"}


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


# --- Trainee Personal Occurrence Sub-Endpoints ---

@router.get("/{trainee_id}/occurrences", response_model=List[PersonalOccurrenceResponse])
def get_trainee_occurrences(
    trainee_id: str,
    occurrence_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:read"))
):
    """Fetch all personal occurrence records (Achievements & Misconduct) for a specific trainee."""
    trainee = student_repo.get(db, trainee_id)
    if not trainee or trainee.deleted_at:
        raise HTTPException(status_code=404, detail="Trainee record not found.")
    return personal_occurrence_repo.get_by_trainee(
        db, trainee_id=trainee_id, occurrence_type=occurrence_type, date_from=date_from, date_to=date_to
    )


@router.post("/{trainee_id}/occurrences", response_model=PersonalOccurrenceResponse)
def add_trainee_occurrence(
    trainee_id: str,
    payload: PersonalOccurrenceCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:write"))
):
    """Record a new personal occurrence (Achievement or Misconduct) for a trainee."""
    if payload.trainee_id != trainee_id:
        payload.trainee_id = trainee_id
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return personal_occurrence_service.create_occurrence(db, payload, current_user.id, ip, ua)


# --- Standalone Personal Occurrence Reporting Endpoints ---

occ_router = APIRouter(prefix="/personal-occurrences", tags=["Personal Occurrence Reporting"])

@occ_router.get("", response_model=PersonalOccurrenceListResponse)
def list_personal_occurrences(
    search: Optional[str] = None,
    trainee_id: Optional[str] = None,
    occurrence_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:read"))
):
    """Search and filter personal occurrence records across trainees."""
    total, items = personal_occurrence_repo.search_occurrences(
        db,
        search_query=search,
        trainee_id=trainee_id,
        occurrence_type=occurrence_type,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": items}


@occ_router.get("/{occurrence_id}", response_model=PersonalOccurrenceResponse)
def get_personal_occurrence_detail(
    occurrence_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:read"))
):
    """Fetch single personal occurrence record by ID."""
    occ = personal_occurrence_repo.get_by_id(db, occurrence_id)
    if not occ:
        raise HTTPException(status_code=404, detail="Personal occurrence record not found.")
    return occ


@occ_router.put("/{occurrence_id}", response_model=PersonalOccurrenceResponse)
def update_personal_occurrence(
    occurrence_id: str,
    payload: PersonalOccurrenceUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:write"))
):
    """Update an existing personal occurrence record."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return personal_occurrence_service.update_occurrence(db, occurrence_id, payload, current_user.id, ip, ua)


@occ_router.delete("/{occurrence_id}")
def delete_personal_occurrence(
    occurrence_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("personal_occurrence:delete"))
):
    """Delete (soft-delete) a personal occurrence record according to policy."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    personal_occurrence_service.delete_occurrence(db, occurrence_id, current_user.id, ip, ua)
    return {"message": "Personal occurrence record deleted successfully."}

