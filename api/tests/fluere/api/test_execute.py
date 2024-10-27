from fastapi.testclient import TestClient


def test_signatures(client: TestClient) -> None:
    response = client.post(
        "/api/execute",
        json={
            "nodes": [
                {
                    "id": "1",
                    "name": "_int",
                    "cache": True,
                    "parameters": [{"name": "value", "value": "5"}],
                },
                {"id": "2", "name": "_str", "cache": True, "parameters": []},
                {"id": "3", "name": "_bool", "cache": True, "parameters": []},
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2", "parameter": "value"},
                {"id": "e2-3", "source": "2", "target": "3", "parameter": "value"},
            ],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"1": 5, "2": "5", "3": True}
