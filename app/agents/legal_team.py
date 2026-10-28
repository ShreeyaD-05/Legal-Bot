"""
legal_team.py — Agno multi-agent team definition for LegalBot.

Architecture: three agents in coordinate mode.
  1. Legal Query Analyzer   — short classification handoff (~200 tokens out)
  2. Legal Research Agent   — calls search_legal_library, short research notes (~300 tokens out)
  3. Legal Answer Reviewer  — writes the final structured answer (~600 tokens out)

Token budget per request (free tier 8K TPM limit):
  - Team coordinator prompt : ~200 tokens
  - Agent 1 output          : ~200 tokens
  - Agent 2 output          : ~300 tokens
  - Agent 3 output          : ~600 tokens
  - Total                   : ~1300 output tokens  ← well within 8K TPM
"""

from agno.agent import Agent
from agno.team import Team
from agno.models.groq import Groq

from app.config import get_settings
from app.agents.tools import search_legal_library

# ─────────────────────────────────────────────────────────────
#  Agent names (exported so other modules can reference them)
# ─────────────────────────────────────────────────────────────

AGENT_NAMES = [
    "Legal Query Analyzer",
    "Legal Research Agent",
    "Legal Answer Reviewer",
]


def build_legal_team() -> Team:
    """
    Instantiate and return the Agno legal Team.

    Raises:
        RuntimeError: If GROQ_API_KEY is not configured.
    """
    settings = get_settings()

    if not settings.groq_configured:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Please set it in your .env file before running LegalBot."
        )

    def make_groq_model() -> Groq:
        return Groq(
            id=settings.groq_model,
            api_key=settings.groq_api_key,
        )

    # ─────────────────────────────────────────────────────────
    #  Agent 1 — Legal Query Analyzer
    #  Produces a SHORT classification (≤150 tokens).
    # ─────────────────────────────────────────────────────────
    query_analyzer = Agent(
        name="Legal Query Analyzer",
        role="Classify the legal domain and list 3 search keywords",
        model=make_groq_model(),
        instructions=[
            "You are a legal intake classifier. Be extremely brief.",
            "From the user's question output ONLY:",
            "DOMAIN: <one of: Tenancy Law | Contract Law | Employment Law | "
            "Intellectual Property | Consumer Protection | Other>",
            "PARTIES: <roles, e.g. landlord/tenant>",
            "KEYWORDS: <3 search terms separated by commas>",
            "Do not write anything else. No explanations.",
        ],
        markdown=False,
    )

    # ─────────────────────────────────────────────────────────
    #  Agent 2 — Legal Research Agent
    #  Calls the tool once, returns brief research notes (≤250 tokens).
    # ─────────────────────────────────────────────────────────
    research_agent = Agent(
        name="Legal Research Agent",
        role="Search the legal library and return key rules",
        model=make_groq_model(),
        tools=[search_legal_library],
        instructions=[
            "You are a legal researcher. Be concise.",
            "1. Call search_legal_library with the KEYWORDS from the previous step.",
            "2. From the results extract the 3 most important legal rules that answer the question.",
            "3. Output ONLY:",
            "RULES:",
            "- <rule 1 in one sentence>",
            "- <rule 2 in one sentence>",
            "- <rule 3 in one sentence>",
            "SOURCE: <document title>",
            "Nothing else. No extra paragraphs.",
        ],
        show_tool_calls=False,
        markdown=False,
    )

    # ─────────────────────────────────────────────────────────
    #  Agent 3 — Legal Answer Reviewer
    #  Writes the full user-facing answer using prior outputs.
    # ─────────────────────────────────────────────────────────
    answer_reviewer = Agent(
        name="Legal Answer Reviewer",
        role="Synthesize a clear, verified legal guidance answer",
        model=make_groq_model(),
        instructions=[
            "You are a senior legal editor. Use the domain, rules, and source from the prior agents "
            "to write a helpful, structured answer. Keep each section concise.",
            "",
            "Use EXACTLY this format:",
            "### ⚖️ Legal Classification",
            "One sentence stating the legal domain and the core issue.",
            "",
            "### 📋 Key Legal Rules",
            "- Rule 1",
            "- Rule 2",
            "- Rule 3",
            "",
            "### 💡 Guidance for Your Situation",
            "2-3 sentences of practical, grounded guidance directly answering the question.",
            "Use words like 'generally' and 'typically'.",
            "",
            "### 📚 Sources Consulted",
            "- <source title from research agent>",
            "",
            "### ⚠️ Important Note",
            "This is educational guidance only — not legal advice. Consult a qualified attorney.",
        ],
        markdown=True,
    )

    # ─────────────────────────────────────────────────────────
    #  Agno Team — coordinate mode
    # ─────────────────────────────────────────────────────────
    legal_team = Team(
        name="LegalBot Multi-Agent Team",
        mode="coordinate",
        model=make_groq_model(),
        members=[
            query_analyzer,
            research_agent,
            answer_reviewer,
        ],
        instructions=[
            "Run the three agents in order:",
            "1. Legal Query Analyzer: classify the question (very short output).",
            "2. Legal Research Agent: search library and extract 3 rules (very short output).",
            "3. Legal Answer Reviewer: write the final structured answer.",
            "Return ONLY the Legal Answer Reviewer's output.",
        ],
        markdown=True,
        show_tool_calls=False,
    )

    return legal_team


def get_agent_names() -> list:
    """Return the list of registered agent names."""
    return AGENT_NAMES.copy()


# ─────────────────────────────────────────────────────────────
#  Orchestrator — run_legal_workflow()
#  Mirrors the zip's run_legal_workflow() but Groq-only
#  (no Gemini Vision dependency).
#
#  image_bytes / image_filename / image_mime_type are accepted so
#  the Streamlit UI can pass an uploaded file; when provided, the
#  raw bytes are base64-encoded and injected as text context so
#  the Groq LLM can at least see the filename and a note that an
#  attachment was supplied.  Full OCR requires a vision-capable
#  model — when Groq adds vision support the block below can be
#  replaced with an actual vision call without touching anything else.
# ─────────────────────────────────────────────────────────────

from typing import Any, Dict, Optional  # noqa: E402  (keep imports local to avoid circular)


def run_legal_workflow(
    question: str,
    team: Optional[Team] = None,
    image_bytes: Optional[bytes] = None,
    image_filename: Optional[str] = None,
    image_mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute the multi-agent legal collaboration on a user question
    and an optional attached document image.

    Args:
        question:        The user's legal question text.
        team:            Pre-built Team instance (created fresh if None).
        image_bytes:     Raw bytes of an uploaded image / document scan.
        image_filename:  Original filename of the uploaded file.
        image_mime_type: MIME type of the uploaded file (e.g. 'image/jpeg').

    Returns:
        dict with keys:
          "answer"  — the final legal guidance text
          "sources" — list of document titles consulted
    """
    from app.agents.tools import clear_consulted_sources, get_last_consulted_sources, search_legal_library  # noqa

    clear_consulted_sources()

    # ── 1. Build evidence context from uploaded image ─────────
    evidence_context = ""
    if image_bytes and image_filename:
        # Groq does not yet expose a vision endpoint via the agno wrapper,
        # so we describe the attachment as text context so the LLM is aware.
        size_kb = len(image_bytes) // 1024
        evidence_context = (
            f"\n\n[ATTACHED DOCUMENT: {image_filename} ({size_kb} KB, {image_mime_type or 'image'})]"
            "\nNote: A document image was uploaded by the user. "
            "Please acknowledge the attachment in your analysis and note that "
            "full OCR extraction is not available in this Groq-only deployment. "
            "Ask the user to paste key text from the document if specific clause "
            "analysis is needed.\n"
            "[END OF ATTACHMENT NOTE]\n"
        )

    # ── 2. Pre-fetch grounding docs (same as zip's step 2) ────
    search_query = f"{question} {evidence_context[:200]}"
    statutory_docs = search_legal_library(search_query)
    sources = get_last_consulted_sources()

    # ── 3. Build the full prompt with grounding context ───────
    workflow_prompt = (
        f"You are LegalBot, a multi-agent legal advisory team consisting of:\n"
        f"1. Legal Query Analyzer: Classify the legal domain and extract material facts.\n"
        f"2. Legal Research Agent: Ground recommendations in the statutory library below.\n"
        f"3. Legal Answer Reviewer: Audit findings and author a clear, professional memorandum.\n\n"
        f"USER LEGAL INQUIRY:\n"
        f"\"\"\"{question}\"\"\"\n"
        f"{evidence_context}\n"
        f"GROUNDING STATUTORY LIBRARY (pre-fetched):\n"
        f"{statutory_docs}\n\n"
        f"Generate the verified Legal Memorandum using EXACTLY this format:\n"
        f"### ⚖️ Legal Classification\n"
        f"One sentence stating the legal domain and core issue.\n\n"
        f"### 📋 Key Legal Rules\n"
        f"- Rule 1 (cite statute/section)\n"
        f"- Rule 2\n"
        f"- Rule 3\n\n"
        f"### 💡 Guidance for Your Situation\n"
        f"2-3 sentences of practical guidance. Use 'generally' and 'typically'.\n\n"
        f"### 📚 Sources Consulted\n"
        f"- <source title from the library>\n\n"
        f"### ⚠️ Important Note\n"
        f"This is educational guidance only — not legal advice. Consult a qualified attorney."
    )

    # ── 4. Run the agent team ─────────────────────────────────
    content_text = ""
    try:
        active_team = team if team is not None else build_legal_team()
        run_output = active_team.run(workflow_prompt)

        # Robust extraction (same 4-way fallback as main.py)
        if hasattr(run_output, "get_content_as_string"):
            try:
                content_text = run_output.get_content_as_string().strip()
            except Exception:
                pass
        if not content_text and getattr(run_output, "content", None):
            content_text = str(run_output.content).strip()
        if not content_text and getattr(run_output, "member_responses", None):
            for mr in reversed(run_output.member_responses):
                c = getattr(mr, "content", None)
                if c:
                    content_text = str(c).strip()
                    break
        if not content_text and getattr(run_output, "messages", None):
            for msg_obj in reversed(run_output.messages):
                if getattr(msg_obj, "role", "") == "assistant" and getattr(msg_obj, "content", None):
                    content_text = str(msg_obj.content).strip()
                    break
        if not content_text:
            content_text = str(run_output)
    except Exception as exc:
        content_text = f"Unable to generate response: {exc}"

    # Merge any additional sources captured during the team run
    final_sources = get_last_consulted_sources()
    if not final_sources:
        final_sources = sources

    return {
        "answer": content_text,
        "sources": final_sources,
    }
