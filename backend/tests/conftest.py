"""Fixtures shared by every test."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    """Calls the app in-process, without starting a server."""
    with TestClient(app) as test_client:
        yield test_client
