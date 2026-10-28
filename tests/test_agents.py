"""
test_agents.py — Tests for Agno agents, Team structure, and the search tool.

Verifies:
  - build_legal_team() returns an Agno Team object
  - The team has exactly 3 member agents
  - Each agent has the correct name and role
  - The Legal Research Agent has the search tool attached
  - search_legal_library returns relevant results for known queries
  - search_legal_library handles edge cases gracefully
  - get_agent_names() returns the correct list
"""

import pytest
from unittest.mock import patch, MagicMock

from app.agents.legal_team import build_legal_team, get_agent_names, AGENT_NAMES
from app.agents.tools import search_legal_library
from app.data.sample_documents import LEGAL_DOCUMENTS, KEYWORD_INDEX, DOCUMENT_BY_ID


# ─────────────────────────────────────────────────────────────
#  Agent Names
# ─────────────────────────────────────────────────────────────

class TestAgentNames:
    """Tests for agent name registration."""

    def test_get_agent_names_returns_list(self):
        """get_agent_names() must return a list."""
        names = get_agent_names()
        assert isinstance(names, list)

    def test_exactly_three_agents(self):
        """There must be exactly three agents."""
        names = get_agent_names()
        assert len(names) == 3

    def test_agent_name_analyzer(self):
        """'Legal Query Analyzer' must be registered."""
        assert "Legal Query Analyzer" in get_agent_names()

    def test_agent_name_researcher(self):
        """'Legal Research Agent' must be registered."""
        assert "Legal Research Agent" in get_agent_names()

    def test_agent_name_reviewer(self):
        """'Legal Answer Reviewer' must be registered."""
        assert "Legal Answer Reviewer" in get_agent_names()

    def test_agent_names_match_constant(self):
        """get_agent_names() must return the same values as AGENT_NAMES."""
        assert get_agent_names() == AGENT_NAMES


# ─────────────────────────────────────────────────────────────
#  Team Construction
# ─────────────────────────────────────────────────────────────

class TestLegalTeamConstruction:
    """Tests for Agno Team creation."""

    def test_build_legal_team_returns_team(self):
        """build_legal_team() must return an Agno Team object."""
        from agno.team import Team
        team = build_legal_team()
        assert isinstance(team, Team)

    def test_team_has_three_members(self):
        """The team must have exactly three member agents."""
        team = build_legal_team()
        assert len(team.members) == 3

    def test_team_member_names(self):
        """Each team member must have the expected name."""
        team = build_legal_team()
        member_names = [m.name for m in team.members]
        for expected in AGENT_NAMES:
            assert expected in member_names, (
                f"Agent '{expected}' not found in team. Got: {member_names}"
            )

    def test_research_agent_has_tool(self):
        """The Legal Research Agent must have the search tool attached."""
        team = build_legal_team()
        research_agent = next(
            (m for m in team.members if m.name == "Legal Research Agent"), None
        )
        assert research_agent is not None, "Legal Research Agent not found in team."
        # Agno stores tools in .tools list
        tool_names = []
        if hasattr(research_agent, "tools") and research_agent.tools:
            for tool in research_agent.tools:
                if callable(tool):
                    tool_names.append(tool.__name__)
                elif hasattr(tool, "name"):
                    tool_names.append(tool.name)
                elif hasattr(tool, "__name__"):
                    tool_names.append(tool.__name__)
        assert "search_legal_library" in tool_names, (
            f"search_legal_library tool not found. Got tools: {tool_names}"
        )

    def test_build_team_raises_without_api_key(self):
        """build_legal_team() must raise RuntimeError when GROQ_API_KEY is missing."""
        with patch("app.agents.legal_team.get_settings") as mock_settings_fn:
            mock_settings = MagicMock()
            mock_settings.groq_configured = False
            mock_settings.groq_api_key    = ""
            mock_settings.groq_model      = "openai/gpt-oss-120b"
            mock_settings_fn.return_value = mock_settings

            with pytest.raises(RuntimeError, match="GROQ_API_KEY"):
                build_legal_team()


# ─────────────────────────────────────────────────────────────
#  Search Tool
# ─────────────────────────────────────────────────────────────

class TestSearchLegalLibrary:
    """Tests for the search_legal_library tool."""

    def test_returns_string(self):
        """search_legal_library must always return a string."""
        result = search_legal_library("security deposit")
        assert isinstance(result, str)

    def test_security_deposit_query(self):
        """Searching 'security deposit' must return tenancy-related content."""
        result = search_legal_library("security deposit")
        assert len(result) > 0
        # Should contain the tenancy document
        assert "deposit" in result.lower() or "tenancy" in result.lower()

    def test_nda_query(self):
        """Searching 'nda confidentiality' must return NDA-related content."""
        result = search_legal_library("nda confidentiality")
        assert "confidential" in result.lower() or "nda" in result.lower()

    def test_employment_query(self):
        """Searching 'wrongful termination' must return employment law content."""
        result = search_legal_library("wrongful termination employment")
        assert "employment" in result.lower() or "termination" in result.lower()

    def test_copyright_query(self):
        """Searching 'copyright infringement' must return IP content."""
        result = search_legal_library("copyright infringement")
        assert "copyright" in result.lower() or "intellectual property" in result.lower()

    def test_consumer_protection_query(self):
        """Searching 'defective product refund' must return consumer protection content."""
        result = search_legal_library("defective product refund consumer")
        assert "consumer" in result.lower() or "warranty" in result.lower()

    def test_empty_query_handled(self):
        """An empty query must return a graceful message, not raise an exception."""
        result = search_legal_library("")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_whitespace_query_handled(self):
        """A whitespace-only query must be handled gracefully."""
        result = search_legal_library("   ")
        assert isinstance(result, str)

    def test_unknown_query_returns_fallback(self):
        """A completely unrelated query must return a fallback message, not crash."""
        result = search_legal_library("quantum physics rocket science")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_result_contains_source_label(self):
        """Results for known topics must include a SOURCE label."""
        result = search_legal_library("landlord tenant lease")
        assert "SOURCE" in result or "source" in result.lower()

    def test_result_limits_to_three_docs(self):
        """Results should contain at most 3 documents (to avoid overwhelming the agent)."""
        result = search_legal_library("law legal rights contract")
        # Count SOURCE occurrences as a proxy for number of docs returned
        count = result.upper().count("SOURCE:")
        assert count <= 3


# ─────────────────────────────────────────────────────────────
#  Knowledge Base / Data Layer
# ─────────────────────────────────────────────────────────────

class TestKnowledgeBase:
    """Tests for the legal document data layer."""

    def test_documents_list_not_empty(self):
        """LEGAL_DOCUMENTS must not be empty."""
        assert len(LEGAL_DOCUMENTS) > 0

    def test_each_document_has_required_fields(self):
        """Every document must have id, title, domain, keywords, and content."""
        required_fields = {"id", "title", "domain", "keywords", "content"}
        for doc in LEGAL_DOCUMENTS:
            for field in required_fields:
                assert field in doc, f"Document {doc.get('id', '?')} missing field '{field}'"

    def test_keyword_index_not_empty(self):
        """KEYWORD_INDEX must be populated."""
        assert len(KEYWORD_INDEX) > 0

    def test_document_by_id_matches_documents(self):
        """DOCUMENT_BY_ID must contain every document in LEGAL_DOCUMENTS."""
        for doc in LEGAL_DOCUMENTS:
            assert doc["id"] in DOCUMENT_BY_ID

    def test_documents_cover_five_domains(self):
        """The knowledge base must cover at least 5 distinct legal domains."""
        domains = {doc["domain"] for doc in LEGAL_DOCUMENTS}
        assert len(domains) >= 5, f"Expected 5+ domains, found: {domains}"
