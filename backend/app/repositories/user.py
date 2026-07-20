from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User, Role, Permission, AuditLog, LoginHistory
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username, User.deleted_at == None).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email, User.deleted_at == None).first()

    def list_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.deleted_at == None).offset(skip).limit(limit).all()

class RoleRepository(BaseRepository[Role]):
    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

class AuditLogRepository:
    def create_log(self, db: Session, user_id: Optional[str], action: str, ip_address: Optional[str], user_agent: Optional[str], details: Optional[str] = None) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

class LoginHistoryRepository:
    def create_history(self, db: Session, user_id: Optional[str], status: str, ip_address: Optional[str], user_agent: Optional[str]) -> LoginHistory:
        history = LoginHistory(
            user_id=user_id,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

user_repo = UserRepository(User)
role_repo = RoleRepository(Role)
audit_repo = AuditLogRepository()
login_history_repo = LoginHistoryRepository()
