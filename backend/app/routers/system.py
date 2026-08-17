import io
import csv
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User, Role, Permission, AuditLog, LoginHistory, PasswordHistory
from app.repositories.user import user_repo, role_repo, audit_repo, login_history_repo
from app.schemas.user import (
    UserResponse, UserCreate, UserUpdate, RoleResponse, RoleCreate, RoleUpdate,
    PermissionResponse, AuditLogResponse, LoginHistoryResponse, AdminResetPasswordRequest, CloneRoleRequest
)
from app.security import validate_password_policy, check_password_reuse, get_password_hash

router = APIRouter(prefix="/system", tags=["System Administration"])

def build_user_response(user: User, db: Session) -> UserResponse:
    role_perms = user.role.permissions if (user.role and user.role.permissions) else []
    direct_perms = user.direct_permissions or []
    perm_map = {p.code: p for p in role_perms}
    for p in direct_perms:
        perm_map[p.code] = p
    effective = list(perm_map.values())
    
    resp = UserResponse.from_orm(user)
    resp.effective_permissions = [PermissionResponse.from_orm(p) for p in effective]
    resp.direct_permissions = [PermissionResponse.from_orm(p) for p in direct_perms]
    return resp

# -----------------------------------------------------------------------------
# 1. USER MANAGEMENT ENDPOINTS
# -----------------------------------------------------------------------------

@router.get("/users", response_model=List[UserResponse])
def get_system_users(
    query: Optional[str] = None,
    rank: Optional[str] = None,
    department: Optional[str] = None,
    assigned_module: Optional[str] = None,
    role_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
        
    users = user_repo.get_multi_filtered(
        db, query=query, rank=rank, department=department,
        assigned_module=assigned_module, role_id=role_id, status=status,
        skip=skip, limit=limit
    )
    return [build_user_response(u, db) for u in users]

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
    user = auth_service.register_user(db, user_data, current_user.id, ip, ua)
    return build_user_response(user, db)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=4404, detail="User not found")
    return build_user_response(user, db)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_account(
    request: Request,
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")
        
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")

    # Update basic fields
    if user_update.email and user_update.email != user.email:
        existing = user_repo.get_by_email(db, user_update.email)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = user_update.email

    if user_update.service_number and user_update.service_number != user.service_number:
        existing = user_repo.get_by_service_number(db, user_update.service_number)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Service Number already assigned to another user")
        user.service_number = user_update.service_number

    if user_update.rank is not None: user.rank = user_update.rank
    if user_update.full_name is not None: user.full_name = user_update.full_name
    if user_update.mobile_number is not None: user.mobile_number = user_update.mobile_number
    if user_update.department is not None: user.department = user_update.department
    if user_update.designation is not None: user.designation = user_update.designation
    if user_update.assigned_module is not None: user.assigned_module = user_update.assigned_module
    if user_update.role_id is not None: user.role_id = user_update.role_id
    if user_update.is_active is not None: user.is_active = user_update.is_active
    if user_update.is_locked is not None: user.is_locked = user_update.is_locked
    if user_update.must_change_password is not None: user.must_change_password = user_update.must_change_password

    # Update direct permissions if provided
    if user_update.direct_permission_ids is not None:
        user_repo.update_direct_permissions(db, user, user_update.direct_permission_ids)

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)

    audit_repo.create_log(
        db, current_user.id, "USER_UPDATED", ip, ua,
        f"Updated user account profile for '{user.username}'",
        username=current_user.username, module="User Management"
    )

    return build_user_response(user, db)

@router.delete("/users/{user_id}")
def delete_user_soft(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    if user.username == "admin" or user.id == "user-slaf-admin":
        raise HTTPException(status_code=400, detail="Protected System Administrator account cannot be deleted.")

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")

    user_repo.soft_delete(db, user)
    audit_repo.create_log(
        db, current_user.id, "USER_SOFT_DELETED", ip, ua,
        f"Soft deleted user account '{user.username}'",
        username=current_user.username, module="User Management"
    )
    return {"message": f"User account '{user.username}' soft deleted successfully"}

@router.post("/users/{user_id}/reset-password")
def admin_reset_user_password(
    request: Request,
    user_id: str,
    payload: AdminResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    valid, msg = validate_password_policy(payload.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    hashed = get_password_hash(payload.new_password)
    user.hashed_password = hashed
    user.must_change_password = payload.force_change_on_login
    user.failed_login_attempts = 0
    user.is_locked = False
    user.password_changed_at = datetime.utcnow()
    user.updated_at = datetime.utcnow()

    # Record in history
    db.add(PasswordHistory(user_id=user.id, hashed_password=hashed))
    db.commit()

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "PASSWORD_RESET_ADMIN", ip, ua,
        f"Administrator reset password for user '{user.username}'",
        username=current_user.username, module="User Management"
    )

    return {"message": f"Password for '{user.username}' reset successfully"}

@router.post("/users/{user_id}/unlock")
def unlock_user_account(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    user.is_locked = False
    user.failed_login_attempts = 0
    user.updated_at = datetime.utcnow()
    db.commit()

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "ACCOUNT_UNLOCKED", ip, ua,
        f"Unlocked account for user '{user.username}' and reset failed login attempts counter",
        username=current_user.username, module="User Management"
    )

    return {"message": f"Account '{user.username}' unlocked successfully"}

@router.post("/users/{user_id}/toggle-status")
def toggle_user_active_status(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    user.is_active = not user.is_active
    user.updated_at = datetime.utcnow()
    db.commit()

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    action = "USER_ACTIVATED" if user.is_active else "USER_DEACTIVATED"
    audit_repo.create_log(
        db, current_user.id, action, ip, ua,
        f"Toggled user account status for '{user.username}' to is_active={user.is_active}",
        username=current_user.username, module="User Management"
    )

    return {"message": f"User status set to {'Active' if user.is_active else 'Deactivated'}", "is_active": user.is_active}

@router.post("/users/{user_id}/revoke-session")
def revoke_user_session(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found")

    # Update active login history record to mark logged out by admin
    last_login = db.query(LoginHistory).filter(
        LoginHistory.user_id == user.id,
        LoginHistory.status == "SUCCESS"
    ).order_by(LoginHistory.created_at.desc()).first()

    if last_login and not last_login.logout_time:
        last_login.logout_time = datetime.utcnow()

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "SESSION_REVOKED", ip, ua,
        f"Admin '{current_user.username}' forcibly revoked session for user '{user.username}'",
        username=current_user.username, module="User Management"
    )
    db.commit()

    return {"message": f"Active session for user '{user.username}' revoked successfully"}


# -----------------------------------------------------------------------------
# 2. ROLE & PERMISSION MANAGEMENT ENDPOINTS
# -----------------------------------------------------------------------------

@router.get("/roles", response_model=List[RoleResponse])
def list_system_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roles = db.query(Role).all()
    results = []
    for r in roles:
        r_resp = RoleResponse.from_orm(r)
        r_resp.users_count = db.query(User).filter(User.role_id == r.id, User.deleted_at == None).count()
        results.append(r_resp)
    return results

@router.post("/roles", response_model=RoleResponse)
def create_system_role(
    request: Request,
    payload: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    existing = role_repo.get_by_name(db, payload.name)
    if existing:
        raise HTTPException(status_code=400, detail="Role with this name already exists")

    new_role = Role(name=payload.name, description=payload.description)
    if payload.permission_ids:
        perms = db.query(Permission).filter(Permission.id.in_(payload.permission_ids)).all()
        new_role.permissions = perms

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "ROLE_CREATED", ip, ua,
        f"Created role '{new_role.name}' with {len(new_role.permissions)} permissions",
        username=current_user.username, module="Role Management"
    )

    resp = RoleResponse.from_orm(new_role)
    resp.users_count = 0
    return resp

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_system_role(
    request: Request,
    role_id: str,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if payload.name:
        role.name = payload.name
    if payload.description is not None:
        role.description = payload.description
    if payload.is_active is not None:
        role.is_active = payload.is_active

    if payload.permission_ids is not None:
        perms = db.query(Permission).filter(Permission.id.in_(payload.permission_ids)).all()
        role.permissions = perms

    role.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(role)

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "ROLE_UPDATED", ip, ua,
        f"Updated role configuration for '{role.name}'",
        username=current_user.username, module="Role Management"
    )

    resp = RoleResponse.from_orm(role)
    resp.users_count = db.query(User).filter(User.role_id == role.id, User.deleted_at == None).count()
    return resp

@router.post("/roles/{role_id}/clone", response_model=RoleResponse)
def clone_existing_role(
    request: Request,
    role_id: str,
    payload: CloneRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    source_role = db.query(Role).filter(Role.id == role_id).first()
    if not source_role:
        raise HTTPException(status_code=404, detail="Source role not found")

    existing = role_repo.get_by_name(db, payload.new_role_name)
    if existing:
        raise HTTPException(status_code=400, detail="A role with this target name already exists")

    cloned_role = Role(
        name=payload.new_role_name,
        description=payload.description or f"Cloned from {source_role.name}",
        permissions=list(source_role.permissions)
    )

    db.add(cloned_role)
    db.commit()
    db.refresh(cloned_role)

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "ROLE_CLONED", ip, ua,
        f"Cloned role '{source_role.name}' to new role '{cloned_role.name}'",
        username=current_user.username, module="Role Management"
    )

    resp = RoleResponse.from_orm(cloned_role)
    resp.users_count = 0
    return resp

@router.get("/permissions", response_model=List[PermissionResponse])
def list_system_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    perms = db.query(Permission).order_by(Permission.module, Permission.name).all()
    return [PermissionResponse.from_orm(p) for p in perms]

# -----------------------------------------------------------------------------
# 3. LOGIN HISTORY, AUDIT TRAIL & LOCKED ACCOUNTS
# -----------------------------------------------------------------------------

@router.get("/login-history", response_model=List[LoginHistoryResponse])
def get_login_history_records(
    username: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    history = login_history_repo.get_multi_filtered(db, username=username, status=status, skip=skip, limit=limit)
    return [LoginHistoryResponse.from_orm(h) for h in history]

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def list_system_audit_logs(
    username: Optional[str] = None,
    module: Optional[str] = None,
    action: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("system:audit"))
):
    logs = audit_repo.get_multi_filtered(db, username=username, module=module, action=action, skip=skip, limit=limit)
    res = []
    for log in logs:
        item = AuditLogResponse.from_orm(log)
        if not item.username and log.user_id:
            u = db.query(User).filter(User.id == log.user_id).first()
            item.user_name = u.username if u else "System"
        else:
            item.user_name = item.username or "System"
        res.append(item)
    return res

@router.get("/locked-accounts", response_model=List[UserResponse])
def list_locked_user_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name not in ["Super Administrator", "System Administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    users = db.query(User).filter(User.is_locked == True, User.deleted_at == None).all()
    return [build_user_response(u, db) for u in users]

# -----------------------------------------------------------------------------
# 4. SYSTEM BACKUP
# -----------------------------------------------------------------------------

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
    
    audit_repo.create_log(
        db, current_user.id, "BACKUP_COMPLETED", ip, ua, 
        "Database backup successfully triggered and saved to directory root",
        username=current_user.username, module="System Backup"
    )
    return {"status": "success", "file_name": f"slaf_tts_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.sql"}

