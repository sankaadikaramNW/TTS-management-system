from datetime import date, timedelta
import pytest
from app.models.academic import Course
from app.models.student import Student, ParadeState, ParadeSubmission, ParadeStatusType, OfficerInCharge
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
def setup_monitoring_data(db_session):
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

    # Create Courses
    c1 = Course(
        id='crs-mon-af',
        code='AERO-MON',
        name='Aero Mechanical Basic',
        trade_id='trade-airframe',
        duration_weeks=24
    )
    c2 = Course(
        id='crs-mon-rad',
        code='RAD-MON',
        name='Radar Tech Basic',
        trade_id='trade-radar',
        duration_weeks=20
    )
    db_session.add_all([c1, c2])

    # Create Students across trades
    s1 = Student(
        id='std-af-01',
        service_number='90001',
        full_name='Trainee AF 1',
        rank='AC',
        trade='Airframe',
        course_id=c1.id,
        batch='101',
        status='Active'
    )
    s2 = Student(
        id='std-af-02',
        service_number='90002',
        full_name='Trainee AF 2',
        rank='LAC',
        trade='Airframe',
        course_id=c1.id,
        batch='101',
        status='Active'
    )
    s3 = Student(
        id='std-rad-01',
        service_number='90003',
        full_name='Trainee Radar 1',
        rank='AC',
        trade='Radar',
        course_id=c2.id,
        batch='102',
        status='Active'
    )
    db_session.add_all([s1, s2, s3])
    db_session.commit()

    # Appoint Officer I/C
    admin_user = db_session.query(User).filter_by(username='admin').first()
    if admin_user:
        oic = OfficerInCharge(
            id='oic-mon-af',
            trade='Airframe',
            user_id=admin_user.id
        )
        db_session.add(oic)
        db_session.commit()

    return {
        "admin_user_id": admin_user.id if admin_user else None,
        "students": [s1, s2, s3]
    }


def test_monitoring_all_not_submitted_initially(client, auth_headers, setup_monitoring_data):
    today = date.today().isoformat()
    res = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["date"] == today
    assert data["summary"]["total_required"] >= 2
    assert data["summary"]["not_submitted"] >= 2
    assert data["summary"]["approved"] == 0
    assert data["summary"]["pending_approval"] == 0


def test_parade_draft_does_not_count_as_submitted(client, auth_headers, setup_monitoring_data):
    today = date.today().isoformat()
    draft_payload = {
        "date": today,
        "trade": "Airframe",
        "records": [
            {"student_id": "std-af-01", "status": "Present", "remarks": "Draft entry"},
            {"student_id": "std-af-02", "status": "Present", "remarks": "Draft entry"}
        ]
    }
    draft_res = client.post("/api/v1/parade/draft", json=draft_payload, headers=auth_headers)
    assert draft_res.status_code == 200

    # Monitoring check: Airframe should still be NOT_SUBMITTED (draft is not submitted)
    res = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    af_item = next(i for i in data["items"] if i["trade"] == "Airframe")
    assert af_item["status_code"] == "NOT_SUBMITTED"


def test_parade_submit_moves_to_pending_approval(client, auth_headers, setup_monitoring_data):
    today = date.today().isoformat()
    admin_id = setup_monitoring_data["admin_user_id"]

    submit_payload = {
        "date": today,
        "trade": "Airframe",
        "approving_officer_id": admin_id,
        "submitter_remarks": "Morning muster complete",
        "records": [
            {"student_id": "std-af-01", "status": "Present", "remarks": ""},
            {"student_id": "std-af-02", "status": "Sick Report", "remarks": "At MI Room"}
        ]
    }
    sub_res = client.post("/api/v1/parade/submit", json=submit_payload, headers=auth_headers)
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["status"].upper() == "SUBMITTED"

    # Check monitoring summary and item
    mon_res = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    assert mon_res.status_code == 200
    mon_data = mon_res.json()
    assert mon_data["summary"]["pending_approval"] == 1
    af_item = next(i for i in mon_data["items"] if i["trade"] == "Airframe")
    assert af_item["status_code"] == "PENDING_APPROVAL"
    assert af_item["submission_id"] == sub_data["id"]

    # Pending queue should contain it
    pending_res = client.get("/api/v1/parade/submissions/pending", headers=auth_headers)
    assert pending_res.status_code == 200
    pending_items = pending_res.json()
    assert any(p["id"] == sub_data["id"] for p in pending_items)


def test_officer_return_for_correction_flow(client, auth_headers, setup_monitoring_data):
    today = date.today().isoformat()
    admin_id = setup_monitoring_data["admin_user_id"]

    # 1. Submit
    client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Airframe",
        "approving_officer_id": admin_id,
        "records": [
            {"student_id": "std-af-01", "status": "Present", "remarks": ""},
            {"student_id": "std-af-02", "status": "Present", "remarks": ""}
        ]
    }, headers=auth_headers)

    # Get submission ID
    mon_res = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    af_item = next(i for i in mon_res.json()["items"] if i["trade"] == "Airframe")
    sub_id = af_item["submission_id"]

    # 2. Return for correction
    return_res = client.post(f"/api/v1/parade/submissions/{sub_id}/return", json={
        "rejection_reason": "Trainee std-af-02 is reported sick at hospital. Please adjust status.",
        "remarks": "Returned for revision"
    }, headers=auth_headers)
    assert return_res.status_code == 200
    ret_data = return_res.json()
    assert ret_data["status"].upper() in ("REJECTED", "RETURNED", "RETURNED_FOR_CORRECTION")
    assert ret_data["rejection_reason"] == "Trainee std-af-02 is reported sick at hospital. Please adjust status."

    # 3. Monitoring verification: status is RETURNED
    mon_res2 = client.get(f"/api/v1/parade/monitoring?parade_date={today}", headers=auth_headers)
    mon_data2 = mon_res2.json()
    assert mon_data2["summary"]["returned"] == 1
    af_item2 = next(i for i in mon_data2["items"] if i["trade"] == "Airframe")
    assert af_item2["status_code"] == "RETURNED"
    assert "rejection_reason" in af_item2


def test_resubmission_updates_existing_record_without_duplicates(client, auth_headers, setup_monitoring_data, db_session):
    today = date.today().isoformat()
    admin_id = setup_monitoring_data["admin_user_id"]

    # Count initial rows
    initial_count = db_session.query(ParadeSubmission).filter_by(trade="Airframe", date=today).count()

    # Resubmit corrected records
    resubmit_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Airframe",
        "approving_officer_id": admin_id,
        "submitter_remarks": "Adjusted std-af-02 to Hospital per Officer instruction",
        "records": [
            {"student_id": "std-af-01", "status": "Present", "remarks": ""},
            {"student_id": "std-af-02", "status": "Hospital", "remarks": "Admitted SLAF Hospital"}
        ]
    }, headers=auth_headers)
    assert resubmit_res.status_code == 200

    # Ensure no duplicate submission rows created
    final_count = db_session.query(ParadeSubmission).filter_by(trade="Airframe", date=today).count()
    assert final_count == 1

    # Status is back to SUBMITTED and rejection reason cleared
    sub = db_session.query(ParadeSubmission).filter_by(trade="Airframe", date=today).first()
    assert sub.status == "SUBMITTED"
    assert sub.rejection_reason is None


def test_official_daily_strength_aggregates_approved_only(client, auth_headers, setup_monitoring_data, db_session):
    today = date.today().isoformat()
    admin_id = setup_monitoring_data["admin_user_id"]

    # 1. Initially nothing is approved -> Present is 0 when official_approved_only=True
    summary_res = client.get(f"/api/v1/parade/summary?parade_date={today}&official_approved_only=true", headers=auth_headers)
    assert summary_res.status_code == 200
    sum_data = summary_res.json()
    assert sum_data["present"] == 0

    # 2. Submit Airframe (1 Present, 1 Hospital)
    submit_res = client.post("/api/v1/parade/submit", json={
        "date": today,
        "trade": "Airframe",
        "approving_officer_id": admin_id,
        "submitter_remarks": "Morning muster",
        "records": [
            {"student_id": "std-af-01", "status": "Present", "remarks": ""},
            {"student_id": "std-af-02", "status": "Hospital", "remarks": "Admitted SLAF Hospital"}
        ]
    }, headers=auth_headers)
    assert submit_res.status_code == 200
    sub_id = submit_res.json()["id"]

    # 3. Before approval, official strength is still 0
    summary_res2 = client.get(f"/api/v1/parade/summary?parade_date={today}&official_approved_only=true", headers=auth_headers)
    assert summary_res2.status_code == 200
    assert summary_res2.json()["present"] == 0

    # 4. Now approve Airframe
    approve_res = client.post(f"/api/v1/parade/submissions/{sub_id}/approve", json={
        "remarks": "Approved as official strength"
    }, headers=auth_headers)
    assert approve_res.status_code == 200

    # 5. Now check official summary again: Present should be 1, Hospital 1
    summary_res3 = client.get(f"/api/v1/parade/summary?parade_date={today}&official_approved_only=true", headers=auth_headers)
    assert summary_res3.status_code == 200
    sum_data3 = summary_res3.json()
    assert sum_data3["present"] == 1
    assert sum_data3["hospital"] == 1


def test_date_range_monitoring(client, auth_headers, setup_monitoring_data):
    start = (date.today() - timedelta(days=3)).isoformat()
    end = date.today().isoformat()

    res = client.get(f"/api/v1/parade/monitoring/date-range?start_date={start}&end_date={end}", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) >= 4
    # Check that past unsubmitted days are flagged overdue
    past_unsubmitted = [i for i in data["items"] if i["date"] < date.today().isoformat() and i["status_code"] == "NOT_SUBMITTED"]
    if past_unsubmitted:
        assert past_unsubmitted[0]["is_overdue"] is True


def test_classical_outstanding_report_endpoint(client, auth_headers, setup_monitoring_data):
    today = date.today().isoformat()
    res = client.get(f"/api/v1/parade/reports/outstanding?parade_date={today}", headers=auth_headers)
    assert res.status_code == 200
    report = res.json()
    assert "title" in report
    assert "SRI LANKA AIR FORCE" in report["title"]
    assert "summary" in report
    assert "rows" in report
    assert len(report["rows"]) >= 2
