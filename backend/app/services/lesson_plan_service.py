"""
Lesson Plan Document Service
Handles PDF validation, Cloudinary upload/replace/delete, and CRUD business logic.
"""
import os
from datetime import datetime
from typing import Optional, Tuple
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

import cloudinary
import cloudinary.uploader
import cloudinary.api

from app.config import settings
from app.models.academic import LessonPlanDocument, Course
from app.repositories.academic import lesson_plan_doc_repo
from app.repositories.user import audit_repo


# --- Cloudinary Initialization ---
def _init_cloudinary():
    """Initialize Cloudinary SDK with environment configuration."""
    if not settings.CLOUDINARY_CLOUD_NAME:
        raise HTTPException(
            status_code=500,
            detail="Cloudinary is not configured. Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET."
        )
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )


# Allowed MIME types sent by various OS/browsers for PDF files
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/x-pdf",
    "application/acrobat",
    "applications/vnd.pdf",
    "text/pdf",
    "application/octet-stream",
    "binary/octet-stream"
}
ALLOWED_EXTENSIONS = {".pdf"}
PDF_MAGIC_BYTES = b"%PDF-"


class LessonPlanService:
    """Core business logic for Lesson Plan Document management."""

    def validate_pdf(self, file: UploadFile, file_bytes: bytes) -> None:
        """
        Backend-only PDF validation.
        Checks: extension, MIME type, file size, and PDF magic header bytes.
        Raises HTTPException on failure.
        """
        # 1. Validate file extension
        if file.filename:
            _, ext = os.path.splitext(file.filename.lower())
            if ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Only PDF lesson plan documents are allowed. Received file with extension '{ext}'."
                )

        # 2. Validate MIME / content type (flexible for browser variations)
        content_type = (file.content_type or "").split(";")[0].strip().lower()
        if content_type and content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF lesson plan documents are allowed. Received content type '{file.content_type}'."
            )

        # 3. Validate file size
        max_size = settings.MAX_LESSON_PLAN_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        if len(file_bytes) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the maximum allowed size of {settings.MAX_LESSON_PLAN_FILE_SIZE_MB} MB."
            )

        if len(file_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        # 4. Validate PDF magic header (%PDF- anywhere in first 1024 bytes)
        if PDF_MAGIC_BYTES not in file_bytes[:1024]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF lesson plan documents are allowed. The uploaded file does not have a valid PDF structure."
            )

    def upload_to_cloudinary(self, file_bytes: bytes, filename: str) -> Tuple[str, str]:
        """
        Upload PDF bytes to Cloudinary.
        Returns: (public_id, secure_url)
        """
        _init_cloudinary()

        # Use raw resource type for non-image/video files (PDFs)
        # Place in a dedicated folder for organization
        try:
            result = cloudinary.uploader.upload(
                file_bytes,
                resource_type="auto",
                folder="tts-lesson-plans",
                public_id=f"{os.path.splitext(filename)[0]}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                overwrite=False,
                use_filename=True,
                unique_filename=True
            )
            return result["public_id"], result["secure_url"]
        except Exception as e:
            err_msg = str(e)
            if "Invalid Signature" in err_msg or "AuthorizationRequired" in type(e).__name__:
                raise HTTPException(
                    status_code=400,
                    detail="Cloudinary Authentication Failed: Invalid CLOUDINARY_API_SECRET in your .env file. Please update CLOUDINARY_API_SECRET with your secret key from your Cloudinary dashboard."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to cloud storage: {err_msg}"
            )

    def delete_from_cloudinary(self, public_id: str) -> bool:
        """Remove a resource from Cloudinary by public_id."""
        _init_cloudinary()
        try:
            result = cloudinary.uploader.destroy(public_id, resource_type="raw")
            return result.get("result") == "ok"
        except Exception:
            return False  # Non-fatal: log but don't block the operation

    # --- CRUD Operations ---

    def create_document(
        self,
        db: Session,
        file: UploadFile,
        course_id: str,
        title: str,
        user_id: str,
        lesson_id: Optional[str] = None,
        subject_name: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        academic_year: Optional[str] = None,
        remarks: Optional[str] = None,
        ip: str = "unknown",
        ua: str = "unknown"
    ) -> LessonPlanDocument:
        """Validate PDF → Upload to Cloudinary → Save DB record → Audit log."""

        # Verify the course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="The selected course does not exist.")

        # Read file bytes
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    file_bytes = pool.submit(lambda: file.file.read()).result()
            else:
                file_bytes = file.file.read()
        except Exception:
            file_bytes = file.file.read()

        # Validate PDF
        self.validate_pdf(file, file_bytes)

        # Upload to Cloudinary
        public_id, secure_url = self.upload_to_cloudinary(file_bytes, file.filename or "lesson_plan.pdf")

        # Verify foreign keys before inserting to prevent MySQL IntegrityError 1452
        from app.models.user import User
        from app.models.academic import Lesson
        uploader = db.query(User).filter(User.id == user_id).first() if user_id else None
        valid_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first() if lesson_id else None

        # Create database record
        doc = LessonPlanDocument(
            course_id=course_id,
            lesson_id=valid_lesson.id if valid_lesson else None,
            title=title,
            description=description,
            subject_name=subject_name,
            version=version,
            academic_year=academic_year,
            remarks=remarks,
            original_file_name=file.filename or "lesson_plan.pdf",
            cloudinary_public_id=public_id,
            cloudinary_url=secure_url,
            resource_type="raw",
            file_size=len(file_bytes),
            mime_type=file.content_type or "application/pdf",
            uploaded_by=uploader.id if uploader else None,
            status="Active"
        )
        created_doc = lesson_plan_doc_repo.create(db, obj_in=doc)

        # Audit log
        audit_repo.create_log(
            db, user_id, "LESSON_PLAN_UPLOADED", ip, ua,
            details=f"Uploaded lesson plan '{title}' for course {course.name} (ID: {course.code})",
            module="Academic"
        )

        return created_doc

    def update_metadata(
        self,
        db: Session,
        doc_id: str,
        update_data: dict,
        user_id: str,
        ip: str = "unknown",
        ua: str = "unknown"
    ) -> LessonPlanDocument:
        """Update document metadata without re-uploading the PDF."""
        doc = lesson_plan_doc_repo.get_by_id(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Lesson plan document not found.")

        for field, val in update_data.items():
            if val is not None and hasattr(doc, field):
                setattr(doc, field, val)

        doc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(doc)

        audit_repo.create_log(
            db, user_id, "LESSON_PLAN_UPDATED", ip, ua,
            details=f"Updated metadata for lesson plan '{doc.title}' (ID: {doc.id})",
            module="Academic"
        )

        return lesson_plan_doc_repo.get_by_id(db, doc_id)

    def replace_document(
        self,
        db: Session,
        doc_id: str,
        new_file: UploadFile,
        user_id: str,
        ip: str = "unknown",
        ua: str = "unknown"
    ) -> LessonPlanDocument:
        """
        Replace the PDF file for an existing document.
        Upload new file first, then update DB, then delete old Cloudinary resource.
        """
        doc = lesson_plan_doc_repo.get_by_id(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Lesson plan document not found.")

        # Read and validate new file
        file_bytes = new_file.file.read()
        self.validate_pdf(new_file, file_bytes)

        # Upload new file to Cloudinary FIRST (safe order)
        new_public_id, new_secure_url = self.upload_to_cloudinary(
            file_bytes, new_file.filename or "lesson_plan.pdf"
        )

        # Save old Cloudinary reference for cleanup
        old_public_id = doc.cloudinary_public_id

        # Update database record
        doc.cloudinary_public_id = new_public_id
        doc.cloudinary_url = new_secure_url
        doc.original_file_name = new_file.filename or "lesson_plan.pdf"
        doc.file_size = len(file_bytes)
        doc.mime_type = new_file.content_type or "application/pdf"
        doc.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(doc)

        # Delete old Cloudinary resource (after successful update)
        self.delete_from_cloudinary(old_public_id)

        audit_repo.create_log(
            db, user_id, "LESSON_PLAN_REPLACED", ip, ua,
            details=f"Replaced PDF for lesson plan '{doc.title}' (ID: {doc.id})",
            module="Academic"
        )

        return lesson_plan_doc_repo.get_by_id(db, doc_id)

    def archive_document(
        self,
        db: Session,
        doc_id: str,
        user_id: str,
        ip: str = "unknown",
        ua: str = "unknown"
    ) -> LessonPlanDocument:
        """Soft-delete / archive a document."""
        doc = lesson_plan_doc_repo.get_by_id(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Lesson plan document not found.")

        doc.status = "Archived"
        doc.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(doc)

        audit_repo.create_log(
            db, user_id, "LESSON_PLAN_ARCHIVED", ip, ua,
            details=f"Archived lesson plan '{doc.title}' (ID: {doc.id})",
            module="Academic"
        )

        return lesson_plan_doc_repo.get_by_id(db, doc_id)

    def delete_document(
        self,
        db: Session,
        doc_id: str,
        user_id: str,
        ip: str = "unknown",
        ua: str = "unknown"
    ) -> dict:
        """Permanently delete a document (admin-level). Removes from Cloudinary and DB."""
        doc = lesson_plan_doc_repo.get_by_id(db, doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Lesson plan document not found.")

        title = doc.title
        public_id = doc.cloudinary_public_id

        # Remove from database
        db.delete(doc)
        db.commit()

        # Remove from Cloudinary
        self.delete_from_cloudinary(public_id)

        audit_repo.create_log(
            db, user_id, "LESSON_PLAN_DELETED", ip, ua,
            details=f"Permanently deleted lesson plan '{title}' (ID: {doc_id})",
            module="Academic"
        )

        return {"message": f"Lesson plan '{title}' has been permanently deleted."}


lesson_plan_service = LessonPlanService()
