from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# ── BED POSITIONS SCHEMAS ──────────────────────────────────
class BedPositionBase(BaseModel):
    position_type: str  # TOP, BOTTOM
    position_code: str  # e.g. B-01-05-TOP
    status: Optional[str] = "Available"  # Available, Occupied, Reserved, Maintenance

class BedPositionResponse(BedPositionBase):
    id: str
    bunk_bed_id: str
    bunk_no: Optional[str] = None
    billet_id: Optional[str] = None
    billet_name: Optional[str] = None
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    student_rank: Optional[str] = None
    student_trade: Optional[str] = None
    parade_status: Optional[str] = None

    class Config:
        from_attributes = True

# ── BUNK BED SCHEMAS ───────────────────────────────────────
class BunkBedBase(BaseModel):
    bunk_no: str  # e.g. B-01-05
    status: Optional[str] = "Active"  # Active, Inactive, Maintenance

class BunkBedCreate(BunkBedBase):
    billet_id: str

class BulkBunkBedCreate(BaseModel):
    billet_id: str
    prefix: Optional[str] = "Bunk-"
    count: int
    start_number: Optional[int] = 1
    status: Optional[str] = "Active"

class BunkBedResponse(BunkBedBase):
    id: str
    billet_id: str
    positions: List[BedPositionResponse] = []
    occupied_count: Optional[int] = 0
    available_count: Optional[int] = 0

    class Config:
        from_attributes = True

# ── BILLET SCHEMAS ──────────────────────────────────────────
class BilletBase(BaseModel):
    name: str
    block: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "Active"

class BilletCreate(BilletBase):
    building_id: str
    bunk_bed_count: Optional[int] = 0  # Number of bunk beds to pre-create

class BilletUpdate(BaseModel):
    name: Optional[str] = None
    block: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class BilletResponse(BilletBase):
    id: str
    building_id: str
    building_name: Optional[str] = None
    bunk_bed_count: int = 0
    capacity: int = 0  # Sleeping positions = bunk_bed_count * 2
    current_occupancy: int = 0
    vacant_count: Optional[int] = 0
    occupancy_rate: Optional[float] = 0.0

    class Config:
        from_attributes = True

# ── BUILDING SCHEMAS ────────────────────────────────────────
class BuildingBase(BaseModel):
    name: str
    type: str  # Officers, Airmen, Airwomen
    capacity: int

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    capacity: Optional[int] = None

class BuildingResponse(BuildingBase):
    id: str
    current_occupancy: int = 0
    billets: List[BilletResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

# ── ALLOCATION & TRANSFER SCHEMAS ────────────────────────────
class AllocationRequest(BaseModel):
    student_id: str
    bed_position_id: str
    remarks: Optional[str] = None

class TransferRequest(BaseModel):
    student_id: str
    new_bed_position_id: str
    remarks: Optional[str] = None

class VacateRequest(BaseModel):
    vacate_reason: str
    remarks: Optional[str] = None

class AllocationResponse(BaseModel):
    id: str
    student_id: str
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    student_rank: Optional[str] = None
    student_trade: Optional[str] = None
    student_batch: Optional[str] = None
    student_course: Optional[str] = None
    parade_status: Optional[str] = None
    bed_position_id: Optional[str] = None
    position_code: Optional[str] = None
    position_type: Optional[str] = None
    bunk_no: Optional[str] = None
    billet_id: Optional[str] = None
    billet_name: Optional[str] = None
    building_id: Optional[str] = None
    building_name: Optional[str] = None
    allocated_at: datetime
    allocated_by: Optional[str] = None
    vacated_at: Optional[datetime] = None
    vacated_by: Optional[str] = None
    vacate_reason: Optional[str] = None
    remarks: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

# ── DASHBOARD SCHEMAS ───────────────────────────────────────
class AccommodationDashboardResponse(BaseModel):
    total_buildings: int
    total_billets: int
    total_bunk_beds: int
    total_sleeping_positions: int
    occupied_positions: int
    available_positions: int
    reserved_positions: int
    maintenance_positions: int
    occupancy_percentage: float
    vacancy_percentage: float
    active_trainees_count: int
