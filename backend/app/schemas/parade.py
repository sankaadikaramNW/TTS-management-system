from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class ParadeStateBase(BaseModel):
    student_id: str
    date: date
    status: str  # Present, Sick Report, Hospital, Leave, Temporary Duty, Course Visit, Detached Duty, AWOL
    remarks: Optional[str] = None

class ParadeStateCreate(ParadeStateBase):
    pass

class ParadeStateUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

class ParadeStateResponse(ParadeStateBase):
    id: str
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    student_rank: Optional[str] = None

    class Config:
        from_attributes = True

class DailyParadeRecord(BaseModel):
    student_id: str
    status: str
    remarks: Optional[str] = None

class DailyParadeUpdateRequest(BaseModel):
    date: date
    records: List[DailyParadeRecord]

class ParadeStateSummary(BaseModel):
    date: date
    total_strength: int
    present: int
    sick_report: int
    hospital: int
    leave: int
    temp_duty: int
    course_visit: int
    detached_duty: int
    awol: int
