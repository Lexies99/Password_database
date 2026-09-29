from fastapi.testclient import TestClient
from app.main import app
from app.core.security import hash_password, verify_password

client = TestClient(app)

def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_password_hashing():
    pwd = "MySecretPassword123!"
    h = hash_password(pwd)
    assert verify_password(pwd, h) is True
    assert verify_password("WrongPassword", h) is False
