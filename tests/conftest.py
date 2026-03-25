"""
Pytest configuration and shared fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient for making requests to the FastAPI app.
    This fixture is function-scoped, so the app state is fresh for each test.
    """
    return TestClient(app)
