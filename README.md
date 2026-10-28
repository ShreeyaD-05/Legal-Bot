# ⚖️ LegalBot — Multi-Agent Legal Assistant

**Course:** Generative and Agentic AI Lab (UAMPC0731)  
**Assignment:** No. 10 — Containerization | A.Y. 2026-2027  
**Department:** Computer Science & Engineering, KIT's College of Engineering (Autonomous), Kolhapur

---

## 🏛️ What is LegalBot?

LegalBot is an educational multi-agent legal guidance assistant. It uses:
- **FastAPI** — backend REST API
- **Agno Framework** — multi-agent team coordination
- **Groq API** — fast LLaMA 3.3 model inference
- **Streamlit** — clean modern frontend UI

It answers legal questions by running three AI agents in a pipeline.

---

## 🤖 Multi-Agent Architecture

```
User Query
    │
    ▼
┌─────────────────────────────┐
│       Agno Legal Team       │
│                             │
│  1. Legal Query Analyzer    │  ← Classifies domain, extracts facts
│         │                   │
│         ▼                   │
│  2. Legal Research Agent    │  ← Searches legal library tool
│         │                   │
│         ▼                   │
│  3. Legal Answer Reviewer   │  ← Audits, formats, adds disclaimer
└─────────────────────────────┘
    │
    ▼
Final Verified Legal Guidance
```

---

## 📁 Project Structure

```
LegalBot/
├── .env.example          # Environment config template
├── .env                  # Your actual secrets (git-ignored)
├── .gitignore
├── requirements.txt
├── README.md
├── streamlit_app.py      # Streamlit UI (recommended)
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Multi-container orchestration
├── app/
│   ├── __init__.py
│   ├── config.py         # Settings & env loading
│   ├── main.py           # FastAPI app (/, /ask, /health)
│   ├── schemas.py        # Pydantic request/response models
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── legal_team.py # Agno Team with 3 agents
│   │   └── tools.py      # search_legal_library tool
│   ├── data/
│   │   ├── __init__.py
│   │   └── sample_documents.py  # Legal knowledge base
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
└── tests/
    ├── __init__.py
    ├── test_health.py
    ├── test_validation.py
    └── test_agents.py
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```powershell
# Copy the template
Copy-Item .env.example .env

# Edit .env and add your Groq API key from https://console.groq.com/keys
```

### 3. Run — Option A: Streamlit (Recommended)

```powershell
streamlit run streamlit_app.py
```
Open: **http://localhost:8501**

### 4. Run — Option B: FastAPI

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- App: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

---

## 🧪 Running Tests

```powershell
pytest -v
```

---

## 🐳 Docker

### Build & Run with Docker Compose

```bash
docker compose up --build
```

- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8000

### Build Image Only

```bash
docker build -t legalbot:latest .
```

---

## 🔌 API Reference

### `GET /health`
```json
{
  "status": "healthy",
  "app_name": "LegalBot — Multi-Agent Legal Assistant",
  "groq_configured": true,
  "model": "openai/gpt-oss-120b",
  "agents": ["Legal Query Analyzer", "Legal Research Agent", "Legal Answer Reviewer"]
}
```

### `POST /ask`
**Request:**
```json
{ "question": "Can a landlord deduct cleaning fees from a security deposit?" }
```
**Response:**
```json
{
  "status": "success",
  "question": "...",
  "answer": "### Legal Classification...",
  "sources": ["Residential Lease & Security Deposits"],
  "disclaimer": "LegalBot provides educational guidance only..."
}
```

---

## ⚖️ Legal Disclaimer

*LegalBot is built exclusively for educational purposes. It does not constitute legal advice or an attorney-client relationship. Always consult a qualified attorney for legal counsel.*
