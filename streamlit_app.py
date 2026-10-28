"""
streamlit_app.py — Streamlit frontend for LegalBot.

Run with:
    streamlit run streamlit_app.py
"""

import re
import streamlit as st

# ── Page config — must be first Streamlit call ────────────────
st.set_page_config(
    page_title="Legal Bot ⚖️",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ───────────────────────────────────────────────────
from app.config import get_settings
from app.agents.legal_team import build_legal_team, run_legal_workflow

# ── Settings (cache-cleared so .env is always fresh on restart)
get_settings.cache_clear()
settings = get_settings()

# ─────────────────────────────────────────────────────────────
#  CSS — unified light theme
#  config.toml already sets base="light" so Streamlit native
#  widgets (buttons, inputs, captions) all render with dark text
#  on light backgrounds automatically.
#  This block only styles the CUSTOM HTML components and the
#  sidebar — no background overrides on the main container.
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Sidebar: navy background, white text ──────────────────── */
[data-testid="stSidebar"] {
    background-color: #1e3a5f !important;
}
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] a {
    color: #f8fafc !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.25) !important;
}
/* Sidebar expander header */
[data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"] {
    color: #f8fafc !important;
}
/* Sidebar st.success / st.error banners readable on navy */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: #f8fafc !important;
}

/* ── Pipeline step cards (sidebar) ─────────────────────────── */
.pipeline-step {
    background: rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.4rem;
    font-size: 0.86rem;
    border-left: 3px solid #c9a84c;
    color: #f8fafc;
}
.pipeline-step span {
    color: rgba(248,250,252,0.78) !important;
}

/* ── Main area: explicit light colours ─────────────────────── */
/* Question quote block */
.question-quote {
    background: #f1f5f9;
    border-left: 4px solid #c9a84c;
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    font-style: italic;
    color: #334155;
    font-size: 0.92rem;
    margin-bottom: 0.75rem;
}

/* Source / evidence pill */
.source-pill {
    display: inline-block;
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #c9a84c;
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.82rem;
    color: #78350f;
    margin: 0.2rem 0.15rem 0.2rem 0;
}

/* Disclaimer box */
.disclaimer-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 0.82rem;
    color: #78350f;
    margin-top: 1rem;
    line-height: 1.6;
}

/* Footer */
.footer-note {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚖️ LegalBot")
    st.markdown("**Multi-Agent Legal Assistant**")
    st.markdown("---")

    st.markdown("### 🖥️ System Status")
    if settings.groq_configured:
        st.success("✅ Groq API Ready")
    else:
        st.error("❌ GROQ_API_KEY missing")
    model_display = settings.groq_model.split("/")[-1]
    st.markdown(
        f'<p style="font-size:0.9rem;margin:0">🤖 <strong>Model:</strong> '
        f'<span style="color:#c9a84c;font-family:monospace">{model_display}</span></p>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🤖 Agent Pipeline")
    for icon, name, desc in [
        ("🔍", "Legal Query Analyzer",  "Classifies domain & extracts key issues"),
        ("📚", "Legal Research Agent",  "Searches legal library for statutes"),
        ("✅", "Legal Answer Reviewer", "Audits claims & formats final answer"),
    ]:
        st.markdown(
            f'<div class="pipeline-step"><strong>{icon} {name}</strong><br/>'
            f'<span style="opacity:0.75;font-size:0.79rem">{desc}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📋 Legal Domains")
    for d in ["🏠 Tenancy & Leases", "📝 Contract Law & NDAs",
              "💡 Intellectual Property", "👔 Employment Law", "🛒 Consumer Protection"]:
        st.markdown(f"- {d}")

    st.markdown("---")
    # ── Grounding library expander (from zip) ─────────────────
    from app.data.sample_documents import LEGAL_DOCUMENTS
    with st.expander("📚 Grounding Legal Library", expanded=False):
        for doc in LEGAL_DOCUMENTS:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"Domain: {doc['domain']}")
            # Show first 120 chars of content as a preview
            preview = doc["content"][:120].replace("\n", " ").strip()
            st.caption(f"{preview}…")
            st.markdown("---")


# ─────────────────────────────────────────────────────────────
#  Main Page
# ─────────────────────────────────────────────────────────────
st.markdown("# ⚖️ LegalBot")
st.markdown(
    "**Multi-Agent Legal Guidance** — powered by "
    "[Agno Framework](https://github.com/agno-agi/agno) · Groq · FastAPI"
)
st.divider()

# Guard: API key required
if not settings.groq_configured:
    st.error(
        "⛔ **GROQ_API_KEY is not configured.**\n\n"
        "Add it to your `.env` file:\n```\nGROQ_API_KEY=gsk_your_key_here\n```\n"
        "Then restart the app."
    )
    st.stop()

# ── Example questions ─────────────────────────────────────────
st.markdown("#### 💡 Try an example")

EXAMPLES = [
    ("🏠 Security Deposit",
     "Can a landlord deduct cleaning fees from a security deposit without providing an itemized statement?"),
    ("👔 Wrongful Termination",
     "What rights do I have if my employer fires me without any valid reason?"),
    ("💡 Copyright Fair Use",
     "Can I use someone else's copyrighted image on my website for educational purposes?"),
    ("📝 NDA Clauses",
     "What key clauses should I include in a Non-Disclosure Agreement with a business partner?"),
    ("🛒 Defective Product",
     "What can I do if a company sold me a defective product and refuses to issue a refund?"),
]

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""
if "response_data" not in st.session_state:
    st.session_state.response_data = None   # persists answer across reruns
if "attached_doc_name" not in st.session_state:
    st.session_state.attached_doc_name = None

cols = st.columns(len(EXAMPLES))
for col, (label, q) in zip(cols, EXAMPLES):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.selected_question = q

st.divider()

# ── Question input ────────────────────────────────────────────
st.markdown("#### ❓ Your Legal Question")

question = st.text_area(
    label="question",
    value=st.session_state.selected_question,
    height=120,
    max_chars=2000,
    placeholder=(
        "Describe your legal situation…\n\n"
        "e.g. My landlord is withholding my security deposit for cleaning costs "
        "but the apartment was clean when I left. What can I do?"
    ),
    label_visibility="collapsed",
)
st.caption(f"{len(question)} / 2000 characters")

# ── Document / photo upload (from zip) ────────────────────────
uploaded_image = st.file_uploader(
    "📷 Upload Document / Agreement Photo (Optional):",
    type=["png", "jpg", "jpeg", "webp"],
    help=(
        "Attach a photo or scan of a rent agreement, NDA, termination letter, "
        "legal notice, invoice, or receipt. The agent will acknowledge the "
        "attachment and analyse any question you pair with it."
    ),
)
if uploaded_image:
    st.caption(f"📎 Attached: `{uploaded_image.name}` ({uploaded_image.size // 1024} KB)")

if question.strip() and len(question.strip()) < 10:
    st.warning("⚠️ Please enter at least 10 characters.")

ask_clicked = st.button(
    "⚖️ Ask LegalBot",
    type="primary",
    disabled=len(question.strip()) < 10,
    use_container_width=True,
)

# Clear button — resets question and cached answer
if st.button("🗑️ Clear", use_container_width=True):
    st.session_state.selected_question = ""
    st.session_state.response_data = None
    st.session_state.attached_doc_name = None
    st.rerun()


# ─────────────────────────────────────────────────────────────
#  Run agents
# ─────────────────────────────────────────────────────────────
if ask_clicked and len(question.strip()) >= 10:

    st.divider()
    st.markdown("### 🔄 Agent Pipeline Running…")

    progress = st.progress(0, text="Starting…")
    status   = st.empty()

    STEPS = [
        (0.15, "🔍 **Legal Query Analyzer** — classifying domain…"),
        (0.50, "📚 **Legal Research Agent** — searching legal library…"),
        (0.85, "✅ **Legal Answer Reviewer** — formatting final answer…"),
        (1.00, "✅ Done"),
    ]

    # Show steps 1-2 before the blocking call
    for pct, msg in STEPS[:2]:
        progress.progress(pct, text=msg)
        status.info(msg)

    answer_text = ""
    sources     = []
    error_msg   = ""

    # Collect image data if uploaded
    img_bytes = uploaded_image.getvalue() if uploaded_image else None
    img_name  = uploaded_image.name       if uploaded_image else None
    img_mime  = uploaded_image.type       if uploaded_image else None

    if img_bytes:
        st.session_state.attached_doc_name = img_name
        st.info(f"📎 Analysing with attached document: `{img_name}`")
    else:
        st.session_state.attached_doc_name = None

    try:
        with st.spinner("Multi-agent team researching statutes and reviewing memo…"):
            result = run_legal_workflow(
                question.strip(),
                image_bytes=img_bytes,
                image_filename=img_name,
                image_mime_type=img_mime,
            )
            answer_text = result.get("answer", "")
            sources     = result.get("sources", [])

        if not answer_text:
            answer_text = "⚠️ The agents did not produce a response. Please try again."

        # Also parse sources from the answer text as fallback
        if not sources:
            in_src = False
            for line in answer_text.splitlines():
                s = line.strip()
                if "Sources Consulted" in s:
                    in_src = True
                    continue
                if in_src and s.startswith("#"):
                    break
                if in_src and s:
                    clean = re.sub(r"^[-*•\d.)\s]+", "", s).strip()
                    clean = re.sub(r"\*+|_+", "", clean).strip()
                    if clean and not clean.lower().startswith("note:") and clean not in sources:
                        sources.append(clean)

    except RuntimeError as exc:
        error_msg = str(exc)
    except Exception as exc:
        error_msg = f"Agent error: {str(exc)}"

    # Persist result in session state so it survives Streamlit reruns
    if not error_msg:
        st.session_state.response_data = {
            "answer": answer_text,
            "sources": sources,
            "question": question.strip(),
            "doc_name": st.session_state.attached_doc_name,
        }
    else:
        st.session_state.response_data = None

    # Finish progress bar
    for pct, msg in STEPS[2:]:
        progress.progress(pct, text=msg)
        status.info(msg)
    progress.empty()
    status.empty()

    # ─────────────────────────────────────────────────────────
    #  Display result
    # ─────────────────────────────────────────────────────────
    if error_msg:
        st.error(f"❌ **Error:** {error_msg}")
        st.info("Please wait a moment and try again — this may be a temporary rate limit.")

# ── Display persisted response (survives Streamlit reruns) ────
if st.session_state.response_data and not (ask_clicked and error_msg):
    resp        = st.session_state.response_data
    answer_text = resp["answer"]
    sources     = resp["sources"]
    q_display   = resp.get("question", question.strip())
    doc_name    = resp.get("doc_name")

    if ask_clicked:
        st.divider()

    st.markdown("### ⚖️ Legal Guidance")

    # Show the question
    st.markdown(
        f'<div class="question-quote">❓ {q_display}</div>',
        unsafe_allow_html=True,
    )

    # Evidence badge — shown when a document was uploaded (from zip)
    if doc_name:
        st.markdown(
            f'<div class="source-pill">📎 <strong>Analysed Evidence:</strong> {doc_name}</div>',
            unsafe_allow_html=True,
        )

    # Render markdown answer in a bordered container
    with st.container(border=True):
        st.markdown(answer_text)

    # Sources
    if sources:
        st.markdown("#### 📚 Sources Consulted")
        for src in sources:
            st.markdown(
                f'<div class="source-pill">📄 {src}</div>',
                unsafe_allow_html=True,
            )

    st.divider()

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Answer",
            data=answer_text,
            file_name="legalbot_answer.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        if st.button("🔄 Ask Another Question", use_container_width=True):
            st.session_state.selected_question = ""
            st.session_state.response_data = None
            st.rerun()

    # Disclaimer
    st.markdown(
        '<div class="disclaimer-box">'
        "⚖️ <strong>Disclaimer:</strong> LegalBot provides educational and informational "
        "guidance only. It does not constitute legal advice, legal representation, or an "
        "attorney-client relationship. Always consult a qualified, licensed attorney."
        "</div>",
        unsafe_allow_html=True,
    )


# ── Footer ─────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p class='footer-note'>"
    "⚖️ LegalBot — for educational purposes only. "
    "Not a substitute for professional legal advice."
    "</p>",
    unsafe_allow_html=True,
)
