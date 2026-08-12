from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.models.student import Student
from app.models.accommodation import (
    AccommodationBuilding, AccommodationBillet, AccommodationBunkBed, 
    BedPosition, AccommodationBed, AccommodationAllocation
)
from app.repositories.accommodation import (
    building_repo, billet_repo, bunk_bed_repo, bed_position_repo, bed_repo, allocation_repo
)
from app.services.accommodation import accommodation_service
from app.schemas.accommodation import (
    BuildingCreate, BuildingUpdate, BuildingResponse,
    BilletCreate, BilletUpdate, BilletResponse,
    BunkBedCreate, BulkBunkBedCreate, BunkBedResponse, BedPositionResponse,
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
    total_bunk_beds = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.deleted_at == None).count()
    
    # Sleeping capacity derived as count of total bed positions or bunk_beds * 2
    total_sleeping_positions = db.query(BedPosition).filter(BedPosition.deleted_at == None).count()
    if total_sleeping_positions == 0 and total_bunk_beds > 0:
        total_sleeping_positions = total_bunk_beds * 2

    occupied_positions = db.query(BedPosition).filter(BedPosition.status == "Occupied", BedPosition.deleted_at == None).count()
    available_positions = db.query(BedPosition).filter(BedPosition.status == "Available", BedPosition.deleted_at == None).count()
    reserved_positions = db.query(BedPosition).filter(BedPosition.status == "Reserved", BedPosition.deleted_at == None).count()
    maintenance_positions = db.query(BedPosition).filter(BedPosition.status == "Maintenance", BedPosition.deleted_at == None).count()
    
    active_trainees_count = db.query(AccommodationAllocation).filter(AccommodationAllocation.status == "Active").count()

    occupancy_pct = (occupied_positions / total_sleeping_positions * 100) if total_sleeping_positions > 0 else 0.0
    vacancy_pct = (available_positions / total_sleeping_positions * 100) if total_sleeping_positions > 0 else 0.0
    
    return {
        "total_buildings": total_buildings,
        "total_billets": total_billets,
        "total_bunk_beds": total_bunk_beds,
        "total_sleeping_positions": total_sleeping_positions,
        "occupied_positions": occupied_positions,
        "available_positions": available_positions,
        "reserved_positions": reserved_positions,
        "maintenance_positions": maintenance_positions,
        "occupancy_percentage": round(occupancy_pct, 1),
        "vacancy_percentage": round(vacancy_pct, 1),
        "active_trainees_count": active_trainees_count
    }

@router.get("/reports")
def get_reports(
    report_type: str = "active",  # active, history, billet_occupancy, trade_wise, course_wise, batch_wise
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    if report_type == "active":
        return allocation_repo.get_all_active(db)
    elif report_type == "history":
        return allocation_repo.get_history(db)
    elif report_type == "billet_occupancy":
        billets = billet_repo.get_all(db)
        results = []
        for b in billets:
            total_bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == b.id, AccommodationBunkBed.deleted_at == None).count()
            total_positions = db.query(BedPosition).join(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == b.id, BedPosition.deleted_at == None).count()
            if total_positions == 0:
                total_positions = total_bunks * 2
            occupied = db.query(BedPosition).join(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == b.id, BedPosition.status == "Occupied", BedPosition.deleted_at == None).count()
            available = total_positions - occupied
            results.append({
                "id": b.id,
                "building_name": b.building.name if b.building else "—",
                "billet_name": b.name,
                "bunk_bed_count": total_bunks,
                "total_positions": total_positions,
                "occupied": occupied,
                "available": max(0, available),
                "occupancy_rate": round((occupied / total_positions * 100), 1) if total_positions > 0 else 0.0
            })
        return results
    elif report_type == "trade_wise":
        active_allocs = allocation_repo.get_all_active(db)
        trade_map = {}
        for a in active_allocs:
            trade = a.student_trade or "Unassigned"
            trade_map[trade] = trade_map.get(trade, 0) + 1
        return [{"trade": k, "count": v} for k, v in trade_map.items()]
    elif report_type == "course_wise":
        active_allocs = allocation_repo.get_all_active(db)
        course_map = {}
        for a in active_allocs:
            course = a.student_course or "General"
            course_map[course] = course_map.get(course, 0) + 1
        return [{"course": k, "count": v} for k, v in course_map.items()]
    elif report_type == "batch_wise":
        active_allocs = allocation_repo.get_all_active(db)
        batch_map = {}
        for a in active_allocs:
            batch = a.student_batch or "Standard"
            batch_map[batch] = batch_map.get(batch, 0) + 1
        return [{"batch": k, "count": v} for k, v in batch_map.items()]
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

@router.get("/history")
def get_accommodation_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return allocation_repo.get_history(db)

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
            vacant_positions = db.query(BedPosition).join(AccommodationBunkBed).filter(
                AccommodationBunkBed.billet_id == billet.id,
                BedPosition.status == "Available",
                BedPosition.deleted_at == None
            ).count()
            billet.vacant_count = vacant_positions
            vacant_total += vacant_positions
        bldg.vacant_count = vacant_total
    return buildings

@router.post("/buildings", response_model=BuildingResponse)
def create_building(
    bldg_data: BuildingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
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
        
    active_allocs = db.query(AccommodationAllocation).join(BedPosition).join(AccommodationBunkBed).join(AccommodationBillet).filter(
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

@router.get("/billets", response_model=List[BilletResponse])
def get_all_billets(
    building_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    if building_id:
        billets = billet_repo.get_by_building(db, building_id)
    else:
        billets = billet_repo.get_all(db)

    for b in billets:
        total_bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == b.id, AccommodationBunkBed.deleted_at == None).count()
        b.bunk_bed_count = total_bunks
        b.capacity = total_bunks * 2
        
        b.vacant_count = db.query(BedPosition).join(AccommodationBunkBed).filter(
            AccommodationBunkBed.billet_id == b.id,
            BedPosition.status == "Available",
            BedPosition.deleted_at == None
        ).count()
        b.building_name = b.building.name if b.building else "—"
        b.occupancy_rate = round((b.current_occupancy / b.capacity * 100), 1) if b.capacity > 0 else 0.0
    return billets

@router.get("/billets/{id}", response_model=BilletResponse)
def get_billet_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    billet = billet_repo.get(db, id)
    if not billet:
        raise HTTPException(status_code=404, detail="Billet not found")
    
    total_bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == billet.id, AccommodationBunkBed.deleted_at == None).count()
    billet.bunk_bed_count = total_bunks
    billet.capacity = total_bunks * 2
    billet.vacant_count = db.query(BedPosition).join(AccommodationBunkBed).filter(
        AccommodationBunkBed.billet_id == billet.id,
        BedPosition.status == "Available",
        BedPosition.deleted_at == None
    ).count()
    billet.building_name = billet.building.name if billet.building else "—"
    billet.occupancy_rate = round((billet.current_occupancy / billet.capacity * 100), 1) if billet.capacity > 0 else 0.0
    return billet

@router.post("/billets", response_model=BilletResponse)
def create_billet(
    billet_data: BilletCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    bldg = building_repo.get(db, billet_data.building_id)
    if not bldg:
        raise HTTPException(status_code=404, detail="Building not found")

    existing = db.query(AccommodationBillet).filter(
        AccommodationBillet.building_id == billet_data.building_id,
        AccommodationBillet.name == billet_data.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Billet name already exists in this building")

    billet = AccommodationBillet(
        building_id=billet_data.building_id,
        name=billet_data.name,
        block=billet_data.block,
        location=billet_data.location,
        description=billet_data.description,
        status=billet_data.status or "Active",
        bunk_bed_count=0,
        capacity=0
    )
    created = billet_repo.create(db, obj_in=billet)

    # Optional: Pre-create bunk beds if count specified
    if billet_data.bunk_bed_count and billet_data.bunk_bed_count > 0:
        bulk_req = BulkBunkBedCreate(
            billet_id=created.id,
            prefix=f"{created.name}-Bunk-",
            count=billet_data.bunk_bed_count
        )
        accommodation_service.bulk_create_bunk_beds(db, bulk_req, current_user.id, "127.0.0.1", "API")

    db.refresh(created)
    total_bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == created.id).count()
    created.bunk_bed_count = total_bunks
    created.capacity = total_bunks * 2
    created.building_name = bldg.name
    return created

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

    updated = billet_repo.update(db, db_obj=billet, obj_in=billet_data)
    total_bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.billet_id == id).count()
    updated.bunk_bed_count = total_bunks
    updated.capacity = total_bunks * 2
    updated.building_name = updated.building.name if updated.building else "—"
    return updated

# ==========================================
# BUNK BED MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/bunks", response_model=List[BunkBedResponse])
def get_bunk_beds(
    billet_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    if billet_id:
        bunks = bunk_bed_repo.get_by_billet(db, billet_id)
    else:
        bunks = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.deleted_at == None).order_by(AccommodationBunkBed.bunk_no.asc()).all()

    results = []
    for bunk in bunks:
        positions = bed_position_repo.get_by_bunk(db, bunk.id)
        pos_responses = []
        for p in positions:
            active_alloc = allocation_repo.get_active_by_position(db, p.id)
            student_id = active_alloc.student_id if active_alloc else None
            student_name = None
            student_service_number = None
            student_rank = None
            student_trade = None
            parade_status = None
            if active_alloc:
                allocation_repo._map_relations(db, active_alloc)
                student_name = active_alloc.student_name
                student_service_number = active_alloc.student_service_number
                student_rank = active_alloc.student_rank
                student_trade = active_alloc.student_trade
                parade_status = active_alloc.parade_status

            pos_responses.append(BedPositionResponse(
                id=p.id,
                bunk_bed_id=p.bunk_bed_id,
                position_type=p.position_type,
                position_code=p.position_code,
                status=p.status,
                student_id=student_id,
                student_name=student_name,
                student_service_number=student_service_number,
                student_rank=student_rank,
                student_trade=student_trade,
                parade_status=parade_status
            ))
        occupied_cnt = sum(1 for p in pos_responses if p.status == "Occupied")
        available_cnt = sum(1 for p in pos_responses if p.status == "Available")
        results.append(BunkBedResponse(
            id=bunk.id,
            billet_id=bunk.billet_id,
            bunk_no=bunk.bunk_no,
            status=bunk.status,
            positions=pos_responses,
            occupied_count=occupied_cnt,
            available_count=available_cnt
        ))
    return results

@router.get("/billets/{billet_id}/bunks", response_model=List[BunkBedResponse])
def get_bunks_by_billet(
    billet_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return get_bunk_beds(billet_id=billet_id, db=db, current_user=current_user)

@router.post("/bunks", response_model=BunkBedResponse)
def create_bunk_bed(
    bunk_data: BunkBedCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "API")
    bunk = accommodation_service.create_bunk_bed(db, bunk_data, current_user.id, ip, ua)
    
    positions = bed_position_repo.get_by_bunk(db, bunk.id)
    pos_responses = [BedPositionResponse.model_validate(p) for p in positions]
    return BunkBedResponse(
        id=bunk.id,
        billet_id=bunk.billet_id,
        bunk_no=bunk.bunk_no,
        status=bunk.status,
        positions=pos_responses,
        occupied_count=0,
        available_count=2
    )

@router.post("/bunks/bulk", response_model=List[BunkBedResponse])
def bulk_create_bunk_beds(
    bulk_data: BulkBunkBedCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "API")
    bunks = accommodation_service.bulk_create_bunk_beds(db, bulk_data, current_user.id, ip, ua)
    return get_bunk_beds(billet_id=bulk_data.billet_id, db=db, current_user=current_user)

@router.get("/bunks/{bunk_id}/positions", response_model=List[BedPositionResponse])
def get_bunk_positions(
    bunk_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    positions = bed_position_repo.get_by_bunk(db, bunk_id)
    results = []
    bunk = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.id == bunk_id).first()
    bunk_no = bunk.bunk_no if bunk else None
    billet_id = bunk.billet_id if bunk else None
    billet_name = bunk.billet.name if (bunk and bunk.billet) else None

    for p in positions:
        active_alloc = allocation_repo.get_active_by_position(db, p.id)
        student_id = active_alloc.student_id if active_alloc else None
        student_name = None
        student_service_number = None
        student_rank = None
        student_trade = None
        parade_status = None
        if active_alloc:
            allocation_repo._map_relations(db, active_alloc)
            student_name = active_alloc.student_name
            student_service_number = active_alloc.student_service_number
            student_rank = active_alloc.student_rank
            student_trade = active_alloc.student_trade
            parade_status = active_alloc.parade_status

        results.append(BedPositionResponse(
            id=p.id,
            bunk_bed_id=p.bunk_bed_id,
            bunk_no=bunk_no,
            billet_id=billet_id,
            billet_name=billet_name,
            position_type=p.position_type,
            position_code=p.position_code,
            status=p.status,
            student_id=student_id,
            student_name=student_name,
            student_service_number=student_service_number,
            student_rank=student_rank,
            student_trade=student_trade,
            parade_status=parade_status
        ))
    return results

@router.get("/positions/available", response_model=List[BedPositionResponse])
def get_available_positions(
    billet_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    if billet_id:
        positions = bed_position_repo.get_available_in_billet(db, billet_id)
    else:
        positions = db.query(BedPosition).filter(BedPosition.status == "Available", BedPosition.deleted_at == None).all()

    results = []
    for p in positions:
        bunk = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.id == p.bunk_bed_id).first()
        b_no = bunk.bunk_no if bunk else None
        b_id = bunk.billet_id if bunk else None
        b_name = bunk.billet.name if (bunk and bunk.billet) else None

        results.append(BedPositionResponse(
            id=p.id,
            bunk_bed_id=p.bunk_bed_id,
            bunk_no=b_no,
            billet_id=b_id,
            billet_name=b_name,
            position_type=p.position_type,
            position_code=p.position_code,
            status=p.status
        ))
    return results

# ==========================================
# ALLOCATION, TRANSFER & VACATE ENDPOINTS
# ==========================================

@router.get("/allocations", response_model=List[AllocationResponse])
def list_allocations(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return allocation_repo.get_all_active(db)

@router.get("/trainees/{trainee_id}", response_model=Optional[AllocationResponse])
def get_trainee_accommodation(
    trainee_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    alloc = allocation_repo.get_active_by_student(db, trainee_id)
    if not alloc:
        return None
    allocation_repo._map_relations(db, alloc)
    return alloc

@router.post("/allocate", response_model=AllocationResponse)
def allocate_trainee_bed(
    request: Request,
    alloc_data: AllocationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "API")
    alloc = accommodation_service.allocate_bed(db, alloc_data, current_user.id, ip, ua)
    return allocation_repo.get_details(db, alloc.id)

@router.post("/transfer", response_model=AllocationResponse)
def transfer_trainee_bed(
    request: Request,
    transfer_data: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "API")
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
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "API")
    alloc = accommodation_service.vacate_bed(db, allocation_id, vacate_data, current_user.id, ip, ua)
    return allocation_repo.get_details(db, alloc.id)
