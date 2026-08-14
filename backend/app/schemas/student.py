from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator

class StudentBase(BaseModel):
    service_number: str
    full_name: str
    initials: Optional[str] = ""
    nic: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = "Male"
    rank: Optional[str] = "Aircraftman"
    trade: Optional[str] = "Airframe"
    course_id: Optional[str] = None
    batch: Optional[str] = "Intake 171"
    squadron: Optional[str] = "Training Squadron"
    unit: Optional[str] = "SLAF TTS Ekala"
    posting: Optional[str] = None
    joining_date: Optional[date] = None
    passing_out_date: Optional[date] = None
    status: Optional[str] = "Active"
    phone: Optional[str] = None
    email: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    blood_group: Optional[str] = "O+"
    medical_category: Optional[str] = "A4G4"
    religion: Optional[str] = "Buddhist"
    nationality: Optional[str] = "Sri Lankan"
    permanent_address: Optional[str] = None
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


class StudentStatusTypeResponse(BaseModel):
    id: str
    code: str
    label: str
    is_active: bool

    class Config:
        from_attributes = True


class RankResponse(BaseModel):
    id: str
    code: str
    label: str
    is_active: bool

    class Config:
        from_attributes = True


class TradeResponse(BaseModel):
    id: str
    code: str
    label: str
    is_active: bool

    class Config:
        from_attributes = True


class TradeCreate(BaseModel):
    code: str
    label: str
    is_active: Optional[bool] = True


class TradeUpdate(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    is_active: Optional[bool] = None


class RankCreate(BaseModel):
    code: str
    label: str
    is_active: Optional[bool] = True


class RankUpdate(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    is_active: Optional[bool] = None


class PersonalOccurrenceCreate(BaseModel):
    trainee_id: str = Field(..., description="Target trainee student ID")
    occurrence_type: str = Field(..., description="ACHIEVEMENT or MISCONDUCT_OFFENSE")
    occurrence_date: date = Field(..., description="Date of occurrence")
    title: str = Field(..., min_length=1, max_length=255, description="Short summary title")
    description: str = Field(..., min_length=1, description="Detailed occurrence description")
    remarks: Optional[str] = Field(None, description="Optional administrative notes")

    @field_validator('occurrence_type')
    @classmethod
    def validate_occurrence_type(cls, v: str) -> str:
        upper_v = v.upper().strip()
        if upper_v not in ['ACHIEVEMENT', 'MISCONDUCT_OFFENSE']:
            raise ValueError("Occurrence type must be strictly 'ACHIEVEMENT' or 'MISCONDUCT_OFFENSE'")
        return upper_v

    @field_validator('title', 'description', 'remarks', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v


class PersonalOccurrenceUpdate(BaseModel):
    occurrence_type: Optional[str] = Field(None, description="ACHIEVEMENT or MISCONDUCT_OFFENSE")
    occurrence_date: Optional[date] = None
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    remarks: Optional[str] = None
    status: Optional[str] = None

    @field_validator('occurrence_type')
    @classmethod
    def validate_occurrence_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            upper_v = v.upper().strip()
            if upper_v not in ['ACHIEVEMENT', 'MISCONDUCT_OFFENSE']:
                raise ValueError("Occurrence type must be strictly 'ACHIEVEMENT' or 'MISCONDUCT_OFFENSE'")
            return upper_v
        return v


class PersonalOccurrenceResponse(BaseModel):
    id: str
    trainee_id: str
    occurrence_type: str
    occurrence_date: date
    title: str
    description: str
    remarks: Optional[str] = None
    status: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    # Joined fields
    trainee_service_number: Optional[str] = None
    trainee_rank: Optional[str] = None
    trainee_full_name: Optional[str] = None
    trainee_trade: Optional[str] = None
    trainee_batch: Optional[str] = None
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True


class PersonalOccurrenceListResponse(BaseModel):
    total: int
    items: List[PersonalOccurrenceResponse]



