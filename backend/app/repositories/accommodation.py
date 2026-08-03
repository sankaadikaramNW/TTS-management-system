from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBed, AccommodationAllocation
from app.models.student import Student
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
        results = db.query(AccommodationAllocation).filter(AccommodationAllocation.status == "History").all()
        for alloc in results:
            self._map_relations(db, alloc)
        return results

    def _map_relations(self, db: Session, alloc: AccommodationAllocation):
        student = db.query(Student).filter(Student.id == alloc.student_id).first()
        bed = db.query(AccommodationBed).filter(AccommodationBed.id == alloc.bed_id).first()
        
        if student:
            alloc.student_name = student.full_name
            alloc.student_service_number = student.service_number
            alloc.student_rank = student.rank
            alloc.student_trade = student.trade
            alloc.student_batch = student.batch
            
        if bed:
            alloc.bed_number = bed.bed_number
            billet = db.query(AccommodationBillet).filter(AccommodationBillet.id == bed.billet_id).first()
            if billet:
                alloc.billet_name = billet.name
                building = db.query(AccommodationBuilding).filter(AccommodationBuilding.id == billet.building_id).first()
                if building:
                    alloc.building_name = building.name

building_repo = BuildingRepository(AccommodationBuilding)
billet_repo = BilletRepository(AccommodationBillet)
bed_repo = BedRepository(AccommodationBed)
allocation_repo = AllocationRepository(AccommodationAllocation)
