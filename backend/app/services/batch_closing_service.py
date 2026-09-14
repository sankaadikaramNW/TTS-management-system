import asyncio
import logging
from datetime import date, datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.academic import Course, Batch, Classroom
from app.models.student import Student
from app.models.accommodation import AccommodationAllocation, BedPosition, AccommodationBed
from app.models.user import AuditLog
from app.services.accommodation import accommodation_service

logger = logging.getLogger("batch_closing_service")


class BatchClosingService:
    """
    Automated and High-Performance Batch Closing / 'Passed Out' Service.
    
    Authoritative Business Rule:
    Uses Course End Date / Batch Passing Out Date as the single source of truth.
    When End Date < Current Date, active courses and batches automatically move to
    'PASSED OUT' status. All historical records are strictly preserved while active
    operational workflows are kept fast and isolated.
    """

    def close_expired_batches(
        self,
        db: Session,
        target_date: Optional[date] = None,
        user_id: Optional[str] = None,
        chunk_size: int = 100,
        ip: str = "127.0.0.1",
        ua: str = "System Automated Batch Task"
    ) -> Dict[str, Any]:
        """
        Targeted, high-performance batch closing process.
        Executes in transactional chunks without full-table memory loading.
        """
        today = target_date or date.today()

        # 1. Targeted Database Query: Identify ONLY expired active courses
        expired_courses_query = db.query(Course.id, Course.code, Course.name, Course.end_date, Course.status).filter(
            Course.deleted_at == None,
            Course.end_date != None,
            Course.end_date < today,
            or_(
                Course.status.in_(['ONGOING', 'Active', 'UPCOMING', 'ACTIVE']),
                Course.status == None
            )
        )
        expired_courses = expired_courses_query.all()
        expired_course_ids = [c.id for c in expired_courses]

        # 2. Targeted Database Query: Identify ONLY expired active batches
        expired_batches_query = db.query(Batch.id, Batch.name, Batch.course_id, Batch.passing_out_date, Batch.status).filter(
            Batch.deleted_at == None,
            or_(
                and_(Batch.passing_out_date != None, Batch.passing_out_date < today),
                Batch.course_id.in_(expired_course_ids)
            ),
            Batch.status.in_(['Active', 'ONGOING', 'UPCOMING', 'ACTIVE'])
        )
        expired_batches = expired_batches_query.all()

        if not expired_courses and not expired_batches:
            return {
                "message": "No expired active batches or courses found.",
                "target_date": today,
                "closed_courses_count": 0,
                "closed_batches_count": 0,
                "affected_students_count": 0,
                "vacated_allocations_count": 0,
                "closed_course_codes": [],
                "closed_batch_names": []
            }

        total_closed_courses = 0
        total_closed_batches = 0
        total_affected_students = 0
        total_vacated_allocations = 0
        closed_course_codes: List[str] = []
        closed_batch_names: List[str] = []

        # 3. Chunked Processing for Courses
        course_chunks = [expired_courses[i:i + chunk_size] for i in range(0, len(expired_courses), chunk_size)]
        for chunk in course_chunks:
            chunk_course_ids = [c.id for c in chunk]
            try:
                # Update course statuses to 'PASSED OUT'
                db_courses = db.query(Course).filter(Course.id.in_(chunk_course_ids)).all()
                for course in db_courses:
                    prev_status = course.status or "ONGOING"
                    course.status = "PASSED OUT"
                    course.is_active = False
                    total_closed_courses += 1
                    closed_course_codes.append(course.code)

                    # Audit log for course closure
                    audit = AuditLog(
                        user_id=user_id,
                        username="System Scheduler",
                        module="Academic Management",
                        action="AUTOMATIC_BATCH_CLOSURE",
                        previous_value=f"Status: {prev_status}",
                        new_value="Status: PASSED OUT",
                        ip_address=ip,
                        user_agent=ua,
                        details=(
                            f"Course '{course.code} - {course.name}' automatically closed and moved to PASSED OUT state. "
                            f"Course End Date ({course.end_date}) has passed as of {today}."
                        ),
                        created_at=datetime.utcnow()
                    )
                    db.add(audit)

                db.commit()
            except Exception as e:
                db.rollback()
                logger.error(f"Error during course closing chunk processing: {e}")

        # 4. Chunked Processing for Batches and related Trainees / Accommodation
        batch_chunks = [expired_batches[i:i + chunk_size] for i in range(0, len(expired_batches), chunk_size)]
        for chunk in batch_chunks:
            chunk_batch_ids = [b.id for b in chunk]
            chunk_batch_names = [b.name for b in chunk]
            chunk_batch_course_ids = [b.course_id for b in chunk if b.course_id]

            try:
                # Update batch statuses to 'PASSED OUT'
                db_batches = db.query(Batch).filter(Batch.id.in_(chunk_batch_ids)).all()
                for batch in db_batches:
                    prev_status = batch.status or "Active"
                    batch.status = "PASSED OUT"
                    total_closed_batches += 1
                    closed_batch_names.append(batch.name)

                    # Audit log for batch closure
                    audit = AuditLog(
                        user_id=user_id,
                        username="System Scheduler",
                        module="Academic Management",
                        action="AUTOMATIC_BATCH_CLOSURE",
                        previous_value=f"Status: {prev_status}",
                        new_value="Status: PASSED OUT",
                        ip_address=ip,
                        user_agent=ua,
                        details=(
                            f"Batch '{batch.name}' automatically closed and moved to PASSED OUT state. "
                            f"Course End Date / Passing Out Date ({batch.passing_out_date}) has passed as of {today}."
                        ),
                        created_at=datetime.utcnow()
                    )
                    db.add(audit)

                # 5. Transition Enrolled Trainees to 'Passed Out'
                students_to_update = db.query(Student).filter(
                    Student.deleted_at == None,
                    Student.status != "Passed Out",
                    or_(
                        Student.course_id.in_(chunk_batch_course_ids),
                        Student.batch.in_(chunk_batch_names)
                    )
                ).all()

                affected_student_ids = [s.id for s in students_to_update]
                for student in students_to_update:
                    student.status = "Passed Out"
                    if not student.passing_out_date:
                        student.passing_out_date = today
                    total_affected_students += 1

                # 6. Release Active Accommodation Allocations
                if affected_student_ids:
                    active_allocations = db.query(AccommodationAllocation).filter(
                        AccommodationAllocation.student_id.in_(affected_student_ids),
                        AccommodationAllocation.status == "Active"
                    ).all()

                    affected_billet_ids = set()
                    for alloc in active_allocations:
                        alloc.status = "History"
                        alloc.vacated_at = datetime.utcnow()
                        alloc.vacated_by = user_id
                        alloc.vacate_reason = "Course/Batch Passed Out"
                        alloc.remarks = f"Automatically vacated upon course/batch completion on {today}."
                        total_vacated_allocations += 1

                        if alloc.bed_position_id:
                            pos = db.query(BedPosition).filter(BedPosition.id == alloc.bed_position_id).first()
                            if pos:
                                pos.status = "Available"
                                if pos.bunk_bed and pos.bunk_bed.billet_id:
                                    affected_billet_ids.add(pos.bunk_bed.billet_id)

                        if alloc.bed_id:
                            bed = db.query(AccommodationBed).filter(AccommodationBed.id == alloc.bed_id).first()
                            if bed:
                                bed.status = "Vacant"
                                if bed.billet_id:
                                    affected_billet_ids.add(bed.billet_id)

                    db.commit()

                    # Synchronize billet and building occupancy counts
                    for billet_id in affected_billet_ids:
                        try:
                            accommodation_service._sync_occupancies(db, billet_id)
                        except Exception as e:
                            logger.warning(f"Failed to sync occupancy for billet {billet_id}: {e}")

                db.commit()
            except Exception as e:
                db.rollback()
                logger.error(f"Error during batch closing chunk processing: {e}")

        logger.info(
            f"[BatchClosingService] Successfully processed closures: "
            f"{total_closed_courses} courses, {total_closed_batches} batches, "
            f"{total_affected_students} trainees updated, {total_vacated_allocations} accommodation allocations vacated."
        )

        return {
            "message": f"Successfully closed {total_closed_courses} expired course(s) and {total_closed_batches} batch(es).",
            "target_date": today,
            "closed_courses_count": total_closed_courses,
            "closed_batches_count": total_closed_batches,
            "affected_students_count": total_affected_students,
            "vacated_allocations_count": total_vacated_allocations,
            "closed_course_codes": closed_course_codes,
            "closed_batch_names": closed_batch_names
        }


batch_closing_service = BatchClosingService()


async def run_batch_closing_scheduler(interval_seconds: int = 86400):
    """
    Background worker that runs batch closure check on startup and then
    periodically (default once daily).
    """
    logger.info("[BatchClosingScheduler] Background task initialized.")
    while True:
        try:
            db = SessionLocal()
            try:
                logger.info("[BatchClosingScheduler] Executing scheduled expiration check...")
                result = batch_closing_service.close_expired_batches(db)
                if result["closed_courses_count"] > 0 or result["closed_batches_count"] > 0:
                    logger.info(f"[BatchClosingScheduler] Completed with updates: {result['message']}")
                else:
                    logger.info("[BatchClosingScheduler] No expired batches to close at this time.")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"[BatchClosingScheduler] Unexpected error during execution: {e}")

        # Sleep until next scheduled run (24 hours by default)
        await asyncio.sleep(interval_seconds)
