from fastapi.testclient import TestClient


def test_signatures(client: TestClient) -> None:
    response = client.get("/api/signatures")
    assert response.status_code == 200
