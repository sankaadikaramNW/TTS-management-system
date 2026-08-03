from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class BedBase(BaseModel):
    bed_number: str
    status: Optional[str] = "Vacant"  # Vacant, Occupied, Maintenance, Reserved

class BedCreate(BedBase):
    billet_id: str

class BedUpdate(BaseModel):
    bed_number: Optional[str] = None
    status: Optional[str] = None

class BedResponse(BedBase):
    id: str
    billet_id: str
    
    class Config:
        from_attributes = True

class BilletBase(BaseModel):
    name: str
    capacity: int

class BilletCreate(BilletBase):
    building_id: str

class BilletUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None

class BilletResponse(BilletBase):
    id: str
    building_id: str
    current_occupancy: int
    beds: List[BedResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

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
    current_occupancy: int
    billets: List[BilletResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

class AllocationRequest(BaseModel):
    student_id: str
    bed_id: str
    remarks: Optional[str] = None

class TransferRequest(BaseModel):
    student_id: str
    new_bed_id: str
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
    bed_id: str
    bed_number: Optional[str] = None
    billet_name: Optional[str] = None
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

class AccommodationDashboardResponse(BaseModel):
    total_buildings: int
    total_billets: int
    total_beds: int
    occupied_beds: int
    vacant_beds: int
    reserved_beds: int
    maintenance_beds: int
    occupancy_percentage: float
    vacancy_percentage: float
