from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.models.student import ParadeStatusType
from app.repositories.parade import parade_repo, submission_repo, officer_repo
from app.services.parade import parade_service
from app.schemas.parade import (
    ParadeStateResponse, DailyParadeUpdateRequest, ParadeStateSummary,
    ParadeStatusTypeResponse, OfficerInChargeCreate, OfficerInChargeResponse,
    ParadeSubmissionCreate, ParadeSubmissionDraftSave, ParadeSubmissionResponse,
    ParadeSubmissionDetailResponse, ApprovalActionRequest, RejectionActionRequest
)

router = APIRouter(prefix="/parade", tags=["Daily Parade State"])


# ─────────────────────────────────────────────────────────────
# Reference Data
# ─────────────────────────────────────────────────────────────

@router.get("/statuses", response_model=List[ParadeStatusTypeResponse])
def get_parade_statuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available parade status types."""
    return db.query(ParadeStatusType).filter(ParadeStatusType.is_active == True).all()


# ─────────────────────────────────────────────────────────────
# Existing Parade State Endpoints (Backward Compatible)
# ─────────────────────────────────────────────────────────────

@router.get("/status", response_model=List[ParadeStateResponse])
def get_daily_parade_state(
    parade_date: Optional[date] = None,
    trade: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    """Get per-student parade records for a given date, optionally filtered by trade."""
    target_date = parade_date or date.today()
    results = parade_repo.get_parade_states_by_date(db, target_date)
    if trade:
        # Filter by student trade
        from app.models.student import Student
        results = [r for r in results if (
            db.query(Student).filter(Student.id == r.student_id).first() or type('', (), {'trade': ''})()
        ).trade == trade]
    return results


@router.get("/summary", response_model=ParadeStateSummary)
def get_daily_parade_summary(
    parade_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    """Get strength summary counts for a given date."""
    target_date = parade_date or date.today()
    return parade_repo.get_summary(db, target_date)


@router.post("/update")
def batch_update_parade_state(
    request: Request,
    update_data: DailyParadeUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:write"))
):
    """Legacy batch update — saves as draft without submission workflow."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.update_daily_parade(db, update_data, current_user.id, ip, ua)


# ─────────────────────────────────────────────────────────────
# Parade Submissions — Approval Workflow
# ─────────────────────────────────────────────────────────────

@router.post("/draft", summary="Save parade records as DRAFT for a specific trade")
def save_draft_parade(
    request: Request,
    draft_data: ParadeSubmissionDraftSave,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:write"))
):
    """Auto-save parade records as DRAFT for a specific trade. Creates a submission record if none exists."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.save_draft(db, draft_data, current_user.id, ip, ua)


@router.post("/submit", summary="Submit parade state for Officer I/C approval")
def submit_parade_for_approval(
    request: Request,
    submission_data: ParadeSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:write"))
):
    """Submit the daily parade state for a specific trade to the designated Officer I/C for approval."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.submit_parade(db, submission_data, current_user.id, ip, ua)


@router.get("/submissions", response_model=List[ParadeSubmissionResponse],
            summary="List parade submissions")
def list_submissions(
    parade_date: Optional[date] = None,
    trade: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    """List parade submissions with optional filters. Officers see all; NCOs see their own."""
    return submission_repo.get_list(db, parade_date, trade, status, limit)


@router.get("/submissions/pending", response_model=List[ParadeSubmissionResponse],
            summary="Get pending approvals for current officer")
def get_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all parade submissions awaiting approval by the currently logged-in user."""
    return submission_repo.get_pending_for_officer(db, current_user.id)


@router.get("/submissions/{submission_id}", response_model=ParadeSubmissionDetailResponse,
            summary="Get full details of a parade submission")
def get_submission_detail(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    """Get full detail of a specific parade submission, including all per-student records."""
    sub = submission_repo.get_by_id(db, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Attach per-student records
    records = parade_repo.get_parade_states_by_submission(db, submission_id)
    sub.records = records
    return sub


@router.post("/submissions/{submission_id}/approve", summary="Approve a parade submission")
def approve_parade_submission(
    submission_id: str,
    request: Request,
    action: ApprovalActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:approve"))
):
    """Approve a submitted parade state. Triggers downstream academic sync and student status updates."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.approve_parade(db, submission_id, current_user.id, action.remarks, ip, ua)


@router.post("/submissions/{submission_id}/reject", summary="Reject a parade submission")
def reject_parade_submission(
    submission_id: str,
    request: Request,
    action: RejectionActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:approve"))
):
    """Reject a submitted parade state with a mandatory reason. Notifies the submitter to revise."""
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return parade_service.reject_parade(db, submission_id, current_user.id, action.rejection_reason, ip, ua)


# ─────────────────────────────────────────────────────────────
# Officer I/C Appointment Management
# ─────────────────────────────────────────────────────────────

@router.get("/officers", response_model=List[OfficerInChargeResponse],
            summary="List all Officer I/C assignments")
def list_officers_in_charge(
    trade: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:read"))
):
    """List all active Officer I/C appointments, optionally filtered by trade."""
    if trade:
        return officer_repo.get_by_trade(db, trade)
    return officer_repo.get_all(db)


@router.post("/officers", response_model=OfficerInChargeResponse, status_code=status.HTTP_201_CREATED,
             summary="Assign an Officer I/C to a trade")
def assign_officer_in_charge(
    request: Request,
    oic_data: OfficerInChargeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:manage_officers"))
):
    """Assign a user as Officer I/C for a specific trade."""
    from app.models.user import User as UserModel
    officer = db.query(UserModel).filter(UserModel.id == oic_data.user_id, UserModel.deleted_at == None).first()
    if not officer:
        raise HTTPException(status_code=404, detail="User not found")
    return officer_repo.assign(db, oic_data.trade, oic_data.user_id, current_user.id)


@router.delete("/officers/{oic_id}", summary="Remove an Officer I/C assignment")
def remove_officer_in_charge(
    oic_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("parade:manage_officers"))
):
    """Deactivate an Officer I/C assignment."""
    success = officer_repo.remove(db, oic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Officer I/C assignment not found")

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    from app.repositories.user import audit_repo
    audit_repo.create_log(
        db, current_user.id, "OIC_ASSIGNMENT_REMOVED", ip, ua,
        f"Removed Officer I/C assignment {oic_id}"
    )

    return {"status": "removed", "oic_id": oic_id}
