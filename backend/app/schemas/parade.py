from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

# ─────────────────────────────────────────────────────────────
# Existing Parade State Schemas
# ─────────────────────────────────────────────────────────────

class ParadeStateBase(BaseModel):
    student_id: str
    date: date
    status: str
    remarks: Optional[str] = None

class ParadeStateCreate(ParadeStateBase):
    pass

class ParadeStateUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None

class ParadeStateResponse(ParadeStateBase):
    id: str
    updated_by: Optional[str] = None
    submission_id: Optional[str] = None
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

class ParadeStatusTypeResponse(BaseModel):
    id: str
    code: str
    label: str
    is_active: bool

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────
# Officer I/C Schemas
# ─────────────────────────────────────────────────────────────

class OfficerInChargeCreate(BaseModel):
    trade: str
    user_id: str

class OfficerInChargeResponse(BaseModel):
    id: str
    trade: str
    user_id: str
    is_active: bool
    appointed_at: datetime
    officer_name: Optional[str] = None
    officer_rank: Optional[str] = None
    officer_service_number: Optional[str] = None
    appointed_by_name: Optional[str] = None

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────────────────────
# Parade Submission Schemas (Approval Workflow)
# ─────────────────────────────────────────────────────────────

class ParadeSubmissionCreate(BaseModel):
    date: date
    trade: str
    approving_officer_id: str
    submitter_remarks: Optional[str] = None
    records: List[DailyParadeRecord]

class ParadeSubmissionDraftSave(BaseModel):
    """Save parade records as DRAFT without submitting for approval."""
    date: date
    trade: str
    records: List[DailyParadeRecord]

class ApprovalActionRequest(BaseModel):
    remarks: Optional[str] = None

class RejectionActionRequest(BaseModel):
    rejection_reason: str

class ParadeSubmissionResponse(BaseModel):
    id: str
    date: date
    trade: str
    status: str  # DRAFT | SUBMITTED | APPROVED | REJECTED
    submitted_by: Optional[str] = None
    approving_officer_id: Optional[str] = None
    submitter_remarks: Optional[str] = None
    approver_remarks: Optional[str] = None
    rejection_reason: Optional[str] = None
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    # Enriched fields (populated in repository)
    submitter_name: Optional[str] = None
    submitter_rank: Optional[str] = None
    officer_name: Optional[str] = None
    officer_rank: Optional[str] = None
    officer_service_number: Optional[str] = None
    total_strength: Optional[int] = None
    present_count: Optional[int] = None
    absent_count: Optional[int] = None

    class Config:
        from_attributes = True

class ParadeSubmissionDetailResponse(ParadeSubmissionResponse):
    """Full detail response including all parade state records."""
    records: Optional[List[ParadeStateResponse]] = None
