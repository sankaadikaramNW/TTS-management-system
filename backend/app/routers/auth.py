from datetime import datetime, timedelta
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, status
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, Role, PasswordHistory
from app.repositories.user import user_repo, audit_repo
from app.security import (
    create_access_token, create_refresh_token, verify_password,
    get_password_hash, decode_token, validate_password_policy, check_password_reuse
)
from app.services.auth import auth_service
from app.schemas.user import (
    LoginRequest, Token, UserResponse, UserCreate, UserProfileUpdate,
    ChangePasswordRequest, RefreshTokenRequest, PermissionResponse
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

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

@router.post("/login", response_model=Token)
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    
    user = auth_service.authenticate_user(db, login_data.username, login_data.password, ip, ua)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(subject=user.username)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": build_user_response(user, db)
    }

@router.post("/refresh", response_model=Token)
def refresh_token(request_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
    username = payload.get("sub")
    user = user_repo.get_by_username(db, username)
    if not user or not user.is_active or user.is_locked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is locked or disabled")
        
    access_token = create_access_token(subject=user.username)
    refresh_token = create_refresh_token(subject=user.username)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": build_user_response(user, db)
    }

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return build_user_response(current_user, db)

@router.put("/profile", response_model=UserResponse)
def update_own_profile(
    request: Request,
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.email and payload.email != current_user.email:
        existing = user_repo.get_by_email(db, payload.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email address is already in use")
        current_user.email = payload.email

    if payload.mobile_number is not None:
        current_user.mobile_number = payload.mobile_number
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.profile_photo is not None:
        current_user.profile_photo = payload.profile_photo

    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "PROFILE_UPDATED", ip, ua, 
        f"User '{current_user.username}' updated contact profile details",
        username=current_user.username, module="User Profile"
    )

    return build_user_response(current_user, db)

@router.post("/change-password")
def change_password(
    request: Request,
    pw_data: ChangePasswordRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not verify_password(pw_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    valid, msg = validate_password_policy(pw_data.new_password)
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    if check_password_reuse(db, current_user.id, pw_data.new_password):
        raise HTTPException(status_code=400, detail="Password reuse prohibited. You cannot reuse any of your recent passwords.")

    hashed = get_password_hash(pw_data.new_password)
    current_user.hashed_password = hashed
    current_user.must_change_password = False
    current_user.password_changed_at = datetime.utcnow()
    current_user.updated_at = datetime.utcnow()

    # Store entry in password history
    db.add(PasswordHistory(user_id=current_user.id, hashed_password=hashed))
    db.commit()
    
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "PASSWORD_CHANGED", ip, ua, 
        f"User '{current_user.username}' changed account password successfully",
        username=current_user.username, module="User Profile"
    )
    
    return {"message": "Password changed successfully"}

@router.post("/upload-avatar")
def upload_profile_avatar(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Allowed: JPG, PNG, WEBP")

    avatar_dir = os.path.join(settings.UPLOAD_DIR, "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    filename = f"avatar_{current_user.id}_{int(datetime.utcnow().timestamp())}{ext}"
    filepath = os.path.join(avatar_dir, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rel_url = f"/uploads/avatars/{filename}"
    current_user.profile_photo = rel_url
    current_user.updated_at = datetime.utcnow()
    db.commit()

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(
        db, current_user.id, "AVATAR_UPLOADED", ip, ua, 
        f"Uploaded new profile avatar for '{current_user.username}'",
        username=current_user.username, module="User Profile"
    )

    return {"message": "Profile photo uploaded successfully", "profile_photo": rel_url}
