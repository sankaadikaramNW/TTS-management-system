from datetime import date, datetime
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student, ParadeSubmission
from app.models.user import User
from app.models.academic import Timetable, AcademicAttendance
from app.models.notification import Notification
from app.repositories.parade import parade_repo, submission_repo, officer_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.parade import (
    DailyParadeUpdateRequest, ParadeSubmissionCreate,
    ParadeSubmissionDraftSave, ApprovalActionRequest, RejectionActionRequest
)


class ParadeStateService:

    # ──────────────────────────────────────────────────────
    # Legacy batch-update (for backward compat / DRAFT saves)
    # ──────────────────────────────────────────────────────
    def update_daily_parade(self, db: Session, update_data: DailyParadeUpdateRequest,
                            user_id: str, ip: str, ua: str) -> dict:
        """Save parade records without triggering downstream sync (Draft mode)."""
        parade_date = update_data.date
        records = update_data.records

        updated_count = 0
        for rec in records:
            student = student_repo.get(db, rec.student_id)
            if not student or student.deleted_at:
                continue

            parade_repo.create_or_update(
                db,
                student_id=rec.student_id,
                parade_date=parade_date,
                status=rec.status,
                remarks=rec.remarks,
                user_id=user_id
            )
            updated_count += 1

        db.commit()

        audit_repo.create_log(
            db, user_id, "PARADE_DRAFT_SAVE", ip, ua,
            f"Draft-saved parade states for {updated_count} students on {parade_date}"
        )

        return {"status": "draft_saved", "updated_count": updated_count}

    # ──────────────────────────────────────────────────────
    # Save DRAFT for a specific trade (with submission record)
    # ──────────────────────────────────────────────────────
    def save_draft(self, db: Session, draft_data: ParadeSubmissionDraftSave,
                   user_id: str, ip: str, ua: str) -> dict:
        """Save parade records as DRAFT for a specific trade, creating a submission record."""
        parade_date = draft_data.date
        trade = draft_data.trade

        # Get or create a DRAFT submission for this trade/date
        # Use None for officer since draft doesn't require an officer yet
        existing = None
        from app.models.student import ParadeSubmission as PS
        existing = db.query(PS).filter(
            PS.date == parade_date,
            PS.trade == trade,
            PS.status.in_(['DRAFT', 'REJECTED'])
        ).first()

        if not existing:
            from app.models.base import generate_uuid
            sub = PS(
                id=generate_uuid(),
                date=parade_date,
                trade=trade,
                submitted_by=user_id,
                status='DRAFT'
            )
            db.add(sub)
            db.flush()
            submission_id = sub.id
        else:
            submission_id = existing.id

        updated_count = 0
        for rec in draft_data.records:
            student = student_repo.get(db, rec.student_id)
            if not student or student.deleted_at:
                continue
            parade_repo.create_or_update(
                db,
                student_id=rec.student_id,
                parade_date=parade_date,
                status=rec.status,
                remarks=rec.remarks,
                user_id=user_id,
                submission_id=submission_id
            )
            updated_count += 1

        db.commit()
        audit_repo.create_log(
            db, user_id, "PARADE_DRAFT_TRADE_SAVE", ip, ua,
            f"Draft-saved parade state for trade '{trade}' — {updated_count} students on {parade_date}"
        )
        return {"status": "draft_saved", "submission_id": submission_id, "updated_count": updated_count}

    # ──────────────────────────────────────────────────────
    # Submit for Approval
    # ──────────────────────────────────────────────────────
    def submit_parade(self, db: Session, submission_data: ParadeSubmissionCreate,
                      user_id: str, ip: str, ua: str) -> dict:
        """Save all records, create/update submission, and mark as SUBMITTED."""
        parade_date = submission_data.date
        trade = submission_data.trade
        officer_id = submission_data.approving_officer_id
        records = submission_data.records

        # Validate officer exists
        officer = db.query(User).filter(User.id == officer_id).first()
        if not officer:
            raise HTTPException(status_code=404, detail="Approving officer not found")

        # Get or create submission
        sub = submission_repo.get_or_create_draft(db, parade_date, trade, user_id, officer_id)

        # Check not already in SUBMITTED/APPROVED state
        if sub.status in ['SUBMITTED', 'APPROVED']:
            raise HTTPException(
                status_code=409,
                detail=f"Parade state for trade '{trade}' on {parade_date} is already {sub.status}. Cannot re-submit."
            )

        # Save all parade state records linked to this submission
        updated_count = 0
        for rec in records:
            student = student_repo.get(db, rec.student_id)
            if not student or student.deleted_at:
                continue
            parade_repo.create_or_update(
                db,
                student_id=rec.student_id,
                parade_date=parade_date,
                status=rec.status,
                remarks=rec.remarks,
                user_id=user_id,
                submission_id=sub.id
            )
            updated_count += 1

        # Transition to SUBMITTED
        submission_repo.submit(
            db, sub.id, user_id, officer_id, submission_data.submitter_remarks
        )

        # Send in-app notification to approving officer
        submitter = db.query(User).filter(User.id == user_id).first()
        notif = Notification(
            user_id=officer_id,
            title=f"Parade State Approval Required — {trade} ({parade_date})",
            message=(
                f"The Daily Parade State for trade '{trade}' on {parade_date} has been submitted "
                f"by {submitter.rank or ''} {submitter.full_name} for your approval. "
                f"Total strength: {updated_count} personnel."
            ),
            type="ALERT"
        )
        db.add(notif)
        db.commit()

        audit_repo.create_log(
            db, user_id, "PARADE_STATE_SUBMITTED", ip, ua,
            f"Submitted parade state for trade '{trade}' on {parade_date} to officer {officer.full_name}. Records: {updated_count}"
        )

        return {
            "status": "submitted",
            "submission_id": sub.id,
            "updated_count": updated_count,
            "approving_officer": f"{officer.rank or ''} {officer.full_name}".strip()
        }

    # ──────────────────────────────────────────────────────
    # Approve Submission
    # ──────────────────────────────────────────────────────
    def approve_parade(self, db: Session, submission_id: str, officer_id: str,
                       remarks: Optional[str], ip: str, ua: str) -> dict:
        """Approve a submitted parade state — triggers downstream academic sync."""
        sub = submission_repo.approve(db, submission_id, officer_id, remarks)
        if not sub:
            raise HTTPException(
                status_code=404,
                detail="Submission not found, not in SUBMITTED status, or you are not the designated approving officer."
            )

        # DOWNSTREAM SYNC — triggered only on official approval
        parade_date = sub.date
        trade = sub.trade
        states = parade_repo.get_parade_states_by_submission(db, submission_id)

        awol_students = []
        for state in states:
            student = student_repo.get(db, state.student_id)
            if not student:
                continue

            old_status = student.status

            # Update master student status (SSOT sync)
            student.status = state.status

            # Academic attendance sync for non-Present statuses
            if state.status != "Present":
                attendance_status = "Absent" if state.status == "AWOL" else "Excused"
                if student.course_id:
                    today_timetables = db.query(Timetable).filter(
                        Timetable.course_id == student.course_id,
                        Timetable.date == parade_date
                    ).all()
                    for tt in today_timetables:
                        att_record = db.query(AcademicAttendance).filter(
                            AcademicAttendance.timetable_id == tt.id,
                            AcademicAttendance.student_id == student.id
                        ).first()
                        if att_record:
                            att_record.status = attendance_status
                            att_record.remarks = f"Auto-synced on parade approval: {state.status}"
                        else:
                            db.add(AcademicAttendance(
                                timetable_id=tt.id,
                                student_id=student.id,
                                status=attendance_status,
                                remarks=f"Auto-synced on parade approval: {state.status}"
                            ))

            # Track AWOL/Hospital for admin alerts
            if state.status in ["AWOL", "Hospital"] and old_status != state.status:
                awol_students.append(student)

        # Critical status notifications to admin/CO
        if awol_students:
            from app.models.user import Role
            notif_users = db.query(User).join(User.role).filter(
                Role.name.in_(["Super Administrator", "Commanding Officer"])
            ).all()
            for admin in notif_users:
                for student in awol_students:
                    db.add(Notification(
                        user_id=admin.id,
                        title=f"CRITICAL STATE ALERT: {student.rank} {student.full_name}",
                        message=(
                            f"Student {student.service_number} is officially confirmed as '{student.status}' "
                            f"for {parade_date} (trade: {trade}). Parade approved by Officer I/C."
                        ),
                        type="ALERT"
                    ))

        # Notify the submitter of approval
        if sub.submitted_by:
            officer = db.query(User).filter(User.id == officer_id).first()
            db.add(Notification(
                user_id=sub.submitted_by,
                title=f"Parade State APPROVED — {trade} ({parade_date})",
                message=(
                    f"Your parade state submission for trade '{trade}' on {parade_date} has been "
                    f"APPROVED by {officer.rank or ''} {officer.full_name}. "
                    + (f"Remarks: {remarks}" if remarks else "")
                ),
                type="INFO"
            ))

        db.commit()

        audit_repo.create_log(
            db, officer_id, "PARADE_STATE_APPROVED", ip, ua,
            f"Approved parade state submission {submission_id} for trade '{trade}' on {parade_date}"
        )

        return {"status": "approved", "submission_id": submission_id, "trade": trade, "date": str(parade_date)}

    # ──────────────────────────────────────────────────────
    # Reject Submission
    # ──────────────────────────────────────────────────────
    def reject_parade(self, db: Session, submission_id: str, officer_id: str,
                      rejection_reason: str, ip: str, ua: str) -> dict:
        """Reject a submitted parade state — notifies submitter to revise."""
        sub = submission_repo.reject(db, submission_id, officer_id, rejection_reason)
        if not sub:
            raise HTTPException(
                status_code=404,
                detail="Submission not found, not in SUBMITTED status, or you are not the designated approving officer."
            )

        # Notify the submitter of rejection
        if sub.submitted_by:
            officer = db.query(User).filter(User.id == officer_id).first()
            db.add(Notification(
                user_id=sub.submitted_by,
                title=f"Parade State REJECTED — {sub.trade} ({sub.date})",
                message=(
                    f"Your parade state submission for trade '{sub.trade}' on {sub.date} has been "
                    f"REJECTED by {officer.rank or ''} {officer.full_name}. "
                    f"Reason: {rejection_reason}. Please revise and resubmit."
                ),
                type="ALERT"
            ))
        db.commit()

        audit_repo.create_log(
            db, officer_id, "PARADE_STATE_REJECTED", ip, ua,
            f"Rejected parade submission {submission_id} for trade '{sub.trade}' on {sub.date}. Reason: {rejection_reason}"
        )

        return {"status": "rejected", "submission_id": submission_id, "reason": rejection_reason}


parade_service = ParadeStateService()
