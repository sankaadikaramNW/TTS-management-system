import pytest
from datetime import date, datetime
from app.models.user import User, Role, Permission
from app.models.student import Student, Trade, ParadeSubmission, ParadeState, ParadeStatusType
from app.models.academic import Course, Batch, Classroom


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
def setup_instructor_routing_data(db_session):
    # Ensure ParadeStatusTypes
    if db_session.query(ParadeStatusType).count() == 0:
        status_types = [
            ParadeStatusType(code='PRESENT', label='Present', can_sit_exam=True),
            ParadeStatusType(code='SICK_REPORT', label='Sick Report', can_sit_exam=False),
            ParadeStatusType(code='HOSPITAL', label='Hospital', can_sit_exam=False),
            ParadeStatusType(code='LEAVE', label='Leave', can_sit_exam=False),
            ParadeStatusType(code='TEMPORARY_DUTY', label='Temporary Duty', can_sit_exam=True),
            ParadeStatusType(code='COURSE_VISIT', label='Course Visit', can_sit_exam=False),
            ParadeStatusType(code='DETACHED_DUTY', label='Detached Duty', can_sit_exam=False),
            ParadeStatusType(code='AWOL', label='AWOL', can_sit_exam=False)
        ]
        db_session.bulk_save_objects(status_types)
        db_session.commit()

    # Ensure Permissions
    required_codes = ["parade:read", "parade:write", "parade:approve", "academic:read", "academic:write"]
    existing_perms = {p.code: p for p in db_session.query(Permission).all()}
    for code in required_codes:
        if code not in existing_perms:
            new_p = Permission(code=code, name=code, module="Parade")
            db_session.add(new_p)
            db_session.commit()
            existing_perms[code] = new_p

    # Ensure Roles
    inst_role = db_session.query(Role).filter_by(name="Instructor").first()
    if not inst_role:
        inst_role = Role(name="Instructor", description="Instructor Role")
        db_session.add(inst_role)
        db_session.commit()

    inst_role.permissions = list(existing_perms.values())
    db_session.commit()

    admin_role = db_session.query(Role).filter_by(name="Super Administrator").first()
    if not admin_role:
        admin_role = Role(name="Super Administrator", description="Super Admin")
        db_session.add(admin_role)
        db_session.commit()

    # Create Instructors
    inst_a = User(
        id="user-inst-a",
        username="inst_kamal",
        email="kamal@slaf.gov.lk",
        full_name="Kamal Perera",
        service_number="51837",
        rank="Sgt",
        designation="Senior Instructor",
        hashed_password="mock_hashed_password",
        role_id=inst_role.id,
        is_active=True
    )
    inst_b = User(
        id="user-inst-b",
        username="inst_nimal",
        email="nimal@slaf.gov.lk",
        full_name="Nimal Silva",
        service_number="51999",
        rank="Cpl",
        designation="Instructor",
        hashed_password="mock_hashed_password",
        role_id=inst_role.id,
        is_active=True
    )
    admin_user = User(
        id="user-admin-routing",
        username="admin_routing",
        email="admin_routing@slaf.gov.lk",
        full_name="Admin Routing Officer",
        service_number="01234",
        rank="Sqn Ldr",
        hashed_password="mock_hashed_password",
        role_id=admin_role.id,
        is_active=True
    )
    db_session.add_all([inst_a, inst_b, admin_user])
    db_session.commit()

    # Create Trades
    trade_ct = Trade(id="trade-ct", code="CT", label="Computer Technician", is_active=True)
    trade_af = Trade(id="trade-af", code="AF", label="Airframe", is_active=True)
    db_session.add_all([trade_ct, trade_af])
    db_session.commit()

    # Create Classrooms
    cr_e06 = Classroom(id="cr-e06", code="E-06", name="Electronics Lab 06", capacity=30, is_active=True)
    db_session.add(cr_e06)
    db_session.commit()

    # Create Courses
    course_ct_26 = Course(
        id="course-ct-26",
        code="CT-26/1",
        name="26/1 Advance Computer Technician",
        trade_id="trade-ct",
        course_type="Advance",
        duration_weeks=24
    )
    course_af_18 = Course(
        id="course-af-18",
        code="AF-18",
        name="18 Basic Airframe",
        trade_id="trade-af",
        course_type="Basic",
        duration_weeks=16
    )
    db_session.add_all([course_ct_26, course_af_18])
    db_session.commit()

    # Create Batches with Instructor Assignments
    # Batch 1: CT-26/1 assigned to Instructor A (Kamal)
    batch_ct = Batch(
        id="batch-ct-26-1",
        name="26/1",
        course_id="course-ct-26",
        trade_id="trade-ct",
        classroom_id="cr-e06",
        instructor_id="user-inst-a",
        status="Active"
    )
    # Batch 2: AF-18 assigned to Instructor B (Nimal)
    batch_af = Batch(
        id="batch-af-18",
        name="18-A",
        course_id="course-af-18",
        trade_id="trade-af",
        instructor_id="user-inst-b",
        status="Active"
    )
    # Batch 3: Unassigned batch (INSTRUCTOR NOT ASSIGNED)
    batch_unassigned = Batch(
        id="batch-unassigned",
        name="99-Unassigned",
        course_id="course-ct-26",
        trade_id="trade-ct",
        instructor_id=None,
        status="Active"
    )
    db_session.add_all([batch_ct, batch_af, batch_unassigned])
    db_session.commit()

    # Add active trainees
    st_ct_1 = Student(
        id="st-ct-01",
        service_number="CT001",
        full_name="Trainee CT One",
        rank="LAC",
        trade="Computer Technician",
        course_id="course-ct-26",
        batch="26/1",
        status="Active"
    )
    st_ct_2 = Student(
        id="st-ct-02",
        service_number="CT002",
        full_name="Trainee CT Two",
        rank="AC",
        trade="Computer Technician",
        course_id="course-ct-26",
        batch="26/1",
        status="Active"
    )
    st_af_1 = Student(
        id="st-af-01",
        service_number="AF001",
        full_name="Trainee AF One",
        rank="LAC",
        trade="Airframe",
        course_id="course-af-18",
        batch="18-A",
        status="Active"
    )
    db_session.add_all([st_ct_1, st_ct_2, st_af_1])
    db_session.commit()

    return {
        "inst_a_id": "user-inst-a",
        "inst_b_id": "user-inst-b",
        "admin_id": "user-admin-routing",
        "course_ct_id": "course-ct-26",
        "course_af_id": "course-af-18",
        "batch_ct_id": "batch-ct-26-1",
        "batch_af_id": "batch-af-18"
    }


def test_parade_submission_auto_determines_assigned_instructor(client, auth_headers, setup_instructor_routing_data, db_session):
    """
    Test Criteria 3 & 5:
    Parade State submitter does NOT select an approving officer.
    System automatically determines the responsible Instructor from the Academic Batch.
    """
    today = date.today().isoformat()
    inst_a_id = setup_instructor_routing_data["inst_a_id"]

    # Submit without approving_officer_id
    submit_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "26/1",
        "submitter_remarks": "CT Morning Muster",
        "records": [
            {"student_id": "st-ct-01", "status": "Present", "remarks": ""},
            {"student_id": "st-ct-02", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)

    assert submit_res.status_code == 200
    data = submit_res.json()
    assert data["status"] == "submitted"
    assert "Kamal Perera" in data["approving_officer"]

    # Verify in DB that approving_officer_id was auto-resolved to Instructor A
    sub = db_session.query(ParadeSubmission).filter_by(id=data["id"]).first()
    assert sub is not None
    assert sub.approving_officer_id == inst_a_id
    assert sub.status == "SUBMITTED"


def test_instructor_approval_queue_isolation(client, auth_headers, setup_instructor_routing_data):
    """
    Test Criteria 4, 6 & 7:
    Instructor A only sees pending parade states for assigned Batches.
    Instructor B does NOT see Instructor A's parade states.
    """
    from app.security import create_access_token
    today = date.today().isoformat()

    # Submit CT (assigned to A)
    client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "26/1",
        "records": [
            {"student_id": "st-ct-01", "status": "Present", "remarks": ""},
            {"student_id": "st-ct-02", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)

    # Submit AF (assigned to B)
    client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Airframe",
        "course_id": setup_instructor_routing_data["course_af_id"],
        "batch": "18-A",
        "records": [
            {"student_id": "st-af-01", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)

    # Instructor A checks pending approvals
    token_a = create_access_token("inst_kamal")
    res_a = client.get("/api/v1/parade/submissions/pending", headers={"Authorization": f"Bearer {token_a}"})
    assert res_a.status_code == 200
    pending_a = res_a.json()
    assert len(pending_a) == 1
    assert pending_a[0]["trade"] == "Computer Technician"

    # Instructor B checks pending approvals
    token_b = create_access_token("inst_nimal")
    res_b = client.get("/api/v1/parade/submissions/pending", headers={"Authorization": f"Bearer {token_b}"})
    assert res_b.status_code == 200
    pending_b = res_b.json()
    assert len(pending_b) == 1
    assert pending_b[0]["trade"] == "Airframe"


def test_backend_prevents_unauthorized_instructor_approval(client, auth_headers, setup_instructor_routing_data):
    """
    Test Criteria 8 & 9:
    Backend independently verifies Instructor-to-Course/Batch relationship.
    Instructor B cannot approve Instructor A's Batch parade state (HTTP 403).
    """
    from app.security import create_access_token
    today = date.today().isoformat()

    # Submit CT (assigned to Instructor A)
    sub_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "26/1",
        "records": [
            {"student_id": "st-ct-01", "status": "Present", "remarks": ""},
            {"student_id": "st-ct-02", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)
    assert sub_res.status_code == 200
    sub_id = sub_res.json()["id"]

    # Unauthorized Instructor B attempts to approve
    token_b = create_access_token("inst_nimal")
    unauth_res = client.post(f"/api/v1/parade/submissions/{sub_id}/approve", json={
        "remarks": "Illegal approval attempt"
    }, headers={"Authorization": f"Bearer {token_b}"})
    assert unauth_res.status_code == 403
    assert "not the assigned Instructor" in unauth_res.json()["detail"]

    # Authorized Instructor A approves
    token_a = create_access_token("inst_kamal")
    auth_res = client.post(f"/api/v1/parade/submissions/{sub_id}/approve", json={
        "remarks": "Official strength verified"
    }, headers={"Authorization": f"Bearer {token_a}"})
    assert auth_res.status_code == 200
    assert auth_res.json()["status"] == "approved"


def test_instructor_not_assigned_handled_safely(client, auth_headers, setup_instructor_routing_data, db_session):
    """
    Test Criteria 10:
    When a batch has INSTRUCTOR NOT ASSIGNED, submission succeeds but cannot be approved by normal instructors.
    """
    from app.security import create_access_token
    today = date.today().isoformat()

    # Add student in unassigned batch
    st_un = Student(
        id="st-un-01",
        service_number="UN001",
        full_name="Trainee Unassigned",
        rank="AC",
        trade="Computer Technician",
        course_id=setup_instructor_routing_data["course_ct_id"],
        batch="99-Unassigned",
        status="Active"
    )
    db_session.add(st_un)
    db_session.commit()

    # Submit parade state for unassigned batch
    submit_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "99-Unassigned",
        "records": [
            {"student_id": "st-un-01", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)
    assert submit_res.status_code == 200
    assert submit_res.json()["approving_officer"] == "INSTRUCTOR NOT ASSIGNED"
    sub_id = submit_res.json()["id"]

    # Check monitoring view indicates NOT ASSIGNED
    mon_res = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    assert mon_res.status_code == 200

    # Normal instructor B cannot approve it
    token_b = create_access_token("inst_nimal")
    appr_res = client.post(f"/api/v1/parade/submissions/{sub_id}/approve", json={}, headers={"Authorization": f"Bearer {token_b}"})
    assert appr_res.status_code == 403


def test_historical_approvals_preserve_original_approver_on_reassignment(client, auth_headers, db_session, setup_instructor_routing_data):
    """
    Test Criteria 11:
    Changing Course/Batch instructor does NOT alter historical approved parade state approver records.
    """
    from app.security import create_access_token
    past_date = "2026-08-01"
    inst_b_id = setup_instructor_routing_data["inst_b_id"]

    # 1. Submit and Approve for past date by Instructor A
    sub_res = client.post("/api/v1/parade/submit", json={
        "date": past_date,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "26/1",
        "records": [
            {"student_id": "st-ct-01", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)
    assert sub_res.status_code == 200
    sub_id = sub_res.json()["id"]

    token_a = create_access_token("inst_kamal")
    client.post(f"/api/v1/parade/submissions/{sub_id}/approve", json={
        "remarks": "Approved August Parade"
    }, headers={"Authorization": f"Bearer {token_a}"})

    # Verify historical submission has Instructor A as approver
    hist_sub_1 = client.get(f"/api/v1/parade/submissions/{sub_id}", headers=auth_headers).json()
    assert hist_sub_1["status"] == "APPROVED"
    assert "Kamal Perera" in hist_sub_1["officer_name"]

    # 2. Academic Module reassigns Batch 26/1 to Instructor B
    batch = db_session.query(Batch).filter_by(id=setup_instructor_routing_data["batch_ct_id"]).first()
    batch.instructor_id = inst_b_id
    db_session.commit()

    # 3. Verify that the historical approved submission STILL shows Instructor A!
    hist_sub_2 = client.get(f"/api/v1/parade/submissions/{sub_id}", headers=auth_headers).json()
    assert hist_sub_2["status"] == "APPROVED"
    assert "Kamal Perera" in hist_sub_2["officer_name"]

    # 4. But new submission routes to Instructor B
    today = date.today().isoformat()
    new_sub_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Computer Technician",
        "course_id": setup_instructor_routing_data["course_ct_id"],
        "batch": "26/1",
        "records": [
            {"student_id": "st-ct-01", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)
    assert new_sub_res.status_code == 200
    assert "Nimal Silva" in new_sub_res.json()["approving_officer"]
