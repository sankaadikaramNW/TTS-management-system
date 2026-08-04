"""
Test script: simulate a student POST submission to identify the exact error
"""
import sys, os
os.chdir('backend')
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.student import Student
from app.services.student import student_service
from app.schemas.student import StudentCreate
from datetime import date

db = SessionLocal()

# Check what DB we're connected to
from app.config import settings
print("DB URL:", settings.database_url)

# Check current student count
from sqlalchemy import func
count = db.query(func.count(Student.id)).scalar()
print("Current student count:", count)

# Try creating a test student
try:
    test_data = StudentCreate(
        service_number="TEST-001",
        initials="TK",
        full_name="TEST KARUNARATNE",
        nic="199912345678",
        dob=date(1999, 1, 1),
        gender="Male",
        rank="Aircraftman",
        trade="Airframe",
        batch="TEST-BATCH-01",
        squadron="Training Squadron",
        unit="SLAF TTS Ekala",
        posting="SLAF Katunayake",
        joining_date=date(2024, 1, 1),
        passing_out_date=date(2025, 1, 1),
        phone="0771234567",
        email="test@slaf.gov.lk",
        emergency_contact_name="Test Contact",
        emergency_contact_phone="0771234567",
        blood_group="O+",
        medical_category="A4G4",
        religion="Buddhist",
        nationality="Sri Lankan",
        permanent_address="123 Test Street, Colombo",
        temporary_address="456 Temp Road, Ekala"
    )
    
    student = student_service.create_student(db, test_data, "user-slaf-admin", "127.0.0.1", "test")
    print("SUCCESS: Student created:", student.id, student.service_number)
    print("  -> Phone:", student.phone)
    print("  -> Email:", student.email)
    print("  -> Squadron:", student.squadron)
    print("  -> Unit:", student.unit)
    print("  -> Posting:", student.posting)
    print("  -> Joining Date:", student.joining_date)
    print("  -> Temp Address:", student.temporary_address)
    
    # Check ParadeState record
    from app.models.student import ParadeState
    ps = db.query(ParadeState).filter(ParadeState.student_id == student.id).first()
    print("  -> Initial Parade State created:", ps.status if ps else "NONE")
    
    # Verify count
    new_count = db.query(func.count(Student.id)).scalar()
    print("New student count:", new_count)
    
    # Clean up test student
    db.delete(student)
    db.commit()
    print("Test student removed (cleanup)")
    
except Exception as e:
    print("ERROR:", type(e).__name__, str(e))
    import traceback
    traceback.print_exc()
finally:
    db.close()
