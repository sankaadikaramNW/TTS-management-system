from datetime import date, datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from app.models.student import Student, ParadeState, ParadeSubmission, OfficerInCharge, Trade
from app.models.academic import Course, Batch
from app.models.user import User


class ParadeStateRepository:
    # ─────────────────────────────────────────────
    # Core Parade State (per-student, per-date)
    # ─────────────────────────────────────────────

    def get_by_student_and_date(self, db: Session, student_id: str, parade_date: date) -> Optional[ParadeState]:
        return db.query(ParadeState).filter(
            ParadeState.student_id == student_id,
            ParadeState.date == parade_date
        ).first()

    def get_parade_states_by_date(self, db: Session, parade_date: date) -> List[ParadeState]:
        results = db.query(ParadeState).filter(ParadeState.date == parade_date).all()
        for p in results:
            student = db.query(Student).filter(Student.id == p.student_id).first()
            if student:
                p.student_name = student.full_name
                p.student_service_number = student.service_number
                p.student_rank = student.rank
        return results

    def get_parade_states_by_submission(self, db: Session, submission_id: str) -> List[ParadeState]:
        results = db.query(ParadeState).filter(ParadeState.submission_id == submission_id).all()
        for p in results:
            student = db.query(Student).filter(Student.id == p.student_id).first()
            if student:
                p.student_name = student.full_name
                p.student_service_number = student.service_number
                p.student_rank = student.rank
        return results

    def create_or_update(self, db: Session, *, student_id: str, parade_date: date,
                         status: str, remarks: Optional[str] = None,
                         user_id: Optional[str] = None,
                         submission_id: Optional[str] = None) -> ParadeState:
        db_obj = self.get_by_student_and_date(db, student_id, parade_date)
        if db_obj:
            db_obj.status = status
            db_obj.remarks = remarks
            db_obj.updated_by = user_id
            if submission_id:
                db_obj.submission_id = submission_id
        else:
            db_obj = ParadeState(
                student_id=student_id,
                date=parade_date,
                status=status,
                remarks=remarks,
                updated_by=user_id,
                submission_id=submission_id
            )
            db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_summary(self, db: Session, parade_date: date, official_approved_only: bool = False) -> dict:
        """
        Get strength summary counts for a given date.
        If official_approved_only=True, only counts students from trades with APPROVED submissions.
        """
        total_enrolled = db.query(Student).filter(
            Student.deleted_at == None, Student.status != "Passed Out"
        ).count()
        
        if official_approved_only:
            # Query only approved submissions for this date
            approved_subs = db.query(ParadeSubmission.id).filter(
                ParadeSubmission.date == parade_date,
                ParadeSubmission.status == 'APPROVED'
            ).all()
            approved_sub_ids = [s[0] for s in approved_subs]
            if approved_sub_ids:
                states = db.query(ParadeState).filter(
                    ParadeState.date == parade_date,
                    ParadeState.submission_id.in_(approved_sub_ids)
                ).all()
            else:
                states = []
        else:
            states = db.query(ParadeState).filter(ParadeState.date == parade_date).all()

        summary = {
            "date": parade_date,
            "total_strength": total_enrolled,
            "present": 0,
            "sick_report": 0,
            "hospital": 0,
            "leave": 0,
            "temp_duty": 0,
            "course_visit": 0,
            "detached_duty": 0,
            "awol": 0
        }

        status_map = {
            "Present": "present",
            "Sick Report": "sick_report",
            "Hospital": "hospital",
            "Leave": "leave",
            "Temporary Duty": "temp_duty",
            "Course Visit": "course_visit",
            "Detached Duty": "detached_duty",
            "AWOL": "awol"
        }

        logged_student_ids = set()
        for state in states:
            logged_student_ids.add(state.student_id)
            key = status_map.get(state.status)
            if key:
                summary[key] += 1

        if not official_approved_only:
            unrecorded_count = total_enrolled - len(logged_student_ids)
            if unrecorded_count > 0:
                summary["present"] += unrecorded_count

        return summary


class ParadeSubmissionRepository:
    # ─────────────────────────────────────────────
    # Submissions (Approval Workflow)
    # ─────────────────────────────────────────────

    def _enrich_submission(self, db: Session, sub: ParadeSubmission) -> ParadeSubmission:
        """Attach display-friendly fields from related User objects and Academic Batch."""
        from app.repositories.academic import batch_repo

        if sub.submitted_by:
            submitter = db.query(User).filter(User.id == sub.submitted_by).first()
            if submitter:
                sub.submitter_name = f"{submitter.rank or ''} {submitter.full_name}".strip()
                sub.submitter_rank = submitter.rank

        if sub.approving_officer_id:
            officer = db.query(User).filter(User.id == sub.approving_officer_id).first()
            if officer:
                sub.officer_name = f"{officer.rank or ''} {officer.full_name}".strip()
                sub.officer_rank = officer.rank
                sub.officer_service_number = officer.service_number

        if sub.returned_by:
            ret_user = db.query(User).filter(User.id == sub.returned_by).first()
            if ret_user:
                sub.returned_by_name = f"{ret_user.rank or ''} {ret_user.full_name}".strip()

        # Resolve assigned instructor from academic batch (SSOT)
        assigned_inst = batch_repo.get_instructor_for_batch(
            db, trade=sub.trade, course_id=sub.course_id, batch_name=sub.batch
        )
        if assigned_inst:
            sub.assigned_instructor_id = assigned_inst.id
            sub.assigned_instructor_name = f"{assigned_inst.rank or ''} {assigned_inst.full_name}".strip()
            sub.assigned_instructor_rank = assigned_inst.rank
            sub.assigned_instructor_service_number = assigned_inst.service_number
            sub.instructor_status = "ASSIGNED"
        else:
            sub.assigned_instructor_id = None
            sub.assigned_instructor_name = "INSTRUCTOR NOT ASSIGNED"
            sub.assigned_instructor_rank = None
            sub.assigned_instructor_service_number = None
            sub.instructor_status = "NOT_ASSIGNED"

        if sub.course_id:
            c = db.query(Course).filter(Course.id == sub.course_id).first()
            if c:
                sub.course_name = c.name

        # Calculate strength counts from linked parade states
        states = db.query(ParadeState).filter(ParadeState.submission_id == sub.id).all()
        sub.total_strength = len(states)
        sub.present_count = sum(1 for s in states if s.status == "Present")
        sub.absent_count = sub.total_strength - sub.present_count

        return sub

    def get_or_create_draft(self, db: Session, parade_date: date, trade: str,
                            submitter_id: str, officer_id: Optional[str] = None,
                            course_id: Optional[str] = None,
                            batch: Optional[str] = None) -> ParadeSubmission:
        """Get existing DRAFT/REJECTED submission or create a new one."""
        from app.repositories.academic import batch_repo

        if not officer_id:
            assigned_inst = batch_repo.get_instructor_for_batch(
                db, trade=trade, course_id=course_id, batch_name=batch
            )
            if assigned_inst:
                officer_id = assigned_inst.id

        existing = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == parade_date,
            ParadeSubmission.trade == trade,
            ParadeSubmission.status.in_(['DRAFT', 'REJECTED'])
        ).first()

        if existing:
            # Update the officer selection and submitter
            existing.submitted_by = submitter_id
            if officer_id:
                existing.approving_officer_id = officer_id
            if course_id:
                existing.course_id = course_id
            if batch:
                existing.batch = batch
            db.commit()
            db.refresh(existing)
            return existing

        sub = ParadeSubmission(
            date=parade_date,
            trade=trade,
            course_id=course_id,
            batch=batch,
            submitted_by=submitter_id,
            approving_officer_id=officer_id,
            status='DRAFT'
        )
        db.add(sub)
        db.commit()
        db.refresh(sub)
        return sub

    def get_by_id(self, db: Session, submission_id: str) -> Optional[ParadeSubmission]:
        sub = db.query(ParadeSubmission).filter(ParadeSubmission.id == submission_id).first()
        if sub:
            sub = self._enrich_submission(db, sub)
        return sub

    def get_list(self, db: Session, parade_date: Optional[date] = None,
                 trade: Optional[str] = None, status: Optional[str] = None,
                 limit: int = 50) -> List[ParadeSubmission]:
        q = db.query(ParadeSubmission)
        if parade_date:
            q = q.filter(ParadeSubmission.date == parade_date)
        if trade:
            q = q.filter(ParadeSubmission.trade == trade)
        if status:
            q = q.filter(ParadeSubmission.status == status)
        results = q.order_by(ParadeSubmission.date.desc(), ParadeSubmission.trade).limit(limit).all()
        return [self._enrich_submission(db, sub) for sub in results]

    def get_pending_for_officer(self, db: Session, officer_id: str) -> List[ParadeSubmission]:
        from app.models.academic import Batch
        # Batches assigned to this instructor
        inst_batches = db.query(Batch).filter(Batch.instructor_id == officer_id, Batch.status == 'Active').all()
        inst_batch_names = [b.name for b in inst_batches]
        inst_course_ids = [b.course_id for b in inst_batches if b.course_id]

        # Query all submitted submissions that target this officer OR match this instructor's active batches
        q = db.query(ParadeSubmission).filter(ParadeSubmission.status == 'SUBMITTED')
        if inst_batches:
            q = q.filter(
                (ParadeSubmission.approving_officer_id == officer_id) |
                (ParadeSubmission.batch.in_(inst_batch_names)) |
                (ParadeSubmission.course_id.in_(inst_course_ids))
            )
        else:
            q = q.filter(ParadeSubmission.approving_officer_id == officer_id)

        results = q.order_by(ParadeSubmission.submitted_at.desc()).all()
        return [self._enrich_submission(db, sub) for sub in results]

    def submit(self, db: Session, submission_id: str, submitter_id: str,
               officer_id: Optional[str] = None, remarks: Optional[str] = None) -> Optional[ParadeSubmission]:
        from app.repositories.academic import batch_repo
        sub = db.query(ParadeSubmission).filter(ParadeSubmission.id == submission_id).first()
        if not sub:
            return None
        
        # Auto-resolve assigned instructor from Course/Batch if not passed
        if not officer_id:
            assigned_inst = batch_repo.get_instructor_for_batch(
                db, trade=sub.trade, course_id=sub.course_id, batch_name=sub.batch
            )
            if assigned_inst:
                officer_id = assigned_inst.id

        sub.status = 'SUBMITTED'
        sub.submitted_by = submitter_id
        sub.approving_officer_id = officer_id
        sub.submitter_remarks = remarks
        sub.submitted_at = datetime.utcnow()
        # Reset previous rejection reason on clean resubmission
        sub.rejection_reason = None
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)

    def approve(self, db: Session, submission_id: str, officer_id: str,
                remarks: Optional[str] = None) -> Optional[ParadeSubmission]:
        sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.id == submission_id,
            ParadeSubmission.status == 'SUBMITTED'
        ).first()
        if not sub:
            return None
        sub.status = 'APPROVED'
        sub.approving_officer_id = officer_id # Preserve exact approver
        sub.approver_remarks = remarks
        sub.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)

    def reject(self, db: Session, submission_id: str, officer_id: str,
               rejection_reason: str, remarks: Optional[str] = None) -> Optional[ParadeSubmission]:
        sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.id == submission_id,
            ParadeSubmission.status == 'SUBMITTED'
        ).first()
        if not sub:
            return None
        sub.status = 'REJECTED'
        sub.rejection_reason = rejection_reason
        sub.approver_remarks = remarks or sub.approver_remarks
        sub.returned_by = officer_id
        sub.returned_at = datetime.utcnow()
        sub.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)

    # ─────────────────────────────────────────────────────────────
    # Submission Monitoring & Outstanding Computations
    # ─────────────────────────────────────────────────────────────

    def get_monitoring_data(
        self,
        db: Session,
        target_date: date,
        trade_filter: Optional[str] = None,
        course_id_filter: Optional[str] = None,
        batch_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        current_user_id: Optional[str] = None,
        only_outstanding: bool = False,
        only_pending: bool = False
    ) -> dict:
        """
        Dynamically determine submission status for all required trade/course/batch units.
        Returns detailed items list and summary KPI metrics.
        """
        today = date.today()
        is_past_date = target_date < today

        # 1. Identify all required Trade units from active students and courses
        # Query distinct (trade, course_id, batch) for active students
        student_units = db.query(
            Student.trade,
            Student.course_id,
            Student.batch,
            func.count(Student.id).label('trainee_count')
        ).filter(
            Student.deleted_at == None,
            Student.status != 'Passed Out'
        ).group_by(
            Student.trade,
            Student.course_id,
            Student.batch
        ).all()

        # Build trade unit dictionary: trade -> info
        # Also ensure every active trade registered in DB is accounted for
        active_trades = db.query(Trade).filter(Trade.is_active == True).all()
        required_units_map = {}

        # First add active trades as baseline units
        for t in active_trades:
            trade_label = t.label or t.code
            # Count active trainees in this trade
            cnt = db.query(Student).filter(
                Student.deleted_at == None,
                Student.status != 'Passed Out',
                Student.trade == trade_label
            ).count()
            if cnt > 0:  # Only require parade state for trades with active trainees
                # Find predominant course/batch if available
                matching_unit = next((u for u in student_units if u.trade == trade_label), None)
                required_units_map[trade_label] = {
                    "trade": trade_label,
                    "course_id": matching_unit.course_id if matching_unit else None,
                    "batch": matching_unit.batch if matching_unit else "N/A",
                    "trainee_count": cnt
                }

        # Also ensure any trade present in student_units is included
        for u in student_units:
            if u.trade and u.trade not in required_units_map and u.trainee_count > 0:
                required_units_map[u.trade] = {
                    "trade": u.trade,
                    "course_id": u.course_id,
                    "batch": u.batch or "N/A",
                    "trainee_count": u.trainee_count
                }

        # 2. Query all existing parade submissions for this date
        submissions = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == target_date
        ).all()
        sub_by_trade = {s.trade: s for s in submissions}

        # 3. Query course lookup
        courses = {c.id: c for c in db.query(Course).all()}

        # 4. Query user lookup for submitters/approvers
        user_cache = {}
        def get_user_info(uid):
            if not uid:
                return None, None
            if uid not in user_cache:
                u = db.query(User).filter(User.id == uid).first()
                if u:
                    user_cache[uid] = (f"{u.rank or ''} {u.full_name}".strip(), u.rank)
                else:
                    user_cache[uid] = ("Unknown", None)
            return user_cache[uid]

        # 5. Build raw monitoring items list
        items = []
        s_no = 1

        for trade_name, unit in sorted(required_units_map.items()):
            sub = sub_by_trade.get(trade_name)
            course_obj = courses.get(unit["course_id"]) if unit["course_id"] else None

            # Derive statuses dynamically
            if not sub:
                sub_status = "NOT_SUBMITTED"
                appr_status = "-"
                status_label = "NOT SUBMITTED"
                status_code = "NOT_SUBMITTED"
                sub_id = None
                sub_by = None
                sub_by_name = None
                sub_by_rank = None
                sub_at = None
                appr_officer_id = None
                appr_officer_name = None
                appr_officer_rank = None
                rev_at = None
                rej_reason = None
                appr_rem = None
                sub_rem = None
            elif sub.status == 'DRAFT':
                sub_status = "DRAFT"
                appr_status = "-"
                status_label = "NOT SUBMITTED"
                status_code = "NOT_SUBMITTED"
                sub_id = sub.id
                sub_by = sub.submitted_by
                sub_by_name, sub_by_rank = get_user_info(sub.submitted_by)
                sub_at = sub.submitted_at
                appr_officer_id = sub.approving_officer_id
                appr_officer_name, appr_officer_rank = get_user_info(sub.approving_officer_id)
                rev_at = sub.reviewed_at
                rej_reason = sub.rejection_reason
                appr_rem = sub.approver_remarks
                sub_rem = sub.submitter_remarks
            elif sub.status == 'SUBMITTED':
                sub_status = "SUBMITTED"
                appr_status = "PENDING APPROVAL"
                status_label = "PENDING APPROVAL"
                status_code = "PENDING_APPROVAL"
                sub_id = sub.id
                sub_by = sub.submitted_by
                sub_by_name, sub_by_rank = get_user_info(sub.submitted_by)
                sub_at = sub.submitted_at
                appr_officer_id = sub.approving_officer_id
                appr_officer_name, appr_officer_rank = get_user_info(sub.approving_officer_id)
                rev_at = sub.reviewed_at
                rej_reason = sub.rejection_reason
                appr_rem = sub.approver_remarks
                sub_rem = sub.submitter_remarks
            elif sub.status == 'APPROVED':
                sub_status = "APPROVED"
                appr_status = "APPROVED"
                status_label = "APPROVED"
                status_code = "APPROVED"
                sub_id = sub.id
                sub_by = sub.submitted_by
                sub_by_name, sub_by_rank = get_user_info(sub.submitted_by)
                sub_at = sub.submitted_at
                appr_officer_id = sub.approving_officer_id
                appr_officer_name, appr_officer_rank = get_user_info(sub.approving_officer_id)
                rev_at = sub.reviewed_at
                rej_reason = sub.rejection_reason
                appr_rem = sub.approver_remarks
                sub_rem = sub.submitter_remarks
            elif sub.status == 'REJECTED':
                sub_status = "RETURNED"
                appr_status = "RETURNED FOR CORRECTION"
                status_label = "RETURNED FOR CORRECTION"
                status_code = "RETURNED"
                sub_id = sub.id
                sub_by = sub.submitted_by
                sub_by_name, sub_by_rank = get_user_info(sub.submitted_by)
                sub_at = sub.submitted_at
                appr_officer_id = sub.approving_officer_id
                appr_officer_name, appr_officer_rank = get_user_info(sub.approving_officer_id)
                rev_at = sub.reviewed_at
                rej_reason = sub.rejection_reason
                appr_rem = sub.approver_remarks
                sub_rem = sub.submitter_remarks
            else:
                sub_status = "NOT_SUBMITTED"
                appr_status = "-"
                status_label = "NOT SUBMITTED"
                status_code = "NOT_SUBMITTED"
                sub_id = None
                sub_by = None
                sub_by_name = None
                sub_by_rank = None
                sub_at = None
                appr_officer_id = None
                appr_officer_name = None
                appr_officer_rank = None
                rev_at = None
                rej_reason = None
                appr_rem = None
                sub_rem = None

            # Resolve assigned instructor from Academic Batch
            from app.repositories.academic import batch_repo
            assigned_inst = batch_repo.get_instructor_for_batch(
                db, trade=trade_name, course_id=unit["course_id"], batch_name=unit["batch"]
            )
            if assigned_inst:
                inst_id = assigned_inst.id
                inst_name = f"{assigned_inst.rank or ''} {assigned_inst.full_name}".strip()
                inst_rank = assigned_inst.rank
                inst_svc = assigned_inst.service_number
                inst_status = "ASSIGNED"
            else:
                inst_id = None
                inst_name = "INSTRUCTOR NOT ASSIGNED"
                inst_rank = None
                inst_svc = None
                inst_status = "NOT_ASSIGNED"

            is_overdue = is_past_date and (status_code in ["NOT_SUBMITTED", "RETURNED"])

            item = {
                "s_no": s_no,
                "trade": trade_name,
                "course_id": unit["course_id"],
                "course_code": course_obj.code if course_obj else None,
                "course_name": course_obj.name if course_obj else None,
                "batch": unit["batch"],
                "total_trainees": unit["trainee_count"],
                "submission_status": sub_status,
                "approval_status": appr_status,
                "status_label": status_label,
                "status_code": status_code,
                "submission_id": sub_id,
                "submitted_by": sub_by,
                "submitted_by_name": sub_by_name,
                "submitted_by_rank": sub_by_rank,
                "submitted_at": sub_at,
                "approving_officer_id": appr_officer_id,
                "approving_officer_name": appr_officer_name,
                "approving_officer_rank": appr_officer_rank,
                "assigned_instructor_id": inst_id,
                "assigned_instructor_name": inst_name,
                "assigned_instructor_rank": inst_rank,
                "assigned_instructor_service_number": inst_svc,
                "instructor_status": inst_status,
                "reviewed_at": rev_at,
                "rejection_reason": rej_reason,
                "approver_remarks": appr_rem,
                "submitter_remarks": sub_rem,
                "is_overdue": is_overdue,
                "deadline": "08:00 hrs",
                "can_submit": status_code in ["NOT_SUBMITTED", "RETURNED"],
                "can_approve": status_code == "PENDING_APPROVAL"
            }
            items.append(item)
            s_no += 1

        # 6. Compute summary KPIs across all required units
        total_req = len(items)
        not_sub = sum(1 for i in items if i["status_code"] == "NOT_SUBMITTED")
        pending = sum(1 for i in items if i["status_code"] == "PENDING_APPROVAL")
        appr = sum(1 for i in items if i["status_code"] == "APPROVED")
        ret = sum(1 for i in items if i["status_code"] == "RETURNED")
        overdue_cnt = sum(1 for i in items if i["is_overdue"])

        summary = {
            "date": target_date,
            "total_required": total_req,
            "not_submitted": not_sub,
            "pending_approval": pending,
            "approved": appr,
            "returned": ret,
            "overdue": overdue_cnt
        }

        # 7. Apply filters to the item list (summary remains based on total required scope)
        filtered_items = items
        if trade_filter and trade_filter != 'All':
            filtered_items = [i for i in filtered_items if i["trade"].lower() == trade_filter.lower()]
        if course_id_filter:
            filtered_items = [i for i in filtered_items if i["course_id"] == course_id_filter]
        if batch_filter and batch_filter != 'All':
            filtered_items = [i for i in filtered_items if i["batch"] == batch_filter]
        if status_filter and status_filter != 'All':
            filtered_items = [i for i in filtered_items if i["status_code"] == status_filter.upper()]
        if only_outstanding:
            filtered_items = [i for i in filtered_items if i["status_code"] in ["NOT_SUBMITTED", "RETURNED"]]
        if only_pending:
            filtered_items = [i for i in filtered_items if i["status_code"] == "PENDING_APPROVAL"]

        # Re-number S/No after filtering
        for idx, item in enumerate(filtered_items, 1):
            item["s_no"] = idx

        return {
            "date": target_date,
            "operational_date": today,
            "summary": summary,
            "items": filtered_items
        }

    def get_date_range_monitoring(
        self,
        db: Session,
        start_date: date,
        end_date: date,
        trade_filter: Optional[str] = None
    ) -> dict:
        """
        Analyze parade state submission compliance across a date range.
        """
        today = date.today()
        # Query distinct required trades
        active_trades = db.query(Trade).filter(Trade.is_active == True).all()
        trade_names = [t.label or t.code for t in active_trades]
        if trade_filter and trade_filter != 'All':
            trade_names = [t for t in trade_names if t.lower() == trade_filter.lower()]

        # Query submissions in date range
        submissions = db.query(ParadeSubmission).filter(
            ParadeSubmission.date >= start_date,
            ParadeSubmission.date <= end_date
        ).all()

        sub_map = {(s.date, s.trade): s for s in submissions}

        # Build daily records
        items = []
        cur_date = start_date
        while cur_date <= end_date:
            for t_name in trade_names:
                sub = sub_map.get((cur_date, t_name))
                if not sub or sub.status == 'DRAFT':
                    status_label = "NOT SUBMITTED"
                    status_code = "NOT_SUBMITTED"
                    sub_id = sub.id if sub else None
                    sub_by = None
                    appr_by = None
                elif sub.status == 'SUBMITTED':
                    status_label = "PENDING APPROVAL"
                    status_code = "PENDING_APPROVAL"
                    sub_id = sub.id
                    sub_by = sub.submitted_by
                    appr_by = sub.approving_officer_id
                elif sub.status == 'APPROVED':
                    status_label = "APPROVED"
                    status_code = "APPROVED"
                    sub_id = sub.id
                    sub_by = sub.submitted_by
                    appr_by = sub.approving_officer_id
                elif sub.status == 'REJECTED':
                    status_label = "RETURNED"
                    status_code = "RETURNED"
                    sub_id = sub.id
                    sub_by = sub.submitted_by
                    appr_by = sub.approving_officer_id
                else:
                    status_label = "NOT SUBMITTED"
                    status_code = "NOT_SUBMITTED"
                    sub_id = None
                    sub_by = None
                    appr_by = None

                is_overdue = cur_date < today and (status_code in ["NOT_SUBMITTED", "RETURNED"])

                items.append({
                    "date": cur_date,
                    "trade": t_name,
                    "course_name": None,
                    "batch": None,
                    "total_trainees": 0,
                    "status_label": status_label,
                    "status_code": status_code,
                    "submission_id": sub_id,
                    "submitted_by_name": sub_by,
                    "approving_officer_name": appr_by,
                    "is_overdue": is_overdue
                })
            cur_date += timedelta(days=1)

        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_entries": len(items),
            "items": items,
            "trades": trade_names
        }


class OfficerInChargeRepository:
    # ─────────────────────────────────────────────
    # Officer I/C Appointments
    # ─────────────────────────────────────────────

    def _enrich(self, db: Session, oic: OfficerInCharge) -> OfficerInCharge:
        officer = db.query(User).filter(User.id == oic.user_id).first()
        if officer:
            oic.officer_name = f"{officer.rank or ''} {officer.full_name}".strip()
            oic.officer_rank = officer.rank
            oic.officer_service_number = officer.service_number
        appointed_by = db.query(User).filter(User.id == oic.appointed_by).first()
        if appointed_by:
            oic.appointed_by_name = appointed_by.full_name
        return oic

    def get_all(self, db: Session) -> List[OfficerInCharge]:
        results = db.query(OfficerInCharge).filter(OfficerInCharge.is_active == True).all()
        return [self._enrich(db, o) for o in results]

    def get_by_trade(self, db: Session, trade: str) -> List[OfficerInCharge]:
        results = db.query(OfficerInCharge).filter(
            OfficerInCharge.trade == trade,
            OfficerInCharge.is_active == True
        ).all()
        return [self._enrich(db, o) for o in results]

    def assign(self, db: Session, trade: str, user_id: str, appointed_by_id: str) -> OfficerInCharge:
        oic = OfficerInCharge(
            trade=trade,
            user_id=user_id,
            appointed_by=appointed_by_id,
            is_active=True,
            appointed_at=datetime.utcnow()
        )
        db.add(oic)
        db.commit()
        db.refresh(oic)
        return self._enrich(db, oic)

    def remove(self, db: Session, oic_id: str) -> bool:
        oic = db.query(OfficerInCharge).filter(OfficerInCharge.id == oic_id).first()
        if not oic:
            return False
        oic.is_active = False
        db.commit()
        return True


parade_repo = ParadeStateRepository()
submission_repo = ParadeSubmissionRepository()
officer_repo = OfficerInChargeRepository()
