from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class PermissionBase(BaseModel):
    name: str
    code: str
    module: Optional[str] = "General"
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: str
    
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[str] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[str]] = None

class RoleResponse(RoleBase):
    id: str
    is_active: Optional[bool] = True
    permissions: List[PermissionResponse] = []
    users_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    service_number: Optional[str] = None
    rank: Optional[str] = None
    full_name: str
    mobile_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    assigned_module: Optional[str] = None
    role_id: str
    is_active: Optional[bool] = True
    must_change_password: Optional[bool] = False

class UserCreate(UserBase):
    password: str
    direct_permission_ids: Optional[List[str]] = []

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    service_number: Optional[str] = None
    rank: Optional[str] = None
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    assigned_module: Optional[str] = None
    role_id: Optional[str] = None
    is_active: Optional[bool] = None
    is_locked: Optional[bool] = None
    must_change_password: Optional[bool] = None
    password: Optional[str] = None
    direct_permission_ids: Optional[List[str]] = None

class UserProfileUpdate(BaseModel):
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    full_name: Optional[str] = None
    profile_photo: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    service_number: Optional[str] = None
    rank: Optional[str] = None
    full_name: str
    mobile_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    assigned_module: Optional[str] = None
    profile_photo: Optional[str] = None
    role_id: str
    role: RoleResponse
    is_active: bool
    is_locked: bool
    must_change_password: Optional[bool] = False
    failed_login_attempts: Optional[int] = 0
    password_changed_at: Optional[datetime] = None
    created_at: datetime
    direct_permissions: List[PermissionResponse] = []
    effective_permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class AdminResetPasswordRequest(BaseModel):
    new_password: str
    force_change_on_login: Optional[bool] = True

class CloneRoleRequest(BaseModel):
    new_role_name: str
    description: Optional[str] = None

class LoginHistoryResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    status: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    logout_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    module: Optional[str] = 'User Management'
    action: str
    previous_value: Optional[str] = None
    new_value: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[str] = None
    created_at: datetime
    user_name: Optional[str] = None

    class Config:
        from_attributes = True
