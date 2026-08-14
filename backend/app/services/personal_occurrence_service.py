from datetime import datetime, date
from typing import Optional, List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student, PersonalOccurrence
from app.repositories.student import personal_occurrence_repo, student_repo
from app.repositories.user import audit_repo
from app.schemas.student import PersonalOccurrenceCreate, PersonalOccurrenceUpdate

class PersonalOccurrenceService:
    def create_occurrence(
        self,
        db: Session,
        payload: PersonalOccurrenceCreate,
        user_id: str,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> PersonalOccurrence:
        """Create a new personal occurrence record for a trainee."""
        # 1. Validate Trainee Existence
        trainee = student_repo.get(db, payload.trainee_id)
        if not trainee or trainee.deleted_at:
            raise HTTPException(status_code=404, detail="Trainee record not found.")

        # 2. Validate Occurrence Type
        occ_type = payload.occurrence_type.upper().strip()
        if occ_type not in ['ACHIEVEMENT', 'MISCONDUCT_OFFENSE']:
            raise HTTPException(
                status_code=400,
                detail="Invalid occurrence type. Allowed values are 'ACHIEVEMENT' or 'MISCONDUCT_OFFENSE'."
            )

        try:
            occurrence = PersonalOccurrence(
                trainee_id=payload.trainee_id,
                occurrence_type=occ_type,
                occurrence_date=payload.occurrence_date,
                title=payload.title.strip(),
                description=payload.description.strip(),
                remarks=payload.remarks.strip() if payload.remarks else None,
                status='Active',
                created_by=user_id
            )
            db.add(occurrence)
            db.commit()
            db.refresh(occurrence)

            # Audit Log
            audit_repo.create_log(
                db=db,
                user_id=user_id,
                action="CREATE_PERSONAL_OCCURRENCE",
                module="Student Management",
                details=f"Recorded {occ_type} '{occurrence.title}' on {occurrence.occurrence_date.strftime('%d.%m.%Y')} for trainee {trainee.service_number} ({trainee.full_name})",
                ip_address=ip,
                user_agent=ua
            )

            return personal_occurrence_repo._enrich(db, occurrence)
        except Exception:
            db.rollback()
            raise

    def update_occurrence(
        self,
        db: Session,
        occurrence_id: str,
        payload: PersonalOccurrenceUpdate,
        user_id: str,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> PersonalOccurrence:
        """Update an existing personal occurrence record."""
        occurrence = personal_occurrence_repo.get_by_id(db, occurrence_id)
        if not occurrence:
            raise HTTPException(status_code=404, detail="Personal occurrence record not found.")

        trainee = student_repo.get(db, occurrence.trainee_id)

        old_type = occurrence.occurrence_type
        old_title = occurrence.title

        if payload.occurrence_type:
            occ_type = payload.occurrence_type.upper().strip()
            if occ_type not in ['ACHIEVEMENT', 'MISCONDUCT_OFFENSE']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid occurrence type. Allowed values are 'ACHIEVEMENT' or 'MISCONDUCT_OFFENSE'."
                )
            occurrence.occurrence_type = occ_type

        if payload.occurrence_date:
            occurrence.occurrence_date = payload.occurrence_date

        if payload.title is not None and payload.title.strip():
            occurrence.title = payload.title.strip()

        if payload.description is not None and payload.description.strip():
            occurrence.description = payload.description.strip()

        if payload.remarks is not None:
            occurrence.remarks = payload.remarks.strip() if payload.remarks.strip() else None

        if payload.status is not None:
            occurrence.status = payload.status

        occurrence.updated_by = user_id

        try:
            db.commit()
            db.refresh(occurrence)

            # Audit Log
            trainee_sn = trainee.service_number if trainee else "N/A"
            audit_repo.create_log(
                db=db,
                user_id=user_id,
                action="UPDATE_PERSONAL_OCCURRENCE",
                module="Student Management",
                details=f"Updated occurrence ID {occurrence_id} for trainee {trainee_sn}. Previous: [{old_type} - {old_title}] -> New: [{occurrence.occurrence_type} - {occurrence.title}]",
                ip_address=ip,
                user_agent=ua
            )

            return personal_occurrence_repo._enrich(db, occurrence)
        except Exception:
            db.rollback()
            raise

    def delete_occurrence(
        self,
        db: Session,
        occurrence_id: str,
        user_id: str,
        ip: Optional[str] = None,
        ua: Optional[str] = None
    ) -> bool:
        """Soft-delete a personal occurrence record."""
        occurrence = personal_occurrence_repo.get_by_id(db, occurrence_id)
        if not occurrence:
            raise HTTPException(status_code=404, detail="Personal occurrence record not found.")

        trainee = student_repo.get(db, occurrence.trainee_id)
        trainee_sn = trainee.service_number if trainee else "N/A"

        try:
            occurrence.deleted_at = datetime.utcnow()
            occurrence.status = 'Archived'
            occurrence.updated_by = user_id
            db.commit()

            # Audit Log
            audit_repo.create_log(
                db=db,
                user_id=user_id,
                action="DELETE_PERSONAL_OCCURRENCE",
                module="Student Management",
                details=f"Soft-deleted {occurrence.occurrence_type} record '{occurrence.title}' (ID {occurrence_id}) for trainee {trainee_sn}",
                ip_address=ip,
                user_agent=ua
            )

            return True
        except Exception:
            db.rollback()
            raise

personal_occurrence_service = PersonalOccurrenceService()
