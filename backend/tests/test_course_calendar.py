import pytest

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_course_calendar_workflow(client):
    headers = get_auth_headers(client)

    # 1. Create isolated Trade & Course for testing
    import uuid
    uid = str(uuid.uuid4())[:8]
    t_res = client.post("/api/v1/academic/trades", json={"code": f"TCAL_{uid}", "label": f"Test Cal Trade {uid}"}, headers=headers)
    assert t_res.status_code == 200
    trade_id = t_res.json()["id"]

    c_res = client.post("/api/v1/academic/courses", json={
        "code": f"TCAL-101-{uid}",
        "name": f"Computer Technician – Advance Course {uid}",
        "trade_id": trade_id,
        "duration_weeks": 24
    }, headers=headers)
    assert c_res.status_code == 200
    course_id = c_res.json()["id"]

    # 2. Create subjects under this course
    s1_res = client.post("/api/v1/academic/subjects", json={
        "course_id": course_id,
        "code": "ENG-101",
        "name": "English Intensive Period",
        "periods": 42
    }, headers=headers)
    assert s1_res.status_code == 200
    s1_data = s1_res.json()
    subject1_id = s1_data["id"]

    s2_res = client.post("/api/v1/academic/subjects", json={
        "course_id": course_id,
        "code": "COM-102",
        "name": "Communication & Practical Training",
        "periods": 30
    }, headers=headers)
    assert s2_res.status_code == 200
    subject2_id = s2_res.json()["id"]

    # Verify fetching course subjects filtered by course_id
    sub_res = client.get(f"/api/v1/academic/subjects/{course_id}", headers=headers)
    assert sub_res.status_code == 200
    subjects_list = sub_res.json()
    assert len(subjects_list) == 2
    assert subjects_list[0]["course_id"] == course_id

    # 3. Fetch active instructors list
    inst_res = client.get("/api/v1/academic/instructors/active", headers=headers)
    assert inst_res.status_code == 200
    instructors = inst_res.json()
    instructor_id = instructors[0]["id"] if len(instructors) > 0 else None

    # 4. Create Phase 1 Entry with linked subject
    p1_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "[ENG-101] English Intensive Period",
        "subject_id": subject1_id,
        "theory_periods": 42,
        "practical_periods": 0,
        "working_days": 7,
        "commencement_date": "2026-05-27",
        "completion_date": "2026-06-05",
        "instructor_id": instructor_id,
        "remarks": "Initial language orientation"
    }, headers=headers)
    assert p1_res.status_code == 200
    p1_data = p1_res.json()
    assert p1_data["phase_name"] == "[ENG-101] English Intensive Period"
    assert p1_data["subject_id"] == subject1_id
    assert p1_data["subject_code"] == "ENG-101"
    assert p1_data["total_periods"] == 42
    p1_id = p1_data["id"]

    # 5. Create Phase 2 Entry with linked subject (non-overlapping dates)
    p2_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "[COM-102] Communication & Practical Training",
        "subject_id": subject2_id,
        "theory_periods": 10,
        "practical_periods": 20,
        "working_days": 5,
        "commencement_date": "2026-06-06",
        "completion_date": "2026-06-12",
        "instructor_id": instructor_id,
        "instructor_status": "ASSIGNED" if instructor_id else "NOT_ASSIGNED",
        "remarks": "Practical communication training"
    }, headers=headers)
    assert p2_res.status_code == 200
    p2_data = p2_res.json()
    assert p2_data["total_periods"] == 30
    assert p2_data["subject_id"] == subject2_id
    p2_id = p2_data["id"]

    # 6. Get full Course Calendar
    cal_res = client.get(f"/api/v1/academic/courses/{course_id}/calendar", headers=headers)
    assert cal_res.status_code == 200
    calendar_entries = cal_res.json()
    assert len(calendar_entries) == 2
    assert calendar_entries[0]["serial_number"] == 1
    assert calendar_entries[1]["serial_number"] == 2

    # 7. Test invalid date validation (completion before commencement -> 400)
    bad_date_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "Invalid Date Phase",
        "subject_id": subject1_id,
        "theory_periods": 10,
        "practical_periods": 5,
        "working_days": 2,
        "commencement_date": "2026-06-15",
        "completion_date": "2026-06-10"
    }, headers=headers)
    assert bad_date_res.status_code == 400

    # 8. Update Phase 1
    up_res = client.put(f"/api/v1/academic/course-calendar/{p1_id}", json={
        "theory_periods": 50,
        "remarks": "Updated orientation period"
    }, headers=headers)
    assert up_res.status_code == 200
    assert up_res.json()["total_periods"] == 50

    # 9. Reorder entries
    reorder_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar/reorder", json={
        "ordered_ids": [p2_id, p1_id]
    }, headers=headers)
    assert reorder_res.status_code == 200
    reordered = reorder_res.json()
    assert reordered[0]["id"] == p2_id
    assert reordered[0]["serial_number"] == 1
    assert reordered[1]["id"] == p1_id
    assert reordered[1]["serial_number"] == 2

    # 10. Delete Phase 2
    del_res = client.delete(f"/api/v1/academic/course-calendar/{p2_id}", headers=headers)
    assert del_res.status_code == 200
