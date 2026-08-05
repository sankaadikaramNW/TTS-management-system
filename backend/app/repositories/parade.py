from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student import Student, ParadeState, ParadeSubmission, OfficerInCharge
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

    def get_summary(self, db: Session, parade_date: date) -> dict:
        total_enrolled = db.query(Student).filter(
            Student.deleted_at == None, Student.status != "Passed Out"
        ).count()
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

        unrecorded_count = total_enrolled - len(logged_student_ids)
        if unrecorded_count > 0:
            summary["present"] += unrecorded_count

        return summary


class ParadeSubmissionRepository:
    # ─────────────────────────────────────────────
    # Parade Submissions (Approval Workflow)
    # ─────────────────────────────────────────────

    def _enrich_submission(self, db: Session, sub: ParadeSubmission) -> ParadeSubmission:
        """Attach display-friendly fields from related User objects."""
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

        # Calculate strength counts from linked parade states
        states = db.query(ParadeState).filter(ParadeState.submission_id == sub.id).all()
        sub.total_strength = len(states)
        sub.present_count = sum(1 for s in states if s.status == "Present")
        sub.absent_count = sub.total_strength - sub.present_count

        return sub

    def get_or_create_draft(self, db: Session, parade_date: date, trade: str,
                            submitter_id: str, officer_id: str) -> ParadeSubmission:
        """Get existing DRAFT/REJECTED submission or create a new one."""
        existing = db.query(ParadeSubmission).filter(
            ParadeSubmission.date == parade_date,
            ParadeSubmission.trade == trade,
            ParadeSubmission.status.in_(['DRAFT', 'REJECTED'])
        ).first()

        if existing:
            # Update the officer selection if it changed
            existing.submitted_by = submitter_id
            existing.approving_officer_id = officer_id
            db.commit()
            db.refresh(existing)
            return existing

        sub = ParadeSubmission(
            date=parade_date,
            trade=trade,
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
        results = db.query(ParadeSubmission).filter(
            ParadeSubmission.approving_officer_id == officer_id,
            ParadeSubmission.status == 'SUBMITTED'
        ).order_by(ParadeSubmission.submitted_at.desc()).all()
        return [self._enrich_submission(db, sub) for sub in results]

    def submit(self, db: Session, submission_id: str, submitter_id: str,
               officer_id: str, remarks: Optional[str] = None) -> ParadeSubmission:
        sub = db.query(ParadeSubmission).filter(ParadeSubmission.id == submission_id).first()
        if not sub:
            return None
        sub.status = 'SUBMITTED'
        sub.submitted_by = submitter_id
        sub.approving_officer_id = officer_id
        sub.submitter_remarks = remarks
        sub.submitted_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)

    def approve(self, db: Session, submission_id: str, officer_id: str,
                remarks: Optional[str] = None) -> Optional[ParadeSubmission]:
        sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.id == submission_id,
            ParadeSubmission.approving_officer_id == officer_id,
            ParadeSubmission.status == 'SUBMITTED'
        ).first()
        if not sub:
            return None
        sub.status = 'APPROVED'
        sub.approver_remarks = remarks
        sub.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)

    def reject(self, db: Session, submission_id: str, officer_id: str,
               rejection_reason: str) -> Optional[ParadeSubmission]:
        sub = db.query(ParadeSubmission).filter(
            ParadeSubmission.id == submission_id,
            ParadeSubmission.approving_officer_id == officer_id,
            ParadeSubmission.status == 'SUBMITTED'
        ).first()
        if not sub:
            return None
        sub.status = 'REJECTED'
        sub.rejection_reason = rejection_reason
        sub.reviewed_at = datetime.utcnow()
        db.commit()
        db.refresh(sub)
        return self._enrich_submission(db, sub)


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
