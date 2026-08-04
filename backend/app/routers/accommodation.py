from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBed, AccommodationAllocation
from app.repositories.accommodation import building_repo, billet_repo, bed_repo, allocation_repo
from app.services.accommodation import accommodation_service
from app.schemas.accommodation import (
    BuildingCreate, BuildingUpdate, BuildingResponse,
    BilletCreate, BilletUpdate, BilletResponse,
    BedCreate, BulkBedCreate, BedUpdate, BedResponse,
    AllocationRequest, AllocationResponse,
    TransferRequest, VacateRequest,
    AccommodationDashboardResponse
)

router = APIRouter(prefix="/accommodation", tags=["Accommodation Management"])

# ==========================================
# DASHBOARD & REPORTS ENDPOINTS
# ==========================================

@router.get("/dashboard", response_model=AccommodationDashboardResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    total_buildings = db.query(AccommodationBuilding).filter(AccommodationBuilding.deleted_at == None).count()
    total_billets = db.query(AccommodationBillet).filter(AccommodationBillet.deleted_at == None).count()
    total_beds = db.query(AccommodationBed).filter(AccommodationBed.deleted_at == None).count()
    
    occupied_beds = db.query(AccommodationBed).filter(AccommodationBed.status == "Occupied", AccommodationBed.deleted_at == None).count()
    vacant_beds = db.query(AccommodationBed).filter(AccommodationBed.status == "Vacant", AccommodationBed.deleted_at == None).count()
    reserved_beds = db.query(AccommodationBed).filter(AccommodationBed.status == "Reserved", AccommodationBed.deleted_at == None).count()
    maintenance_beds = db.query(AccommodationBed).filter(AccommodationBed.status == "Maintenance", AccommodationBed.deleted_at == None).count()
    
    occupancy_pct = (occupied_beds / total_beds * 100) if total_beds > 0 else 0.0
    vacancy_pct = (vacant_beds / total_beds * 100) if total_beds > 0 else 0.0
    
    return {
        "total_buildings": total_buildings,
        "total_billets": total_billets,
        "total_beds": total_beds,
        "occupied_beds": occupied_beds,
        "vacant_beds": vacant_beds,
        "reserved_beds": reserved_beds,
        "maintenance_beds": maintenance_beds,
        "occupancy_percentage": round(occupancy_pct, 1),
        "vacancy_percentage": round(vacancy_pct, 1)
    }

@router.get("/reports")
def get_reports(
    report_type: str = "active",  # active, history, billet_occupancy
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    if report_type == "active":
        return allocation_repo.get_all_active(db)
    elif report_type == "history":
        return allocation_repo.get_history(db)
    elif report_type == "billet_occupancy":
        billets = db.query(AccommodationBillet).filter(AccommodationBillet.deleted_at == None).all()
        results = []
        for b in billets:
            total_beds = db.query(AccommodationBed).filter(AccommodationBed.billet_id == b.id, AccommodationBed.deleted_at == None).count()
            occupied = db.query(AccommodationBed).filter(AccommodationBed.billet_id == b.id, AccommodationBed.status == "Occupied", AccommodationBed.deleted_at == None).count()
            vacant = db.query(AccommodationBed).filter(AccommodationBed.billet_id == b.id, AccommodationBed.status == "Vacant", AccommodationBed.deleted_at == None).count()
            results.append({
                "id": b.id,
                "building_name": b.building.name,
                "billet_name": b.name,
                "capacity": b.capacity,
                "occupied": occupied,
                "vacant": vacant,
                "occupancy_rate": round((occupied / b.capacity * 100), 1) if b.capacity > 0 else 0
            })
        return results
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

# ==========================================
# MASTER BUILDING MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/buildings", response_model=List[BuildingResponse])
def get_buildings(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    buildings = building_repo.get_all(db)
    for bldg in buildings:
        vacant_total = 0
        for billet in bldg.billets:
            vacant_beds = sum(1 for bed in billet.beds if bed.status == "Vacant")
            billet.vacant_count = vacant_beds
            vacant_total += vacant_beds
        bldg.vacant_count = vacant_total
    return buildings

@router.post("/buildings", response_model=BuildingResponse)
def create_building(
    bldg_data: BuildingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    # Check uniqueness
    existing = db.query(AccommodationBuilding).filter(AccommodationBuilding.name == bldg_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Building name already exists")
    
    bldg = AccommodationBuilding(
        name=bldg_data.name,
        type=bldg_data.type,
        capacity=bldg_data.capacity
    )
    return building_repo.create(db, obj_in=bldg)

@router.put("/buildings/{id}", response_model=BuildingResponse)
def update_building(
    id: str,
    bldg_data: BuildingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    bldg = building_repo.get(db, id)
    if not bldg:
        raise HTTPException(status_code=404, detail="Building not found")
    
    return building_repo.update(db, db_obj=bldg, obj_in=bldg_data)

@router.delete("/buildings/{id}")
def delete_building(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    bldg = building_repo.get(db, id)
    if not bldg:
        raise HTTPException(status_code=404, detail="Building not found")
        
    # Check if there are active beds allocated in this building
    active_allocs = db.query(AccommodationAllocation).join(AccommodationBed).join(AccommodationBillet).filter(
        AccommodationBillet.building_id == id,
        AccommodationAllocation.status == "Active"
    ).count()
    if active_allocs > 0:
        raise HTTPException(status_code=400, detail="Cannot delete a building with active bed allocations")

    building_repo.remove(db, id=id)
    return {"message": "Building deleted successfully"}

# ==========================================
# MASTER BILLET MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/billets/{building_id}", response_model=List[BilletResponse])
def get_billets(
    building_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    billets = billet_repo.get_by_building(db, building_id)
    for b in billets:
        b.vacant_count = sum(1 for bed in b.beds if bed.status == "Vacant")
    return billets

@router.post("/billets", response_model=BilletResponse)
def create_billet(
    billet_data: BilletCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    bldg = building_repo.get(db, billet_data.building_id)
    if not bldg:
        raise HTTPException(status_code=404, detail="Building not found")

    # Validate building total capacity
    current_bldg_capacity = sum(b.capacity for b in bldg.billets)
    if current_bldg_capacity + billet_data.capacity > bldg.capacity:
        raise HTTPException(status_code=400, detail="Billet capacity exceeds remaining building capacity")

    # Check unique name in building
    existing = db.query(AccommodationBillet).filter(
        AccommodationBillet.building_id == billet_data.building_id,
        AccommodationBillet.name == billet_data.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Billet name already exists in this building")

    billet = AccommodationBillet(
        building_id=billet_data.building_id,
        name=billet_data.name,
        capacity=billet_data.capacity
    )
    return billet_repo.create(db, obj_in=billet)

@router.put("/billets/{id}", response_model=BilletResponse)
def update_billet(
    id: str,
    billet_data: BilletUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    billet = billet_repo.get(db, id)
    if not billet:
        raise HTTPException(status_code=404, detail="Billet not found")

    # If capacity is being changed, check that new capacity covers current occupancy
    if billet_data.capacity is not None:
        if billet_data.capacity < billet.current_occupancy:
            raise HTTPException(status_code=400, detail="New capacity is less than current occupancy")

    return billet_repo.update(db, db_obj=billet, obj_in=billet_data)

# ==========================================
# MASTER BED MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/beds/billet/{billet_id}", response_model=List[BedResponse])
def get_beds_by_billet(
    billet_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return bed_repo.get_by_billet(db, billet_id)

@router.post("/beds", response_model=BedResponse)
def create_bed(
    bed_data: BedCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    billet = billet_repo.get(db, bed_data.billet_id)
    if not billet:
        raise HTTPException(status_code=404, detail="Billet not found")

    # Check capacity limits
    current_beds_count = db.query(AccommodationBed).filter(
        AccommodationBed.billet_id == bed_data.billet_id,
        AccommodationBed.deleted_at == None
    ).count()
    if current_beds_count >= billet.capacity:
        raise HTTPException(status_code=400, detail="Cannot exceed billet capacity")

    # Check uniqueness within billet
    existing = db.query(AccommodationBed).filter(
        AccommodationBed.billet_id == bed_data.billet_id,
        AccommodationBed.bed_number == bed_data.bed_number,
        AccommodationBed.deleted_at == None
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bed number already exists in this billet")

    bed = AccommodationBed(
        billet_id=bed_data.billet_id,
        bed_number=bed_data.bed_number,
        status=bed_data.status
    )
    return bed_repo.create(db, obj_in=bed)

@router.post("/beds/bulk", response_model=List[BedResponse])
def bulk_create_beds(
    bulk_data: BulkBedCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    billet = billet_repo.get(db, bulk_data.billet_id)
    if not billet:
        raise HTTPException(status_code=404, detail="Billet not found")

    if bulk_data.count <= 0:
        raise HTTPException(status_code=400, detail="Bed count must be greater than 0")

    if bulk_data.count > 100:
        raise HTTPException(status_code=400, detail="Cannot generate more than 100 beds at a time")

    existing_beds = db.query(AccommodationBed).filter(
        AccommodationBed.billet_id == bulk_data.billet_id,
        AccommodationBed.deleted_at == None
    ).all()

    if len(existing_beds) + bulk_data.count > billet.capacity:
        remaining = max(0, billet.capacity - len(existing_beds))
        raise HTTPException(
            status_code=400, 
            detail=f"Bulk creation of {bulk_data.count} beds exceeds billet capacity limit. Remaining bed capacity: {remaining} beds."
        )

    existing_numbers = {b.bed_number for b in existing_beds}
    prefix = bulk_data.prefix if bulk_data.prefix is not None else "Bed "
    start_num = bulk_data.start_number if bulk_data.start_number is not None else 1

    created_beds = []
    for i in range(bulk_data.count):
        num = start_num + i
        bed_num = f"{prefix}{num}"
        if bed_num in existing_numbers:
            continue
        
        bed = AccommodationBed(
            billet_id=bulk_data.billet_id,
            bed_number=bed_num,
            status=bulk_data.status or "Vacant"
        )
        db.add(bed)
        created_beds.append(bed)

    db.commit()
    for b in created_beds:
        db.refresh(b)

    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    from app.repositories.user import audit_repo
    audit_repo.create_log(
        db, current_user.id, "BULK_BEDS_CREATED", ip, ua,
        f"Bulk created {len(created_beds)} beds in billet '{billet.name}'"
    )

    return created_beds

@router.put("/beds/{id}", response_model=BedResponse)
def update_bed(
    id: str,
    bed_data: BedUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    bed = bed_repo.get(db, id)
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")

    # If updating status, ensure we don't mark an active occupied bed as vacant directly (must go through vacate)
    if bed_data.status is not None and bed.status == "Occupied" and bed_data.status != "Occupied":
        active_alloc = db.query(AccommodationAllocation).filter(
            AccommodationAllocation.bed_id == id,
            AccommodationAllocation.status == "Active"
        ).first()
        if active_alloc:
            raise HTTPException(
                status_code=400, 
                detail="Bed has an active allocation. Please vacate the bed using the vacate endpoint."
            )

    return bed_repo.update(db, db_obj=bed, obj_in=bed_data)

# ==========================================
# ALLOCATION, TRANSFER & VACATE ENDPOINTS
# ==========================================

@router.get("/allocations", response_model=List[AllocationResponse])
def list_allocations(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return allocation_repo.get_all_active(db)

@router.post("/allocate", response_model=AllocationResponse)
def allocate_trainee_bed(
    request: Request,
    alloc_data: AllocationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    alloc = accommodation_service.allocate_bed(db, alloc_data, current_user.id, ip, ua)
    return allocation_repo.get_details(db, alloc.id)

@router.post("/transfer", response_model=AllocationResponse)
def transfer_trainee_bed(
    request: Request,
    transfer_data: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    alloc = accommodation_service.transfer_bed(db, transfer_data, current_user.id, ip, ua)
    return allocation_repo.get_details(db, alloc.id)

@router.post("/vacate/{allocation_id}", response_model=AllocationResponse)
def vacate_trainee_bed(
    allocation_id: str,
    request: Request,
    vacate_data: VacateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    alloc = accommodation_service.vacate_bed(db, allocation_id, vacate_data, current_user.id, ip, ua)
    return allocation_repo.get_details(db, alloc.id)
