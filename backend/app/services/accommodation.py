from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBed, AccommodationAllocation
from app.repositories.accommodation import bed_repo, allocation_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.accommodation import AllocationRequest, TransferRequest, VacateRequest

class AccommodationService:
    def allocate_bed(self, db: Session, request: AllocationRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        student = student_repo.get(db, request.student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Trainee not found")

        bed = bed_repo.get(db, request.bed_id)
        if not bed or bed.deleted_at:
            raise HTTPException(status_code=404, detail="Bed record not found")

        if bed.status != "Vacant":
            raise HTTPException(status_code=400, detail="Requested bed is not vacant")

        # Check if trainee is already allocated elsewhere
        active_alloc = allocation_repo.get_active_by_student(db, request.student_id)
        if active_alloc:
            # Auto vacate from old bed
            self._vacate_alloc_internal(db, active_alloc, "Transfer", "System auto-vacated for transfer", user_id)

        # Allocate new bed
        bed.status = "Occupied"
        new_alloc = AccommodationAllocation(
            student_id=request.student_id,
            bed_id=request.bed_id,
            allocated_at=datetime.utcnow(),
            allocated_by=user_id,
            remarks=request.remarks,
            status="Active"
        )
        allocation_repo.create(db, obj_in=new_alloc)
        db.commit()

        # Recalculate counts (ensures SQLite occupancy values stay in sync)
        self._sync_occupancies(db, bed.billet_id)

        audit_repo.create_log(
            db, user_id, "BED_ALLOCATED", ip, ua,
            f"Allocated bed {bed.bed_number} to trainee {student.service_number} in Billet {bed.billet.name}"
        )
        return new_alloc

    def transfer_bed(self, db: Session, request: TransferRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        student = student_repo.get(db, request.student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Trainee not found")

        new_bed = bed_repo.get(db, request.new_bed_id)
        if not new_bed or new_bed.deleted_at:
            raise HTTPException(status_code=404, detail="Destination bed not found")

        if new_bed.status != "Vacant":
            raise HTTPException(status_code=400, detail="Destination bed is not vacant")

        active_alloc = allocation_repo.get_active_by_student(db, request.student_id)
        if not active_alloc:
            raise HTTPException(status_code=400, detail="Trainee is not currently allocated to any bed")

        old_bed_id = active_alloc.bed_id
        old_bed = bed_repo.get(db, old_bed_id)

        # Vacate old bed
        self._vacate_alloc_internal(db, active_alloc, "Transfer", request.remarks, user_id)

        # Allocate new bed
        new_bed.status = "Occupied"
        new_alloc = AccommodationAllocation(
            student_id=request.student_id,
            bed_id=request.new_bed_id,
            allocated_at=datetime.utcnow(),
            allocated_by=user_id,
            remarks=request.remarks,
            status="Active"
        )
        allocation_repo.create(db, obj_in=new_alloc)
        db.commit()

        # Recalculate occupancies
        if old_bed:
            self._sync_occupancies(db, old_bed.billet_id)
        self._sync_occupancies(db, new_bed.billet_id)

        audit_repo.create_log(
            db, user_id, "BED_TRANSFERRED", ip, ua,
            f"Transferred trainee {student.service_number} from Bed {old_bed.bed_number if old_bed else 'unknown'} to Bed {new_bed.bed_number}"
        )
        return new_alloc

    def vacate_bed(self, db: Session, allocation_id: str, request: VacateRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        alloc = db.query(AccommodationAllocation).filter(AccommodationAllocation.id == allocation_id).first()
        if not alloc or alloc.status == "History":
            raise HTTPException(status_code=404, detail="Active allocation record not found")

        bed = bed_repo.get(db, alloc.bed_id)
        self._vacate_alloc_internal(db, alloc, request.vacate_reason, request.remarks, user_id)
        db.commit()

        if bed:
            self._sync_occupancies(db, bed.billet_id)

        student = student_repo.get(db, alloc.student_id)
        service_no = student.service_number if student else "unknown"

        audit_repo.create_log(
            db, user_id, "BED_VACATED", ip, ua,
            f"Vacated bed ID {alloc.bed_id} (Reason: {request.vacate_reason}) previously held by trainee {service_no}"
        )
        return alloc

    def _vacate_alloc_internal(self, db: Session, alloc: AccommodationAllocation, reason: str, remarks: str, user_id: str):
        bed = bed_repo.get(db, alloc.bed_id)
        if bed:
            bed.status = "Vacant"

        alloc.vacated_at = datetime.utcnow()
        alloc.vacated_by = user_id
        alloc.vacate_reason = reason
        alloc.remarks = remarks
        alloc.status = "History"

    def _sync_occupancies(self, db: Session, billet_id: str):
        """Helper to sync building and billet current occupancy counts.
        Runs locally to guarantee SQLite DB matches the triggers behavior on MySQL.
        """
        billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == billet_id).first()
        if billet:
            # Count how many beds in this billet have active allocations
            active_count = db.query(AccommodationAllocation).join(AccommodationBed).filter(
                AccommodationBed.billet_id == billet_id,
                AccommodationAllocation.status == "Active"
            ).count()
            billet.current_occupancy = active_count

            # Count total building occupancy
            bldg = db.query(AccommodationBuilding).filter(AccommodationBuilding.id == billet.building_id).first()
            if bldg:
                bldg_count = db.query(AccommodationAllocation).join(AccommodationBed).join(AccommodationBillet).filter(
                    AccommodationBillet.building_id == bldg.id,
                    AccommodationAllocation.status == "Active"
                ).count()
                bldg.current_occupancy = bldg_count
            db.commit()

accommodation_service = AccommodationService()
