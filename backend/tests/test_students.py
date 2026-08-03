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

