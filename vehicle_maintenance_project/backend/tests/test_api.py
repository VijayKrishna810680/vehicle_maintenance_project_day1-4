import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_vehicle():
    payload = {"vin":"TESTVIN123","make":"Toyota","model":"Corolla","year":2020}
    r = client.post("/vehicles/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["vin"] == "TESTVIN123"

def test_chat_endpoint():
    r = client.post("/chat", json={"message":"Hello"})
    assert r.status_code == 200
    assert "response" in r.json()
