from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user import user_repo, login_history_repo, audit_repo
from app.security import verify_password, create_access_token, create_refresh_token, get_password_hash
from app.schemas.user import UserCreate

class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str, ip_address: Optional[str], user_agent: Optional[str]) -> Optional[User]:
        user = user_repo.get_by_username(db, username)
        if not user:
            # Create a mock failed log for audit safety
            login_history_repo.create_history(db, None, "FAILED", ip_address, user_agent)
            return None
            
        if user.is_locked:
            login_history_repo.create_history(db, user.id, "LOCKED", ip_address, user_agent)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is locked due to multiple failed login attempts. Contact Super Administrator."
            )
            
        if not verify_password(password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                login_history_repo.create_history(db, user.id, "LOCKED", ip_address, user_agent)
                audit_repo.create_log(db, user.id, "ACCOUNT_LOCKED", ip_address, user_agent, "Account auto-locked due to 5 failures")
            else:
                login_history_repo.create_history(db, user.id, "FAILED", ip_address, user_agent)
            db.commit()
            return None
            
        # Reset counters on success
        user.failed_login_attempts = 0
        db.commit()
        
        login_history_repo.create_history(db, user.id, "SUCCESS", ip_address, user_agent)
        return user

    def register_user(self, db: Session, user_in: UserCreate, request_user_id: Optional[str], ip_address: str, user_agent: str) -> User:
        # Check duplicate
        if user_repo.get_by_username(db, user_in.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if user_repo.get_by_email(db, user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
            
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role_id=user_in.role_id,
            is_active=user_in.is_active
        )
        created_user = user_repo.create(db, obj_in=db_user)
        audit_repo.create_log(
            db, request_user_id, "USER_CREATED", ip_address, user_agent, 
            f"Created user username={created_user.username} role_id={created_user.role_id}"
        )
        return created_user

auth_service = AuthService()
