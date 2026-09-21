from datetime import date, timedelta
import pytest
from app.models.academic import Course, Batch
from app.models.student import Student, ParadeState, ParadeSubmission, ParadeStatusType, OfficerInCharge
from app.models.user import User, Role, Permission, AuditLog

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
def setup_night_parade_data(db_session):
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

    # Create Course
    course = Course(
        id='crs-night-01',
        code='AERO-NIGHT',
        name='Aero Mechanical Engineering',
        trade_id='trade-aero',
        duration_weeks=24
    )
    db_session.add(course)
    db_session.flush()

    # Create Trainees with distinct statuses
    # S1: Present, S2: Hospital, S3: Sick Report, S4: Leave, S5: Present
    s1 = Student(
        id='std-night-01',
        service_number='80001',
        full_name='Perera A B',
        rank='AC',
        trade='Airframe',
        course_id=course.id,
        batch='Batch A',
        medical_category='A4G4',
        status='Active'
    )
    s2 = Student(
        id='std-night-02',
        service_number='80002',
        full_name='Silva K L',
        rank='Cpl',
        trade='Airframe',
        course_id=course.id,
        batch='Batch A',
        medical_category='A4G2',
        status='Active'
    )
    s3 = Student(
        id='std-night-03',
        service_number='80003',
        full_name='Fernando M D',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        batch='Batch A',
        medical_category='A4G4',
        status='Active'
    )
    s4 = Student(
        id='std-night-04',
        service_number='80004',
        full_name='Gunaratne R P',
        rank='AC',
        trade='Airframe',
        course_id=course.id,
        batch='Batch A',
        medical_category='A4G4',
        status='Active'
    )
    s5 = Student(
        id='std-night-05',
        service_number='80005',
        full_name='Jayasinghe N T',
        rank='AC',
        trade='Airframe',
        course_id=course.id,
        batch='Batch A',
        medical_category='A4G4',
        status='Active'
    )
    db_session.add_all([s1, s2, s3, s4, s5])
    db_session.commit()

    return {
        "course": course,
        "students": [s1, s2, s3, s4, s5]
    }


def test_06_night_parade_opened_before_morning_parade_exists(client, auth_headers, db_session, setup_night_parade_data):
    """
    TEST 06: Night Parade opened before Morning Parade State exists.
    System must indicate Morning Baseline is unavailable and reject completion.
    """
    test_date = date(2026, 9, 21)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # 1. Fetch Context - should indicate morning_available = False
    res = client.get(f"/api/v1/parade/night/context?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["morning_available"] is False
    assert len(data["trainees"]) == 0

    # 2. Attempt to complete Night Parade without Morning Parade - must be rejected with 400
    payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "records": [
            {"student_id": s1.id, "night_status": "Present", "is_verified": True}
        ]
    }
    comp_res = client.post("/api/v1/parade/night/complete", json=payload, headers=auth_headers)
    assert comp_res.status_code == 400
    assert "MORNING PARADE STATE NOT AVAILABLE" in comp_res.json()["detail"]


def test_01_to_05_status_comparison_and_transitions(client, auth_headers, db_session, setup_night_parade_data):
    """
    TEST 01: Morning = Present, Evening = Present -> Inherited, status_changed = False
    TEST 02: Morning = Hospital, Evening = Present (discharged) -> status_changed = True
    TEST 03: Morning = Sick Report, Evening = Present (fit for duty) -> status_changed = True
    TEST 04: Morning = Leave, Evening = Leave -> Inherited, status_changed = False
    TEST 05: Morning = Present, Evening = Hospital (admitted afternoon) -> status_changed = True
    TEST 07: Draft state saving without modifying Morning records.
    """
    test_date = date(2026, 9, 22)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # Set up Morning Parade baseline
    m_sub = ParadeSubmission(
        id='sub-m-22',
        date=test_date,
        trade='Airframe',
        parade_type='MORNING',
        status='APPROVED'
    )
    db_session.add(m_sub)
    m1 = ParadeState(student_id=s1.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    m2 = ParadeState(student_id=s2.id, date=test_date, parade_type='MORNING', status='Hospital', submission_id=m_sub.id, remarks='Admitted in morning')
    m3 = ParadeState(student_id=s3.id, date=test_date, parade_type='MORNING', status='Sick Report', submission_id=m_sub.id)
    m4 = ParadeState(student_id=s4.id, date=test_date, parade_type='MORNING', status='Leave', submission_id=m_sub.id)
    m5 = ParadeState(student_id=s5.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    db_session.add_all([m1, m2, m3, m4, m5])
    db_session.commit()

    # 1. Open Night Parade context - inherits baseline initially
    ctx_res = client.get(f"/api/v1/parade/night/context?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    assert ctx_res.status_code == 200
    ctx_data = ctx_res.json()
    assert ctx_data["morning_available"] is True
    assert len(ctx_data["trainees"]) == 5

    t_map = {t["student_id"]: t for t in ctx_data["trainees"]}
    assert t_map[s1.id]["morning_status"] == "Present"
    assert t_map[s1.id]["night_status"] == "Present"
    assert t_map[s2.id]["morning_status"] == "Hospital"
    assert t_map[s3.id]["morning_status"] == "Sick Report"
    assert t_map[s4.id]["morning_status"] == "Leave"
    assert t_map[s5.id]["morning_status"] == "Present"

    # 2. Save Draft of Evening Roll Call with changes
    draft_payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "submitter_remarks": "Evening roll call draft in progress",
        "records": [
            {"student_id": s1.id, "morning_status": "Present", "night_status": "Present", "is_verified": True},
            {"student_id": s2.id, "morning_status": "Hospital", "night_status": "Present", "remarks": "Discharged from hospital at 1600 hrs", "is_verified": True},
            {"student_id": s3.id, "morning_status": "Sick Report", "night_status": "Present", "remarks": "Marked fit by Medical Officer", "is_verified": True},
            {"student_id": s4.id, "morning_status": "Leave", "night_status": "Leave", "is_verified": True},
            {"student_id": s5.id, "morning_status": "Present", "night_status": "Hospital", "remarks": "Admitted to Base Hospital at 1730 hrs with fever", "is_verified": True}
        ]
    }
    draft_res = client.post("/api/v1/parade/night/draft", json=draft_payload, headers=auth_headers)
    assert draft_res.status_code == 200
    assert draft_res.json()["status"] in ["saved", "draft_saved"]
    assert draft_res.json()["changed_count"] == 3

    # Verify context reflecting draft states
    ctx_res2 = client.get(f"/api/v1/parade/night/context?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    t_map2 = {t["student_id"]: t for t in ctx_res2.json()["trainees"]}

    # TEST 01: Morning = Present, Night = Present -> Changed = False
    assert t_map2[s1.id]["night_status"] == "Present"
    assert t_map2[s1.id]["status_changed"] is False

    # TEST 02: Morning = Hospital, Night = Present -> Changed = True
    assert t_map2[s2.id]["morning_status"] == "Hospital"
    assert t_map2[s2.id]["night_status"] == "Present"
    assert t_map2[s2.id]["status_changed"] is True
    assert "Discharged from hospital" in t_map2[s2.id]["remarks"]

    # TEST 03: Morning = Sick Report, Night = Present -> Changed = True
    assert t_map2[s3.id]["morning_status"] == "Sick Report"
    assert t_map2[s3.id]["night_status"] == "Present"
    assert t_map2[s3.id]["status_changed"] is True

    # TEST 04: Morning = Leave, Night = Leave -> Changed = False
    assert t_map2[s4.id]["morning_status"] == "Leave"
    assert t_map2[s4.id]["night_status"] == "Leave"
    assert t_map2[s4.id]["status_changed"] is False

    # TEST 05: Morning = Present, Night = Hospital -> Changed = True
    assert t_map2[s5.id]["morning_status"] == "Present"
    assert t_map2[s5.id]["night_status"] == "Hospital"
    assert t_map2[s5.id]["status_changed"] is True

    # Verify Morning records are UNCHANGED in DB
    m_check = db_session.query(ParadeState).filter(ParadeState.student_id == s2.id, ParadeState.parade_type == 'MORNING').first()
    assert m_check.status == 'Hospital'
    assert m_check.remarks == 'Admitted in morning'


def test_strength_reconciliation_and_completion_workflow(client, auth_headers, db_session, setup_night_parade_data):
    """
    STRENGTH & ACCOUNTABILITY COMPLETION VALIDATION:
    1. Rejects completion if strength is incomplete (e.g. Accounted = 4, Expected = 5).
    2. Allows completion when Expected Strength = Total Valid Night Statuses (5/5).
    3. Rejects duplicate completion with 409.
    4. NO INSTRUCTOR APPROVAL REQUIRED — transitions directly to COMPLETED.
    """
    test_date = date(2026, 9, 23)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # Create approved morning baseline for all 5 trainees
    m_sub = ParadeSubmission(id='sub-m-23', date=test_date, trade='Airframe', parade_type='MORNING', status='APPROVED')
    db_session.add(m_sub)
    for s in [s1, s2, s3, s4, s5]:
        db_session.add(ParadeState(student_id=s.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id))
    db_session.commit()

    # 1. Attempt completion with INCOMPLETE records (only 4 of 5 trainees)
    incomplete_payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "submitter_remarks": "Night roll call partially completed",
        "records": [
            {"student_id": s1.id, "night_status": "Present", "is_verified": True},
            {"student_id": s2.id, "night_status": "Hospital", "remarks": "Inward", "is_verified": True},
            {"student_id": s3.id, "night_status": "Present", "is_verified": True},
            {"student_id": s4.id, "night_status": "Leave", "is_verified": True}
            # Missing s5!
        ]
    }
    inc_res = client.post("/api/v1/parade/night/complete", json=incomplete_payload, headers=auth_headers)
    assert inc_res.status_code == 400
    assert "Expected Strength: 5, Accounted: 4, Unverified: 1" in inc_res.json()["detail"]

    # 2. Complete Night Parade with all 5 trainees verified
    complete_payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "submitter_remarks": "Night roll call 100% verified and complete.",
        "records": [
            {"student_id": s1.id, "night_status": "Present", "is_verified": True},
            {"student_id": s2.id, "night_status": "Hospital", "remarks": "Inward", "is_verified": True},
            {"student_id": s3.id, "night_status": "Present", "is_verified": True},
            {"student_id": s4.id, "night_status": "Leave", "is_verified": True},
            {"student_id": s5.id, "night_status": "Present", "is_verified": True}
        ]
    }
    comp_res = client.post("/api/v1/parade/night/complete", json=complete_payload, headers=auth_headers)
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["status"] == "completed"
    assert comp_data["expected_strength"] == 5
    assert comp_data["accounted_strength"] == 5

    # 3. Verify submission is marked COMPLETED in database
    night_sub = db_session.query(ParadeSubmission).filter(
        ParadeSubmission.date == test_date,
        ParadeSubmission.trade == 'Airframe',
        ParadeSubmission.parade_type == 'NIGHT'
    ).first()
    assert night_sub is not None
    assert night_sub.status == 'COMPLETED'

    # 4. Duplicate completion attempt must fail with 409
    dup_res = client.post("/api/v1/parade/night/complete", json=complete_payload, headers=auth_headers)
    assert dup_res.status_code == 409
    assert "already COMPLETED" in dup_res.json()["detail"]


def test_no_instructor_approval_dependency(client, auth_headers, db_session, setup_night_parade_data):
    """
    NO INSTRUCTOR APPROVAL RULE:
    Night Parade is an accountability exercise that does not depend on instructor assignment or approval.
    """
    test_date = date(2026, 9, 24)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # Morning Baseline
    m_sub = ParadeSubmission(id='sub-m-24', date=test_date, trade='Airframe', parade_type='MORNING', status='APPROVED')
    db_session.add(m_sub)
    for s in [s1, s2, s3, s4, s5]:
        db_session.add(ParadeState(student_id=s.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id))
    db_session.commit()

    # Complete Night Parade directly (no approving_officer_id provided)
    payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "submitter_remarks": "Evening muster roll confirmed.",
        "records": [
            {"student_id": s1.id, "night_status": "Present", "is_verified": True},
            {"student_id": s2.id, "night_status": "Sick Report", "remarks": "Reported sick at 1900 hrs", "is_verified": True},
            {"student_id": s3.id, "night_status": "Present", "is_verified": True},
            {"student_id": s4.id, "night_status": "Leave", "is_verified": True},
            {"student_id": s5.id, "night_status": "Present", "is_verified": True}
        ]
    }
    res = client.post("/api/v1/parade/night/complete", json=payload, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "completed"

    # Context reflects COMPLETED status directly
    ctx = client.get(f"/api/v1/parade/night/context?parade_date={test_date}&trade=Airframe", headers=auth_headers).json()
    assert ctx["night_submission_status"] == "COMPLETED"
    assert ctx["is_accountability_complete"] is True
    assert ctx["expected_strength"] == 5
    assert ctx["accounted_strength"] == 5
    assert ctx["unverified_count"] == 0


def test_night_parade_summary_and_report(client, auth_headers, db_session, setup_night_parade_data):
    """Test Night Parade Summary aggregations, trade-wise, category-wise, and formal report generation."""
    test_date = date(2026, 9, 25)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # Create baseline and night states
    m_sub = ParadeSubmission(id='sub-m-25', date=test_date, trade='Airframe', parade_type='MORNING', status='APPROVED')
    db_session.add(m_sub)
    m1 = ParadeState(student_id=s1.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    m2 = ParadeState(student_id=s2.id, date=test_date, parade_type='MORNING', status='Hospital', submission_id=m_sub.id)
    m3 = ParadeState(student_id=s3.id, date=test_date, parade_type='MORNING', status='Sick Report', submission_id=m_sub.id)
    m4 = ParadeState(student_id=s4.id, date=test_date, parade_type='MORNING', status='Leave', submission_id=m_sub.id)
    m5 = ParadeState(student_id=s5.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    db_session.add_all([m1, m2, m3, m4, m5])
    db_session.commit()

    # Night records
    n_sub = ParadeSubmission(id='sub-n-25', date=test_date, trade='Airframe', parade_type='NIGHT', status='COMPLETED')
    db_session.add(n_sub)
    n1 = ParadeState(student_id=s1.id, date=test_date, parade_type='NIGHT', status='Present', morning_status='Present', status_changed=False, submission_id=n_sub.id)
    n2 = ParadeState(student_id=s2.id, date=test_date, parade_type='NIGHT', status='Present', morning_status='Hospital', status_changed=True, submission_id=n_sub.id)
    n3 = ParadeState(student_id=s3.id, date=test_date, parade_type='NIGHT', status='Present', morning_status='Sick Report', status_changed=True, submission_id=n_sub.id)
    n4 = ParadeState(student_id=s4.id, date=test_date, parade_type='NIGHT', status='Leave', morning_status='Leave', status_changed=False, submission_id=n_sub.id)
    n5 = ParadeState(student_id=s5.id, date=test_date, parade_type='NIGHT', status='Hospital', morning_status='Present', status_changed=True, submission_id=n_sub.id)
    db_session.add_all([n1, n2, n3, n4, n5])
    db_session.commit()

    # 1. Summary endpoint
    sum_res = client.get(f"/api/v1/parade/night/summary?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    assert sum_res.status_code == 200
    sum_data = sum_res.json()
    assert sum_data["total_expected"] == 5
    assert sum_data["present"] == 3 # s1, s2, s3
    assert sum_data["hospital"] == 1 # s5
    assert sum_data["leave"] == 1 # s4
    assert sum_data["status_changed_count"] == 3

    # Verify transitions
    transitions = {f"{t['from_status']}->{t['to_status']}": t['count'] for t in sum_data["transitions"]}
    assert transitions.get("Hospital->Present") == 1
    assert transitions.get("Sick Report->Present") == 1
    assert transitions.get("Present->Hospital") == 1

    # Verify trade-wise and category-wise
    assert len(sum_data["trade_wise"]) >= 1
    assert len(sum_data["category_wise"]) >= 1

    # 2. Formal Report endpoint
    rep_res = client.get(f"/api/v1/parade/night/report?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    assert rep_res.status_code == 200
    rep_data = rep_res.json()
    assert "SRI LANKA AIR FORCE" in rep_data["title"]
    assert "NIGHT PARADE STATE" in rep_data["subtitle"]
    assert len(rep_data["rows"]) == 5
    r2 = next(r for r in rep_data["rows"] if r["service_number"] == '80002')
    assert r2["morning_status"] == 'Hospital'
    assert r2["night_status"] == 'Present'
    assert r2["status_changed"] == 'YES'


def test_partial_save_and_reload_persistence(client, auth_headers, db_session, setup_night_parade_data):
    """
    TEST: Verify /api/v1/parade/night/save endpoint:
    1. Saves partial progress (e.g. only 1 trainee's status changed: Hospital -> Present).
    2. Morning parade record remains strictly untouched (Hospital).
    3. Night parade record is permanently saved as Present with status_changed = True.
    4. Reload context returns saved night status.
    5. Night submission status is IN_PROGRESS (not COMPLETED).
    """
    test_date = date(2026, 9, 26)
    s1, s2, s3, s4, s5 = setup_night_parade_data["students"]

    # Set up Morning Parade baseline
    m_sub = ParadeSubmission(id='sub-m-26', date=test_date, trade='Airframe', parade_type='MORNING', status='APPROVED')
    db_session.add(m_sub)
    m1 = ParadeState(student_id=s1.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    m2 = ParadeState(student_id=s2.id, date=test_date, parade_type='MORNING', status='Hospital', submission_id=m_sub.id, remarks='Morning admission')
    m3 = ParadeState(student_id=s3.id, date=test_date, parade_type='MORNING', status='Sick Report', submission_id=m_sub.id)
    m4 = ParadeState(student_id=s4.id, date=test_date, parade_type='MORNING', status='Leave', submission_id=m_sub.id)
    m5 = ParadeState(student_id=s5.id, date=test_date, parade_type='MORNING', status='Present', submission_id=m_sub.id)
    db_session.add_all([m1, m2, m3, m4, m5])
    db_session.commit()

    # 1. User changes only s2 (Hospital -> Present with remark) and clicks SAVE NIGHT PARADE
    save_payload = {
        "date": str(test_date),
        "trade": "Airframe",
        "submitter_remarks": "Partial evening roll call progress",
        "records": [
            {
                "student_id": s2.id,
                "night_status": "Present",
                "remarks": "Discharged from hospital and returned to camp"
            }
        ]
    }

    save_res = client.post("/api/v1/parade/night/save", json=save_payload, headers=auth_headers)
    assert save_res.status_code == 200
    save_data = save_res.json()
    assert save_data["status"] == "saved"
    assert save_data["updated_count"] == 1
    assert save_data["changed_count"] == 1
    assert "last_saved_at" in save_data

    # 2. Verify Morning DB record is 100% UNCHANGED
    m2_db = db_session.query(ParadeState).filter(
        ParadeState.student_id == s2.id,
        ParadeState.date == test_date,
        ParadeState.parade_type == 'MORNING'
    ).first()
    assert m2_db.status == 'Hospital'
    assert m2_db.remarks == 'Morning admission'

    # 3. Verify Night DB record is permanently stored
    n2_db = db_session.query(ParadeState).filter(
        ParadeState.student_id == s2.id,
        ParadeState.date == test_date,
        ParadeState.parade_type == 'NIGHT'
    ).first()
    assert n2_db is not None
    assert n2_db.status == 'Present'
    assert n2_db.morning_status == 'Hospital'
    assert n2_db.status_changed is True
    assert "Discharged from hospital" in n2_db.remarks

    # 4. Verify reload context reflects saved night status
    ctx_res = client.get(f"/api/v1/parade/night/context?parade_date={test_date}&trade=Airframe", headers=auth_headers)
    assert ctx_res.status_code == 200
    trainees = {t["student_id"]: t for t in ctx_res.json()["trainees"]}
    assert trainees[s2.id]["morning_status"] == "Hospital"
    assert trainees[s2.id]["night_status"] == "Present"
    assert trainees[s2.id]["status_changed"] is True
    assert "Discharged from hospital" in trainees[s2.id]["remarks"]

    # 5. Verify submission status is IN_PROGRESS (not COMPLETED)
    assert ctx_res.json()["night_submission_status"] in ["IN_PROGRESS", "DRAFT"]

