# ═══════════════════════════════════════════════════════════════
#  LegalBot — Optimized Multi-Stage Dockerfile
#
#  Stage 1 (builder): installs all Python dependencies from
#                     pre-downloaded wheels (no internet needed
#                     inside Docker — avoids proxy/SSL issues).
#  Stage 2 (runtime): copies only the venv + app code — no build
#                     tools, no cache, minimal attack surface.
#
#  Build:   docker compose up --build
#  Run:     docker compose up -d
# ═══════════════════════════════════════════════════════════════


# ───────────────────────────────────────────────────────────────
#  Stage 1 — Builder
#  Install dependencies from local wheels into /opt/venv
#  so Stage 2 can copy the clean venv.
# ───────────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Create an isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy pre-downloaded wheels and requirements into the build context
# The wheels/ folder was created with:
#   pip download -r requirements.txt --dest wheels \
#       --platform manylinux2014_x86_64 --python-version 3.11 --only-binary=:all:
COPY wheels/         ./wheels/
COPY requirements.txt .

# Install from local wheels — no network access required
RUN pip install --upgrade pip --no-index --find-links ./wheels || \
    pip install --upgrade pip && \
    pip install --no-cache-dir --no-index --find-links ./wheels -r requirements.txt


# ───────────────────────────────────────────────────────────────
#  Stage 2 — Runtime
#  Lean image: only the venv + application code.
# ───────────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm AS runtime

# Metadata labels (OCI standard)
LABEL org.opencontainers.image.title="LegalBot"
LABEL org.opencontainers.image.description="Multi-Agent Legal Assistant — GenAI & ML DevOps Lab"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="KIT College of Engineering, Kolhapur"

# Runtime Python settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Point PATH at the venv copied from builder
    PATH="/opt/venv/bin:$PATH" \
    # Default env values (overridden by --env-file or docker-compose)
    HOST=0.0.0.0 \
    PORT=8000 \
    GROQ_MODEL=openai/gpt-oss-120b \
    REQUEST_TIMEOUT=60

# Create a non-root user for security
RUN addgroup --system appgroup && \
    adduser  --system --ingroup appgroup --no-create-home appuser

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
# .dockerignore excludes .env, __pycache__, .venv, etc.
COPY app/             ./app/
COPY streamlit_app.py .
COPY requirements.txt .
# Copy Streamlit theme config (dark mode, server settings)
COPY .streamlit/      ./.streamlit/

# Give ownership to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# ── Exposed ports ──────────────────────────────────────────────
# 8000 → FastAPI  (uvicorn)
# 8501 → Streamlit
EXPOSE 8000
EXPOSE 8501

# ── Healthcheck ────────────────────────────────────────────────
# Docker will poll GET /health every 30 s.
# 3 consecutive failures → container marked "unhealthy".
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c \
        "import urllib.request; \
         urllib.request.urlopen('http://localhost:8000/health')" \
    || exit 1

# ── Default command — FastAPI via uvicorn ──────────────────────
# Override in docker-compose for Streamlit (see compose file).
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info"]
