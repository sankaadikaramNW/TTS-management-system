from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

class AccommodationBuilding(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_buildings'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(30), nullable=False)  # Officers, Airmen, Airwomen
    capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0)

    # Relationships
    billets = relationship("AccommodationBillet", back_populates="building", cascade="all, delete-orphan")

class AccommodationBillet(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_billets'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    building_id = Column(String(36), ForeignKey('accommodation_buildings.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0)

    # Relationships
    building = relationship("AccommodationBuilding", back_populates="billets")
    beds = relationship("AccommodationBed", back_populates="billet", cascade="all, delete-orphan")

class AccommodationBed(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_beds'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    billet_id = Column(String(36), ForeignKey('accommodation_billets.id', ondelete='CASCADE'), nullable=False)
    bed_number = Column(String(30), nullable=False)
    status = Column(String(30), default='Vacant')  # Vacant, Occupied, Maintenance, Reserved

    # Relationships
    billet = relationship("AccommodationBillet", back_populates="beds")
    allocations = relationship("AccommodationAllocation", back_populates="bed", cascade="all, delete-orphan")

class AccommodationAllocation(Base):
    __tablename__ = 'accommodation_allocations'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    bed_id = Column(String(36), ForeignKey('accommodation_beds.id', ondelete='CASCADE'), nullable=False)
    allocated_at = Column(DateTime, default=datetime.utcnow)
    allocated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    vacated_at = Column(DateTime, nullable=True)
    vacated_by = Column(String(36), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    vacate_reason = Column(String(100), nullable=True)
    remarks = Column(Text, nullable=True)
    status = Column(String(20), default='Active')  # Active, History
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="allocations")
    bed = relationship("AccommodationBed", back_populates="allocations")
    allocator = relationship("User", foreign_keys=[allocated_by])
    vacator = relationship("User", foreign_keys=[vacated_by])
