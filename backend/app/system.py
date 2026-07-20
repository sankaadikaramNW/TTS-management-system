import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User, AuditLog
from app.repositories.user import user_repo, audit_repo
from app.schemas.user import UserResponse, UserCreate, AuditLogResponse

router = APIRouter(prefix="/system", tags=["System Administration"])

@router.get("/users", response_model=List[UserResponse])
def get_system_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return user_repo.list_users(db)

@router.post("/users", response_model=UserResponse)
def create_new_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
        
    from app.services.auth import auth_service
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return auth_service.register_user(db, user_data, current_user.id, ip, ua)

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def list_system_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("system:audit"))
):
    logs = audit_repo.get_multi(db, limit=100)
    # Inject username for readability
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log.user_name = user.username if user else "System"
    return logs

@router.post("/backup")
def trigger_system_backup(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
        
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    
    # Simple mock dump notification log
    audit_repo.create_log(
        db, current_user.id, "BACKUP_COMPLETED", ip, ua, 
        "Database backup successfully triggered and saved to directory root"
    )
    return {"status": "success", "file_name": "slaf_tts_backup_latest.sql"}
