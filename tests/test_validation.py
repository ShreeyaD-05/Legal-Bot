"""
test_validation.py — Tests for input validation and error handling on POST /ask.

Verifies:
  - Empty string is rejected with 422
  - Whitespace-only string is rejected with 422
  - Questions shorter than 10 characters are rejected with 422
  - Questions exactly 10 characters long are accepted
  - Missing 'question' field returns 422
  - Overly long questions (> 2000 chars) are rejected with 422
  - When Groq is not configured, a 503 is returned
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ── Mock the team so tests that send valid questions don't hit Groq ──
def _mock_team():
    """Return a mock team whose run() returns a canned response instantly."""
    mock = MagicMock()
    mock_resp = MagicMock()
    # Must be a real string, not a MagicMock, so Pydantic validation passes
    mock_resp.content = "### ⚖️ Legal Classification\nMocked answer for testing."
    mock_resp.get_content_as_string.return_value = "### ⚖️ Legal Classification\nMocked answer for testing."
    mock_resp.member_responses = []
    mock_resp.messages = []
    mock.run.return_value = mock_resp
    return mock


class TestInputValidation:
    """Tests for QuestionRequest Pydantic validation."""

    def test_empty_string_rejected(self):
        """An empty question string must return 422 Unprocessable Entity."""
        response = client.post("/ask", json={"question": ""})
        assert response.status_code == 422

    def test_whitespace_only_rejected(self):
        """A whitespace-only question must return 422."""
        response = client.post("/ask", json={"question": "     "})
        assert response.status_code == 422

    def test_too_short_rejected(self):
        """A question under 10 characters must return 422."""
        response = client.post("/ask", json={"question": "Help me"})
        assert response.status_code == 422

    def test_exactly_10_chars_accepted_structure(self):
        """
        A question of exactly 10 characters must pass validation.
        The team is mocked so no real Groq API call is made.
        """
        with patch("app.main.build_legal_team", return_value=_mock_team()):
            response = client.post("/ask", json={"question": "1234567890"})
        assert response.status_code != 422

    def test_missing_question_field_rejected(self):
        """A request body with no 'question' field must return 422."""
        response = client.post("/ask", json={})
        assert response.status_code == 422

    def test_null_question_rejected(self):
        """A null question must return 422."""
        response = client.post("/ask", json={"question": None})
        assert response.status_code == 422

    def test_too_long_rejected(self):
        """A question exceeding 2000 characters must return 422."""
        long_question = "a" * 2001
        response = client.post("/ask", json={"question": long_question})
        assert response.status_code == 422

    def test_valid_max_length_accepted_structure(self):
        """A question of exactly 2000 characters must pass validation."""
        max_question = "What are my tenant rights regarding security deposit deductions? " * 30
        max_question = max_question[:2000]
        with patch("app.main.build_legal_team", return_value=_mock_team()):
            response = client.post("/ask", json={"question": max_question})
        assert response.status_code != 422

    def test_validation_error_returns_detail(self):
        """422 response must include a 'detail' field explaining the error."""
        response = client.post("/ask", json={"question": "short"})
        assert response.status_code == 422
        body = response.json()
        assert "detail" in body


class TestServiceUnavailable:
    """Tests for 503 when Groq API key is not configured."""

    def test_missing_groq_key_returns_503(self):
        """
        When groq_configured is False, POST /ask must return 503.
        We patch settings to simulate a missing key.
        """
        with patch("app.main.settings") as mock_settings:
            mock_settings.groq_configured = False
            mock_settings.groq_model      = "openai/gpt-oss-120b"
            mock_settings.app_name        = "LegalBot — Multi-Agent Legal Assistant"
            mock_settings.app_version     = "1.0.0"

            response = client.post(
                "/ask",
                json={"question": "Can a landlord evict me without notice?"},
            )
            assert response.status_code == 503

    def test_503_response_has_detail(self):
        """503 response must include a 'detail' message."""
        with patch("app.main.settings") as mock_settings:
            mock_settings.groq_configured = False
            mock_settings.groq_model      = "openai/gpt-oss-120b"
            mock_settings.app_name        = "LegalBot — Multi-Agent Legal Assistant"
            mock_settings.app_version     = "1.0.0"

            response = client.post(
                "/ask",
                json={"question": "Can a landlord evict me without notice?"},
            )
            body = response.json()
            assert "detail" in body
            assert len(body["detail"]) > 0
