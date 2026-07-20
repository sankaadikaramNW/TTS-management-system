from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import generate_uuid, TimeStampedModelMixin

class AccommodationBuilding(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_buildings'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(30), nullable=False)  # Officers, Airmen, Airwomen
    capacity = Column(Integer, nullable=False)

    # Relationships
    billets = relationship("AccommodationBillet", back_populates="building", cascade="all, delete-orphan")

class AccommodationBillet(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_billets'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    building_id = Column(String(36), ForeignKey('accommodation_buildings.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)

    # Relationships
    building = relationship("AccommodationBuilding", back_populates="billets")
    rooms = relationship("AccommodationRoom", back_populates="billet", cascade="all, delete-orphan")

class AccommodationRoom(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_rooms'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    billet_id = Column(String(36), ForeignKey('accommodation_billets.id', ondelete='CASCADE'), nullable=False)
    room_number = Column(String(30), nullable=False)
    capacity = Column(Integer, nullable=False)

    # Relationships
    billet = relationship("AccommodationBillet", back_populates="rooms")
    beds = relationship("AccommodationBed", back_populates="room", cascade="all, delete-orphan")

class AccommodationBed(Base, TimeStampedModelMixin):
    __tablename__ = 'accommodation_beds'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    room_id = Column(String(36), ForeignKey('accommodation_rooms.id', ondelete='CASCADE'), nullable=False)
    bed_number = Column(String(30), nullable=False)
    status = Column(String(30), default='Vacant')  # Vacant, Occupied, Maintenance

    # Relationships
    room = relationship("AccommodationRoom", back_populates="beds")
    allocations = relationship("AccommodationAllocation", back_populates="bed", cascade="all, delete-orphan")

class AccommodationAllocation(Base):
    __tablename__ = 'accommodation_allocations'

    id = Column(String(36), primary_key=True, default=generate_uuid)
    student_id = Column(String(36), ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    bed_id = Column(String(36), ForeignKey('accommodation_beds.id', ondelete='CASCADE'), nullable=False)
    allocated_at = Column(DateTime, default=datetime.utcnow)
    vacated_at = Column(DateTime, nullable=True)
    status = Column(String(20), default='Active')  # Active, History
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="allocations")
    bed = relationship("AccommodationBed", back_populates="allocations")
