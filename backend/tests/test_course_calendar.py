import pytest

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_course_calendar_workflow(client):
    headers = get_auth_headers(client)

    # 1. Fetch available trades & courses
    courses_res = client.get("/api/v1/academic/courses", headers=headers)
    if courses_res.status_code == 200 and len(courses_res.json()) > 0:
        course_id = courses_res.json()[0]["id"]
    else:
        # Create a trade & course for testing
        t_res = client.post("/api/v1/academic/trades", json={"code": "TESTCAL", "label": "Test Calendar Trade"}, headers=headers)
        trade_id = t_res.json()["id"]
        c_res = client.post("/api/v1/academic/courses", json={
            "code": "TEST-CAL-101",
            "name": "Computer Technician – 26/1 Advance Course",
            "trade_id": trade_id,
            "duration_weeks": 24
        }, headers=headers)
        course_id = c_res.json()["id"]

    # 2. Fetch active instructors list
    inst_res = client.get("/api/v1/academic/instructors/active", headers=headers)
    assert inst_res.status_code == 200
    instructors = inst_res.json()
    instructor_id = instructors[0]["id"] if len(instructors) > 0 else None

    # 3. Create Phase 1 Entry (English Intensive Period)
    p1_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "English Intensive Period",
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
    assert p1_data["phase_name"] == "English Intensive Period"
    assert p1_data["total_periods"] == 42
    p1_id = p1_data["id"]

    # 4. Create Phase 2 Entry (Communication Ceremony & Practical)
    p2_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "Communication Ceremony & Practical",
        "theory_periods": 10,
        "practical_periods": 20,
        "working_days": 5,
        "commencement_date": "2026-06-05",
        "completion_date": "2026-06-12",
        "instructor_id": instructor_id
    }, headers=headers)
    assert p2_res.status_code == 200
    p2_data = p2_res.json()
    assert p2_data["total_periods"] == 30
    p2_id = p2_data["id"]

    # 5. Get full Course Calendar
    cal_res = client.get(f"/api/v1/academic/courses/{course_id}/calendar", headers=headers)
    assert cal_res.status_code == 200
    calendar_entries = cal_res.json()
    assert len(calendar_entries) >= 2
    assert calendar_entries[0]["serial_number"] == 1
    assert calendar_entries[1]["serial_number"] == 2

    # 6. Test invalid date validation (completion before commencement -> 400)
    bad_date_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar", json={
        "phase_name": "Invalid Date Phase",
        "theory_periods": 10,
        "practical_periods": 5,
        "working_days": 2,
        "commencement_date": "2026-06-15",
        "completion_date": "2026-06-10"
    }, headers=headers)
    assert bad_date_res.status_code == 400

    # 7. Update Phase 1
    up_res = client.put(f"/api/v1/academic/course-calendar/{p1_id}", json={
        "theory_periods": 50,
        "remarks": "Updated orientation period"
    }, headers=headers)
    assert up_res.status_code == 200
    assert up_res.json()["total_periods"] == 50

    # 8. Reorder entries
    reorder_res = client.post(f"/api/v1/academic/courses/{course_id}/calendar/reorder", json={
        "ordered_ids": [p2_id, p1_id]
    }, headers=headers)
    assert reorder_res.status_code == 200
    reordered = reorder_res.json()
    assert reordered[0]["id"] == p2_id
    assert reordered[0]["serial_number"] == 1
    assert reordered[1]["id"] == p1_id
    assert reordered[1]["serial_number"] == 2

    # 9. Delete Phase 2
    del_res = client.delete(f"/api/v1/academic/course-calendar/{p2_id}", headers=headers)
    assert del_res.status_code == 200
