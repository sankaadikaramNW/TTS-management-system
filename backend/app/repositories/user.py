from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.user import User, Role, Permission, AuditLog, LoginHistory, PasswordHistory
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def get_by_id(self, db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id, User.deleted_at == None).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username, User.deleted_at == None).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email, User.deleted_at == None).first()

    def get_by_service_number(self, db: Session, service_number: str) -> Optional[User]:
        if not service_number:
            return None
        return db.query(User).filter(User.service_number == service_number, User.deleted_at == None).first()

    def get_multi_filtered(
        self,
        db: Session,
        query: Optional[str] = None,
        rank: Optional[str] = None,
        department: Optional[str] = None,
        assigned_module: Optional[str] = None,
        role_id: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        q = db.query(User).filter(User.deleted_at == None)

        if query:
            search = f"%{query}%"
            q = q.filter(
                or_(
                    User.username.like(search),
                    User.full_name.like(search),
                    User.email.like(search),
                    User.service_number.like(search)
                )
            )

        if rank:
            q = q.filter(User.rank == rank)
        if department:
            q = q.filter(User.department == department)
        if assigned_module:
            q = q.filter(User.assigned_module == assigned_module)
        if role_id:
            q = q.filter(User.role_id == role_id)

        if status:
            if status.upper() == 'ACTIVE':
                q = q.filter(User.is_active == True, User.is_locked == False)
            elif status.upper() == 'INACTIVE':
                q = q.filter(User.is_active == False)
            elif status.upper() == 'LOCKED':
                q = q.filter(User.is_locked == True)

        return q.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    def soft_delete(self, db: Session, user: User) -> User:
        user.is_active = False
        user.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user

    def update_direct_permissions(self, db: Session, user: User, permission_ids: List[str]):
        perms = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        user.direct_permissions = perms
        db.commit()
        db.refresh(user)

class RoleRepository(BaseRepository[Role]):
    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def list_all_with_counts(self, db: Session) -> List[Role]:
        return db.query(Role).all()

class AuditLogRepository:
    def create_log(
        self,
        db: Session,
        user_id: Optional[str],
        action: str,
        ip_address: Optional[str],
        user_agent: Optional[str],
        details: Optional[str] = None,
        username: Optional[str] = None,
        module: Optional[str] = 'User Management',
        previous_value: Optional[str] = None,
        new_value: Optional[str] = None
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            username=username,
            module=module,
            action=action,
            previous_value=previous_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def get_multi_filtered(
        self,
        db: Session,
        username: Optional[str] = None,
        module: Optional[str] = None,
        action: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        q = db.query(AuditLog)
        if username:
            q = q.filter(AuditLog.username.like(f"%{username}%"))
        if module:
            q = q.filter(AuditLog.module == module)
        if action:
            q = q.filter(AuditLog.action == action)
        return q.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

class LoginHistoryRepository:
    def create_history(
        self,
        db: Session,
        user_id: Optional[str],
        username: Optional[str],
        status: str,
        ip_address: Optional[str],
        user_agent: Optional[str]
    ) -> LoginHistory:
        history = LoginHistory(
            user_id=user_id,
            username=username,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def get_multi_filtered(
        self,
        db: Session,
        username: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[LoginHistory]:
        q = db.query(LoginHistory)
        if username:
            q = q.filter(LoginHistory.username.like(f"%{username}%"))
        if status:
            q = q.filter(LoginHistory.status == status)
        return q.order_by(LoginHistory.created_at.desc()).offset(skip).limit(limit).all()

user_repo = UserRepository(User)
role_repo = RoleRepository(Role)
audit_repo = AuditLogRepository()
login_history_repo = LoginHistoryRepository()
