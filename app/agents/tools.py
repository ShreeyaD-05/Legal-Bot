"""
tools.py — Legal library search tool used by the Legal Research Agent.

The search_legal_library function is registered as an Agno tool.
It searches the sample_documents knowledge base using keyword matching
and returns grounded legal content + source titles for citations.

Source tracking (added from zip comparison):
  - _last_consulted_sources  : set of document titles touched in this request
  - get_last_consulted_sources() : retrieve after run_legal_workflow()
  - clear_consulted_sources()    : reset before each new request
"""

from typing import List, Set
from app.data.sample_documents import (
    LEGAL_DOCUMENTS,
    KEYWORD_INDEX,
    DOCUMENT_BY_ID,
)

# ── Source tracking (query-level) ────────────────────────────
# Stores titles of every document consulted during the current request.
# Call clear_consulted_sources() before each new request,
# and get_last_consulted_sources() after to retrieve citations.
_last_consulted_sources: Set[str] = set()


def get_last_consulted_sources() -> List[str]:
    """Return a sorted list of document titles consulted in the last search session."""
    return sorted(list(_last_consulted_sources))


def clear_consulted_sources() -> None:
    """Reset the consulted-sources tracker before starting a new request."""
    _last_consulted_sources.clear()


def search_legal_library(query: str) -> str:
    """
    Search the legal document library for content relevant to the query.

    Scoring (matches zip's tiered approach):
      title match   → +4 per token
      keyword match → +3 per token
      domain match  → +2 per token
      content match → +1 per token

    Also records every consulted document title in _last_consulted_sources
    so the FastAPI layer can return them as structured citations.

    Args:
        query: A legal search query string (e.g., "security deposit deduction rules").

    Returns:
        A formatted string containing all relevant legal content and source titles.
        If nothing is found, returns a graceful fallback message.
    """
    if not query or not query.strip():
        return "No query provided. Please supply a legal search term."

    # Tokenise — strip punctuation, skip tiny words
    query_words = [
        w.lower().strip("?,.;:\"'()")
        for w in query.split()
        if len(w) > 2
    ]

    # ── Tiered scoring ────────────────────────────────────────
    scores: dict = {}
    for doc in LEGAL_DOCUMENTS:
        score = 0
        doc_keywords  = [k.lower() for k in doc.get("keywords", [])]
        title_lower   = doc.get("title",   "").lower()
        domain_lower  = doc.get("domain",  "").lower()
        content_lower = doc.get("content", "").lower()

        for token in query_words:
            if token in title_lower:
                score += 4
            if token in doc_keywords:
                score += 3
            if token in domain_lower:
                score += 2
            if token in content_lower:
                score += 1

        if score > 0:
            scores[doc["id"]] = score

    # ── Fallback: substring match if nothing scored ───────────
    if not scores:
        for doc in LEGAL_DOCUMENTS:
            for kw in doc["keywords"]:
                for word in query_words:
                    if word in kw or kw in word:
                        scores[doc["id"]] = scores.get(doc["id"], 0) + 1
                        break

    # ── Rank, limit to top 3, format ─────────────────────────
    ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:3]

    if not ranked_ids:
        available = ", ".join(f"'{d['title']}'" for d in LEGAL_DOCUMENTS)
        return (
            "No specific statutes found for this query in the legal library. "
            f"Available documents: {available}. "
            "Base the response on general legal principles and note that "
            "jurisdiction-specific statutes should be verified."
        )

    results = []
    for doc_id in ranked_ids:
        doc = DOCUMENT_BY_ID[doc_id]
        # Record for citation tracking
        _last_consulted_sources.add(doc["title"])
        results.append(
            f"📄 SOURCE: {doc['title']}\n"
            f"🏛️  DOMAIN: {doc['domain']}\n"
            f"{'─' * 60}\n"
            f"{doc['content']}\n"
        )

    return "\n\n".join(results)
