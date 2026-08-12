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
    block = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False, default=0)  # Sleeping positions capacity (bunk_bed_count * 2)
    bunk_bed_count = Column(Integer, default=0)  # Total physical bunk beds
    current_occupancy = Column(Integer, default=0)
    status = Column(String(30), default='Active')

    # Relationships
    building = relationship("AccommodationBuilding", back_populates="billets")
    bunk_beds = relationship("AccommodationBunkBed", back_populates="billet", cascade="all, delete-orphan")
    beds = relationship("AccommodationBed", back_populates="billet", cascade="all, delete-orphan")

class AccommodationBunkBed(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_bunk_beds'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    billet_id = Column(String(36), ForeignKey('accommodation_billets.id', ondelete='CASCADE'), nullable=False)
    bunk_no = Column(String(50), nullable=False)  # e.g. B-01-05
    status = Column(String(30), default='Active')  # Active, Inactive, Maintenance

    # Relationships
    billet = relationship("AccommodationBillet", back_populates="bunk_beds")
    positions = relationship("BedPosition", back_populates="bunk_bed", cascade="all, delete-orphan")

class BedPosition(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_bed_positions'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    bunk_bed_id = Column(String(36), ForeignKey('accommodation_bunk_beds.id', ondelete='CASCADE'), nullable=False)
    position_type = Column(String(20), nullable=False)  # TOP, BOTTOM
    position_code = Column(String(60), nullable=False, unique=True)  # e.g. B-01-05-TOP
    status = Column(String(30), default='Available')  # Available, Occupied, Reserved, Maintenance

    # Relationships
    bunk_bed = relationship("AccommodationBunkBed", back_populates="positions")
    allocations = relationship("AccommodationAllocation", back_populates="position", cascade="all, delete-orphan")

class AccommodationBed(Base, TimeStampedModelMixin):
    """Legacy bed model preserved for backwards compatibility."""
    __tablename__ = 'accommodation_beds'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    billet_id = Column(String(36), ForeignKey('accommodation_billets.id', ondelete='CASCADE'), nullable=False)
    bed_number = Column(String(30), nullable=False)
    status = Column(String(30), default='Vacant')

    billet = relationship("AccommodationBillet", back_populates="beds")
    allocations = relationship("AccommodationAllocation", back_populates="bed", cascade="all, delete-orphan")

class AccommodationAllocation(Base):
    __tablename__ = 'accommodation_allocations'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    bed_position_id = Column(String(36), ForeignKey('accommodation_bed_positions.id', ondelete='CASCADE'), nullable=True)
    bed_id = Column(String(36), ForeignKey('accommodation_beds.id', ondelete='CASCADE'), nullable=True)
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
    position = relationship("BedPosition", back_populates="allocations")
    bed = relationship("AccommodationBed", back_populates="allocations")
    allocator = relationship("User", foreign_keys=[allocated_by])
    vacator = relationship("User", foreign_keys=[vacated_by])
