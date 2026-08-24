from datetime import date
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, Request, Response, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, PermissionChecker
from app.models.user import User
from app.schemas.reports import (
    StandardReportResponse, ReportFilterMetaResponse, ReportExportRequest
)
from app.services.report_service import report_service

router = APIRouter(prefix="/reports", tags=["Enterprise Reporting System"])


# ─────────────────────────────────────────────────────────────
# 1. Filter Metadata
# ─────────────────────────────────────────────────────────────
@router.get("/meta/filters", response_model=ReportFilterMetaResponse, summary="Get master data for report filter dropdowns")
def get_report_filters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return report_service.get_filter_metadata(db)


# ─────────────────────────────────────────────────────────────
# 2. Student Dossier Report
# ─────────────────────────────────────────────────────────────
@router.get("/students", response_model=StandardReportResponse, summary="Compile Student Personal Dossiers Report")
def get_student_report(
    request: Request,
    trade: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    batch: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    squadron: Optional[str] = Query(None),
    rank: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_student_report(
        db, current_user, trade=trade, course_id=course_id, batch=batch,
        status=status, squadron=squadron, rank=rank, search=search, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 3. Parade State Strength Report
# ─────────────────────────────────────────────────────────────
@router.get("/parade-state", response_model=StandardReportResponse, summary="Compile Trade Parade State & Strength Report")
def get_parade_report(
    request: Request,
    parade_date: Optional[date] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    trade: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    approval_status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_parade_report(
        db, current_user, parade_date=parade_date, date_from=date_from,
        date_to=date_to, trade=trade, status=status, approval_status=approval_status, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 4. Academic Examination Results Report
# ─────────────────────────────────────────────────────────────
@router.get("/academic-results", response_model=StandardReportResponse, summary="Compile Examination Results & Marksheet Report")
def get_academic_results_report(
    request: Request,
    exam_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None),
    subject_id: Optional[str] = Query(None),
    batch: Optional[str] = Query(None),
    result_status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_academic_results_report(
        db, current_user, exam_id=exam_id, course_id=course_id,
        subject_id=subject_id, batch=batch, result_status=result_status, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 5. Classroom Attendance Register Report
# ─────────────────────────────────────────────────────────────
@router.get("/attendance", response_model=StandardReportResponse, summary="Compile Classroom Attendance Register Report")
def get_attendance_report(
    request: Request,
    course_id: Optional[str] = Query(None),
    subject_id: Optional[str] = Query(None),
    batch: Optional[str] = Query(None),
    instructor_id: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_attendance_report(
        db, current_user, course_id=course_id, subject_id=subject_id,
        batch=batch, instructor_id=instructor_id, date_from=date_from,
        date_to=date_to, status=status, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 6. Accommodation & Billeting Report
# ─────────────────────────────────────────────────────────────
@router.get("/accommodation", response_model=StandardReportResponse, summary="Compile Trainee Billeting & Accommodation Report")
def get_accommodation_report(
    request: Request,
    building_id: Optional[str] = Query(None),
    billet_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    bunk_level: Optional[str] = Query(None),
    trade: Optional[str] = Query(None),
    batch: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_accommodation_report(
        db, current_user, building_id=building_id, billet_id=billet_id,
        status=status, bunk_level=bunk_level, trade=trade, batch=batch, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 7. Course Calendar Schedule Report
# ─────────────────────────────────────────────────────────────
@router.get("/course-calendar", response_model=StandardReportResponse, summary="Compile Course Training Calendar Report")
def get_course_calendar_report(
    request: Request,
    course_id: Optional[str] = Query(None),
    batch_id: Optional[str] = Query(None),
    phase: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_course_calendar_report(
        db, current_user, course_id=course_id, batch_id=batch_id,
        phase=phase, date_from=date_from, date_to=date_to, ip=ip, ua=ua
    )


# ─────────────────────────────────────────────────────────────
# 8. Personal Occurrence Report (Achievements & Misconduct)
# ─────────────────────────────────────────────────────────────
@router.get("/occurrences", response_model=StandardReportResponse, summary="Compile Trainee Personal Occurrence & Conduct Dossier")
def get_occurrence_report(
    request: Request,
    trainee_id: Optional[str] = Query(None),
    occurrence_type: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    trade: Optional[str] = Query(None),
    batch: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    return report_service.get_occurrence_report(
        db, current_user, trainee_id=trainee_id, occurrence_type=occurrence_type,
        date_from=date_from, date_to=date_to, trade=trade, batch=batch,
        search=search, client_ip=ip, user_agent=ua
    )


# ─────────────────────────────────────────────────────────────
# 8. Export Endpoints (Excel & PDF)
# ─────────────────────────────────────────────────────────────
@router.post("/export/excel", summary="Generate and download native Excel (.xlsx) workbook")
def export_report_excel(
    payload: ReportExportRequest,
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    excel_bytes = report_service.export_report_excel(
        title=payload.title or payload.report_type.replace("_", " ").title(),
        header=payload.header_info or {},
        summary=payload.summary_stats or {},
        columns=payload.columns,
        rows=payload.rows
    )
    filename = f"SLAF_TTS_{payload.report_type.upper()}_{date.today().strftime('%Y%m%d')}.xlsx"
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/export/pdf", summary="Generate and download native PDF document")
def export_report_pdf(
    payload: ReportExportRequest,
    current_user: User = Depends(PermissionChecker("reports:read"))
):
    pdf_bytes = report_service.export_report_pdf(
        title=payload.title or payload.report_type.replace("_", " ").title(),
        header=payload.header_info or {},
        summary=payload.summary_stats or {},
        columns=payload.columns,
        rows=payload.rows
    )
    filename = f"SLAF_TTS_{payload.report_type.upper()}_{date.today().strftime('%Y%m%d')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
