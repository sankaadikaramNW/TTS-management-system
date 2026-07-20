from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class BedBase(BaseModel):
    bed_number: str
    status: Optional[str] = "Vacant" # Vacant, Occupied, Maintenance

class BedCreate(BedBase):
    room_id: str

class BedResponse(BedBase):
    id: str
    room_id: str
    
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    capacity: int

class RoomCreate(RoomBase):
    billet_id: str

class RoomResponse(RoomBase):
    id: str
    billet_id: str
    beds: List[BedResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

class BilletBase(BaseModel):
    name: str
    capacity: int

class BilletCreate(BilletBase):
    building_id: str

class BilletResponse(BilletBase):
    id: str
    building_id: str
    rooms: List[RoomResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

class BuildingBase(BaseModel):
    name: str
    type: str  # Officers, Airmen, Airwomen
    capacity: int

class BuildingCreate(BuildingBase):
    pass

class BuildingResponse(BuildingBase):
    id: str
    billets: List[BilletResponse] = []
    vacant_count: Optional[int] = 0

    class Config:
        from_attributes = True

class AllocationRequest(BaseModel):
    student_id: str
    bed_id: str

class AllocationResponse(BaseModel):
    id: str
    student_id: str
    student_name: Optional[str] = None
    student_service_number: Optional[str] = None
    bed_id: str
    bed_number: Optional[str] = None
    room_number: Optional[str] = None
    billet_name: Optional[str] = None
    building_name: Optional[str] = None
    allocated_at: datetime
    vacated_at: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True
