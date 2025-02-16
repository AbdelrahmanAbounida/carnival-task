from fastapi.testclient import TestClient


def test_base_route(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_compilance_route_correct_ports(
    client: TestClient, correct_dep_port: str, correct_arrival_port: str
):
    resp = client.post(
        "/api/v1/compilance",
        json={"departure_port": correct_dep_port, "arrival_port": correct_arrival_port},
    )
    assert resp.status_code == 200


def test_compilance_route_wrong_ports(client: TestClient):
    resp = client.post(
        "/api/v1/compilance", json={"departure_port": "PORT1", "arrival_port": "PORT2"}
    )
    assert resp.status_code == 500  # TODO:: SHOULD BE 404
