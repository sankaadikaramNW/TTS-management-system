from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.accommodation import AccommodationBed, AccommodationAllocation
from app.repositories.accommodation import bed_repo, allocation_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.accommodation import AllocationRequest

class AccommodationService:
    def allocate_bed(self, db: Session, request: AllocationRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        student = student_repo.get(db, request.student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Student not found")

        bed = bed_repo.get(db, request.bed_id)
        if not bed or bed.deleted_at:
            raise HTTPException(status_code=404, detail="Bed not found")

        if bed.status != "Vacant":
            raise HTTPException(status_code=400, detail="Requested bed is not vacant")

        # Check if student is already allocated elsewhere
        active_alloc = allocation_repo.get_active_by_student(db, request.student_id)
        if active_alloc:
            # Auto vacate from old bed
            self.vacate_bed(db, active_alloc.id, user_id, ip, ua)

        # Allocate new bed
        bed.status = "Occupied"
        new_alloc = AccommodationAllocation(
            student_id=request.student_id,
            bed_id=request.bed_id,
            allocated_at=datetime.utcnow(),
            status="Active"
        )
        allocation_repo.create(db, obj_in=new_alloc)
        db.commit()

        audit_repo.create_log(
            db, user_id, "BED_ALLOCATED", ip, ua,
            f"Allocated bed {bed.bed_number} to student {student.service_number}"
        )
        return new_alloc

    def vacate_bed(self, db: Session, allocation_id: str, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        alloc = db.query(AccommodationAllocation).filter(AccommodationAllocation.id == allocation_id).first()
        if not alloc or alloc.status == "History":
            raise HTTPException(status_code=404, detail="Active allocation record not found")

        bed = bed_repo.get(db, alloc.bed_id)
        if bed:
            bed.status = "Vacant"

        alloc.vacated_at = datetime.utcnow()
        alloc.status = "History"
        db.commit()

        student = student_repo.get(db, alloc.student_id)
        service_no = student.service_number if student else "unknown"

        audit_repo.create_log(
            db, user_id, "BED_VACATED", ip, ua,
            f"Vacated bed ID {alloc.bed_id} previously held by student {service_no}"
        )
        return alloc

accommodation_service = AccommodationService()
