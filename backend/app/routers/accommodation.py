from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.repositories.accommodation import building_repo, billet_repo, room_repo, bed_repo, allocation_repo
from app.services.accommodation import accommodation_service
from app.schemas.accommodation import BuildingResponse, BilletResponse, RoomResponse, BedResponse, AllocationRequest, AllocationResponse

router = APIRouter(prefix="/accommodation", tags=["Accommodation Management"])

@router.get("/buildings", response_model=List[BuildingResponse])
def get_buildings(
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    buildings = building_repo.get_all(db)
    for bldg in buildings:
        # Calculate vacancies count
        vacant_total = 0
        for billet in bldg.billets:
            for room in billet.rooms:
                vacant_beds = sum(1 for bed in room.beds if bed.status == "Vacant")
                room.vacant_count = vacant_beds
                vacant_total += vacant_beds
            billet.vacant_count = sum(r.vacant_count for r in billet.rooms)
        bldg.vacant_count = vacant_total
    return buildings

@router.get("/billets/{building_id}", response_model=List[BilletResponse])
def get_billets(
    building_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return billet_repo.get_by_building(db, building_id)

@router.get("/rooms/{billet_id}", response_model=List[RoomResponse])
def get_rooms(
    billet_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return room_repo.get_by_billet(db, billet_id)

@router.get("/beds/{room_id}", response_model=List[BedResponse])
def get_beds(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:read"))
):
    return bed_repo.get_by_room(db, room_id)

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
    return allocation_repo.get(db, alloc.id) # returns loaded mapping

@router.post("/vacate/{allocation_id}", response_model=AllocationResponse)
def vacate_trainee_bed(
    allocation_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("room:write"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    alloc = accommodation_service.vacate_bed(db, allocation_id, current_user.id, ip, ua)
    return alloc
