"""
Shared pytest fixtures.

Fixtures defined here are available to all test modules without explicit
import.  Keep this file focused on infrastructure concerns (app client,
settings overrides, database setup) rather than domain-specific data.
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings


@pytest.fixture(scope="session")
def test_settings():
    """
    Provide a Settings instance with values safe for testing.

    We override get_settings() via dependency_overrides in the app fixture
    so that tests never read from a real .env file or require a live OpenAI key.
    """
    from app.core.config import Settings

    # Provide a dummy API key so Pydantic validation does not fail.
    # No real API calls are made in unit tests.
    return Settings(
        openai_api_key="sk-test-000000000000000000000000000000000000000000000000",
        environment="test",
        log_level="WARNING",
    )


@pytest.fixture(scope="session")
def app(test_settings):
    """
    Create a TestClient-ready FastAPI app with overridden dependencies.

    Using scope="session" means the app is constructed once per test run,
    which is efficient for integration tests that share state-free endpoints
    like the health check.
    """
    from app.api.dependencies import get_app_settings
    from app.main import create_app

    application = create_app()
    application.dependency_overrides[get_app_settings] = lambda: test_settings
    return application


@pytest.fixture(scope="session")
def client(app) -> TestClient:
    """Synchronous HTTP test client wrapping the FastAPI app."""
    with TestClient(app) as c:
        yield c
