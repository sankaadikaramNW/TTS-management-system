from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student
from app.models.accommodation import AccommodationBuilding
from app.models.user import User, Role
from app.models.notification import Notification

router = APIRouter(prefix="/public", tags=["Public Portal"])

@router.get("/stats")
def get_public_stats(db: Session = Depends(get_db)):
    # 1. Active Trainees count
    active_trainees = db.query(Student).filter(
        Student.deleted_at == None,
        Student.status == 'Active'
    ).count()

    # 2. Active Training Batches count
    active_batches = db.query(Student.batch).filter(
        Student.deleted_at == None,
        Student.status == 'Active'
    ).distinct().count()

    # 3. Instructors count
    instructors = db.query(User).join(Role).filter(
        User.deleted_at == None,
        User.is_active == True,
        Role.name == 'Instructor'
    ).count()

    # 4. Accommodation Buildings count
    buildings = db.query(AccommodationBuilding).filter(
        AccommodationBuilding.deleted_at == None
    ).count()

    return {
        "active_trainees": active_trainees,
        "active_batches": active_batches,
        "instructors": instructors,
        "buildings": buildings
    }

@router.get("/notices")
def get_public_notices(db: Session = Depends(get_db)):
    # Fetch public notices (notifications where user_id is None)
    notices = db.query(Notification).filter(
        Notification.user_id == None
    ).order_by(Notification.created_at.desc()).all()
    
    return [
        {
            "id": notice.id,
            "title": notice.title,
            "message": notice.message,
            "type": notice.type,
            "created_at": notice.created_at
        }
        for notice in notices
    ]
