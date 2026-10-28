"""
test_health.py — Tests for GET / and GET /health endpoints.

Verifies:
  - The root endpoint returns HTML with status 200
  - The health endpoint returns valid JSON with all required fields
  - The agents list contains all three expected agent names
  - The health response structure matches the HealthResponse schema
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.agents.legal_team import AGENT_NAMES

# Create a synchronous test client for FastAPI
client = TestClient(app)


class TestRootEndpoint:
    """Tests for GET /"""

    def test_root_returns_200(self):
        """Root endpoint should return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_html(self):
        """Root endpoint should return an HTML page."""
        response = client.get("/")
        assert "text/html" in response.headers["content-type"]

    def test_root_contains_legalbot(self):
        """HTML page should mention LegalBot."""
        response = client.get("/")
        assert "LegalBot" in response.text


class TestHealthEndpoint:
    """Tests for GET /health"""

    def test_health_returns_200(self):
        """Health endpoint should return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Health endpoint should return valid JSON."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)

    def test_health_status_field(self):
        """Health response must include 'status' field set to 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_app_name(self):
        """Health response must include the app name."""
        response = client.get("/health")
        data = response.json()
        assert "app_name" in data
        assert "LegalBot" in data["app_name"]

    def test_health_groq_configured_field(self):
        """Health response must include 'groq_configured' boolean field."""
        response = client.get("/health")
        data = response.json()
        assert "groq_configured" in data
        assert isinstance(data["groq_configured"], bool)

    def test_health_model_field(self):
        """Health response must include a non-empty 'model' field."""
        response = client.get("/health")
        data = response.json()
        assert "model" in data
        assert len(data["model"]) > 0

    def test_health_agents_list(self):
        """Health response must include 'agents' as a list of three names."""
        response = client.get("/health")
        data = response.json()
        assert "agents" in data
        assert isinstance(data["agents"], list)
        assert len(data["agents"]) == 3

    def test_health_agents_names(self):
        """Health response agents must match the expected agent names."""
        response = client.get("/health")
        data = response.json()
        for expected_name in AGENT_NAMES:
            assert expected_name in data["agents"], (
                f"Expected agent '{expected_name}' not found in health response. "
                f"Got: {data['agents']}"
            )

    def test_health_no_api_key_leak(self):
        """Health response must never contain the raw GROQ API key."""
        response = client.get("/health")
        body = response.text
        # The key starts with 'gsk_' — ensure it's not in the response
        assert "gsk_" not in body, "API key leaked in health response!"
