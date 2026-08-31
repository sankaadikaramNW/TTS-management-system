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
        from app.repositories.academic import batch_repo

        parade_date = submission_data.date
        trade = submission_data.trade
        course_id = submission_data.course_id
        batch = submission_data.batch
        officer_id = submission_data.approving_officer_id
        records = submission_data.records

        # If not provided, automatically determine assigned Instructor from Course/Batch
        if not officer_id:
            assigned_inst = batch_repo.get_instructor_for_batch(
                db, trade=trade, course_id=course_id, batch_name=batch
            )
            if assigned_inst:
                officer_id = assigned_inst.id

        # Look up instructor details if assigned
        officer = db.query(User).filter(User.id == officer_id).first() if officer_id else None

        # Get or create submission
        sub = submission_repo.get_or_create_draft(
            db, parade_date, trade, user_id, officer_id, course_id=course_id, batch=batch
        )

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

        # Send in-app notification to approving instructor (if assigned)
        submitter = db.query(User).filter(User.id == user_id).first()
        if officer_id and officer:
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

        action_name = "PARADE_STATE_RESUBMITTED" if sub.status == 'REJECTED' else "PARADE_STATE_SUBMITTED"
        approver_display = f"{officer.rank or ''} {officer.full_name}".strip() if officer else "INSTRUCTOR NOT ASSIGNED"
        audit_repo.create_log(
            db, user_id, action_name, ip, ua,
            f"Submitted parade state for trade '{trade}' on {parade_date} to {approver_display}. Records: {updated_count}"
        )

        return {
            "status": "submitted",
            "id": sub.id,
            "submission_id": sub.id,
            "updated_count": updated_count,
            "approving_officer": approver_display
        }

    # ──────────────────────────────────────────────────────
    # Approve Submission
    # ──────────────────────────────────────────────────────
    def approve_parade(self, db: Session, submission_id: str, officer_id: str,
                       remarks: Optional[str], ip: str, ua: str) -> dict:
        """Approve a submitted parade state — verifies instructor authorization & triggers downstream academic sync."""
        from app.repositories.academic import batch_repo

        sub_record = db.query(ParadeSubmission).filter(ParadeSubmission.id == submission_id).first()
        if not sub_record:
            raise HTTPException(status_code=404, detail="Submission not found")
        if sub_record.status != 'SUBMITTED':
            raise HTTPException(
                status_code=400,
                detail=f"Submission is not in SUBMITTED status (current status: {sub_record.status})"
            )

        # Verify caller authorization
        approver_user = db.query(User).filter(User.id == officer_id).first()
        is_admin = False
        if approver_user and approver_user.role:
            is_admin = approver_user.role.name in ["Super Administrator", "System Administrator", "Commanding Officer"]

        assigned_inst = batch_repo.get_instructor_for_batch(
            db, trade=sub_record.trade, course_id=sub_record.course_id, batch_name=sub_record.batch
        )
        is_assigned_instructor = (assigned_inst and assigned_inst.id == officer_id) or (sub_record.approving_officer_id == officer_id)

        if not is_admin and not is_assigned_instructor:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You are not the assigned Instructor for this Course/Batch."
            )

        sub = submission_repo.approve(db, submission_id, officer_id, remarks)
        if not sub:
            raise HTTPException(status_code=500, detail="Failed to approve submission")

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
                            f"for {parade_date} (trade: {trade}). Parade approved by Instructor."
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
                    f"APPROVED by {officer.rank or ''} {officer.full_name if officer else 'Instructor'}. "
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
    # Reject / Return Submission for Correction
    # ──────────────────────────────────────────────────────
    def reject_parade(self, db: Session, submission_id: str, officer_id: str,
                      rejection_reason: str, ip: str, ua: str,
                      remarks: Optional[str] = None) -> dict:
        """Reject/return a submitted parade state for correction with authorization check."""
        from app.repositories.academic import batch_repo

        sub_record = db.query(ParadeSubmission).filter(ParadeSubmission.id == submission_id).first()
        if not sub_record:
            raise HTTPException(status_code=404, detail="Submission not found")
        if sub_record.status != 'SUBMITTED':
            raise HTTPException(
                status_code=400,
                detail=f"Submission is not in SUBMITTED status (current status: {sub_record.status})"
            )

        # Verify caller authorization
        approver_user = db.query(User).filter(User.id == officer_id).first()
        is_admin = False
        if approver_user and approver_user.role:
            is_admin = approver_user.role.name in ["Super Administrator", "System Administrator", "Commanding Officer"]

        assigned_inst = batch_repo.get_instructor_for_batch(
            db, trade=sub_record.trade, course_id=sub_record.course_id, batch_name=sub_record.batch
        )
        is_assigned_instructor = (assigned_inst and assigned_inst.id == officer_id) or (sub_record.approving_officer_id == officer_id)

        if not is_admin and not is_assigned_instructor:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: You are not the assigned Instructor for this Course/Batch."
            )

        sub = submission_repo.reject(db, submission_id, officer_id, rejection_reason, remarks)
        if not sub:
            raise HTTPException(status_code=500, detail="Failed to return submission")

        # Notify the submitter of the return with reasons
        if sub.submitted_by:
            officer = db.query(User).filter(User.id == officer_id).first()
            officer_name = f"{officer.rank or ''} {officer.full_name}".strip() if officer else "Instructor"
            db.add(Notification(
                user_id=sub.submitted_by,
                title=f"Parade State RETURNED FOR CORRECTION — {sub.trade} ({sub.date})",
                message=(
                    f"Your parade state for {sub.trade} on {sub.date} was returned by {officer_name}. "
                    f"Reason: {rejection_reason}."
                ),
                type="ALERT"
            ))
            db.commit()

        audit_repo.create_log(
            db, officer_id, "PARADE_STATE_RETURNED", ip, ua,
            f"Returned parade submission {submission_id} for trade '{sub.trade}' on {sub.date}. Reason: {rejection_reason}"
        )

        return {
            "status": "returned_for_correction",
            "submission_id": submission_id,
            "id": submission_id,
            "trade": sub.trade,
            "date": str(sub.date),
            "rejection_reason": rejection_reason,
            "reason": rejection_reason
        }

    # ──────────────────────────────────────────────────────
    # Monitoring & Outstanding Service Functions
    # ──────────────────────────────────────────────────────
    def get_monitoring(self, db: Session, target_date: date,
                       trade: Optional[str] = None,
                       course_id: Optional[str] = None,
                       batch: Optional[str] = None,
                       status_filter: Optional[str] = None,
                       only_outstanding: bool = False,
                       only_pending: bool = False) -> dict:
        """Get live monitoring status and items for all required trades."""
        return submission_repo.get_monitoring_data(
            db, target_date=target_date,
            trade_filter=trade, course_id_filter=course_id,
            batch_filter=batch, status_filter=status_filter,
            only_outstanding=only_outstanding,
            only_pending=only_pending
        )

    def get_date_range_monitoring(self, db: Session, start_date: date, end_date: date,
                                  trade: Optional[str] = None) -> dict:
        """Get multi-day compliance tracking across date range."""
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="start_date cannot be after end_date")
        return submission_repo.get_date_range_monitoring(db, start_date, end_date, trade)

    def get_my_outstanding(self, db: Session, current_user: User, target_date: date) -> dict:
        """Get outstanding items relevant to the currently logged in user (Instructor or Officer)."""
        from app.models.academic import Batch
        # Check batches where user is assigned instructor
        assigned_batches = db.query(Batch).filter(Batch.instructor_id == current_user.id, Batch.status == 'Active').all()
        inst_batch_names = [b.name for b in assigned_batches]
        inst_course_ids = [b.course_id for b in assigned_batches if b.course_id]

        # Officer I/C assignments
        assigned_oic = officer_repo.get_all(db)
        user_trades = [o.trade for o in assigned_oic if o.user_id == current_user.id]

        monitoring_data = submission_repo.get_monitoring_data(db, target_date=target_date)
        # If user is Officer I/C of specific trades, show those trades; otherwise show all outstanding
        if user_trades:
            monitoring_data["items"] = [i for i in monitoring_data["items"] if i["trade"] in user_trades]
            for idx, itm in enumerate(monitoring_data["items"], 1):
                itm["s_no"] = idx

        return monitoring_data

    def get_outstanding_report_data(self, db: Session, current_user: User,
                                    target_date: date, trade: Optional[str] = None,
                                    status_filter: Optional[str] = None,
                                    ip: str = "127.0.0.1", ua: str = "Unknown") -> dict:
        """Compile classical Sri Lanka Air Force Outstanding Parade State Report dataset."""
        monitoring_data = submission_repo.get_monitoring_data(
            db, target_date=target_date, trade_filter=trade, status_filter=status_filter
        )
        summary = monitoring_data["summary"]
        items = monitoring_data["items"]

        audit_repo.create_log(
            db, current_user.id, "REPORT_GENERATED", ip, ua,
            f"Generated Outstanding Parade State Report for date: {target_date}"
        )

        rows = []
        for idx, item in enumerate(items, 1):
            rows.append({
                "s_no": idx,
                "trade": item["trade"],
                "course_name": item["course_name"] or "N/A",
                "batch": item["batch"] or "N/A",
                "total_trainees": item["total_trainees"],
                "submission_status": item["submission_status"],
                "approval_status": item["approval_status"],
                "status_label": item["status_label"],
                "submitted_by": item["submitted_by_name"] or "-",
                "submitted_at": item["submitted_at"].strftime("%Y-%m-%d %H:%M") if item["submitted_at"] else "-",
                "approving_officer": item["approving_officer_name"] or "-",
                "reviewed_at": item["reviewed_at"].strftime("%Y-%m-%d %H:%M") if item["reviewed_at"] else "-",
                "remarks": item["rejection_reason"] or item["submitter_remarks"] or item["approver_remarks"] or "-"
            })

        return {
            "title": "SRI LANKA AIR FORCE • TRADE TRAINING SCHOOL",
            "subtitle": f"OUTSTANDING & PENDING PARADE STATE REPORT — {target_date.strftime('%d %B %Y').upper()}",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "generated_by": f"{current_user.rank or ''} {current_user.full_name} ({current_user.username})",
            "parade_date": str(target_date),
            "summary": summary,
            "rows": rows
        }


parade_service = ParadeStateService()
