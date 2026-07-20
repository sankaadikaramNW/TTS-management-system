from datetime import date, datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class LiveParadeStrength(BaseModel):
    total_enrolled: int
    present: int
    sick_report: int
    hospital: int
    leave: int
    temp_duty: int
    course_visit: int
    detached_duty: int
    awol: int

class AccommodationOccupancy(BaseModel):
    total_beds: int
    occupied_beds: int
    vacant_beds: int
    maintenance_beds: int
    occupancy_rate: float

class AcademicStatusSummary(BaseModel):
    course_count: int
    average_pass_rate: float
    active_timetables_today: int

class RecentActivityLog(BaseModel):
    id: str
    username: str
    action: str
    details: Optional[str] = None
    created_at: datetime

class DashboardSummaryResponse(BaseModel):
    parade: LiveParadeStrength
    accommodation: AccommodationOccupancy
    academic: AcademicStatusSummary
    recent_activities: List[RecentActivityLog] = []

class NotificationResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: str
    message: str
    type: str  # INFO, WARNING, ALERT
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
