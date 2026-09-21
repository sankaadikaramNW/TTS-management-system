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

    def get_by_student_and_date(self, db: Session, student_id: str, parade_date: date, parade_type: str = 'MORNING') -> Optional[ParadeState]:
        q = db.query(ParadeState).filter(
            ParadeState.student_id == student_id,
            ParadeState.date == parade_date
        )
        if parade_type == 'MORNING':
            q = q.filter(or_(ParadeState.parade_type == 'MORNING', ParadeState.parade_type == None))
        else:
            q = q.filter(ParadeState.parade_type == parade_type)
        return q.first()

    def get_parade_states_by_date(self, db: Session, parade_date: date, parade_type: str = 'MORNING') -> List[ParadeState]:
        q = db.query(ParadeState).filter(ParadeState.date == parade_date)
        if parade_type == 'MORNING':
            q = q.filter(or_(ParadeState.parade_type == 'MORNING', ParadeState.parade_type == None))
        else:
            q = q.filter(ParadeState.parade_type == parade_type)
        results = q.all()
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
                         submission_id: Optional[str] = None,
                         parade_type: str = 'MORNING',
                         morning_status: Optional[str] = None,
                         status_changed: bool = False) -> ParadeState:
        db_obj = self.get_by_student_and_date(db, student_id, parade_date, parade_type=parade_type)
        if db_obj:
            db_obj.status = status
            db_obj.remarks = remarks
            db_obj.updated_by = user_id
            db_obj.parade_type = parade_type
            if morning_status is not None:
                db_obj.morning_status = morning_status
            db_obj.status_changed = status_changed
            if submission_id:
                db_obj.submission_id = submission_id
        else:
            db_obj = ParadeState(
                student_id=student_id,
                date=parade_date,
                parade_type=parade_type,
                status=status,
                morning_status=morning_status,
                status_changed=status_changed,
                remarks=remarks,
                updated_by=user_id,
                submission_id=submission_id
            )
            db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_night_parade_context(self, db: Session, parade_date: date, trade: str,
                                 course_id: Optional[str] = None,
                                 batch: Optional[str] = None) -> dict:
        """
        Retrieves morning baseline and night working roll-call states for a trade/group on a date.
        If no morning parade state exists, morning_available is returned as False.
        """
        from app.repositories.academic import batch_repo

        # 1. Fetch active students in target trade/group
        sq = db.query(Student).filter(
            Student.deleted_at == None,
            Student.status != 'Passed Out'
        )
        if trade and trade != 'All':
            sq = sq.filter(Student.trade == trade)
        if course_id:
            sq = sq.filter(Student.course_id == course_id)
        if batch and batch != 'All':
            sq = sq.filter(Student.batch == batch)

        students = sq.order_by(Student.service_number.asc()).all()
        student_ids = [s.id for s in students]

        # 2. Check Morning Parade records for these students
        morning_states = db.query(ParadeState).filter(
            ParadeState.date == parade_date,
            ParadeState.student_id.in_(student_ids),
            or_(ParadeState.parade_type == 'MORNING', ParadeState.parade_type == None)
        ).all() if student_ids else []

        morning_state_map = {m.student_id: m for m in morning_states}

        # Check Morning Parade Submission
        morning_sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == parade_date,
            ParadeSubmission.trade == trade,
            or_(ParadeSubmission.parade_type == 'MORNING', ParadeSubmission.parade_type == None)
        ).first() if trade and trade != 'All' else None

        morning_available = len(morning_states) > 0

        # Course name resolution
        course_name = None
        if course_id:
            c = db.query(Course).filter(Course.id == course_id).first()
            if c:
                course_name = c.name

        # 3. Check Night Parade Submission
        night_sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == parade_date,
            ParadeSubmission.trade == trade,
            ParadeSubmission.parade_type == 'NIGHT'
        ).first() if trade and trade != 'All' else None

        # 4. Check Night Parade records
        night_states = db.query(ParadeState).filter(
            ParadeState.date == parade_date,
            ParadeState.student_id.in_(student_ids),
            ParadeState.parade_type == 'NIGHT'
        ).all() if student_ids else []
        night_state_map = {n.student_id: n for n in night_states}

        # Resolve assigned instructor
        assigned_inst = batch_repo.get_instructor_for_batch(
            db, trade=trade, course_id=course_id, batch_name=batch
        )

        trainees = []
        if morning_available:
            for s in students:
                m_state = morning_state_map.get(s.id)
                m_status = m_state.status if m_state else "Present"
                n_state = night_state_map.get(s.id)

                if n_state:
                    n_status = n_state.status
                    rem = n_state.remarks or ""
                    changed = (n_status != m_status)
                    is_ver = True
                else:
                    n_status = m_status
                    rem = ""
                    changed = False
                    is_ver = False

                c_name = course_name or (s.course.name if s.course else "N/A")

                trainees.append({
                    "student_id": s.id,
                    "service_number": s.service_number,
                    "rank": s.rank or "AC",
                    "full_name": s.full_name,
                    "trade": s.trade or "N/A",
                    "course_id": s.course_id,
                    "course_name": c_name,
                    "batch": s.batch or "N/A",
                    "medical_category": s.medical_category or "A4G4",
                    "morning_status": m_status,
                    "night_status": n_status,
                    "status_changed": changed,
                    "remarks": rem,
                    "is_verified": is_ver
                })

        # Dynamic Strength & Accountability Calculation
        expected_strength = len(students)
        VALID_STATUSES = {
            "Present", "Hospital", "Sick Report", "Leave",
            "AWOL", "Temporary Duty", "Course Visit", "Detached Duty"
        }
        accounted_strength = sum(1 for t in trainees if t["is_verified"] and t["night_status"] in VALID_STATUSES)
        unverified_count = max(0, expected_strength - accounted_strength)
        is_accountability_complete = (expected_strength > 0 and unverified_count == 0)

        can_complete = (night_sub.status != 'COMPLETED') if night_sub else True

        completed_user = None
        if night_sub and night_sub.status == 'COMPLETED':
            c_uid = night_sub.submitted_by
            if c_uid:
                completed_user = db.query(User).filter(User.id == c_uid).first()
        completed_by_name = f"{completed_user.rank or ''} {completed_user.full_name}".strip() if completed_user else None

        appr_id = night_sub.approving_officer_id if night_sub else (assigned_inst.id if assigned_inst else None)
        appr_user = db.query(User).filter(User.id == appr_id).first() if appr_id else None
        appr_name = f"{appr_user.rank or ''} {appr_user.full_name}".strip() if appr_user else (
            f"{assigned_inst.rank or ''} {assigned_inst.full_name}".strip() if assigned_inst else None
        )
        appr_rank = appr_user.rank if appr_user else (assigned_inst.rank if assigned_inst else None)

        return {
            "date": parade_date,
            "trade": trade or "All",
            "course_id": course_id,
            "course_name": course_name,
            "batch": batch,
            "morning_available": morning_available,
            "morning_submission_status": morning_sub.status if morning_sub else ("RECORDED" if morning_available else "NOT_AVAILABLE"),
            "morning_submission_id": morning_sub.id if morning_sub else None,
            "night_submission_id": night_sub.id if night_sub else None,
            "night_submission_status": night_sub.status if night_sub else "DRAFT",
            "submitter_remarks": night_sub.submitter_remarks if night_sub else None,
            "completed_by_name": completed_by_name,
            "completed_at": night_sub.reviewed_at or night_sub.submitted_at if night_sub else None,
            "is_accountability_complete": is_accountability_complete,
            "expected_strength": expected_strength,
            "accounted_strength": accounted_strength,
            "unverified_count": unverified_count,
            "can_complete": can_complete,
            "can_submit": can_complete,
            "can_approve": False,
            "approving_officer_id": appr_id,
            "approving_officer_name": appr_name,
            "approving_officer_rank": appr_rank,
            "assigned_instructor_id": assigned_inst.id if assigned_inst else None,
            "assigned_instructor_name": f"{assigned_inst.rank or ''} {assigned_inst.full_name}".strip() if assigned_inst else None,
            "assigned_instructor_rank": assigned_inst.rank if assigned_inst else None,
            "instructor_status": "ASSIGNED" if assigned_inst else "NOT_ASSIGNED",
            "approver_remarks": night_sub.approver_remarks if night_sub else None,
            "rejection_reason": night_sub.rejection_reason if night_sub else None,
            "trainees": trainees
        }

    def get_night_summary_and_breakdowns(self, db: Session, parade_date: date,
                                         trade: Optional[str] = None,
                                         course_id: Optional[str] = None,
                                         batch: Optional[str] = None) -> dict:
        """
        Calculates overall strength, trade-wise strength, category-wise strength,
        and morning-to-night status transitions for Night Parade.
        """
        sq = db.query(Student).filter(
            Student.deleted_at == None,
            Student.status != 'Passed Out'
        )
        if trade and trade != 'All':
            sq = sq.filter(Student.trade == trade)
        if course_id:
            sq = sq.filter(Student.course_id == course_id)
        if batch and batch != 'All':
            sq = sq.filter(Student.batch == batch)
        students = sq.all()
        student_ids = [s.id for s in students]

        m_states = db.query(ParadeState).filter(
            ParadeState.date == parade_date,
            ParadeState.student_id.in_(student_ids),
            or_(ParadeState.parade_type == 'MORNING', ParadeState.parade_type == None)
        ).all() if student_ids else []
        m_map = {m.student_id: m.status for m in m_states}

        n_states = db.query(ParadeState).filter(
            ParadeState.date == parade_date,
            ParadeState.student_id.in_(student_ids),
            ParadeState.parade_type == 'NIGHT'
        ).all() if student_ids else []
        n_map = {n.student_id: n for n in n_states}

        status_keys = {
            "Present": "present",
            "Sick Report": "sick_report",
            "Hospital": "hospital",
            "Leave": "leave",
            "Temporary Duty": "temp_duty",
            "Course Visit": "course_visit",
            "Detached Duty": "detached_duty",
            "AWOL": "awol"
        }

        total_expected = len(students)
        counts = {
            "present": 0, "sick_report": 0, "hospital": 0, "leave": 0,
            "temp_duty": 0, "course_visit": 0, "detached_duty": 0,
            "awol": 0, "other": 0
        }
        changed_count = 0
        unverified_count = 0

        transitions_map = {}
        trade_data = {}
        category_data = {}

        for s in students:
            m_status = m_map.get(s.id, "Present")
            n_state = n_map.get(s.id)
            if n_state:
                n_status = n_state.status
                is_changed = (n_status != m_status)
                is_unver = False
            else:
                n_status = m_status
                is_changed = False
                is_unver = True
                unverified_count += 1

            if is_changed:
                changed_count += 1
                pair = (m_status, n_status)
                transitions_map[pair] = transitions_map.get(pair, 0) + 1

            k = status_keys.get(n_status, "other")
            counts[k] = counts.get(k, 0) + 1

            # Trade aggregation
            t_name = s.trade or "Unassigned"
            if t_name not in trade_data:
                trade_data[t_name] = {
                    "label": t_name, "expected": 0, "present": 0, "sick_report": 0,
                    "hospital": 0, "leave": 0, "awol": 0, "course_visit": 0,
                    "temp_duty": 0, "detached_duty": 0, "other": 0, "changed": 0, "unverified": 0
                }
            trade_data[t_name]["expected"] += 1
            trade_data[t_name][k] = trade_data[t_name].get(k, 0) + 1
            if is_changed:
                trade_data[t_name]["changed"] += 1
            if is_unver:
                trade_data[t_name]["unverified"] += 1

            # Category aggregation (Medical Category)
            cat_name = s.medical_category or "A4G4"
            if cat_name not in category_data:
                category_data[cat_name] = {
                    "label": cat_name, "expected": 0, "present": 0, "sick_report": 0,
                    "hospital": 0, "leave": 0, "awol": 0, "course_visit": 0,
                    "temp_duty": 0, "detached_duty": 0, "other": 0, "changed": 0, "unverified": 0
                }
            category_data[cat_name]["expected"] += 1
            category_data[cat_name][k] = category_data[cat_name].get(k, 0) + 1
            if is_changed:
                category_data[cat_name]["changed"] += 1
            if is_unver:
                category_data[cat_name]["unverified"] += 1

        transitions_list = [
            {"from_status": f, "to_status": t, "count": c}
            for (f, t), c in sorted(transitions_map.items(), key=lambda x: x[1], reverse=True)
        ]

        return {
            "date": parade_date,
            "trade": trade,
            "total_expected": total_expected,
            "present": counts["present"],
            "sick_report": counts["sick_report"],
            "hospital": counts["hospital"],
            "leave": counts["leave"],
            "awol": counts["awol"],
            "course_visit": counts["course_visit"],
            "temp_duty": counts["temp_duty"],
            "detached_duty": counts["detached_duty"],
            "other": counts["other"],
            "status_changed_count": changed_count,
            "unverified_count": unverified_count,
            "trade_wise": list(trade_data.values()),
            "category_wise": list(category_data.values()),
            "transitions": transitions_list
        }

    def get_summary(self, db: Session, parade_date: date, official_approved_only: bool = False, parade_type: str = 'MORNING') -> dict:
        """
        Get strength summary counts for a given date.
        If official_approved_only=True, only counts students from trades with APPROVED submissions.
        """
        total_enrolled = db.query(Student).filter(
            Student.deleted_at == None, Student.status != "Passed Out"
        ).count()
        
        if official_approved_only:
            # Query only approved submissions for this date
            q_sub = db.query(ParadeSubmission.id).filter(
                ParadeSubmission.date == parade_date,
                ParadeSubmission.status == 'APPROVED'
            )
            if parade_type == 'MORNING':
                q_sub = q_sub.filter(or_(ParadeSubmission.parade_type == 'MORNING', ParadeSubmission.parade_type == None))
            else:
                q_sub = q_sub.filter(ParadeSubmission.parade_type == parade_type)
            approved_subs = q_sub.all()
            approved_sub_ids = [s[0] for s in approved_subs]
            if approved_sub_ids:
                states = db.query(ParadeState).filter(
                    ParadeState.date == parade_date,
                    ParadeState.submission_id.in_(approved_sub_ids)
                ).all()
            else:
                states = []
        else:
            q_state = db.query(ParadeState).filter(ParadeState.date == parade_date)
            if parade_type == 'MORNING':
                q_state = q_state.filter(or_(ParadeState.parade_type == 'MORNING', ParadeState.parade_type == None))
            else:
                q_state = q_state.filter(ParadeState.parade_type == parade_type)
            states = q_state.all()

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
                            batch: Optional[str] = None,
                            parade_type: str = 'MORNING') -> ParadeSubmission:
        """Get existing DRAFT/REJECTED submission or create a new one."""
        from app.repositories.academic import batch_repo

        if not officer_id:
            assigned_inst = batch_repo.get_instructor_for_batch(
                db, trade=trade, course_id=course_id, batch_name=batch
            )
            if assigned_inst:
                officer_id = assigned_inst.id

        q = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == parade_date,
            ParadeSubmission.trade == trade,
            ParadeSubmission.status.in_(['DRAFT', 'REJECTED'])
        )
        if parade_type == 'MORNING':
            q = q.filter(or_(ParadeSubmission.parade_type == 'MORNING', ParadeSubmission.parade_type == None))
        else:
            q = q.filter(ParadeSubmission.parade_type == parade_type)

        existing = q.first()

        if existing:
            # Update the officer selection and submitter
            existing.submitted_by = submitter_id
            existing.parade_type = parade_type
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
            parade_type=parade_type,
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
                 parade_type: Optional[str] = None,
                 limit: int = 50) -> List[ParadeSubmission]:
        q = db.query(ParadeSubmission)
        if parade_date:
            q = q.filter(ParadeSubmission.date == parade_date)
        if trade:
            q = q.filter(ParadeSubmission.trade == trade)
        if status:
            q = q.filter(ParadeSubmission.status == status)
        if parade_type:
            if parade_type == 'MORNING':
                q = q.filter(or_(ParadeSubmission.parade_type == 'MORNING', ParadeSubmission.parade_type == None))
            else:
                q = q.filter(ParadeSubmission.parade_type == parade_type)
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
