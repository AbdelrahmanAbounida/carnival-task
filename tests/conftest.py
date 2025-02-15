import pytest
from fastapi.testclient import TestClient

from carnival.app import app


@pytest.fixture
def client():
    client = TestClient(app=app)
    yield client
