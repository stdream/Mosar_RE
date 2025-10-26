"""
Unit tests for NER (Named Entity Recognition) Node
"""

import pytest
from unittest.mock import MagicMock, patch
import json

from src.graphrag.nodes.ner_node import (
    extract_entities_from_context,
    _extract_entities_with_gpt4,
    _validate_with_entity_dict
)
from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


class TestExtractEntitiesWithGPT4:
    """Test GPT-4 entity extraction."""

    def test_extract_entities_success(self, env_setup, mock_gpt4_json_response):
        """Test successful entity extraction with GPT-4."""
        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = mock_gpt4_json_response
            mock_openai.return_value = client_instance

            context = "The R-ICU handles network communication using CAN and Ethernet."
            question = "What components handle networking?"

            entities = _extract_entities_with_gpt4(context, question)

            assert "Component" in entities
            assert "R-ICU" in entities["Component"]
            assert "Protocol" in entities
            assert "CAN" in entities["Protocol"]

    def test_extract_entities_json_parse_error(self, env_setup):
        """Test entity extraction with invalid JSON response."""
        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            mock_message.content = "This is not valid JSON"
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            client_instance.chat.completions.create.return_value = mock_response
            mock_openai.return_value = client_instance

            entities = _extract_entities_with_gpt4("context", "question")

            # Should return empty dict on JSON parse failure
            assert entities == {}

    def test_extract_entities_api_error(self, env_setup):
        """Test entity extraction with API error."""
        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.chat.completions.create.side_effect = Exception("API Error")
            mock_openai.return_value = client_instance

            entities = _extract_entities_with_gpt4("context", "question")

            # Should return empty dict on API error
            assert entities == {}


class TestValidateWithEntityDict:
    """Test entity validation against Entity Dictionary."""

    def test_validate_exact_match(self):
        """Test validation with exact match in dictionary."""
        entities = {
            "Component": ["R-ICU", "WM"],
            "Requirement": ["FuncR_S110"]
        }

        # Entity resolver should handle validation
        with patch('src.utils.entity_resolver.EntityResolver') as mock_resolver:
            resolver_instance = MagicMock()
            resolver_instance.resolve_exact.side_effect = [
                {"id": "R-ICU", "type": "Component"},
                {"id": "WM", "type": "Component"},
                {"id": "FuncR_S110", "type": "Requirement"}
            ]
            mock_resolver.return_value = resolver_instance

            validated = _validate_with_entity_dict(entities)

            assert "Component" in validated
            assert "R-ICU" in validated["Component"]
            assert "WM" in validated["Component"]
            assert "Requirement" in validated
            assert "FuncR_S110" in validated["Requirement"]

    def test_validate_fuzzy_match(self):
        """Test validation with fuzzy matching."""
        entities = {
            "Component": ["R ICU"]  # Typo - missing hyphen
        }

        with patch('src.utils.entity_resolver.EntityResolver') as mock_resolver:
            resolver_instance = MagicMock()
            resolver_instance.resolve_exact.return_value = None
            resolver_instance.resolve_fuzzy.return_value = {
                "id": "R-ICU",
                "confidence": 0.9
            }
            mock_resolver.return_value = resolver_instance

            validated = _validate_with_entity_dict(entities)

            # Should fuzzy match to R-ICU
            assert "Component" in validated
            assert "R-ICU" in validated["Component"]

    def test_validate_no_match(self):
        """Test validation with no match found."""
        entities = {
            "Component": ["UNKNOWN_COMPONENT"]
        }

        with patch('src.utils.entity_resolver.EntityResolver') as mock_resolver:
            resolver_instance = MagicMock()
            resolver_instance.resolve_exact.return_value = None
            resolver_instance.resolve_fuzzy.return_value = {"confidence": 0.3}  # Low confidence
            mock_resolver.return_value = resolver_instance

            validated = _validate_with_entity_dict(entities)

            # Should keep original if no good match
            assert "Component" in validated
            assert "UNKNOWN_COMPONENT" in validated["Component"]


class TestExtractEntitiesFromContext:
    """Test the main NER node function."""

    def test_extract_entities_success(self, env_setup, sample_graph_rag_state, sample_vector_results):
        """Test successful entity extraction from context."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = sample_vector_results

        with patch('src.graphrag.nodes.ner_node._extract_entities_with_gpt4') as mock_gpt4, \
             patch('src.graphrag.nodes.ner_node._validate_with_entity_dict') as mock_validate:

            mock_gpt4.return_value = {
                "Component": ["R-ICU", "WM"],
                "Requirement": ["FuncR_S110"],
                "Protocol": ["CAN", "Ethernet"]
            }
            mock_validate.return_value = {
                "Component": ["R-ICU", "WM"],
                "Requirement": ["FuncR_S110"],
                "Protocol": ["CAN", "Ethernet"]
            }

            result_state = extract_entities_from_context(state)

            assert result_state["extracted_entities"] is not None
            assert "Component" in result_state["extracted_entities"]
            assert "R-ICU" in result_state["extracted_entities"]["Component"]

    def test_extract_entities_no_sections(self, env_setup, sample_graph_rag_state):
        """Test entity extraction with no sections available."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = []

        result_state = extract_entities_from_context(state)

        assert result_state["extracted_entities"] == {}

    def test_extract_entities_truncation(self, env_setup, sample_graph_rag_state):
        """Test entity extraction with large context (truncation)."""
        state = sample_graph_rag_state.copy()

        # Create very large sections
        large_sections = [
            {
                "section_id": f"SEC-{i}",
                "title": f"Section {i}",
                "content": "A" * 5000,  # 5000 chars each
                "document": "TEST",
                "doc_type": "test",
                "score": 0.9
            }
            for i in range(5)
        ]
        state["top_k_sections"] = large_sections

        with patch('src.graphrag.nodes.ner_node._extract_entities_with_gpt4') as mock_gpt4, \
             patch('src.graphrag.nodes.ner_node._validate_with_entity_dict') as mock_validate:

            mock_gpt4.return_value = {"Component": ["R-ICU"]}
            mock_validate.return_value = {"Component": ["R-ICU"]}

            result_state = extract_entities_from_context(state)

            # Check that GPT-4 was called with truncated context
            call_args = mock_gpt4.call_args
            context_arg = call_args[1]["context"]

            # Should be truncated to max_chars (16000) + truncation message
            assert len(context_arg) <= 16050  # 16000 + "[truncated]"

    def test_extract_entities_preserves_state(self, env_setup, sample_graph_rag_state, sample_vector_results):
        """Test that entity extraction preserves existing state."""
        state = sample_graph_rag_state.copy()
        state["top_k_sections"] = sample_vector_results

        with patch('src.graphrag.nodes.ner_node._extract_entities_with_gpt4') as mock_gpt4, \
             patch('src.graphrag.nodes.ner_node._validate_with_entity_dict') as mock_validate:

            mock_gpt4.return_value = {"Component": ["R-ICU"]}
            mock_validate.return_value = {"Component": ["R-ICU"]}

            result_state = extract_entities_from_context(state)

            # Check that original state fields are preserved
            assert result_state["user_question"] == state["user_question"]
            assert result_state["top_k_sections"] == state["top_k_sections"]
            assert result_state["query_path"] == state["query_path"]
