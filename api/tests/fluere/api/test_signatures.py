from fastapi.testclient import TestClient

from fluere.app import app

client = TestClient(app)


def test_signatures():
    response = client.get("/api/signatures")
    assert response.status_code == 200
