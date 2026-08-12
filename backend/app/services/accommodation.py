from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.accommodation import (
    AccommodationBuilding, AccommodationBillet, AccommodationBunkBed, 
    BedPosition, AccommodationBed, AccommodationAllocation
)
from app.repositories.accommodation import (
    bunk_bed_repo, bed_position_repo, bed_repo, allocation_repo, billet_repo
)
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.accommodation import AllocationRequest, TransferRequest, VacateRequest, BunkBedCreate, BulkBunkBedCreate

class AccommodationService:
    def create_bunk_bed(self, db: Session, request: BunkBedCreate, user_id: str, ip: str, ua: str) -> AccommodationBunkBed:
        billet = billet_repo.get(db, request.billet_id)
        if not billet or billet.deleted_at:
            raise HTTPException(status_code=404, detail="Billet not found")

        if billet.status == "Inactive":
            raise HTTPException(status_code=400, detail="Cannot add bunk beds to an inactive billet")

        # Check unique bunk_no within billet
        existing = db.query(AccommodationBunkBed).filter(
            AccommodationBunkBed.billet_id == request.billet_id,
            AccommodationBunkBed.bunk_no == request.bunk_no,
            AccommodationBunkBed.deleted_at == None
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Bunk bed '{request.bunk_no}' already exists in this billet")

        bunk = AccommodationBunkBed(
            billet_id=request.billet_id,
            bunk_no=request.bunk_no,
            status=request.status or "Active"
        )
        db.add(bunk)
        db.flush()  # get bunk.id

        # Business Rule #2: Automatically create TOP and BOTTOM bed positions
        top_pos = BedPosition(
            bunk_bed_id=bunk.id,
            position_type="TOP",
            position_code=f"{request.bunk_no}-TOP",
            status="Available"
        )
        bottom_pos = BedPosition(
            bunk_bed_id=bunk.id,
            position_type="BOTTOM",
            position_code=f"{request.bunk_no}-BOTTOM",
            status="Available"
        )
        db.add_all([top_pos, bottom_pos])
        db.commit()
        db.refresh(bunk)

        # Update billet totals
        self._update_billet_bunk_counts(db, request.billet_id)

        audit_repo.create_log(
            db, user_id, "BUNK_BED_CREATED", ip, ua,
            f"Created Bunk Bed '{request.bunk_no}' with TOP & BOTTOM positions in Billet '{billet.name}'"
        )
        return bunk

    def bulk_create_bunk_beds(self, db: Session, request: BulkBunkBedCreate, user_id: str, ip: str, ua: str):
        billet = billet_repo.get(db, request.billet_id)
        if not billet or billet.deleted_at:
            raise HTTPException(status_code=404, detail="Billet not found")

        if request.count <= 0 or request.count > 100:
            raise HTTPException(status_code=400, detail="Count must be between 1 and 100")

        existing_bunks = db.query(AccommodationBunkBed).filter(
            AccommodationBunkBed.billet_id == request.billet_id,
            AccommodationBunkBed.deleted_at == None
        ).all()
        existing_numbers = {b.bunk_no for b in existing_bunks}

        prefix = request.prefix if request.prefix is not None else "Bunk-"
        start_num = request.start_number if request.start_number is not None else 1

        created_bunks = []
        for i in range(request.count):
            num = start_num + i
            num_str = f"{num:02d}" if num < 10 else f"{num}"
            bunk_no = f"{prefix}{num_str}"
            if bunk_no in existing_numbers:
                continue

            bunk = AccommodationBunkBed(
                billet_id=request.billet_id,
                bunk_no=bunk_no,
                status=request.status or "Active"
            )
            db.add(bunk)
            db.flush()

            top_pos = BedPosition(
                bunk_bed_id=bunk.id,
                position_type="TOP",
                position_code=f"{bunk_no}-TOP",
                status="Available"
            )
            bottom_pos = BedPosition(
                bunk_bed_id=bunk.id,
                position_type="BOTTOM",
                position_code=f"{bunk_no}-BOTTOM",
                status="Available"
            )
            db.add_all([top_pos, bottom_pos])
            created_bunks.append(bunk)

        db.commit()
        self._update_billet_bunk_counts(db, request.billet_id)

        audit_repo.create_log(
            db, user_id, "BULK_BUNKS_CREATED", ip, ua,
            f"Bulk created {len(created_bunks)} bunk beds in billet '{billet.name}'"
        )
        return created_bunks

    def allocate_bed(self, db: Session, request: AllocationRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        student = student_repo.get(db, request.student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Trainee not found")

        position = bed_position_repo.get(db, request.bed_position_id)
        if not position or position.deleted_at:
            raise HTTPException(status_code=404, detail="Bed position record not found")

        bunk = position.bunk_bed
        if bunk and bunk.status == "Inactive":
            raise HTTPException(status_code=400, detail="Cannot allocate positions in an inactive bunk bed")

        if position.status != "Available":
            raise HTTPException(status_code=400, detail="Requested bed position is not available")

        # Business Rule #7: Prevent Duplicate Accommodation
        active_alloc = allocation_repo.get_active_by_student(db, request.student_id)
        if active_alloc:
            raise HTTPException(
                status_code=400, 
                detail="Selected trainee is already assigned to an active accommodation position."
            )

        # Business Rule #8: Prevent Double Allocation
        active_pos_alloc = allocation_repo.get_active_by_position(db, request.bed_position_id)
        if active_pos_alloc:
            raise HTTPException(
                status_code=400, 
                detail="Requested bed position already has an active trainee assigned."
            )

        # Allocate bed position
        position.status = "Occupied"
        new_alloc = AccommodationAllocation(
            student_id=request.student_id,
            bed_position_id=request.bed_position_id,
            allocated_at=datetime.utcnow(),
            allocated_by=user_id,
            remarks=request.remarks,
            status="Active"
        )
        allocation_repo.create(db, obj_in=new_alloc)
        db.commit()

        if bunk:
            self._sync_occupancies(db, bunk.billet_id)

        audit_repo.create_log(
            db, user_id, "BED_POSITION_ALLOCATED", ip, ua,
            f"Allocated position '{position.position_code}' to trainee {student.service_number} ({student.full_name})"
        )
        return new_alloc

    def transfer_bed(self, db: Session, request: TransferRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        student = student_repo.get(db, request.student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Trainee not found")

        new_pos = bed_position_repo.get(db, request.new_bed_position_id)
        if not new_pos or new_pos.deleted_at:
            raise HTTPException(status_code=404, detail="Destination bed position not found")

        if new_pos.status != "Available":
            raise HTTPException(status_code=400, detail="Destination bed position is not available")

        active_alloc = allocation_repo.get_active_by_student(db, request.student_id)
        if not active_alloc:
            raise HTTPException(status_code=400, detail="Trainee is not currently allocated to any bed position")

        old_pos = bed_position_repo.get(db, active_alloc.bed_position_id) if active_alloc.bed_position_id else None

        # Vacate old position
        self._vacate_alloc_internal(db, active_alloc, "Transfer", request.remarks or "Transferred to new bed position", user_id)

        # Allocate new position
        new_pos.status = "Occupied"
        new_alloc = AccommodationAllocation(
            student_id=request.student_id,
            bed_position_id=request.new_bed_position_id,
            allocated_at=datetime.utcnow(),
            allocated_by=user_id,
            remarks=request.remarks,
            status="Active"
        )
        allocation_repo.create(db, obj_in=new_alloc)
        db.commit()

        # Recalculate occupancies
        if old_pos and old_pos.bunk_bed:
            self._sync_occupancies(db, old_pos.bunk_bed.billet_id)
        if new_pos.bunk_bed:
            self._sync_occupancies(db, new_pos.bunk_bed.billet_id)

        old_code = old_pos.position_code if old_pos else "previous position"
        audit_repo.create_log(
            db, user_id, "BED_POSITION_TRANSFERRED", ip, ua,
            f"Transferred trainee {student.service_number} from position '{old_code}' to position '{new_pos.position_code}'"
        )
        return new_alloc

    def vacate_bed(self, db: Session, allocation_id: str, request: VacateRequest, user_id: str, ip: str, ua: str) -> AccommodationAllocation:
        alloc = db.query(AccommodationAllocation).filter(AccommodationAllocation.id == allocation_id).first()
        if not alloc or alloc.status == "History":
            raise HTTPException(status_code=404, detail="Active allocation record not found")

        pos = bed_position_repo.get(db, alloc.bed_position_id) if alloc.bed_position_id else None
        self._vacate_alloc_internal(db, alloc, request.vacate_reason, request.remarks, user_id)
        db.commit()

        if pos and pos.bunk_bed:
            self._sync_occupancies(db, pos.bunk_bed.billet_id)

        student = student_repo.get(db, alloc.student_id)
        service_no = student.service_number if student else "unknown"

        audit_repo.create_log(
            db, user_id, "BED_POSITION_VACATED", ip, ua,
            f"Vacated bed position (Reason: {request.vacate_reason}) previously held by trainee {service_no}"
        )
        return alloc

    def _vacate_alloc_internal(self, db: Session, alloc: AccommodationAllocation, reason: str, remarks: str, user_id: str):
        if alloc.bed_position_id:
            pos = bed_position_repo.get(db, alloc.bed_position_id)
            if pos:
                pos.status = "Available"
        if alloc.bed_id:
            bed = bed_repo.get(db, alloc.bed_id)
            if bed:
                bed.status = "Vacant"

        alloc.vacated_at = datetime.utcnow()
        alloc.vacated_by = user_id
        alloc.vacate_reason = reason
        alloc.remarks = remarks
        alloc.status = "History"

    def _update_billet_bunk_counts(self, db: Session, billet_id: str):
        billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == billet_id).first()
        if billet:
            count = db.query(AccommodationBunkBed).filter(
                AccommodationBunkBed.billet_id == billet_id,
                AccommodationBunkBed.deleted_at == None
            ).count()
            billet.bunk_bed_count = count
            billet.capacity = count * 2  # Total sleeping positions capacity
            db.commit()

    def _sync_occupancies(self, db: Session, billet_id: str):
        billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == billet_id).first()
        if billet:
            # Count active allocations in this billet
            active_count = db.query(AccommodationAllocation).join(BedPosition, AccommodationAllocation.bed_position_id == BedPosition.id).join(AccommodationBunkBed, BedPosition.bunk_bed_id == AccommodationBunkBed.id).filter(
                AccommodationBunkBed.billet_id == billet_id,
                AccommodationAllocation.status == "Active"
            ).count()
            billet.current_occupancy = active_count

            # Count total building occupancy
            bldg = db.query(AccommodationBuilding).filter(AccommodationBuilding.id == billet.building_id).first()
            if bldg:
                bldg_count = db.query(AccommodationAllocation).join(BedPosition, AccommodationAllocation.bed_position_id == BedPosition.id).join(AccommodationBunkBed, BedPosition.bunk_bed_id == AccommodationBunkBed.id).join(AccommodationBillet, AccommodationBunkBed.billet_id == AccommodationBillet.id).filter(
                    AccommodationBillet.building_id == bldg.id,
                    AccommodationAllocation.status == "Active"
                ).count()
                bldg.current_occupancy = bldg_count
            db.commit()

accommodation_service = AccommodationService()
