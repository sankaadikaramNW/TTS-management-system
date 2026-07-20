from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, Role
from app.repositories.user import user_repo, audit_repo
from app.security import create_access_token, create_refresh_token, verify_password, get_password_hash, decode_token
from app.services.auth import auth_service
from app.schemas.user import LoginRequest, Token, UserResponse, UserCreate, ChangePasswordRequest, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

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
        "user": user
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
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(
    request: Request,
    pw_data: ChangePasswordRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not verify_password(pw_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
        
    current_user.hashed_password = get_password_hash(pw_data.new_password)
    db.commit()
    
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    audit_repo.create_log(db, current_user.id, "PASSWORD_CHANGED", ip, ua, "User changed password successfully")
    
    return {"message": "Password changed successfully"}
