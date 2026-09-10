import pytest

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_and_search_student(client):
    headers = get_auth_headers(client)
    
    # 1. Create Student
    student_payload = {
        "service_number": "SLAF/12345",
        "initials": "A.B.C.",
        "full_name": "Ranasinghe K.A.",
        "nic": "199512345678",
        "dob": "1995-05-12",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "course_id": None,
        "batch": "120th Intake",
        "joining_date": "2026-01-01",
        "emergency_contact_name": "Ranasinghe Senior",
        "emergency_contact_phone": "0771234567",
        "blood_group": "O+",
        "religion": "Buddhist",
        "permanent_address": "No 10, Galle Road, Colombo"
    }
    
    response = client.post("/api/v1/students", json=student_payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["service_number"] == "SLAF/12345"
    assert "qr_code_data" in response.json()

    # 2. Check Service Number duplication
    response_dup = client.post("/api/v1/students", json=student_payload, headers=headers)
    assert response_dup.status_code == 400
    assert "already exists" in response_dup.json()["detail"]

    # 3. Search Students
    response_search = client.get("/api/v1/students", params={"search": "Ranasinghe"}, headers=headers)
    assert response_search.status_code == 200
    assert response_search.json()["total"] == 1
    assert response_search.json()["items"][0]["service_number"] == "SLAF/12345"


def test_get_student_statuses(client):
    headers = get_auth_headers(client)
    response = client.get("/api/v1/students/statuses", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Check that Active, Sick Report, and Leave exist in the returned list
    codes = [item["code"] for item in data]
    assert "ACTIVE" in codes
    assert "SICK_REPORT" in codes
    assert "LEAVE" in codes


def test_get_student_ranks_and_trades(client):
    headers = get_auth_headers(client)
    
    # Check ranks endpoint
    response_ranks = client.get("/api/v1/students/ranks", headers=headers)
    assert response_ranks.status_code == 200
    ranks_data = response_ranks.json()
    assert len(ranks_data) > 0
    rank_codes = [r["code"] for r in ranks_data]
    assert "AC" in rank_codes
    assert "LAC" in rank_codes

    # Check trades endpoint
    response_trades = client.get("/api/v1/students/trades", headers=headers)
    assert response_trades.status_code == 200
    trades_data = response_trades.json()
    assert len(trades_data) > 0
    trade_codes = [t["code"] for t in trades_data]
    assert "AIRFRAME" in trade_codes
    assert "AVIONICS" in trade_codes


def test_academic_course_batch_creation_to_student_enrollment_flow(client):
    headers = get_auth_headers(client)

    # 1. Academic Activity: Create Course "2/2026 Account Assistant – Basic Course"
    # First get or create Trade
    trade_res = client.get("/api/v1/academic/trades", headers=headers)
    trade_id = trade_res.json()[0]["id"] if len(trade_res.json()) > 0 else None

    course_payload = {
        "code": "2/2026",
        "name": "Account Assistant – Basic Course",
        "trade_id": trade_id,
        "course_type": "Basic",
        "duration_weeks": 24,
        "intake_capacity": 30,
        "start_date": "2026-02-01",
        "end_date": "2026-07-31",
        "description": "Account Assistant Basic Course for Intake 2026",
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200, course_res.text
    created_course = course_res.json()
    course_id = created_course["id"]
    assert created_course["code"] == "2/2026"
    assert created_course["name"] == "Account Assistant – Basic Course"

    # Create Batch under this course
    batch_payload = {
        "name": "2/2026",
        "course_id": course_id,
        "trade_id": trade_id,
        "intake_date": "2026-02-01",
        "passing_out_date": "2026-07-31",
        "capacity": 30,
        "status": "Active"
    }
    batch_res = client.post("/api/v1/academic/batches", json=batch_payload, headers=headers)
    assert batch_res.status_code == 200, batch_res.text

    # 2. Student Registration: Fetch Course Enrollment Options
    enroll_options_res = client.get("/api/v1/academic/courses/enrollment-options", headers=headers)
    assert enroll_options_res.status_code == 200
    options = enroll_options_res.json()
    assert len(options) > 0

    # Verify that "2/2026 Account Assistant – Basic Course" appears automatically
    matching_option = next((opt for opt in options if opt["course_id"] == course_id), None)
    assert matching_option is not None
    assert matching_option["course_code"] == "2/2026"
    assert matching_option["course_name"] == "Account Assistant – Basic Course"
    assert matching_option["batch_name"] == "2/2026"
    assert matching_option["status"] == "Active"

    # 3. Trainee Arrival & Registration: Enroll Trainee in the existing course/batch
    trainee_payload = {
        "service_number": "SLAF/99001",
        "initials": "S.A.",
        "full_name": "Sanka Adikaram",
        "nic": "199612349901",
        "dob": "1996-08-15",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": matching_option["trade_name"] or "Airframe",
        "course_id": course_id,
        "batch": "2/2026",
        "joining_date": "2026-02-01",
        "passing_out_date": "2026-07-31",
        "emergency_contact_name": "Father",
        "emergency_contact_phone": "0779998888",
        "blood_group": "A+",
        "religion": "Buddhist",
        "permanent_address": "TTS Ekala, Ja-Ela"
    }
    register_res = client.post("/api/v1/students", json=trainee_payload, headers=headers)
    assert register_res.status_code == 200, register_res.text
    trainee = register_res.json()
    assert trainee["course_id"] == course_id
    assert trainee["batch"] == "2/2026"

    # 4. Verify Single Source of Truth relationship
    student_details_res = client.get(f"/api/v1/students/{trainee['id']}", headers=headers)
    assert student_details_res.status_code == 200
    student_data = student_details_res.json()
    assert student_data["course_id"] == course_id
    assert "2/2026" in student_data["course_name"]
    assert "Account Assistant" in student_data["course_name"]


def test_multiple_course_creation_and_enrollment_availability(client):
    headers = get_auth_headers(client)

    # Create another course: "3/2026 Computer Technician – Basic Course"
    course_payload = {
        "code": "3/2026",
        "name": "Computer Technician – Basic Course",
        "course_type": "Basic",
        "duration_weeks": 20,
        "intake_capacity": 25,
        "start_date": "2026-03-01",
        "end_date": "2026-08-01",
        "is_active": True
    }
    course_res = client.post("/api/v1/academic/courses", json=course_payload, headers=headers)
    assert course_res.status_code == 200
    c_id = course_res.json()["id"]

    # Verify both courses appear in enrollment options
    options_res = client.get("/api/v1/academic/courses/enrollment-options", headers=headers)
    assert options_res.status_code == 200
    options = options_res.json()
    course_codes = [opt["course_code"] for opt in options]
    assert "3/2026" in course_codes

    # Enroll trainee in 3/2026
    trainee_payload = {
        "service_number": "SLAF/99002",
        "initials": "K.M.",
        "full_name": "Kamal Perera",
        "nic": "199712349902",
        "dob": "1997-04-10",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "course_id": c_id,
        "batch": "3/2026",
        "emergency_contact_name": "Parent",
        "emergency_contact_phone": "0771112222",
        "permanent_address": "Kandy"
    }
    reg_res = client.post("/api/v1/students", json=trainee_payload, headers=headers)
    assert reg_res.status_code == 200
    assert reg_res.json()["course_id"] == c_id


def test_backend_validation_rejects_invalid_course_enrollment(client):
    headers = get_auth_headers(client)

    # Attempt to enroll trainee with a non-existent course ID
    bogus_payload = {
        "service_number": "SLAF/99003",
        "initials": "X.Y.",
        "full_name": "Invalid Course Trainee",
        "nic": "199812349903",
        "dob": "1998-01-01",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "course_id": "non-existent-course-uuid-999",
        "batch": "Fake Batch",
        "emergency_contact_name": "Contact",
        "emergency_contact_phone": "0770000000",
        "permanent_address": "Colombo"
    }
    res = client.post("/api/v1/students", json=bogus_payload, headers=headers)
    assert res.status_code == 400
    assert "does not exist" in res.json()["detail"]


def test_backend_validation_rejects_duplicate_enrollment(client):
    headers = get_auth_headers(client)

    # Register initial student
    payload = {
        "service_number": "SLAF/99004",
        "initials": "D.N.",
        "full_name": "Duplicate Test Trainee",
        "nic": "199912349904",
        "dob": "1999-01-01",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "batch": "Batch 2026",
        "emergency_contact_name": "Contact",
        "emergency_contact_phone": "0770000000",
        "permanent_address": "Colombo"
    }
    res1 = client.post("/api/v1/students", json=payload, headers=headers)
    assert res1.status_code == 200

    # Attempt duplicate registration with same service number
    res2 = client.post("/api/v1/students", json=payload, headers=headers)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


