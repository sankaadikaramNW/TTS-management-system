import pytest

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_bunk_bed_accommodation_full_workflow(client):
    headers = get_auth_headers(client)

    # 1. Create a Building
    b_res = client.post("/api/v1/accommodation/buildings", json={
        "name": "Test Block Gamma (T3)",
        "type": "Airmen",
        "capacity": 40
    }, headers=headers)
    assert b_res.status_code == 200
    bldg_id = b_res.json()["id"]

    # 2. Create a Billet inside the Building
    bil_res = client.post("/api/v1/accommodation/billets", json={
        "building_id": bldg_id,
        "name": "Test Billet Gamma-1",
        "bunk_bed_count": 5
    }, headers=headers)
    assert bil_res.status_code == 200
    billet_id = bil_res.json()["id"]

    # 3. Create a Bunk Bed inside the Billet (verifying automatic TOP and BOTTOM position creation)
    bunk_res = client.post("/api/v1/accommodation/bunks", json={
        "billet_id": billet_id,
        "bunk_no": "B-01-05",
        "status": "Active"
    }, headers=headers)
    assert bunk_res.status_code == 200
    bunk_data = bunk_res.json()
    assert bunk_data["bunk_no"] == "B-01-05"
    assert len(bunk_data["positions"]) == 2
    
    pos_types = {p["position_type"] for p in bunk_data["positions"]}
    assert "TOP" in pos_types and "BOTTOM" in pos_types

    top_pos = next(p for p in bunk_data["positions"] if p["position_type"] == "TOP")
    bottom_pos = next(p for p in bunk_data["positions"] if p["position_type"] == "BOTTOM")

    # 4. Create two students for allocation testing
    student_payload_1 = {
        "service_number": "SLAF/88881",
        "initials": "A.B.",
        "full_name": "Trainee Alpha",
        "nic": "200088888881",
        "dob": "2000-01-01",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "course_id": None,
        "batch": "120th Intake",
        "joining_date": "2026-01-01",
        "emergency_contact_name": "Parent Alpha",
        "emergency_contact_phone": "0770000001",
        "blood_group": "A+",
        "religion": "Buddhist",
        "permanent_address": "Katunayake Base"
    }
    s1_res = client.post("/api/v1/students", json=student_payload_1, headers=headers)
    assert s1_res.status_code == 200
    student1_id = s1_res.json()["id"]

    student_payload_2 = {
        "service_number": "SLAF/88882",
        "initials": "C.D.",
        "full_name": "Trainee Beta",
        "nic": "200088888882",
        "dob": "2000-02-02",
        "gender": "Male",
        "rank": "Leading Aircraftman",
        "trade": "Avionics",
        "course_id": None,
        "batch": "120th Intake",
        "joining_date": "2026-01-01",
        "emergency_contact_name": "Parent Beta",
        "emergency_contact_phone": "0770000002",
        "blood_group": "B+",
        "religion": "Christian",
        "permanent_address": "Ekala Base"
    }
    s2_res = client.post("/api/v1/students", json=student_payload_2, headers=headers)
    assert s2_res.status_code == 200
    student2_id = s2_res.json()["id"]

    # 5. Allocate TOP Position to Trainee Alpha
    alloc1_res = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student1_id,
        "bed_position_id": top_pos["id"],
        "remarks": "Assigned to TOP bed position"
    }, headers=headers)
    assert alloc1_res.status_code == 200
    alloc1_data = alloc1_res.json()
    assert alloc1_data["position_code"] == top_pos["position_code"]

    # 6. Attempt assigning Trainee Alpha to another position (should fail: Duplicate Trainee Accommodation)
    dup_trainee_res = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student1_id,
        "bed_position_id": bottom_pos["id"]
    }, headers=headers)
    assert dup_trainee_res.status_code == 400
    assert "already assigned" in dup_trainee_res.json()["detail"].lower()

    # 7. Attempt assigning Trainee Beta to the already occupied TOP position (should fail: Double Allocation)
    dup_pos_res = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student2_id,
        "bed_position_id": top_pos["id"]
    }, headers=headers)
    assert dup_pos_res.status_code == 400
    assert "not available" in dup_pos_res.json()["detail"].lower()

    # 8. Allocate BOTTOM Position to Trainee Beta (Same Bunk, 2 positions)
    alloc2_res = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student2_id,
        "bed_position_id": bottom_pos["id"],
        "remarks": "Assigned to BOTTOM bed position of same bunk"
    }, headers=headers)
    assert alloc2_res.status_code == 200

    # 9. Verify Bunk Positions Status
    bunk_positions_res = client.get(f"/api/v1/accommodation/bunks/{bunk_data['id']}/positions", headers=headers)
    assert bunk_positions_res.status_code == 200
    positions_list = bunk_positions_res.json()
    assert all(p["status"] == "Occupied" for p in positions_list)

    # 10. Transfer Trainee Alpha to a new Bunk position
    new_bunk_res = client.post("/api/v1/accommodation/bunks", json={
        "billet_id": billet_id,
        "bunk_no": "B-01-06",
        "status": "Active"
    }, headers=headers)
    assert new_bunk_res.status_code == 200
    new_top_pos = next(p for p in new_bunk_res.json()["positions"] if p["position_type"] == "TOP")

    trans_res = client.post("/api/v1/accommodation/transfer", json={
        "student_id": student1_id,
        "new_bed_position_id": new_top_pos["id"],
        "remarks": "Transferred to B-01-06-TOP"
    }, headers=headers)
    assert trans_res.status_code == 200

    # 11. Vacate Trainee Beta from BOTTOM Position
    vac_res = client.post(f"/api/v1/accommodation/vacate/{alloc2_res.json()['id']}", json={
        "vacate_reason": "Course Completed",
        "remarks": "Passed out successfully"
    }, headers=headers)
    assert vac_res.status_code == 200

    # 12. Check Dashboard Statistics API
    dash_res = client.get("/api/v1/accommodation/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash = dash_res.json()
    assert dash["total_bunk_beds"] >= 2
    assert dash["total_sleeping_positions"] >= 4
