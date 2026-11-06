import logging
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.student import Student
from app.models.accommodation import AccommodationBuilding
from app.models.user import User, Role
from app.models.notification import Notification
from app.models.academic import Batch
from app.repositories.academic import instructor_repo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/public", tags=["Public Portal"])

# Trainees who have finished training or left are excluded from active count
INACTIVE_STUDENT_STATUSES = [
    'Passed Out', 'PASSED OUT', 'passed out',
    'Discharged', 'discharged',
    'Struck Off', 'struck off',
    'Inactive', 'inactive'
]

@router.get("/stats")
def get_public_stats(response: Response, db: Session = Depends(get_db)):
    # Ensure responses are never cached by browsers, CDN, or proxies for live data
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    try:
        # 1. Active Trainees count
        # In SLAF TTS, active trainees are all enrolled students (status can be 'Active', 'Present',
        # 'Sick Report', 'Leave', 'Hospital', 'AWOL', etc.) who are not passed out or discharged.
        active_trainees = db.query(Student).filter(
            Student.deleted_at.is_(None),
            ~Student.status.in_(INACTIVE_STUDENT_STATUSES)
        ).count()

        # Fallback if student statuses are uninitialized or null
        if active_trainees == 0:
            active_trainees = db.query(Student).filter(
                Student.deleted_at.is_(None)
            ).count()

        # 2. Active Training Batches count
        # Count from formal Batch records or distinct batches associated with active trainees
        batch_table_count = db.query(Batch).filter(
            Batch.deleted_at.is_(None),
            func.lower(Batch.status).notin_(['completed', 'archived', 'passed out'])
        ).count()

        student_batch_count = db.query(Student.batch).filter(
            Student.deleted_at.is_(None),
            ~Student.status.in_(INACTIVE_STUDENT_STATUSES),
            Student.batch.isnot(None),
            Student.batch != '',
            Student.batch != 'N/A',
            Student.batch != '-'
        ).distinct().count()

        active_batches = max(batch_table_count, student_batch_count)

        # 3. Instructors count
        # Query from SSOT User management using role & designation criteria
        instructors_list = instructor_repo.get_instructors(db)
        instructors = len(instructors_list)
        if instructors == 0:
            instructors = db.query(User).join(Role, User.role_id == Role.id, isouter=True).filter(
                User.deleted_at.is_(None),
                User.is_active == True,
                (Role.name == 'Instructor') | (Role.id == 'role-instructor')
            ).count()

        # 4. Accommodation Buildings count
        buildings = db.query(AccommodationBuilding).filter(
            AccommodationBuilding.deleted_at.is_(None)
        ).count()

        return {
            "active_trainees": active_trainees,
            "active_batches": active_batches,
            "instructors": instructors,
            "buildings": buildings
        }
    except Exception as e:
        logger.error(f"Error fetching public stats: {e}")
        return {
            "active_trainees": 0,
            "active_batches": 0,
            "instructors": 0,
            "buildings": 0
        }

@router.get("/notices")
def get_public_notices(response: Response, db: Session = Depends(get_db)):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    try:
        # Fetch public notices (notifications where user_id is None)
        notices = db.query(Notification).filter(
            Notification.user_id.is_(None)
        ).order_by(Notification.created_at.desc()).all()
        
        return [
            {
                "id": notice.id,
                "title": notice.title,
                "message": notice.message,
                "type": notice.type or "INFO",
                "created_at": notice.created_at.isoformat() if notice.created_at else None
            }
            for notice in notices
        ]
    except Exception as e:
        logger.error(f"Error fetching public notices: {e}")
        return []

