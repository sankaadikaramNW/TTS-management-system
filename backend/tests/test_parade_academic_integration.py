from datetime import date, timedelta
import pytest
from app.models.academic import Course, Subject, Exam, ExamMark
from app.models.student import Student, ParadeState, ParadeSubmission, ParadeStatusType
from app.models.user import User, AuditLog

@pytest.fixture
def auth_headers(client):
    # Login as admin to get token
    login_data = {
        "username": "admin",
        "password": "Admin@123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_setup(db_session):
    # Ensure ParadeStatusTypes are present
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

    # Create Course & Subject
    course = Course(
        id='crs-aero-26',
        code='AERO-2026',
        name='Aeronautical Engineering Basic',
        trade_id='trade-airframe',
        duration_weeks=24
    )
    db_session.add(course)

    subject = Subject(
        id='subj-propulsion-01',
        course_id=course.id,
        code='AERO-101',
        name='Aircraft Propulsion Systems',
        periods=40
    )
    db_session.add(subject)

    # Create Trainees
    t_present = Student(
        id='std-01-present',
        service_number='51837',
        full_name='Trainee Alpha',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        status='Active',
        batch='26/1'
    )
    t_leave = Student(
        id='std-02-leave',
        service_number='51838',
        full_name='Trainee Bravo',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        status='Active',
        batch='26/1'
    )
    t_hospital = Student(
        id='std-03-hospital',
        service_number='51839',
        full_name='Trainee Charlie',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        status='Active',
        batch='26/1'
    )
    t_awol = Student(
        id='std-04-awol',
        service_number='51840',
        full_name='Trainee Delta',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        status='Active',
        batch='26/1'
    )
    t_course_visit = Student(
        id='std-05-cvisit',
        service_number='51841',
        full_name='Trainee Echo',
        rank='LAC',
        trade='Airframe',
        course_id=course.id,
        status='Active',
        batch='26/1'
    )

    db_session.add_all([t_present, t_leave, t_hospital, t_awol, t_course_visit])
    db_session.commit()

    return {
        'course': course,
        'subject': subject,
        'students': {
            'present': t_present,
            'leave': t_leave,
            'hospital': t_hospital,
            'awol': t_awol,
            'course_visit': t_course_visit
        }
    }


def test_parade_state_academic_integration_workflow(client, auth_headers, test_setup, db_session):
    setup = test_setup
    course = setup['course']
    subject = setup['subject']
    students = setup['students']
    exam_date = date(2026, 9, 10)

    # 1. Schedule Examination for exam_date
    exam = Exam(
        id='exam-phase-01',
        course_id=course.id,
        subject_id=subject.id,
        type='Phase Test',
        date=exam_date,
        max_marks=100.0,
        pass_marks=50.0
    )
    db_session.add(exam)
    db_session.commit()

    # 2. Setup APPROVED Parade State for exam_date
    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    parade_sub = ParadeSubmission(
        id='ps-sub-20260910',
        date=exam_date,
        trade='Airframe',
        status='APPROVED',
        submitted_by=admin_user.id,
        approving_officer_id=admin_user.id
    )
    db_session.add(parade_sub)

    ps_records = [
        ParadeState(student_id=students['present'].id, date=exam_date, status='Present', submission_id=parade_sub.id),
        ParadeState(student_id=students['leave'].id, date=exam_date, status='Leave', submission_id=parade_sub.id),
        ParadeState(student_id=students['hospital'].id, date=exam_date, status='Hospital', submission_id=parade_sub.id),
        ParadeState(student_id=students['awol'].id, date=exam_date, status='AWOL', submission_id=parade_sub.id),
        ParadeState(student_id=students['course_visit'].id, date=exam_date, status='Course Visit', submission_id=parade_sub.id)
    ]
    db_session.add_all(ps_records)
    db_session.commit()

    # 3. TEST 1 - TEST 5: GET /academic/exams/{exam_id}/result-sheet
    res = client.get(f"/api/v1/academic/exams/{exam.id}/result-sheet", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()

    assert data["exam_id"] == exam.id
    assert data["is_parade_approved"] is True
    assert data["summary"]["total_trainees"] == 5
    assert data["summary"]["eligible_count"] == 1  # only Present
    assert data["summary"]["did_not_sit_count"] == 4

    st_map = {s["service_number"]: s for s in data["students"]}

    # TEST 1: Present -> marks_entry_allowed = True
    assert st_map['51837']["can_sit_exam"] is True
    assert st_map['51837']["marks_entry_allowed"] is True
    assert st_map['51837']["parade_state_status"] == 'Present'

    # TEST 2: Leave -> marks_entry_allowed = False, result_status = LEAVE
    assert st_map['51838']["can_sit_exam"] is False
    assert st_map['51838']["marks_entry_allowed"] is False
    assert st_map['51838']["result_status"] == 'LEAVE'

    # TEST 3: Hospital -> marks_entry_allowed = False, result_status = IN HOSPITAL
    assert st_map['51839']["can_sit_exam"] is False
    assert st_map['51839']["marks_entry_allowed"] is False
    assert st_map['51839']["result_status"] == 'IN HOSPITAL'

    # TEST 4: AWOL -> marks_entry_allowed = False, result_status = AWOL
    assert st_map['51840']["can_sit_exam"] is False
    assert st_map['51840']["marks_entry_allowed"] is False
    assert st_map['51840']["result_status"] == 'AWOL'

    # TEST 5: Course Visit -> marks_entry_allowed = False, result_status = COURSE VISIT
    assert st_map['51841']["can_sit_exam"] is False
    assert st_map['51841']["marks_entry_allowed"] is False
    assert st_map['51841']["result_status"] == 'COURSE VISIT'


def test_unapproved_parade_state_does_not_block_exam(client, auth_headers, test_setup, db_session):
    # TEST 6: Parade State = Pending / Draft -> Does not block as official status
    setup = test_setup
    course = setup['course']
    subject = setup['subject']
    students = setup['students']
    pending_date = date(2026, 9, 15)

    exam_pending = Exam(
        id='exam-pending-ps',
        course_id=course.id,
        subject_id=subject.id,
        type='Phase Test',
        date=pending_date,
        max_marks=100.0,
        pass_marks=50.0
    )
    db_session.add(exam_pending)

    # Draft / Pending submission
    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    sub_pending = ParadeSubmission(
        id='ps-draft-20260915',
        date=pending_date,
        trade='Airframe',
        status='SUBMITTED',
        submitted_by=admin_user.id
    )
    db_session.add(sub_pending)
    p_leave = ParadeState(student_id=students['leave'].id, date=pending_date, status='Leave', submission_id=sub_pending.id)
    db_session.add(p_leave)
    db_session.commit()

    res = client.get(f"/api/v1/academic/exams/{exam_pending.id}/result-sheet", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["is_parade_approved"] is False

    st_map = {s["service_number"]: s for s in data["students"]}
    # Because submission is still SUBMITTED (pending approval), it does not officially block:
    assert st_map['51838']["can_sit_exam"] is True
    assert st_map['51838']["is_parade_approved"] is False


def test_date_based_isolation(client, auth_headers, test_setup, db_session):
    # TEST 8: Old Parade State status on a different date does not block exam on today's date
    setup = test_setup
    course = setup['course']
    subject = setup['subject']
    students = setup['students']

    old_date = date(2026, 9, 1)
    new_exam_date = date(2026, 9, 20)

    # Student was on Leave on old_date
    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    sub_old = ParadeSubmission(id='ps-old-date', date=old_date, trade='Airframe', status='APPROVED', submitted_by=admin_user.id)
    db_session.add(sub_old)
    p_old = ParadeState(student_id=students['leave'].id, date=old_date, status='Leave', submission_id=sub_old.id)
    db_session.add(p_old)

    exam_new = Exam(id='exam-new-date', course_id=course.id, subject_id=subject.id, type='Phase Test', date=new_exam_date, max_marks=100.0)
    db_session.add(exam_new)
    db_session.commit()

    res = client.get(f"/api/v1/academic/exams/{exam_new.id}/result-sheet", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    st_map = {s["service_number"]: s for s in data["students"]}
    # Should not be blocked by old date
    assert st_map['51838']["can_sit_exam"] is True


def test_backend_validation_rejects_ineligible_marks_submission(client, auth_headers, test_setup, db_session):
    # TEST 10: Unauthorized/direct API attempt to submit marks for an ineligible trainee
    setup = test_setup
    course = setup['course']
    subject = setup['subject']
    students = setup['students']
    test_date = date(2026, 9, 25)

    exam = Exam(id='exam-val-test', course_id=course.id, subject_id=subject.id, type='Phase Test', date=test_date, max_marks=100.0, pass_marks=50.0)
    db_session.add(exam)

    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    sub = ParadeSubmission(id='ps-val-test', date=test_date, trade='Airframe', status='APPROVED', submitted_by=admin_user.id)
    db_session.add(sub)
    p_awol = ParadeState(student_id=students['awol'].id, date=test_date, status='AWOL', submission_id=sub.id)
    db_session.add(p_awol)
    db_session.commit()

    # Attempt to post marks for AWOL trainee
    payload = {
        "exam_id": exam.id,
        "records": [
            {"student_id": students['awol'].id, "marks_obtained": 85.0, "remarks": "Malicious direct submission"}
        ]
    }
    res = client.post("/api/v1/academic/exam-marks", json=payload, headers=auth_headers)
    # Must be rejected with 400
    assert res.status_code == 400
    assert "AWOL" in res.json()["detail"] or "override" in res.json()["detail"].lower()


def test_controlled_officer_override_and_audit(client, auth_headers, test_setup, db_session):
    # TEST 11: Authorized officer override allows ineligible trainee to sit and records audit log
    setup = test_setup
    course = setup['course']
    subject = setup['subject']
    students = setup['students']
    ov_date = date(2026, 9, 30)

    exam = Exam(id='exam-override-test', course_id=course.id, subject_id=subject.id, type='Final Exam', date=ov_date, max_marks=100.0, pass_marks=50.0)
    db_session.add(exam)

    admin_user = db_session.query(User).filter(User.username == 'admin').first()
    sub = ParadeSubmission(id='ps-ov-test', date=ov_date, trade='Airframe', status='APPROVED', submitted_by=admin_user.id)
    db_session.add(sub)
    p_hosp = ParadeState(student_id=students['hospital'].id, date=ov_date, status='Hospital', submission_id=sub.id)
    db_session.add(p_hosp)
    db_session.commit()

    # Step 1: Perform controlled override
    override_payload = {
        "student_id": students['hospital'].id,
        "reason": "Special medical clearance granted by Senior Medical Officer for afternoon exam session",
        "remarks": "Cleared to sit theory paper only"
    }
    res_ov = client.post(f"/api/v1/academic/exams/{exam.id}/override-eligibility", json=override_payload, headers=auth_headers)
    assert res_ov.status_code == 200
    ov_data = res_ov.json()
    st_ov = next(s for s in ov_data["students"] if s["student_id"] == students['hospital'].id)
    assert st_ov["is_overridden"] is True
    assert st_ov["can_sit_exam"] is True
    assert st_ov["marks_entry_allowed"] is True

    # Step 2: Now enter marks successfully
    marks_payload = {
        "exam_id": exam.id,
        "records": [
            {"student_id": students['hospital'].id, "marks_obtained": 76.5, "remarks": "Sat via medical clearance override"}
        ]
    }
    res_marks = client.post("/api/v1/academic/exam-marks", json=marks_payload, headers=auth_headers)
    assert res_marks.status_code == 200

    # Step 3: Verify Result Sheet displays PASS
    res_sheet = client.get(f"/api/v1/academic/exams/{exam.id}/result-sheet", headers=auth_headers)
    assert res_sheet.status_code == 200
    updated_st = next(s for s in res_sheet.json()["students"] if s["student_id"] == students['hospital'].id)
    assert updated_st["marks_obtained"] == 76.5
    assert updated_st["result_status"] == 'PASS'
    assert updated_st["is_overridden"] is True

    # Step 4: Verify Audit Trail entry was recorded
    audit = db_session.query(AuditLog).filter(AuditLog.action == "EXAM_ELIGIBILITY_OVERRIDDEN").first()
    assert audit is not None
    assert "Special medical clearance" in audit.details
