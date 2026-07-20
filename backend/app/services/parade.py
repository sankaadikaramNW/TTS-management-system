from datetime import date, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.student import Student
from app.models.academic import Timetable, AcademicAttendance
from app.models.notification import Notification
from app.repositories.parade import parade_repo
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.parade import DailyParadeUpdateRequest

class ParadeStateService:
    def update_daily_parade(self, db: Session, update_data: DailyParadeUpdateRequest, user_id: str, ip: str, ua: str) -> dict:
        parade_date = update_data.date
        records = update_data.records
        
        updated_count = 0
        for rec in records:
            student = student_repo.get(db, rec.student_id)
            if not student or student.deleted_at:
                continue

            # Update master Student status (SSOT Sync)
            old_status = student.status
            student.status = rec.status
            
            # Record Parade State log
            parade_repo.create_or_update(
                db, 
                student_id=rec.student_id, 
                parade_date=parade_date, 
                status=rec.status, 
                remarks=rec.remarks,
                user_id=user_id
            )
            
            # SSOT Dependency Sync 1: Academic Attendance
            # If student is NOT Present (e.g. Leave, Sick, AWOL), automatically mark any timetable periods for today as Absent or Excused
            if rec.status != "Present":
                attendance_status = "Excused"
                if rec.status in ["AWOL"]:
                    attendance_status = "Absent"
                
                # Find all timetables for this student's course today
                if student.course_id:
                    today_timetables = db.query(Timetable).filter(
                        Timetable.course_id == student.course_id,
                        Timetable.date == parade_date
                    ).all()
                    
                    for tt in today_timetables:
                        # Check if attendance already exists
                        att_record = db.query(AcademicAttendance).filter(
                            AcademicAttendance.timetable_id == tt.id,
                            AcademicAttendance.student_id == student.id
                        ).first()
                        
                        if att_record:
                            att_record.status = attendance_status
                            att_record.remarks = f"Auto-synced from Parade State: {rec.status}"
                        else:
                            new_att = AcademicAttendance(
                                timetable_id=tt.id,
                                student_id=student.id,
                                status=attendance_status,
                                remarks=f"Auto-synced from Parade State: {rec.status}"
                            )
                            db.add(new_att)

            # SSOT Dependency Sync 2: Send system warning notifications for critical statuses like AWOL or Hospital
            if rec.status in ["AWOL", "Hospital"] and old_status != rec.status:
                admin_users = db.query(Student).filter(Student.deleted_at == None).all() # (Just generic notification context)
                # Query all admin/CO role users to notify them
                from app.models.user import User, Role
                notif_users = db.query(User).join(User.role).filter(Role.name.in_(["Super Administrator", "Commanding Officer"])).all()
                for admin in notif_users:
                    notif = Notification(
                        user_id=admin.id,
                        title=f"CRITICAL STATE ALERT: {student.rank} {student.full_name}",
                        message=f"Student {student.service_number} is reported as '{rec.status}' on {parade_date}. Parade remarks: {rec.remarks or 'None'}",
                        type="ALERT"
                    )
                    db.add(notif)
            
            updated_count += 1

        db.commit()
        
        audit_repo.create_log(
            db, user_id, "PARADE_STATE_BATCH_UPDATE", ip, ua, 
            f"Batch-updated parade states for {updated_count} students on date {parade_date}"
        )
        
        return {"status": "success", "updated_count": updated_count}

parade_service = ParadeStateService()
