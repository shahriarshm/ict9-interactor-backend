from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data
