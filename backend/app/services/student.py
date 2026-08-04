import io
import base64
import qrcode
from datetime import date
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.student import Student
from app.repositories.student import student_repo
from app.repositories.user import audit_repo
from app.schemas.student import StudentCreate, StudentUpdate

class StudentService:
    def create_student(self, db: Session, student_in: StudentCreate, user_id: str, ip: str, ua: str) -> Student:
        # Check duplicate service number
        if student_repo.get_by_service_number(db, student_in.service_number):
            raise HTTPException(status_code=400, detail=f"Student with Service Number '{student_in.service_number}' already exists")
            
        # Check duplicate NIC
        if student_repo.get_by_nic(db, student_in.nic):
            raise HTTPException(status_code=400, detail=f"Student with NIC '{student_in.nic}' already exists")

        # Generate QR code representation
        qr_base64 = self.generate_student_qr(student_in.service_number)

        db_student = Student(
            service_number=student_in.service_number,
            initials=student_in.initials,
            full_name=student_in.full_name,
            nic=student_in.nic,
            dob=student_in.dob,
            gender=student_in.gender,
            rank=student_in.rank,
            trade=student_in.trade,
            course_id=student_in.course_id,
            batch=student_in.batch,
            squadron=student_in.squadron or "Training Squadron",
            unit=student_in.unit or "SLAF TTS Ekala",
            posting=student_in.posting,
            joining_date=student_in.joining_date or date.today(),
            passing_out_date=student_in.passing_out_date,
            status=student_in.status or "Active",
            phone=student_in.phone,
            email=student_in.email,
            emergency_contact_name=student_in.emergency_contact_name,
            emergency_contact_phone=student_in.emergency_contact_phone,
            blood_group=student_in.blood_group,
            medical_category=student_in.medical_category or "A4G4",
            religion=student_in.religion,
            nationality=student_in.nationality or "Sri Lankan",
            permanent_address=student_in.permanent_address,
            temporary_address=student_in.temporary_address,
            qr_code_data=qr_base64
        )

        student = student_repo.create(db, obj_in=db_student)
        
        # Record initial parade state for registration date
        from app.repositories.parade import parade_repo
        parade_repo.create_or_update(
            db,
            student_id=student.id,
            parade_date=student.joining_date,
            status=student.status or "Present",
            remarks="Initial registration record",
            user_id=user_id
        )

        audit_repo.create_log(
            db, user_id, "STUDENT_CREATED", ip, ua, 
            f"Created student record {student.service_number} ({student.full_name})"
        )
        return student

    def update_student(self, db: Session, student_id: str, student_in: StudentUpdate, user_id: str, ip: str, ua: str) -> Student:
        student = student_repo.get(db, student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Student record not found")

        # NIC duplicate check
        if student_in.nic and student_in.nic != student.nic:
            if student_repo.get_by_nic(db, student_in.nic):
                raise HTTPException(status_code=400, detail=f"Another student with NIC '{student_in.nic}' already exists")

        # Status changes trigger audits
        status_change = ""
        if student_in.status and student_in.status != student.status:
            status_change = f"Status changed from {student.status} to {student_in.status}"
            student.status = student_in.status

        updated_student = student_repo.update(db, db_obj=student, obj_in=student_in)
        audit_repo.create_log(
            db, user_id, "STUDENT_UPDATED", ip, ua, 
            f"Updated student record {updated_student.service_number}. {status_change}"
        )
        return updated_student

    def delete_student(self, db: Session, student_id: str, user_id: str, ip: str, ua: str) -> Student:
        student = student_repo.get(db, student_id)
        if not student or student.deleted_at:
            raise HTTPException(status_code=404, detail="Student record not found")

        deleted_student = student_repo.remove(db, id=student_id)
        audit_repo.create_log(
            db, user_id, "STUDENT_DELETED", ip, ua, 
            f"Soft-deleted student record {student.service_number} ({student.full_name})"
        )
        return deleted_student

    def generate_student_qr(self, service_number: str) -> str:
        # Generate base64 data URL representing QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        # Validation payload contains Service Number
        qr.add_data(f"SLAF_TTS_VALIDATION:{service_number}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_str}"

student_service = StudentService()
