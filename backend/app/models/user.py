from datetime import datetime
from sqlalchemy import Table, Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

# Association Table for Many-to-Many Role-Permission relationship
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', String(36), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', String(36), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

# Association Table for Optional Direct User-Permission Assignment
user_permissions = Table(
    'user_permissions',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', String(36), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role")

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    module = Column(String(50), nullable=True, default='General')  # e.g., Student Management, Accommodation, Academic, System
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    direct_users = relationship("User", secondary=user_permissions, back_populates="direct_permissions")

class User(Base, TimeStampedModelMixin):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    service_number = Column(String(50), nullable=True, index=True)
    rank = Column(String(50), nullable=True)
    full_name = Column(String(100), nullable=False)
    mobile_number = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    assigned_module = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    profile_photo = Column(String(255), nullable=True)
    role_id = Column(String(36), ForeignKey('roles.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    must_change_password = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    password_changed_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True, index=True)

    # Relationships
    role = relationship("Role", back_populates="users")
    direct_permissions = relationship("Permission", secondary=user_permissions, back_populates="direct_users")
    login_history = relationship("LoginHistory", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")

class PasswordHistory(Base):
    __tablename__ = 'password_history'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="password_history")

class LoginHistory(Base):
    __tablename__ = 'login_history'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    username = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False)  # SUCCESS, FAILED, LOCKED
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    logout_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="login_history")

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    username = Column(String(50), nullable=True)
    module = Column(String(50), nullable=True, default='User Management')
    action = Column(String(100), nullable=False)  # USER_CREATED, ROLE_ASSIGNED, PASSWORD_CHANGED, etc.
    previous_value = Column(String(1000), nullable=True)
    new_value = Column(String(1000), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    details = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
