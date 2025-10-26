"""
Unit tests for Response Synthesis Node
"""

import pytest
from unittest.mock import MagicMock, patch

from src.graphrag.nodes.synthesize_node import (
    synthesize_response,
    _synthesize_from_graph,
    _synthesize_from_vectors,
    _format_graph_results,
    _extract_citations
)
from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


class TestFormatGraphResults:
    """Test graph results formatting."""

    def test_format_empty_results(self):
        """Test formatting with empty results."""
        formatted = _format_graph_results([])
        assert "No graph results available" in formatted

    def test_format_results(self, sample_graph_results):
        """Test formatting with actual results."""
        formatted = _format_graph_results(sample_graph_results)

        assert "component_id" in formatted
        assert "R-ICU" in formatted
        # Should be valid JSON
        import json
        parsed = json.loads(formatted)
        assert len(parsed) == 1

    def test_format_results_truncation(self):
        """Test formatting with large results (truncation)."""
        large_results = [{"key": "A" * 10000} for _ in range(100)]
        formatted = _format_graph_results(large_results)

        # Should be truncated
        assert len(formatted) <= 8050  # 8000 + "[truncated]"
        assert "[truncated]" in formatted


class TestExtractCitations:
    """Test citation extraction."""

    def test_extract_citations_from_graph(self, sample_graph_results):
        """Test citation extraction from graph results."""
        citations = _extract_citations(sample_graph_results, [])

        assert len(citations) > 0
        assert citations[0]["type"] == "component"
        assert citations[0]["id"] == "R-ICU"

    def test_extract_citations_from_sections(self, sample_vector_results):
        """Test citation extraction from vector results."""
        citations = _extract_citations([], sample_vector_results)

        assert len(citations) > 0
        assert citations[0]["type"] == "document_section"
        assert "DDD" in citations[0]["source"]

    def test_extract_citations_mixed(self, sample_graph_results, sample_vector_results):
        """Test citation extraction from both graph and vector results."""
        citations = _extract_citations(sample_graph_results, sample_vector_results)

        # Should have citations from both sources
        types = [c["type"] for c in citations]
        assert "component" in types
        assert "document_section" in types

    def test_extract_citations_limit(self):
        """Test that citations are limited to 5 per source."""
        large_graph_results = [
            {"requirement_id": f"REQ_{i}"} for i in range(10)
        ]
        citations = _extract_citations(large_graph_results, [])

        # Should be limited to 5
        assert len(citations) <= 5


class TestSynthesizeFromGraph:
    """Test synthesis from graph results."""

    def test_synthesize_graph_english(self, env_setup, sample_graph_rag_state, sample_graph_results, sample_vector_results, mock_gpt4_response):
        """Test graph synthesis in English."""
        state = sample_graph_rag_state.copy()
        state["graph_results"] = sample_graph_results
        state["top_k_sections"] = sample_vector_results
        state["cypher_query"] = "MATCH (c:Component) RETURN c"

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            response = _synthesize_from_graph(state, "en")

            assert "answer" in response
            assert "citations" in response
            assert len(response["answer"]) > 0

            # Verify GPT-4 was called with correct parameters
            call_args = client_instance.chat.completions.create.call_args
            assert call_args[1]["model"] == "gpt-4o"
            assert call_args[1]["temperature"] == 0.3

    def test_synthesize_graph_korean(self, env_setup, sample_graph_rag_state, sample_graph_results, mock_gpt4_response):
        """Test graph synthesis in Korean."""
        state = sample_graph_rag_state.copy()
        state["graph_results"] = sample_graph_results
        state["language"] = "ko"

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            response = _synthesize_from_graph(state, "ko")

            assert "answer" in response
            # Check that Korean prompt was used
            call_args = client_instance.chat.completions.create.call_args
            messages = call_args[1]["messages"]
            assert any("MOSAR" in msg["content"] for msg in messages)

    def test_synthesize_graph_no_results(self, env_setup, sample_graph_rag_state):
        """Test graph synthesis with no results."""
        state = sample_graph_rag_state.copy()
        state["graph_results"] = []
        state["top_k_sections"] = []

        response = _synthesize_from_graph(state, "en")

        assert "couldn't find" in response["answer"].lower()
        assert response["citations"] == []

    def test_synthesize_graph_gpt4_error(self, env_setup, sample_graph_rag_state, sample_graph_results):
        """Test graph synthesis with GPT-4 API error."""
        state = sample_graph_rag_state.copy()
        state["graph_results"] = sample_graph_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = client_instance

            response = _synthesize_from_graph(state, "en")

            assert "Error generating response" in response["answer"]
            assert response["citations"] == []


class TestSynthesizeFromVectors:
    """Test synthesis from vector search results only."""

    def test_synthesize_vectors_success(self, env_setup, sample_graph_rag_state, sample_vector_results, mock_gpt4_response):
        """Test successful vector-only synthesis."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = sample_vector_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            response = _synthesize_from_vectors(state, "en")

            assert "answer" in response
            assert "citations" in response
            assert len(response["citations"]) > 0

    def test_synthesize_vectors_no_sections(self, env_setup, sample_graph_rag_state):
        """Test vector synthesis with no sections."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = []

        response = _synthesize_from_vectors(state, "en")

        assert "No relevant documents found" in response["answer"]
        assert response["citations"] == []

    def test_synthesize_vectors_korean(self, env_setup, sample_graph_rag_state, sample_vector_results, mock_gpt4_response):
        """Test vector synthesis in Korean."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = sample_vector_results
        state["language"] = "ko"

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            response = _synthesize_from_vectors(state, "ko")

            assert "answer" in response


class TestSynthesizeResponse:
    """Test main synthesis node function."""

    def test_synthesize_pure_cypher(self, env_setup, sample_graph_rag_state, sample_graph_results, mock_gpt4_response):
        """Test synthesis with pure Cypher path."""
        state = sample_graph_rag_state.copy()
        state["query_path"] = QueryPath.PURE_CYPHER
        state["graph_results"] = sample_graph_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            result_state = synthesize_response(state)

            assert result_state["final_answer"] is not None
            assert len(result_state["final_answer"]) > 0
            assert result_state["citations"] is not None

    def test_synthesize_hybrid(self, env_setup, sample_graph_rag_state, sample_graph_results, sample_vector_results, mock_gpt4_response):
        """Test synthesis with hybrid path."""
        state = sample_graph_rag_state.copy()
        state["query_path"] = QueryPath.HYBRID
        state["graph_results"] = sample_graph_results
        state["top_k_sections"] = sample_vector_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            result_state = synthesize_response(state)

            assert result_state["final_answer"] is not None
            assert result_state["citations"] is not None

    def test_synthesize_pure_vector(self, env_setup, sample_graph_rag_state, sample_vector_results, mock_gpt4_response):
        """Test synthesis with pure vector path."""
        state = sample_graph_rag_state.copy()
        state["query_path"] = QueryPath.PURE_VECTOR
        state["top_k_sections"] = sample_vector_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            result_state = synthesize_response(state)

            assert result_state["final_answer"] is not None

    def test_synthesize_preserves_state(self, env_setup, sample_graph_rag_state, sample_graph_results, mock_gpt4_response):
        """Test that synthesis preserves existing state."""
        state = sample_graph_rag_state.copy()
        state["query_path"] = QueryPath.PURE_CYPHER
        state["graph_results"] = sample_graph_results

        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_response
            mock_openai.return_value = client_instance

            result_state = synthesize_response(state)

            # Check that original state is preserved
            assert result_state["user_question"] == state["user_question"]
            assert result_state["query_path"] == state["query_path"]
            assert result_state["graph_results"] == state["graph_results"]
