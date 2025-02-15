from fastapi.testclient import TestClient


def test_base_route(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()
