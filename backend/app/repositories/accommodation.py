from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.models.accommodation import (
    AccommodationBuilding, AccommodationBillet, AccommodationBunkBed, 
    BedPosition, AccommodationBed, AccommodationAllocation
)
from app.models.student import Student, ParadeState
from app.models.academic import Course
from app.repositories.base import BaseRepository

class BuildingRepository(BaseRepository[AccommodationBuilding]):
    def get_all(self, db: Session) -> List[AccommodationBuilding]:
        return db.query(AccommodationBuilding).filter(AccommodationBuilding.deleted_at == None).all()

class BilletRepository(BaseRepository[AccommodationBillet]):
    def get_by_building(self, db: Session, building_id: str) -> List[AccommodationBillet]:
        return db.query(AccommodationBillet).filter(
            AccommodationBillet.building_id == building_id, 
            AccommodationBillet.deleted_at == None
        ).all()

    def get_all(self, db: Session) -> List[AccommodationBillet]:
        return db.query(AccommodationBillet).filter(AccommodationBillet.deleted_at == None).all()

class BunkBedRepository(BaseRepository[AccommodationBunkBed]):
    def get_by_billet(self, db: Session, billet_id: str) -> List[AccommodationBunkBed]:
        return db.query(AccommodationBunkBed).filter(
            AccommodationBunkBed.billet_id == billet_id, 
            AccommodationBunkBed.deleted_at == None
        ).all()

class BedPositionRepository(BaseRepository[BedPosition]):
    def get_by_bunk(self, db: Session, bunk_bed_id: str) -> List[BedPosition]:
        return db.query(BedPosition).filter(
            BedPosition.bunk_bed_id == bunk_bed_id,
            BedPosition.deleted_at == None
        ).all()

    def get_available_in_billet(self, db: Session, billet_id: str) -> List[BedPosition]:
        return db.query(BedPosition).join(AccommodationBunkBed).filter(
            AccommodationBunkBed.billet_id == billet_id,
            AccommodationBunkBed.deleted_at == None,
            BedPosition.status == "Available",
            BedPosition.deleted_at == None
        ).all()

class BedRepository(BaseRepository[AccommodationBed]):
    def get_by_billet(self, db: Session, billet_id: str) -> List[AccommodationBed]:
        return db.query(AccommodationBed).filter(
            AccommodationBed.billet_id == billet_id, 
            AccommodationBed.deleted_at == None
        ).all()

class AllocationRepository(BaseRepository[AccommodationAllocation]):
    def get_active_by_student(self, db: Session, student_id: str) -> Optional[AccommodationAllocation]:
        return db.query(AccommodationAllocation).filter(
            AccommodationAllocation.student_id == student_id,
            AccommodationAllocation.status == "Active"
        ).first()

    def get_active_by_position(self, db: Session, bed_position_id: str) -> Optional[AccommodationAllocation]:
        return db.query(AccommodationAllocation).filter(
            AccommodationAllocation.bed_position_id == bed_position_id,
            AccommodationAllocation.status == "Active"
        ).first()

    def get_active_by_bed(self, db: Session, bed_id: str) -> Optional[AccommodationAllocation]:
        return db.query(AccommodationAllocation).filter(
            AccommodationAllocation.bed_id == bed_id,
            AccommodationAllocation.status == "Active"
        ).first()

    def get_all_active(self, db: Session) -> List[AccommodationAllocation]:
        results = db.query(AccommodationAllocation).filter(AccommodationAllocation.status == "Active").all()
        for alloc in results:
            self._map_relations(db, alloc)
        return results

    def get_details(self, db: Session, allocation_id: str) -> Optional[AccommodationAllocation]:
        alloc = db.query(AccommodationAllocation).filter(AccommodationAllocation.id == allocation_id).first()
        if alloc:
            self._map_relations(db, alloc)
        return alloc

    def get_history(self, db: Session) -> List[AccommodationAllocation]:
        results = db.query(AccommodationAllocation).filter(AccommodationAllocation.status == "History").order_by(AccommodationAllocation.updated_at.desc()).all()
        for alloc in results:
            self._map_relations(db, alloc)
        return results

    def _map_relations(self, db: Session, alloc: AccommodationAllocation):
        student = db.query(Student).filter(Student.id == alloc.student_id).first()
        pos = None
        if alloc.bed_position_id:
            pos = db.query(BedPosition).filter(BedPosition.id == alloc.bed_position_id).first()
        bed = None
        if alloc.bed_id:
            bed = db.query(AccommodationBed).filter(AccommodationBed.id == alloc.bed_id).first()

        if student:
            alloc.student_name = student.full_name
            alloc.student_service_number = student.service_number
            alloc.student_rank = student.rank
            alloc.student_trade = student.trade
            alloc.student_batch = student.batch
            
            # Map course code/name if available
            if student.course_id:
                c = db.query(Course).filter(Course.id == student.course_id).first()
                alloc.student_course = c.code if c else None

            # Fetch today's parade state status
            today = date.today()
            ps = db.query(ParadeState).filter(
                ParadeState.student_id == student.id,
                ParadeState.date == today
            ).first()
            alloc.parade_status = ps.status if ps else "Present"

        if pos:
            alloc.position_code = pos.position_code
            alloc.position_type = pos.position_type
            bunk = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.id == pos.bunk_bed_id).first()
            if bunk:
                alloc.bunk_no = bunk.bunk_no
                billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == bunk.billet_id).first()
                if billet:
                    alloc.billet_id = billet.id
                    alloc.billet_name = billet.name
                    building = db.query(AccommodationBuilding).filter(AccommodationBuilding.id == billet.building_id).first()
                    if building:
                        alloc.building_id = building.id
                        alloc.building_name = building.name
        elif bed:
            alloc.position_code = bed.bed_number
            billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == bed.billet_id).first()
            if billet:
                alloc.billet_id = billet.id
                alloc.billet_name = billet.name
                building = db.query(AccommodationBuilding).filter(AccommodationBuilding.id == billet.building_id).first()
                if building:
                    alloc.building_id = building.id
                    alloc.building_name = building.name

building_repo = BuildingRepository(AccommodationBuilding)
billet_repo = BilletRepository(AccommodationBillet)
bunk_bed_repo = BunkBedRepository(AccommodationBunkBed)
bed_position_repo = BedPositionRepository(BedPosition)
bed_repo = BedRepository(AccommodationBed)
allocation_repo = AllocationRepository(AccommodationAllocation)
