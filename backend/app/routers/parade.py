from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.repositories.parade import parade_repo
from app.services.parade import parade_service
from app.schemas.parade import ParadeStateResponse, DailyParadeUpdateRequest, ParadeStateSummary, ParadeStatusTypeResponse
from app.models.student import ParadeStatusType

router = APIRouter(prefix="/parade", tags=["Daily Parade State"])

@router.get("/statuses", response_model=List[ParadeStatusTypeResponse])
def get_parade_statuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(ParadeStatusType).filter(ParadeStatusType.is_active == True).all()


@router.get("/status", response_model=List[ParadeStateResponse])
def get_daily_parade_state(
    parade_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    target_date = parade_date or date.today()
    return parade_repo.get_parade_states_by_date(db, target_date)

@router.get("/summary", response_model=ParadeStateSummary)
def get_daily_parade_summary(
    parade_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    target_date = parade_date or date.today()
    return parade_repo.get_summary(db, target_date)

@router.post("/update")
def batch_update_parade_state(
    request: Request,
    update_data: DailyParadeUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.update_daily_parade(db, update_data, current_user.id, ip, ua)
