from datetime import date, datetime
import pytest
from app.models.academic import Course, Subject, Batch, Exam, ExamMark, AcademicAttendance, CourseCalendar, Timetable, Lesson
from app.models.student import Student, ParadeState, ParadeSubmission, ParadeStatusType, PersonalOccurrence
from app.models.accommodation import AccommodationBuilding, AccommodationBillet, AccommodationBunkBed, BedPosition, AccommodationAllocation
from app.models.user import User, AuditLog



@pytest.fixture
def auth_headers(client):
    login_data = {
        "username": "admin",
        "password": "Admin@123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def report_test_data(db_session):
    # 1. Course & Subject & Batch
    course = Course(
        id='crs-rep-01',
        code='AERO-REPORT',
        name='Aero Mechanical Engineering',
        trade_id='trade-airframe',
        duration_weeks=12
    )
    db_session.add(course)

    subject = Subject(
        id='subj-rep-01',
        course_id=course.id,
        code='AERO-REP-101',
        name='Aerodynamics & Thermodynamics',
        periods=30
    )
    db_session.add(subject)

    batch = Batch(
        id='batch-rep-26-1',
        name='26/1',
        course_id=course.id,
        status='Active'
    )
    db_session.add(batch)

    # 2. Students
    s1 = Student(
        id='std-rep-01',
        service_number='58001',
        full_name='Perera K A',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        batch='26/1',
        status='Active'
    )
    s2 = Student(
        id='std-rep-02',
        service_number='58002',
        full_name='Silva M T',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        batch='26/1',
        status='Leave'
    )
    s3 = Student(
        id='std-rep-03',
        service_number='58003',
        full_name='Fernando S L',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        batch='26/1',
        status='Active'
    )
    db_session.add_all([s1, s2, s3])
    db_session.commit()

    # 3. Parade State
    rep_date = date(2026, 9, 15)
    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    submission = ParadeSubmission(
        id='ps-sub-rep-01',
        date=rep_date,
        trade='Airframe',
        status='APPROVED',
        submitted_by=admin_user.id,
        approving_officer_id=admin_user.id,
        reviewed_at=datetime(2026, 9, 15, 8, 30)
    )
    db_session.add(submission)

    p1 = ParadeState(student_id=s1.id, date=rep_date, status='Present', submission_id=submission.id)
    p2 = ParadeState(student_id=s2.id, date=rep_date, status='Leave', submission_id=submission.id)
    p3 = ParadeState(student_id=s3.id, date=rep_date, status='Hospital', submission_id=submission.id)
    db_session.add_all([p1, p2, p3])

    # 4. Exam & ExamMarks
    exam = Exam(
        id='exam-rep-01',
        course_id=course.id,
        subject_id=subject.id,
        type='Phase Test',
        date=rep_date,
        max_marks=100.0,
        pass_marks=50.0
    )
    db_session.add(exam)
    db_session.commit()

    em1 = ExamMark(exam_id=exam.id, student_id=s1.id, marks_obtained=82.5, status='Pass')
    db_session.add(em1)

    # 5. Attendance
    lesson = Lesson(id='les-rep-01', subject_id=subject.id, name='Gas Dynamics')
    db_session.add(lesson)
    db_session.commit()

    tt = Timetable(
        id='tt-rep-01',
        course_id=course.id,
        subject_id=subject.id,
        lesson_id=lesson.id,
        instructor_id=admin_user.id,
        date=rep_date,
        period_number=1
    )
    db_session.add(tt)
    db_session.commit()

    att1 = AcademicAttendance(
        timetable_id=tt.id,
        student_id=s1.id,
        status='Present'
    )
    att2 = AcademicAttendance(
        timetable_id=tt.id,
        student_id=s2.id,
        status='Absent'
    )
    db_session.add_all([att1, att2])

    # 6. Accommodation
    building = AccommodationBuilding(id='bld-rep-01', name='Block Alpha HQ', type='Airmen', capacity=10)
    db_session.add(building)
    db_session.commit()

    billet = AccommodationBillet(id='billet-rep-01', building_id=building.id, name='Billet 01', bunk_bed_count=2, capacity=4, status='Active')
    db_session.add(billet)
    db_session.commit()

    bunk = AccommodationBunkBed(id='bunk-rep-01', billet_id=billet.id, bunk_no='B-01', status='Active')
    db_session.add(bunk)
    db_session.commit()

    pos_top = BedPosition(id='pos-top-01', bunk_bed_id=bunk.id, position_type='TOP', position_code='B-01-TOP', status='Occupied')
    pos_bot = BedPosition(id='pos-bot-01', bunk_bed_id=bunk.id, position_type='BOTTOM', position_code='B-01-BOT', status='Available')
    db_session.add_all([pos_top, pos_bot])
    db_session.commit()

    alloc = AccommodationAllocation(
        student_id=s1.id,
        bed_position_id=pos_top.id,
        allocated_by=admin_user.id,
        allocated_at=datetime(2026, 9, 1)
    )
    db_session.add(alloc)

    # 7. Course Calendar Entry
    cal_entry = CourseCalendar(
        course_id=course.id,
        subject_id=subject.id,
        instructor_id=admin_user.id,
        serial_number=1,
        phase_name='Phase 1',
        working_days=5,
        commencement_date=rep_date,
        completion_date=date(2026, 9, 20),
        theory_periods=4,
        practical_periods=2,
        total_periods=6
    )
    db_session.add(cal_entry)
    db_session.commit()

    return {
        "course": course,
        "subject": subject,
        "batch": batch,
        "students": [s1, s2, s3],
        "exam": exam,
        "rep_date": rep_date
    }


# ─────────────────────────────────────────────────────────────
# Integration Tests
# ─────────────────────────────────────────────────────────────

def test_get_filter_metadata(client, auth_headers, report_test_data):
    res = client.get("/api/v1/reports/meta/filters", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert "trades" in data
    assert "courses" in data
    assert "batches" in data
    assert "ranks" in data
    assert "billets" in data


def test_student_dossier_report(client, auth_headers, report_test_data):
    res = client.get("/api/v1/reports/students?trade=Airframe", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "student"
    assert "header" in data
    assert "columns" in data
    assert "summary_stats" in data
    assert data["total_records"] >= 3
    assert any(r["service_number"] == "58001" for r in data["rows"])


def test_parade_state_report_with_summary(client, auth_headers, report_test_data):
    dt = str(report_test_data["rep_date"])
    res = client.get(f"/api/v1/reports/parade-state?parade_date={dt}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "parade"
    assert data["total_records"] == 3

    # Verify summary metrics
    stats = {s["label"]: s["value"] for s in data["summary_stats"]}
    assert stats["Total Strength"] == 3
    assert stats["Present Strength"] == 1
    assert stats["On Leave"] == 1
    assert stats["In Hospital"] == 1


def test_academic_results_report_with_parade_integration(client, auth_headers, report_test_data):
    exam = report_test_data["exam"]
    res = client.get(f"/api/v1/reports/academic-results?exam_id={exam.id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "academic_results"

    st_rows = {r["service_number"]: r for r in data["rows"]}
    # Present student sat and scored 82.5
    assert st_rows["58001"]["marks_obtained"] == "82.5"
    assert st_rows["58001"]["result_status"] == "PASS"

    # Leave student shows LEAVE
    assert st_rows["58002"]["marks_obtained"] == "--"
    assert st_rows["58002"]["result_status"] == "LEAVE"

    # Hospital student shows IN HOSPITAL
    assert st_rows["58003"]["marks_obtained"] == "--"
    assert st_rows["58003"]["result_status"] == "IN HOSPITAL"


def test_attendance_register_report(client, auth_headers, report_test_data):
    dt = str(report_test_data["rep_date"])
    res = client.get(f"/api/v1/reports/attendance?date_from={dt}&date_to={dt}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "attendance"
    assert data["total_records"] == 2


def test_accommodation_billeting_report(client, auth_headers, report_test_data):
    res = client.get("/api/v1/reports/accommodation", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "accommodation"
    assert data["total_records"] >= 2
    assert any(r["bunk_level"] == "TOP" and r["bed_status"] == "Occupied" for r in data["rows"])


def test_course_calendar_schedule_report(client, auth_headers, report_test_data):
    course = report_test_data["course"]
    res = client.get(f"/api/v1/reports/course-calendar?course_id={course.id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "course_calendar"
    assert data["total_records"] >= 1
    assert data["rows"][0]["total_periods"] == 6


def test_excel_export_endpoint(client, auth_headers, report_test_data):
    payload = {
        "report_type": "student",
        "title": "Trainee Dossiers Official Export",
        "header_info": {"generated_by": "Test Officer", "generated_at": "2026-08-24 16:00"},
        "summary_stats": {"Total Trainees": 3, "Active": 2, "Leave": 1},
        "columns": [
            {"field": "s_no", "label": "S/No"},
            {"field": "service_number", "label": "Service No"},
            {"field": "full_name", "label": "Name"},
            {"field": "trade", "label": "Trade"},
            {"field": "status", "label": "Status"}
        ],
        "rows": [
            {"s_no": 1, "service_number": "58001", "full_name": "Perera K A", "trade": "Airframe", "status": "Active"},
            {"s_no": 2, "service_number": "58002", "full_name": "Silva M T", "trade": "Airframe", "status": "Leave"},
            {"s_no": 3, "service_number": "58003", "full_name": "Fernando S L", "trade": "Airframe", "status": "Active"}
        ]
    }
    res = client.post("/api/v1/reports/export/excel", json=payload, headers=auth_headers)
    assert res.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in res.headers["content-type"]
    assert len(res.content) > 1000  # valid binary bytes


def test_pdf_export_endpoint(client, auth_headers, report_test_data):
    payload = {
        "report_type": "parade",
        "title": "Daily Parade State Official PDF",
        "header_info": {"generated_by": "Test Officer", "generated_at": "2026-08-24 16:00"},
        "summary_stats": {"Total Strength": 3, "Present": 1, "Leave": 1, "Hospital": 1},
        "columns": [
            {"field": "s_no", "label": "S/No"},
            {"field": "service_number", "label": "Service No"},
            {"field": "full_name", "label": "Name"},
            {"field": "trade", "label": "Trade"},
            {"field": "parade_status", "label": "Status"}
        ],
        "rows": [
            {"s_no": 1, "service_number": "58001", "full_name": "Perera K A", "trade": "Airframe", "parade_status": "Present"},
            {"s_no": 2, "service_number": "58002", "full_name": "Silva M T", "trade": "Airframe", "parade_status": "Leave"},
            {"s_no": 3, "service_number": "58003", "full_name": "Fernando S L", "trade": "Airframe", "parade_status": "Hospital"}
        ]
    }
    res = client.post("/api/v1/reports/export/pdf", json=payload, headers=auth_headers)
    assert res.status_code == 200
    assert "application/pdf" in res.headers["content-type"]
    assert len(res.content) > 1000  # valid binary PDF bytes


def test_reports_rbac_security(client, report_test_data):
    # Anonymous request without token must be rejected with 401
    res = client.get("/api/v1/reports/students")
    assert res.status_code == 401


def test_personal_occurrences_report(client, auth_headers, report_test_data, db_session):
    student = report_test_data["students"][0]
    occ = PersonalOccurrence(
        trainee_id=student.id,
        occurrence_type="ACHIEVEMENT",
        occurrence_date=date(2026, 8, 20),
        title="Best in Airframe Practical Assessment",
        description="Demonstrated exemplary mechanical skill during hydraulic rig testing.",
        remarks="Awarded Commendation by OCT"
    )
    db_session.add(occ)
    db_session.commit()

    res = client.get(f"/api/v1/reports/occurrences?trainee_id={student.id}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["report_type"] == "occurrences"
    assert data["total_records"] >= 1
    assert data["rows"][0]["service_number"] == student.service_number
    assert "ACHIEVEMENT" in data["rows"][0]["occurrence_type"]


def test_report_audit_logging(client, auth_headers, report_test_data, db_session):
    client.get("/api/v1/reports/students?trade=Airframe", headers=auth_headers)
    audit = db_session.query(AuditLog).filter(AuditLog.action == "REPORT_GENERATED").first()
    assert audit is not None
    assert "STUDENT_DOSSIER" in audit.details

