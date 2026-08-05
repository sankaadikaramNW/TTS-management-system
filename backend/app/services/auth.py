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
            login_history_repo.create_history(db, None, username, "FAILED", ip_address, user_agent)
            return None
            
        if user.is_locked:
            login_history_repo.create_history(db, user.id, username, "LOCKED", ip_address, user_agent)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is locked due to multiple failed login attempts. Contact System Administrator."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Please contact your system administrator."
            )
            
        if not verify_password(password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                login_history_repo.create_history(db, user.id, username, "LOCKED", ip_address, user_agent)
                audit_repo.create_log(
                    db, user.id, "ACCOUNT_LOCKED", ip_address, user_agent, 
                    "Account auto-locked due to 5 consecutive failed login attempts", username=username, module="Authentication"
                )
            else:
                login_history_repo.create_history(db, user.id, username, "FAILED", ip_address, user_agent)
            db.commit()
            return None
            
        # Reset failed attempts counter on success
        user.failed_login_attempts = 0
        db.commit()
        
        login_history_repo.create_history(db, user.id, username, "SUCCESS", ip_address, user_agent)
        audit_repo.create_log(
            db, user.id, "USER_LOGIN", ip_address, user_agent, 
            f"User '{username}' logged in successfully", username=username, module="Authentication"
        )
        return user

    def register_user(self, db: Session, user_in: UserCreate, request_user_id: Optional[str], ip_address: str, user_agent: str) -> User:
        from app.security import validate_password_policy, get_password_hash
        from app.models.user import PasswordHistory

        # Unique checks
        if user_repo.get_by_username(db, user_in.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        if user_repo.get_by_email(db, user_in.email):
            raise HTTPException(status_code=400, detail="Email address already registered")
        if user_in.service_number and user_repo.get_by_service_number(db, user_in.service_number):
            raise HTTPException(status_code=400, detail="Service Number already registered to an existing account")

        # Password policy check
        valid, msg = validate_password_policy(user_in.password)
        if not valid:
            raise HTTPException(status_code=400, detail=msg)
            
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            service_number=user_in.service_number,
            rank=user_in.rank,
            full_name=user_in.full_name,
            mobile_number=user_in.mobile_number,
            department=user_in.department,
            designation=user_in.designation,
            assigned_module=user_in.assigned_module,
            hashed_password=hashed_password,
            role_id=user_in.role_id,
            is_active=user_in.is_active if user_in.is_active is not None else True,
            must_change_password=user_in.must_change_password or False,
            password_changed_at=datetime.utcnow()
        )
        created_user = user_repo.create(db, obj_in=db_user)

        # Record initial entry in password history
        pass_hist = PasswordHistory(user_id=created_user.id, hashed_password=hashed_password)
        db.add(pass_hist)

        # Handle direct permissions
        if user_in.direct_permission_ids:
            user_repo.update_direct_permissions(db, created_user, user_in.direct_permission_ids)

        db.commit()
        db.refresh(created_user)

        audit_repo.create_log(
            db, request_user_id, "USER_CREATED", ip_address, user_agent, 
            f"Created user username='{created_user.username}', full_name='{created_user.full_name}', role_id='{created_user.role_id}'",
            username=created_user.username, module="User Management"
        )
        return created_user

auth_service = AuthService()
