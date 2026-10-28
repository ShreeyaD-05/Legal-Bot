"""
main.py — FastAPI application entry point for LegalBot.

Exposes three endpoints:
  GET  /         → serves the single-page HTML UI
  GET  /health   → returns system health & agent registration status
  POST /ask      → submits a question to the multi-agent legal team

Static files (HTML / CSS / JS) are served from app/static/.
"""

import asyncio
import logging
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import QuestionRequest, LegalResponse, ErrorResponse, HealthResponse
from app.agents.legal_team import build_legal_team, get_agent_names
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
)

# ── Logging — no sensitive data ───────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("legalbot")

# ─────────────────────────────────────────────────────────────
#  App initialisation
# ─────────────────────────────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "LegalBot is an educational multi-agent legal guidance assistant "
        "powered by FastAPI, Agno, and the Groq LLaMA 3.3 model."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow requests from any origin (useful for dev / Docker networking)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static folder so CSS / JS are accessible at /static/...
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ─────────────────────────────────────────────────────────────
#  Utility: extract source titles from agent output
# ─────────────────────────────────────────────────────────────

def _extract_sources(answer_text: str) -> list[str]:
    """
    Parse the '### 📚 Sources Consulted' section from the reviewer's output
    and return a deduplicated list of source title strings.
    """
    sources: list[str] = []
    in_sources_section = False

    for line in answer_text.splitlines():
        stripped = line.strip()

        # Detect the sources section header
        if "Sources Consulted" in stripped:
            in_sources_section = True
            continue

        # Stop at the next header
        if in_sources_section and stripped.startswith("#"):
            break

        # Collect non-empty bullet lines
        if in_sources_section and stripped:
            # Remove markdown list markers (-, *, •, numbers)
            clean = re.sub(r"^[-*•\d.)\s]+", "", stripped).strip()
            if clean and clean not in sources:
                sources.append(clean)

    return sources


# ─────────────────────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    """
    GET /
    Serves the single-page web application (index.html).
    """
    index_path = STATIC_DIR / "index.html"
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"), status_code=200)


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health Check",
    tags=["System"],
)
async def health_check():
    """
    GET /health
    Returns the application health status, configured model, and registered agents.
    Does NOT expose the raw API key — only whether it is configured.
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        groq_configured=settings.groq_configured,
        model=settings.groq_model,
        agents=get_agent_names(),
    )


@app.post(
    "/ask",
    response_model=LegalResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error — question too short or empty."},
        503: {"model": ErrorResponse, "description": "Groq API key not configured."},
        504: {"model": ErrorResponse, "description": "Agent pipeline timed out."},
        500: {"model": ErrorResponse, "description": "Agent processing error."},
    },
    summary="Ask a Legal Question",
    tags=["Legal"],
)
async def ask_question(request: QuestionRequest):
    """
    POST /ask
    Submits a legal question to the three-agent pipeline:
      1. Legal Query Analyzer
      2. Legal Research Agent (uses search_legal_library tool)
      3. Legal Answer Reviewer

    The agent team runs inside a worker thread so the async event loop
    is never blocked. A configurable timeout protects against stalled requests.
    Returns structured legal guidance with sources and a disclaimer.
    """
    # ── Guard: Groq must be configured ───────────────────────
    if not settings.groq_configured:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "GROQ_API_KEY is not configured. "
                "Please add it to your .env file and restart the server."
            ),
        )

    logger.info("Processing legal inquiry (%d chars)…", len(request.question))

    # ── Run synchronous Agno team in a thread ─────────────────
    def _run_team() -> tuple[str, list[str]]:
        """Execute the agent team and return (answer_text, sources)."""
        clear_consulted_sources()
        team     = build_legal_team()
        response = team.run(request.question)

        # Robust answer extraction (same 4-way fallback as Streamlit)
        answer_text = ""
        if hasattr(response, "get_content_as_string"):
            try:
                answer_text = response.get_content_as_string().strip()
            except Exception:
                pass
        if not answer_text and getattr(response, "content", None):
            answer_text = str(response.content).strip()
        if not answer_text and getattr(response, "member_responses", None):
            for mr in reversed(response.member_responses):
                c = getattr(mr, "content", None)
                if c:
                    answer_text = str(c).strip()
                    break
        if not answer_text and getattr(response, "messages", None):
            for msg_obj in reversed(response.messages):
                if getattr(msg_obj, "role", "") == "assistant" and getattr(msg_obj, "content", None):
                    answer_text = str(msg_obj.content).strip()
                    break

        if not answer_text:
            answer_text = "The legal team was unable to produce a response. Please try again."

        # Prefer structured source tracking; fall back to text parsing
        sources = get_last_consulted_sources()
        if not sources:
            sources = _extract_sources(answer_text)

        return answer_text, sources

    try:
        answer_text, sources = await asyncio.wait_for(
            asyncio.to_thread(_run_team),
            timeout=settings.request_timeout,
        )

    except asyncio.TimeoutError:
        logger.error("Agent pipeline timed out after %ds.", settings.request_timeout)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=(
                f"Analysis timed out after {settings.request_timeout} seconds. "
                "Please try a shorter or simpler question."
            ),
        )

    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))

    except Exception as exc:
        # Prevent raw API key from appearing in error responses
        error_msg = str(exc)
        if settings.groq_api_key and settings.groq_api_key in error_msg:
            error_msg = error_msg.replace(settings.groq_api_key, "[REDACTED]")
        logger.exception("Agent error: %s", error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing error: {error_msg}",
        )

    return LegalResponse(
        status="success",
        question=request.question,
        answer=answer_text,
        sources=sources,
    )


# ─────────────────────────────────────────────────────────────
#  Dev-server entry point (mirrors zip's __main__ block)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
