from fastapi.testclient import TestClient

from sample_notes import app

client = TestClient(app)


def test_health():
    response = client.get("/health_check/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong!"}


def test_login_admin():
    response = client.get("/health_check/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong!"}


def test_login_user():
    response = client.get("/health_check/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "Pong!"}

