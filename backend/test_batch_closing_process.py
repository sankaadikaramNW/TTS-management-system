import sys
import os
from datetime import date, datetime, timedelta

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.database import SessionLocal, engine, Base
from app.models.academic import Course, Batch, Classroom
from app.models.student import Student, Trade
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBunkBed, BedPosition, AccommodationAllocation
from app.models.user import User, Role, AuditLog
from app.services.batch_closing_service import batch_closing_service
from app.repositories.academic import course_repo

def run_tests():
    print("=" * 70)
    print("RUNNING AUTOMATED TEST: BATCH CLOSING / 'PASSED OUT' PROCESS")
    print("=" * 70)

    db = SessionLocal()
    try:
        # 1. Setup Test Trade
        test_trade = db.query(Trade).filter(Trade.code == "TEST_AIR").first()
        if not test_trade:
            test_trade = Trade(code="TEST_AIR", label="Test Airframe", is_active=True)
            db.add(test_trade)
            db.commit()
            db.refresh(test_trade)

        # 2. Setup Test Accommodation
        building = db.query(AccommodationBuilding).filter(AccommodationBuilding.name == "Test Hangar Bld").first()
        if not building:
            building = AccommodationBuilding(name="Test Hangar Bld", type="Airmen", capacity=20, current_occupancy=0)
            db.add(building)
            db.commit()
            db.refresh(building)

        billet = db.query(AccommodationBillet).filter(AccommodationBillet.name == "Test Billet 01").first()
        if not billet:
            billet = AccommodationBillet(building_id=building.id, name="Test Billet 01", capacity=10, current_occupancy=0)
            db.add(billet)
            db.commit()
            db.refresh(billet)

        bunk = db.query(AccommodationBunkBed).filter(AccommodationBunkBed.bunk_no == "TB-01").first()
        if not bunk:
            bunk = AccommodationBunkBed(billet_id=billet.id, bunk_no="TB-01", status="Active")
            db.add(bunk)
            db.commit()
            db.refresh(bunk)

        bed_pos = db.query(BedPosition).filter(BedPosition.position_code == "TB-01-TOP").first()
        if not bed_pos:
            bed_pos = BedPosition(bunk_bed_id=bunk.id, position_type="TOP", position_code="TB-01-TOP", status="Available")
            db.add(bed_pos)
            db.commit()
            db.refresh(bed_pos)

        # 3. Create Expired Course & Batch (End Date in the Past: 2026-01-01 to 2026-03-01)
        past_start = date(2026, 1, 1)
        past_end = date(2026, 3, 1)
        test_course_code = f"TEST-EXP-{int(datetime.utcnow().timestamp())}"
        
        course = Course(
            code=test_course_code,
            name="Test Expired Course Aircraft Assist",
            trade_id=test_trade.id,
            start_date=past_start,
            end_date=past_end,
            duration_weeks=8,
            status="ONGOING",
            is_active=True
        )
        db.add(course)
        db.commit()
        db.refresh(course)

        batch_name = f"Batch-{test_course_code}"
        batch = Batch(
            name=batch_name,
            course_id=course.id,
            trade_id=test_trade.id,
            intake_date=past_start,
            passing_out_date=past_end,
            status="Active"
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)

        # 4. Create Enrolled Student
        student_svc_no = f"S-{int(datetime.utcnow().timestamp())}"
        student = Student(
            service_number=student_svc_no,
            full_name="Test Trainee Expiration",
            course_id=course.id,
            batch=batch.name,
            status="Active"
        )
        db.add(student)
        db.commit()
        db.refresh(student)

        # 5. Allocate Student to Bed Position
        bed_pos.status = "Occupied"
        alloc = AccommodationAllocation(
            student_id=student.id,
            bed_position_id=bed_pos.id,
            allocated_at=datetime.utcnow(),
            status="Active"
        )
        db.add(alloc)
        db.commit()

        print("\n[PRE-CHECK] Initial State Verified:")
        print(f"  Course: {course.code} (Status: {course.status}, IsActive: {course.is_active}, EndDate: {course.end_date})")
        print(f"  Batch: {batch.name} (Status: {batch.status}, PassingOutDate: {batch.passing_out_date})")
        print(f"  Student: {student.service_number} (Status: {student.status})")
        print(f"  Bed Position: {bed_pos.position_code} (Status: {bed_pos.status})")
        print(f"  Allocation: {alloc.id} (Status: {alloc.status})")

        # 6. Execute Batch Closing Process
        print("\n[EXECUTION] Running batch_closing_service.close_expired_batches()...")
        result = batch_closing_service.close_expired_batches(db)
        print(f"  Result summary: {result}")

        # 7. Verification Assertions
        db.expire_all()
        updated_course = db.query(Course).filter(Course.id == course.id).first()
        updated_batch = db.query(Batch).filter(Batch.id == batch.id).first()
        updated_student = db.query(Student).filter(Student.id == student.id).first()
        updated_bed_pos = db.query(BedPosition).filter(BedPosition.id == bed_pos.id).first()
        updated_alloc = db.query(AccommodationAllocation).filter(AccommodationAllocation.id == alloc.id).first()

        print("\n[POST-CHECK] Validating Results:")
        print(f"  Course Status: {updated_course.status} (Expected: PASSED OUT)")
        print(f"  Course IsActive: {updated_course.is_active} (Expected: False)")
        print(f"  Batch Status: {updated_batch.status} (Expected: PASSED OUT)")
        print(f"  Student Status: {updated_student.status} (Expected: Passed Out)")
        print(f"  Bed Position Status: {updated_bed_pos.status} (Expected: Available)")
        print(f"  Allocation Status: {updated_alloc.status} (Expected: History)")
        print(f"  Allocation Vacate Reason: {updated_alloc.vacate_reason}")

        assert updated_course.status == "PASSED OUT", f"Course status is {updated_course.status}"
        assert updated_course.is_active == False, f"Course is_active is {updated_course.is_active}"
        assert updated_batch.status == "PASSED OUT", f"Batch status is {updated_batch.status}"
        assert updated_student.status == "Passed Out", f"Student status is {updated_student.status}"
        assert updated_bed_pos.status == "Available", f"Bed position status is {updated_bed_pos.status}"
        assert updated_alloc.status == "History", f"Allocation status is {updated_alloc.status}"
        assert updated_alloc.vacated_at is not None, "Allocation vacated_at should be set"

        # 8. Verify Enrollment Options Exclusion
        enrollment_options = course_repo.get_enrollment_options(db)
        enrolled_ids = [opt["course_id"] for opt in enrollment_options]
        assert course.id not in enrolled_ids, "Passed out course must NOT appear in enrollment options"
        print(f"  [PASSED] Passed-out course excluded from active Course Enrollment options.")

        # 9. Verify Audit Log
        audit_entry = db.query(AuditLog).filter(
            AuditLog.action == "AUTOMATIC_BATCH_CLOSURE",
            AuditLog.details.like(f"%{course.code}%")
        ).first()
        assert audit_entry is not None, "Audit log entry should exist for automatic batch closure"
        print(f"  [PASSED] Audit log verified: {audit_entry.details}")

        # 10. Verify Idempotency
        print("\n[IDEMPOTENCY] Running batch_closing_service a second time...")
        second_result = batch_closing_service.close_expired_batches(db)
        print(f"  Second run summary: {second_result}")
        assert second_result["closed_courses_count"] == 0, "Second run should not re-close courses"
        print("  [PASSED] Idempotency confirmed: No duplicate closures or errors on re-run.")

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED SUCCESSFULLY! (10/10 Verification Checks)")
        print("=" * 70)

    finally:
        db.close()

if __name__ == "__main__":
    run_tests()
