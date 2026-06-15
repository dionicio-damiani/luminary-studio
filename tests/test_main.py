"""Tests for the FastAPI app in app/main.py (TestClient is httpx-based)."""

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app import main

VALID_PAYLOAD = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "subject": "Project inquiry",
    "message": "Hello, I'd love to discuss a potential project with your studio.",
}


@pytest.fixture()
def client():
    """TestClient with a clean rate-limit bucket before and after each test."""
    main.limiter.reset()
    with TestClient(main.app) as test_client:
        yield test_client
    main.limiter.reset()


@pytest.fixture()
def mock_resend_send(monkeypatch):
    """Enable the Resend code path but replace Emails.send with a mock (no real API calls)."""
    monkeypatch.setattr(main, "RESEND_API_KEY", "test-api-key")
    mock_send = MagicMock(return_value={"id": "email_test_123"})
    monkeypatch.setattr(main.resend.Emails, "send", mock_send)
    return mock_send


class TestIndex:
    def test_index_returns_200_and_html(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Luminary Studio" in response.text
        assert "<form" in response.text


class TestHealth:
    def test_health_returns_ok(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestSecurityHeaders:
    def test_security_headers_present(self, client):
        response = client.get("/")

        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "SAMEORIGIN"
        assert "content-security-policy" in response.headers
        assert "strict-transport-security" in response.headers


class TestRobotsAndSitemap:
    def test_robots_returns_basic_rules(self, client):
        response = client.get("/robots.txt")

        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        assert "User-agent: *" in response.text
        assert "Allow: /" in response.text

    def test_robots_includes_sitemap_when_site_url_set(self, client, monkeypatch):
        monkeypatch.setattr(main, "SITE_URL", "https://example.com")

        response = client.get("/robots.txt")

        assert "Sitemap: https://example.com/sitemap.xml" in response.text

    def test_sitemap_returns_xml(self, client):
        response = client.get("/sitemap.xml")

        assert response.status_code == 200
        assert "application/xml" in response.headers["content-type"]
        assert "<urlset" in response.text
        assert "<loc>" in response.text


class TestLegalPages:
    def test_privacy_returns_200_and_html(self, client):
        response = client.get("/privacy")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Privacy Policy" in response.text

    def test_terms_returns_200_and_html(self, client):
        response = client.get("/terms")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Terms of Service" in response.text


class TestNotFound:
    def test_unknown_route_returns_404_page(self, client):
        response = client.get("/this-page-does-not-exist")

        assert response.status_code == 404
        assert "text/html" in response.headers["content-type"]
        assert "404" in response.text


class TestContactSuccess:
    def test_valid_submission_sends_email_via_mocked_resend(self, client, mock_resend_send):
        response = client.post("/api/contact", json=VALID_PAYLOAD)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "Jane Doe" in body["message"]

        mock_resend_send.assert_called_once()
        sent_params = mock_resend_send.call_args[0][0]
        assert sent_params["reply_to"] == VALID_PAYLOAD["email"]
        assert "Jane Doe" in sent_params["subject"]
        assert VALID_PAYLOAD["message"] in sent_params["html"]

    def test_valid_submission_without_resend_configured(self, client, monkeypatch):
        monkeypatch.setattr(main, "RESEND_API_KEY", "")
        mock_send = MagicMock()
        monkeypatch.setattr(main.resend.Emails, "send", mock_send)

        response = client.post("/api/contact", json=VALID_PAYLOAD)

        assert response.status_code == 200
        assert response.json()["success"] is True
        mock_send.assert_not_called()

    def test_resend_failure_returns_502(self, client, mock_resend_send):
        mock_resend_send.side_effect = main.resend.exceptions.ValidationError(
            message="You can only send testing emails to your own email address.",
            error_type="validation_error",
            code=403,
        )

        response = client.post("/api/contact", json=VALID_PAYLOAD)

        assert response.status_code == 502
        assert response.json()["success"] is False


class TestContactValidation:
    def test_invalid_email_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "email": "not-an-email"}

        response = client.post("/api/contact", json=payload)

        assert response.status_code == 422

    def test_empty_fields_return_422(self, client):
        payload = {"name": "", "email": "", "subject": "", "message": ""}

        response = client.post("/api/contact", json=payload)

        assert response.status_code == 422

    def test_message_too_short_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "message": "short"}

        response = client.post("/api/contact", json=payload)

        assert response.status_code == 422


class TestRateLimiting:
    def test_sixth_request_within_a_minute_is_rate_limited(self, client, monkeypatch):
        monkeypatch.setattr(main, "RESEND_API_KEY", "")
        monkeypatch.setattr(main.resend.Emails, "send", MagicMock())

        for _ in range(5):
            response = client.post("/api/contact", json=VALID_PAYLOAD)
            assert response.status_code == 200

        response = client.post("/api/contact", json=VALID_PAYLOAD)

        assert response.status_code == 429
        assert "error" in response.json()
