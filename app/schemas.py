"""
schemas.py — Pydantic models for request and response validation.

All data entering or leaving the /ask endpoint is validated here.
This keeps FastAPI route handlers clean and ensures type safety.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


# ─────────────────────────────────────────────────────────────
#  Request Models
# ─────────────────────────────────────────────────────────────

class QuestionRequest(BaseModel):
    """
    Request body for POST /ask.
    The 'question' field must be a non-empty string of at least 10 characters.
    """

    question: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="The legal question to be answered by the multi-agent team.",
        examples=["Can a landlord deduct cleaning fees from a security deposit?"],
    )

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        """Strip whitespace and reject blank or trivially short questions."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Question must not be empty or whitespace only.")
        if len(stripped) < 10:
            raise ValueError("Question is too short. Please provide at least 10 characters.")
        return stripped


# ─────────────────────────────────────────────────────────────
#  Response Models
# ─────────────────────────────────────────────────────────────

class LegalResponse(BaseModel):
    """
    Successful response from POST /ask.
    Contains the agent's answer, consulted sources, and a mandatory disclaimer.
    """

    status: str = Field(default="success", description="Response status: 'success' or 'error'.")
    question: str = Field(..., description="The original question that was asked.")
    answer: str = Field(..., description="Structured legal guidance from the multi-agent team.")
    sources: List[str] = Field(
        default_factory=list,
        description="Legal documents and statutes consulted during research.",
    )
    disclaimer: str = Field(
        default=(
            "⚖️ Disclaimer: LegalBot provides educational and informational guidance only. "
            "It does not constitute legal advice, legal representation, or an attorney-client "
            "relationship. Always consult a qualified, licensed attorney for legal counsel."
        ),
        description="Mandatory legal disclaimer.",
    )


class ErrorResponse(BaseModel):
    """
    Error response returned when something goes wrong.
    Used for 422 validation errors and 503 service unavailable.
    """

    status: str = Field(default="error")
    detail: str = Field(..., description="Human-readable error message.")
    question: Optional[str] = Field(default=None, description="The question that caused the error.")


class HealthResponse(BaseModel):
    """
    Response from GET /health.
    Confirms which agents are registered and whether Groq is configured.
    """

    status: str = Field(default="healthy")
    app_name: str = Field(..., description="Application name.")
    groq_configured: bool = Field(..., description="True if GROQ_API_KEY is set.")
    model: str = Field(..., description="The Groq model being used.")
    agents: List[str] = Field(
        ...,
        description="Names of the three registered legal agents.",
    )
