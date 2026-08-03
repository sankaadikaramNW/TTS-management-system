import pytest

def get_auth_headers(client):
    res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_accommodation_full_workflow(client):
    headers = get_auth_headers(client)

    # 1. Create a Building
    b_res = client.post("/api/v1/accommodation/buildings", json={
        "name": "Test Block Beta (T2)",
        "type": "Airmen",
        "capacity": 20
    }, headers=headers)
    assert b_res.status_code == 200
    bldg_id = b_res.json()["id"]

    # 2. Create a Billet inside the Building
    bil_res = client.post("/api/v1/accommodation/billets", json={
        "building_id": bldg_id,
        "name": "Test Billet B-1",
        "capacity": 10
    }, headers=headers)
    assert bil_res.status_code == 200
    billet_id = bil_res.json()["id"]

    # 3. Create two Beds inside the Billet
    bed1_res = client.post("/api/v1/accommodation/beds", json={
        "billet_id": billet_id,
        "bed_number": "01",
        "status": "Vacant"
    }, headers=headers)
    assert bed1_res.status_code == 200
    bed1_id = bed1_res.json()["id"]

    bed2_res = client.post("/api/v1/accommodation/beds", json={
        "billet_id": billet_id,
        "bed_number": "02",
        "status": "Vacant"
    }, headers=headers)
    assert bed2_res.status_code == 200
    bed2_id = bed2_res.json()["id"]

    # 4. Create a student to assign to the bed
    student_payload = {
        "service_number": "SLAF/99999",
        "initials": "X.Y.Z.",
        "full_name": "Trainee Tester",
        "nic": "200099999999",
        "dob": "2000-01-01",
        "gender": "Male",
        "rank": "Aircraftman",
        "trade": "Airframe",
        "course_id": None,
        "batch": "120th Intake",
        "joining_date": "2026-01-01",
        "emergency_contact_name": "Contact Parent",
        "emergency_contact_phone": "0770000000",
        "blood_group": "A+",
        "religion": "Buddhist",
        "permanent_address": "Test Base, Katunayake"
    }
    s_res = client.post("/api/v1/students", json=student_payload, headers=headers)
    assert s_res.status_code == 200
    student_id = s_res.json()["id"]

    # 5. Allocate Bed 01 to the Trainee
    alloc_res = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student_id,
        "bed_id": bed1_id,
        "remarks": "Initial placement"
    }, headers=headers)
    assert alloc_res.status_code == 200
    alloc_id = alloc_res.json()["id"]

    # Verify bed status is now Occupied
    bed_check = client.get(f"/api/v1/accommodation/beds/billet/{billet_id}", headers=headers)
    assert bed_check.status_code == 200
    assert any(b["id"] == bed1_id and b["status"] == "Occupied" for b in bed_check.json())

    # 6. Attempt allocating the same occupied Bed 01 to another (should fail)
    fail_alloc = client.post("/api/v1/accommodation/allocate", json={
        "student_id": student_id,
        "bed_id": bed1_id
    }, headers=headers)
    assert fail_alloc.status_code == 400

    # 7. Transfer Trainee to Bed 02
    trans_res = client.post("/api/v1/accommodation/transfer", json={
        "student_id": student_id,
        "new_bed_id": bed2_id,
        "remarks": "Moved due to maintenance check"
    }, headers=headers)
    assert trans_res.status_code == 200

    # Verify old bed is Vacant, and new bed is Occupied
    bed_check2 = client.get(f"/api/v1/accommodation/beds/billet/{billet_id}", headers=headers)
    assert any(b["id"] == bed1_id and b["status"] == "Vacant" for b in bed_check2.json())
    assert any(b["id"] == bed2_id and b["status"] == "Occupied" for b in bed_check2.json())

    # 8. Vacate Bed 02
    vac_res = client.post(f"/api/v1/accommodation/vacate/{trans_res.json()['id']}", json={
        "vacate_reason": "Course Completed",
        "remarks": "End of training term"
    }, headers=headers)
    assert vac_res.status_code == 200

    # Verify both beds are now Vacant
    bed_check3 = client.get(f"/api/v1/accommodation/beds/billet/{billet_id}", headers=headers)
    assert all(b["status"] == "Vacant" for b in bed_check3.json())
