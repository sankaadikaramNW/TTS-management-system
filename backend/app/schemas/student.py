from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    service_number: str
    initials: str
    full_name: str
    nic: str
    dob: date
    gender: str
    rank: str
    trade: str
    course_id: Optional[str] = None
    batch: str
    squadron: Optional[str] = "Training Squadron"
    unit: Optional[str] = "SLAF TTS Ekala"
    posting: Optional[str] = None
    joining_date: date
    passing_out_date: Optional[date] = None
    status: Optional[str] = "Active"
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    emergency_contact_name: str
    emergency_contact_phone: str
    blood_group: str
    medical_category: Optional[str] = "A4G4"
    religion: str
    nationality: Optional[str] = "Sri Lankan"
    permanent_address: str
    temporary_address: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    initials: Optional[str] = None
    full_name: Optional[str] = None
    nic: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    rank: Optional[str] = None
    trade: Optional[str] = None
    course_id: Optional[str] = None
    batch: Optional[str] = None
    squadron: Optional[str] = None
    unit: Optional[str] = None
    posting: Optional[str] = None
    joining_date: Optional[date] = None
    passing_out_date: Optional[date] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_group: Optional[str] = None
    medical_category: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None
    permanent_address: Optional[str] = None
    temporary_address: Optional[str] = None
    profile_photo_path: Optional[str] = None

class StudentShortResponse(BaseModel):
    id: str
    service_number: str
    initials: str
    full_name: str
    rank: str
    trade: str
    status: str

    class Config:
        from_attributes = True

class StudentResponse(StudentBase):
    id: str
    profile_photo_path: Optional[str] = None
    qr_code_data: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    course_name: Optional[str] = None

    class Config:
        from_attributes = True

class StudentListResponse(BaseModel):
    total: int
    items: List[StudentResponse]
