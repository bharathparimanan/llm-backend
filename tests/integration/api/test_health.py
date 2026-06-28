"""
Integration tests for GET /api/v1/health endpoints.

These tests send real HTTP requests through the FastAPI test client and
assert on HTTP status codes and response bodies.  No mocking of route
logic — we test the full middleware → route → response pipeline.
"""

from fastapi.testclient import TestClient

from app.core.constants import API_V1_PREFIX, HEALTH_STATUS_OK, REQUEST_ID_HEADER


def test_liveness_returns_200(client: TestClient) -> None:
    response = client.get(f"{API_V1_PREFIX}/health")
    assert response.status_code == 200


def test_liveness_body_contains_status_ok(client: TestClient) -> None:
    body = client.get(f"{API_V1_PREFIX}/health").json()
    assert body["status"] == HEALTH_STATUS_OK


def test_liveness_body_contains_service_name(client: TestClient) -> None:
    body = client.get(f"{API_V1_PREFIX}/health").json()
    assert "service" in body
    assert body["service"] == "foundation-ai"


def test_liveness_response_has_request_id_header(client: TestClient) -> None:
    response = client.get(f"{API_V1_PREFIX}/health")
    assert REQUEST_ID_HEADER in response.headers


def test_readiness_returns_200(client: TestClient) -> None:
    response = client.get(f"{API_V1_PREFIX}/health/ready")
    assert response.status_code == 200


def test_readiness_body_contains_checks(client: TestClient) -> None:
    body = client.get(f"{API_V1_PREFIX}/health/ready").json()
    assert "checks" in body
    assert body["checks"]["api"] == HEALTH_STATUS_OK
