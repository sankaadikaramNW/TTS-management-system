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
    parade_type: Optional[str] = 'MORNING'
    morning_status: Optional[str] = None
    status_changed: Optional[bool] = False
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
    can_sit_exam: bool = True
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
    approving_officer_id: Optional[str] = None
    course_id: Optional[str] = None
    batch: Optional[str] = None
    submitter_remarks: Optional[str] = None
    records: List[DailyParadeRecord]

class ParadeSubmissionDraftSave(BaseModel):
    """Save parade records as DRAFT without submitting for approval."""
    date: date
    trade: str
    course_id: Optional[str] = None
    batch: Optional[str] = None
    records: List[DailyParadeRecord]

class ApprovalActionRequest(BaseModel):
    remarks: Optional[str] = None

class RejectionActionRequest(BaseModel):
    rejection_reason: str

class ParadeSubmissionResponse(BaseModel):
    id: str
    date: date
    trade: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    batch: Optional[str] = None
    status: str  # DRAFT | SUBMITTED | APPROVED | REJECTED
    submitted_by: Optional[str] = None
    approving_officer_id: Optional[str] = None
    submitter_remarks: Optional[str] = None
    approver_remarks: Optional[str] = None
    rejection_reason: Optional[str] = None
    returned_by: Optional[str] = None
    returned_at: Optional[datetime] = None
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
    assigned_instructor_id: Optional[str] = None
    assigned_instructor_name: Optional[str] = None
    assigned_instructor_rank: Optional[str] = None
    assigned_instructor_service_number: Optional[str] = None
    instructor_status: Optional[str] = None
    total_strength: Optional[int] = None
    present_count: Optional[int] = None
    absent_count: Optional[int] = None

    class Config:
        from_attributes = True

class ParadeSubmissionDetailResponse(ParadeSubmissionResponse):
    """Full detail response including all parade state records."""
    records: Optional[List[ParadeStateResponse]] = None


# ─────────────────────────────────────────────────────────────
# Parade Submission Monitoring & Outstanding Schemas
# ─────────────────────────────────────────────────────────────

class ParadeReturnActionRequest(BaseModel):
    rejection_reason: str
    remarks: Optional[str] = None

class ParadeMonitoringSummary(BaseModel):
    date: date
    total_required: int = 0
    not_submitted: int = 0
    pending_approval: int = 0
    approved: int = 0
    returned: int = 0
    overdue: int = 0

class ParadeMonitoringItem(BaseModel):
    s_no: int
    trade: str
    course_id: Optional[str] = None
    course_code: Optional[str] = None
    course_name: Optional[str] = None
    batch: Optional[str] = None
    total_trainees: int = 0
    submission_status: str  # NOT_SUBMITTED | DRAFT | SUBMITTED | APPROVED | RETURNED
    approval_status: str    # '-' | PENDING APPROVAL | APPROVED | RETURNED FOR CORRECTION
    status_label: str       # NOT SUBMITTED | PENDING APPROVAL | APPROVED | RETURNED FOR CORRECTION
    status_code: str        # NOT_SUBMITTED | PENDING_APPROVAL | APPROVED | RETURNED
    submission_id: Optional[str] = None
    submitted_by: Optional[str] = None
    submitted_by_name: Optional[str] = None
    submitted_by_rank: Optional[str] = None
    submitted_at: Optional[datetime] = None
    approving_officer_id: Optional[str] = None
    approving_officer_name: Optional[str] = None
    approving_officer_rank: Optional[str] = None
    assigned_instructor_id: Optional[str] = None
    assigned_instructor_name: Optional[str] = None
    assigned_instructor_rank: Optional[str] = None
    assigned_instructor_service_number: Optional[str] = None
    instructor_status: Optional[str] = "ASSIGNED" # ASSIGNED | NOT_ASSIGNED
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    approver_remarks: Optional[str] = None
    submitter_remarks: Optional[str] = None
    is_overdue: bool = False
    deadline: Optional[str] = "08:00 hrs"
    can_submit: bool = True
    can_approve: bool = False

class ParadeMonitoringResponse(BaseModel):
    date: date
    operational_date: date
    summary: ParadeMonitoringSummary
    items: List[ParadeMonitoringItem]

class ParadeDateRangeMonitoringItem(BaseModel):
    date: date
    trade: str
    course_name: Optional[str] = None
    batch: Optional[str] = None
    total_trainees: int = 0
    status_label: str
    status_code: str
    submission_id: Optional[str] = None
    submitted_by_name: Optional[str] = None
    approving_officer_name: Optional[str] = None
    is_overdue: bool = False

class ParadeDateRangeResponse(BaseModel):
    start_date: date
    end_date: date
    total_entries: int
    items: List[ParadeDateRangeMonitoringItem]
    trades: List[str]


# ─────────────────────────────────────────────────────────────
# Night Parade State & Evening Roll Call Schemas
# ─────────────────────────────────────────────────────────────

class NightParadeRecord(BaseModel):
    student_id: str
    night_status: str
    morning_status: Optional[str] = None
    remarks: Optional[str] = None
    is_verified: bool = True

class NightParadeSaveDraftRequest(BaseModel):
    date: date
    trade: str
    course_id: Optional[str] = None
    batch: Optional[str] = None
    submitter_remarks: Optional[str] = None
    records: List[NightParadeRecord]

# Semantic alias
NightParadeSaveRequest = NightParadeSaveDraftRequest

class NightParadeSaveResponse(BaseModel):
    status: str
    submission_id: Optional[str] = None
    updated_count: int = 0
    changed_count: int = 0
    last_saved_at: Optional[str] = None

class NightParadeCompleteRequest(BaseModel):
    """Complete and lock Night Parade Roll Call with 100% accountability verification."""
    date: date
    trade: str
    course_id: Optional[str] = None
    batch: Optional[str] = None
    submitter_remarks: Optional[str] = None
    records: List[NightParadeRecord]

class NightParadeSubmitRequest(NightParadeCompleteRequest):
    """Alias for backward compatibility."""
    approving_officer_id: Optional[str] = None

class NightParadeTraineeItem(BaseModel):
    student_id: str
    service_number: str
    rank: Optional[str] = "AC"
    full_name: str
    trade: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    batch: Optional[str] = None
    medical_category: Optional[str] = "A4G4"
    morning_status: Optional[str] = None
    night_status: Optional[str] = None
    status_changed: bool = False
    remarks: Optional[str] = None
    is_verified: bool = False

class NightParadeContextResponse(BaseModel):
    date: date
    trade: str
    course_id: Optional[str] = None
    course_name: Optional[str] = None
    batch: Optional[str] = None
    morning_available: bool
    morning_submission_status: Optional[str] = None
    morning_submission_id: Optional[str] = None
    night_submission_id: Optional[str] = None
    night_submission_status: Optional[str] = None  # DRAFT | IN_PROGRESS | COMPLETED
    submitter_remarks: Optional[str] = None
    completed_by_name: Optional[str] = None
    completed_at: Optional[datetime] = None
    is_accountability_complete: bool = False
    expected_strength: int = 0
    accounted_strength: int = 0
    unverified_count: int = 0
    can_complete: bool = True
    trainees: List[NightParadeTraineeItem]

    # Optional legacy fields for backward compatibility
    can_submit: bool = True
    can_approve: bool = False
    approving_officer_id: Optional[str] = None
    approving_officer_name: Optional[str] = None
    approving_officer_rank: Optional[str] = None
    assigned_instructor_id: Optional[str] = None
    assigned_instructor_name: Optional[str] = None
    assigned_instructor_rank: Optional[str] = None
    instructor_status: Optional[str] = None
    approver_remarks: Optional[str] = None
    rejection_reason: Optional[str] = None

class NightStatusTransitionItem(BaseModel):
    from_status: str
    to_status: str
    count: int

class NightStrengthBreakdownItem(BaseModel):
    label: str
    expected: int = 0
    present: int = 0
    sick_report: int = 0
    hospital: int = 0
    leave: int = 0
    awol: int = 0
    course_visit: int = 0
    temp_duty: int = 0
    detached_duty: int = 0
    other: int = 0
    changed: int = 0
    unverified: int = 0

class NightParadeSummaryResponse(BaseModel):
    date: date
    trade: Optional[str] = None
    total_expected: int = 0
    present: int = 0
    sick_report: int = 0
    hospital: int = 0
    leave: int = 0
    awol: int = 0
    course_visit: int = 0
    temp_duty: int = 0
    detached_duty: int = 0
    other: int = 0
    status_changed_count: int = 0
    unverified_count: int = 0
    trade_wise: List[NightStrengthBreakdownItem] = []
    category_wise: List[NightStrengthBreakdownItem] = []
    transitions: List[NightStatusTransitionItem] = []

