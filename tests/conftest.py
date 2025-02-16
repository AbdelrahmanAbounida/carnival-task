import pytest
from fastapi.testclient import TestClient

from carnival.app import app


@pytest.fixture
def client():
    client = TestClient(app=app)
    yield client


@pytest.fixture
def correct_dep_port():
    return "OMSTQ"


@pytest.fixture
def correct_arrival_port():
    return "AEJEA"
