from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.student import Student, ParadeState
from app.models.accommodation import AccommodationBed
from app.models.academic import Course, Timetable, ExamMark
from app.models.user import AuditLog, User
from app.repositories.parade import parade_repo

class DashboardService:
    def get_summary(self, db: Session) -> dict:
        today = date.today()
        
        # 1. Live Parade Strength (Auto default unrecorded to 'Present')
        parade_summary = parade_repo.get_summary(db, today)
        live_parade = {
            "total_enrolled": parade_summary["total_strength"],
            "present": parade_summary["present"],
            "sick_report": parade_summary["sick_report"],
            "hospital": parade_summary["hospital"],
            "leave": parade_summary["leave"],
            "temp_duty": parade_summary["temp_duty"],
            "course_visit": parade_summary["course_visit"],
            "detached_duty": parade_summary["detached_duty"],
            "awol": parade_summary["awol"]
        }

        # 2. Accommodation Stats
        total_beds = db.query(AccommodationBed).filter(AccommodationBed.deleted_at == None).count()
        occupied_beds = db.query(AccommodationBed).filter(AccommodationBed.deleted_at == None, AccommodationBed.status == "Occupied").count()
        maintenance_beds = db.query(AccommodationBed).filter(AccommodationBed.deleted_at == None, AccommodationBed.status == "Maintenance").count()
        vacant_beds = total_beds - occupied_beds - maintenance_beds
        
        occupancy_rate = 0.0
        if total_beds > 0:
            occupancy_rate = round((occupied_beds / total_beds) * 100, 2)
            
        accommodation_stats = {
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "vacant_beds": vacant_beds,
            "maintenance_beds": maintenance_beds,
            "occupancy_rate": occupancy_rate
        }

        # 3. Academic Stats
        course_count = db.query(Course).filter(Course.deleted_at == None).count()
        timetables_today = db.query(Timetable).filter(Timetable.date == today).count()
        
        # Calculate overall pass rate from exam marks
        total_marks = db.query(ExamMark).count()
        pass_marks = db.query(ExamMark).filter(ExamMark.status == "Pass").count()
        pass_rate = 0.0
        if total_marks > 0:
            pass_rate = round((pass_marks / total_marks) * 100, 2)
            
        academic_stats = {
            "course_count": course_count,
            "average_pass_rate": pass_rate,
            "active_timetables_today": timetables_today
        }

        # 4. Recent Actions Audit log list
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(8).all()
        recent_activities = []
        for log in logs:
            user = db.query(User).filter(User.id == log.user_id).first()
            recent_activities.append({
                "id": log.id,
                "username": user.username if user else "System",
                "action": log.action,
                "details": log.details,
                "created_at": log.created_at
            })

        return {
            "parade": live_parade,
            "accommodation": accommodation_stats,
            "academic": academic_stats,
            "recent_activities": recent_activities
        }

dashboard_service = DashboardService()
