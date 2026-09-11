import pytest
from app.schemas.academic import calculate_duration_from_dates
from datetime import date

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_calculate_duration_from_dates_unit():
    # 05/10/2026 to 25/12/2026 is 82 days (11 Weeks 5 Days), ceil 12 weeks
    weeks, formatted = calculate_duration_from_dates(date(2026, 10, 5), date(2026, 12, 25))
    assert formatted == "11 Weeks 5 Days"
    assert weeks == 12

    # Exactly 2 weeks (14 days)
    weeks, formatted = calculate_duration_from_dates(date(2026, 1, 1), date(2026, 1, 14))
    assert formatted == "2 Weeks"
    assert weeks == 2

    # 5 days
    weeks, formatted = calculate_duration_from_dates(date(2026, 1, 1), date(2026, 1, 5))
    assert formatted == "5 Days"
    assert weeks == 1

    # Same date (1 day)
    weeks, formatted = calculate_duration_from_dates(date(2026, 1, 1), date(2026, 1, 1))
    assert formatted == "1 Day"
    assert weeks == 1

    # End earlier than start
    weeks, formatted = calculate_duration_from_dates(date(2026, 1, 10), date(2026, 1, 5))
    assert formatted == ""
    assert weeks == 0


def test_batch_create_and_duration(client):
    headers = get_auth_headers(client)

    # 1. Create a Course first
    course_payload = {
        "code": "CRS-AUTO-01",
        "name": "Auto Duration Avionics Course",
        "course_type": "Basic",
        "start_date": "2026-10-05",
        "end_date": "2026-12-25",
        "intake_capacity": 25,
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    course_data = course_res.json()
    assert course_data["duration_weeks"] == 12
    assert course_data["duration_formatted"] == "11 Weeks 5 Days"
    course_id = course_data["id"]

    # 2. Configure New Batch with Start Date & End Date
    batch_payload = {
        "name": "Batch Auto-2026-A",
        "course_id": course_id,
        "intake_date": "2026-10-05",
        "passing_out_date": "2026-12-25",
        "capacity": 25,
        "status": "Active"
    }
    batch_res = client.post("/api/v1/academic/batches", json=batch_payload, headers=headers)
    assert batch_res.status_code == 200
    batch_data = batch_res.json()
    assert batch_data["name"] == "Batch Auto-2026-A"
    assert batch_data["intake_date"] == "2026-10-05"
    assert batch_data["passing_out_date"] == "2026-12-25"
    assert batch_data["duration_formatted"] == "11 Weeks 5 Days"

    # 3. List batches and check duration_formatted is present
    list_res = client.get("/api/v1/academic/batches", headers=headers)
    assert list_res.status_code == 200
    found = [b for b in list_res.json() if b["id"] == batch_data["id"]]
    assert len(found) == 1
    assert found[0]["duration_formatted"] == "11 Weeks 5 Days"


def test_batch_rejects_invalid_date_range(client):
    headers = get_auth_headers(client)

    # Create a course for the test
    course_payload = {
        "code": "CRS-INV-TEST-01",
        "name": "Invalid Test Course",
        "course_type": "Basic",
        "duration_weeks": 10,
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    course_id = course_res.json()["id"]

    # Invalid range: end date before start date
    invalid_batch = {
        "name": "Invalid Date Batch",
        "course_id": course_id,
        "intake_date": "2026-10-20",
        "passing_out_date": "2026-10-15",
        "capacity": 20,
        "status": "Active"
    }
    res = client.post("/api/v1/academic/batches", json=invalid_batch, headers=headers)
    assert res.status_code in [400, 422]
    detail = str(res.json())
    assert "End date cannot be earlier than the start date" in detail


def test_course_rejects_invalid_date_range(client):
    headers = get_auth_headers(client)

    invalid_course = {
        "code": "CRS-INV-DATE",
        "name": "Invalid Date Course",
        "course_type": "Basic",
        "start_date": "2026-10-20",
        "end_date": "2026-10-15",
        "intake_capacity": 30,
        "is_active": True
    }
    res = client.post("/api/v1/academic/courses", json=invalid_course, headers=headers)
    assert res.status_code in [400, 422]
    detail = str(res.json())
    assert "End date cannot be earlier than the start date" in detail


def test_course_calendar_bounds_validation(client):
    headers = get_auth_headers(client)

    # 1. Create a course with configured start and end date
    course_payload = {
        "code": "CRS-CAL-SYNC-01",
        "name": "Calendar Sync Test Course",
        "course_type": "Basic",
        "start_date": "2026-10-05",
        "end_date": "2026-12-25",
        "intake_capacity": 30,
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    course_id = course_res.json()["id"]

    # 2. Add calendar entry BEFORE course start date (01/10/2026) -> must be rejected
    early_cal = {
        "phase_name": "Early Phase",
        "theory_periods": 10,
        "practical_periods": 5,
        "working_days": 3,
        "commencement_date": "2026-10-01",
        "completion_date": "2026-10-04",
        "instructor_status": "NOT_ASSIGNED",
        "remarks": "Nomination pending"
    }
    early_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json=early_cal, headers=headers)
    assert early_res.status_code == 400
    assert "The selected calendar date must be within the configured course/batch start and end dates" in early_res.json()["detail"]

    # 3. Add calendar entry AFTER course end date (26/12/2026) -> must be rejected
    late_cal = {
        "phase_name": "Late Phase",
        "theory_periods": 10,
        "practical_periods": 5,
        "working_days": 3,
        "commencement_date": "2026-12-26",
        "completion_date": "2026-12-30",
        "instructor_status": "NOT_ASSIGNED",
        "remarks": "Nomination pending"
    }
    late_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json=late_cal, headers=headers)
    assert late_res.status_code == 400
    assert "The selected calendar date must be within the configured course/batch start and end dates" in late_res.json()["detail"]

    # 4. Add valid calendar entry inside range (10/10/2026 to 20/10/2026) -> must succeed
    valid_cal = {
        "phase_name": "Valid Phase 1",
        "theory_periods": 20,
        "practical_periods": 10,
        "working_days": 8,
        "commencement_date": "2026-10-10",
        "completion_date": "2026-10-20",
        "instructor_status": "NOT_ASSIGNED",
        "remarks": "Assigned to Lead Instructor"
    }
    valid_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json=valid_cal, headers=headers)
    assert valid_res.status_code == 200
    cal_id = valid_res.json()["id"]
    assert valid_res.json()["phase_name"] == "Valid Phase 1"


def test_course_update_cascade_validation(client):
    headers = get_auth_headers(client)

    # 1. Create course
    course_payload = {
        "code": "CRS-CASCADE-01",
        "name": "Cascade Test Course",
        "course_type": "Basic",
        "start_date": "2026-10-01",
        "end_date": "2026-12-31",
        "intake_capacity": 30,
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    course_id = course_res.json()["id"]

    # 2. Add calendar entry: 2026-10-05 to 2026-10-20
    cal_payload = {
        "phase_name": "Basic Aerodynamics",
        "theory_periods": 15,
        "practical_periods": 5,
        "working_days": 10,
        "commencement_date": "2026-10-05",
        "completion_date": "2026-10-20",
        "instructor_status": "NOT_ASSIGNED",
        "remarks": "Pending Officer"
    }
    cal_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json=cal_payload, headers=headers)
    assert cal_res.status_code == 200

    # 3. Attempt to shrink course start date to 2026-10-10 (making the phase at 2026-10-05 invalid) -> MUST be blocked
    shrink_res = client.put(f"/api/v1/academic/courses/{course_id}", json={"start_date": "2026-10-10"}, headers=headers)
    assert shrink_res.status_code == 400
    detail = shrink_res.json()["detail"]
    assert "Cannot change course dates" in detail
    assert "Basic Aerodynamics" in detail

    # 4. Adjust end date to 2026-11-30 (all existing phases still within range) -> MUST succeed
    valid_shrink = client.put(f"/api/v1/academic/courses/{course_id}", json={"end_date": "2026-11-30"}, headers=headers)
    assert valid_shrink.status_code == 200
    assert valid_shrink.json()["end_date"] == "2026-11-30"


def test_timetable_and_exam_course_bounds(client):
    headers = get_auth_headers(client)

    # 1. Create course and subject
    course_payload = {
        "code": "CRS-TT-EXAM-01",
        "name": "Timetable & Exam Bounds Course",
        "start_date": "2026-10-01",
        "end_date": "2026-10-31",
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    course_id = course_res.json()["id"]

    sub_res = client.post("/api/v1/academic/subjects", json={
        "course_id": course_id,
        "code": "AERO-101",
        "name": "Aerodynamics 101",
        "periods": 30
    }, headers=headers)
    assert sub_res.status_code == 200
    sub_id = sub_res.json()["id"]

    # 2. Create exam outside course date range (2026-11-15 > 2026-10-31) -> rejected
    exam_payload = {
        "course_id": course_id,
        "subject_id": sub_id,
        "type": "Phase Test",
        "date": "2026-11-15",
        "max_marks": 100,
        "pass_marks": 50
    }
    exam_res = client.post("/api/v1/academic/exams", json=exam_payload, headers=headers)
    assert exam_res.status_code == 400
    assert "Exam date" in exam_res.json()["detail"]

    # 3. Create exam inside course date range (2026-10-25) -> success
    exam_payload["date"] = "2026-10-25"
    exam_valid_res = client.post("/api/v1/academic/exams", json=exam_payload, headers=headers)
    assert exam_valid_res.status_code == 200


def test_date_aware_status_logic():
    from app.schemas.academic import get_date_aware_status
    from datetime import date, timedelta

    today = date.today()
    past_start = today - timedelta(days=30)
    past_end = today - timedelta(days=5)
    future_start = today + timedelta(days=5)
    future_end = today + timedelta(days=30)

    # Past dates -> COMPLETED
    assert get_date_aware_status(past_start, past_end) == "COMPLETED"

    # Future dates -> UPCOMING
    assert get_date_aware_status(future_start, future_end) == "UPCOMING"

    # Encompassing today -> ONGOING
    assert get_date_aware_status(past_start, future_end) == "ONGOING"

