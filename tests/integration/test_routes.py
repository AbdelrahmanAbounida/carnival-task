from fastapi.testclient import TestClient
import os


# api fixed header
headers = {"server-api-key": os.environ.get("SERVER_API_KEY")}


def test_base_route(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_compilance_route_correct_ports(
    client: TestClient, correct_dep_port: str, correct_arrival_port: str
):
    params = {"departure_port": correct_dep_port, "arrival_port": correct_arrival_port}

    resp = client.get("api/v1/compilance", params=params, headers=headers)
    assert resp.status_code == 200


def test_compilance_route_wrong_ports(client: TestClient):
    params = {"departure_port": "ABCD", "arrival_port": "ABCD"}
    resp = client.get("api/v1/compilance", params=params, headers=headers)
    assert resp.status_code == 500  # TODO:: SHOULD BE 404
