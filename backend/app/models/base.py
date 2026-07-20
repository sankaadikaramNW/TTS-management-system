import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class TimeStampedModelMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    def restore(self):
        self.deleted_at = None
