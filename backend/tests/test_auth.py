import pytest

def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "admin"

def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_logout_success(client):
    # First login to get token
    res = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin@123"}
    )
    token = res.json()["access_token"]
    
    # Call logout with bearer token
    logout_res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert logout_res.status_code == 200
    assert logout_res.json()["message"] == "Logged out successfully"

def test_logout_unauthorized(client):
    logout_res = client.post("/api/v1/auth/logout")
    assert logout_res.status_code == 401

