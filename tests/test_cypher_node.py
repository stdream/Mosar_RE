"""
Unit tests for Cypher Query Node
"""

import pytest
from unittest.mock import MagicMock, patch

from src.graphrag.nodes.cypher_node import (
    run_template_cypher,
    run_contextual_cypher,
    _build_contextual_query
)
from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


class TestBuildContextualQuery:
    """Test contextual Cypher query building."""

    def test_build_query_component_protocol(self):
        """Test query building for Component + Protocol."""
        entities = {
            "Component": ["R-ICU"],
            "Protocol": ["CAN", "Ethernet"]
        }
        question = "What protocols does R-ICU use?"

        query = _build_contextual_query(question, entities)

        assert "Component" in query
        assert "Protocol" in query
        assert "'R-ICU'" in query
        assert "'CAN'" in query
        assert "'Ethernet'" in query

    def test_build_query_component_requirement(self):
        """Test query building for Component + Requirement."""
        entities = {
            "Component": ["R-ICU"],
            "Requirement": ["FuncR_S110"]
        }
        question = "What requirements does R-ICU implement?"

        query = _build_contextual_query(question, entities)

        assert "Component" in query
        assert "Requirement" in query
        assert "'R-ICU'" in query
        assert "'FuncR_S110'" in query
        assert "RELATES_TO" in query

    def test_build_query_requirement_testcase(self):
        """Test query building for Requirement + TestCase."""
        entities = {
            "Requirement": ["FuncR_S110"],
            "TestCase": ["CT-A-1"]
        }
        question = "What tests verify FuncR_S110?"

        query = _build_contextual_query(question, entities)

        assert "Requirement" in query
        assert "TestCase" in query
        assert "'FuncR_S110'" in query
        assert "'CT-A-1'" in query
        assert "VERIFIES" in query

    def test_build_query_component_only_test_context(self):
        """Test query building for Component only with test/verify keywords."""
        entities = {
            "Component": ["R-ICU"]
        }
        question = "What tests verify R-ICU?"

        query = _build_contextual_query(question, entities)

        assert "Component" in query
        assert "TestCase" in query
        assert "'R-ICU'" in query
        assert "VERIFIES" in query

    def test_build_query_component_only_general(self):
        """Test query building for Component only (general query)."""
        entities = {
            "Component": ["R-ICU"]
        }
        question = "Tell me about R-ICU"

        query = _build_contextual_query(question, entities)

        assert "Component" in query
        assert "'R-ICU'" in query
        assert "Requirement" in query  # Should include requirements

    def test_build_query_requirement_only(self):
        """Test query building for Requirement only."""
        entities = {
            "Requirement": ["FuncR_S110"]
        }
        question = "Tell me about FuncR_S110"

        query = _build_contextual_query(question, entities)

        assert "Requirement" in query
        assert "'FuncR_S110'" in query
        assert "DERIVES_FROM" in query  # Should include parent/child

    def test_build_query_testcase_only(self):
        """Test query building for TestCase only."""
        entities = {
            "TestCase": ["CT-A-1"]
        }
        question = "Tell me about test CT-A-1"

        query = _build_contextual_query(question, entities)

        assert "TestCase" in query
        assert "'CT-A-1'" in query

    def test_build_query_no_entities(self):
        """Test query building with no entities."""
        entities = {}
        question = "General question"

        query = _build_contextual_query(question, entities)

        # Should return generic fallback query
        assert "MATCH" in query
        assert "LIMIT" in query


class TestRunTemplateCypher:
    """Test template Cypher execution node."""

    def test_run_template_with_requirement(self, env_setup, sample_graph_rag_state, sample_graph_results):
        """Test template Cypher with requirement entity."""
        state = sample_graph_rag_state.copy()
        state["matched_entities"] = {"requirements": ["FuncR_S110"]}

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j, \
             patch('src.query.cypher_templates.CypherTemplates') as mock_templates:

            # Mock Neo4j
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_graph_results
            mock_neo4j.return_value = neo4j_instance

            # Mock templates
            templates_instance = MagicMock()
            templates_instance.get_requirement_traceability.return_value = "MATCH (r:Requirement) RETURN r"
            mock_templates.return_value = templates_instance

            result_state = run_template_cypher(state)

            assert result_state["graph_results"] is not None
            assert len(result_state["graph_results"]) > 0
            assert result_state["cypher_query"] is not None
            templates_instance.get_requirement_traceability.assert_called_once_with("FuncR_S110")

    def test_run_template_with_component(self, env_setup, sample_graph_rag_state, sample_graph_results):
        """Test template Cypher with component entity."""
        state = sample_graph_rag_state.copy()
        state["matched_entities"] = {"components": ["R-ICU"]}

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j, \
             patch('src.query.cypher_templates.CypherTemplates') as mock_templates:

            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_graph_results
            mock_neo4j.return_value = neo4j_instance

            templates_instance = MagicMock()
            templates_instance.get_component_requirements.return_value = "MATCH (c:Component) RETURN c"
            mock_templates.return_value = templates_instance

            result_state = run_template_cypher(state)

            assert result_state["graph_results"] is not None
            templates_instance.get_component_requirements.assert_called_once_with("R-ICU")

    def test_run_template_no_entities(self, env_setup, sample_graph_rag_state):
        """Test template Cypher with no matched entities."""
        state = sample_graph_rag_state.copy()
        state["matched_entities"] = {}

        result_state = run_template_cypher(state)

        assert result_state["graph_results"] == []

    def test_run_template_neo4j_error(self, env_setup, sample_graph_rag_state):
        """Test template Cypher with Neo4j execution error."""
        state = sample_graph_rag_state.copy()
        state["matched_entities"] = {"requirements": ["FuncR_S110"]}

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j, \
             patch('src.query.cypher_templates.CypherTemplates') as mock_templates:

            neo4j_instance = MagicMock()
            neo4j_instance.execute.side_effect = Exception("Database error")
            mock_neo4j.return_value = neo4j_instance

            templates_instance = MagicMock()
            templates_instance.get_requirement_traceability.return_value = "MATCH (r:Requirement) RETURN r"
            mock_templates.return_value = templates_instance

            result_state = run_template_cypher(state)

            assert result_state["graph_results"] == []
            assert "Cypher execution error" in result_state["error"]


class TestRunContextualCypher:
    """Test contextual Cypher execution node."""

    def test_run_contextual_success(self, env_setup, sample_graph_rag_state, sample_extracted_entities, sample_graph_results):
        """Test successful contextual Cypher execution."""
        state = sample_graph_rag_state.copy()
        state["extracted_entities"] = sample_extracted_entities

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_graph_results
            mock_neo4j.return_value = neo4j_instance

            result_state = run_contextual_cypher(state)

            assert result_state["graph_results"] is not None
            assert len(result_state["graph_results"]) > 0
            assert result_state["cypher_query"] is not None
            assert "Component" in result_state["cypher_query"]
            neo4j_instance.execute.assert_called_once()

    def test_run_contextual_no_entities(self, env_setup, sample_graph_rag_state):
        """Test contextual Cypher with no extracted entities."""
        state = sample_graph_rag_state.copy()
        state["extracted_entities"] = {}

        result_state = run_contextual_cypher(state)

        assert result_state["graph_results"] == []

    def test_run_contextual_neo4j_error(self, env_setup, sample_graph_rag_state, sample_extracted_entities):
        """Test contextual Cypher with Neo4j error."""
        state = sample_graph_rag_state.copy()
        state["extracted_entities"] = sample_extracted_entities

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:
            neo4j_instance = MagicMock()
            neo4j_instance.execute.side_effect = Exception("Query execution failed")
            mock_neo4j.return_value = neo4j_instance

            result_state = run_contextual_cypher(state)

            assert result_state["graph_results"] == []
            assert "Cypher execution error" in result_state["error"]

    def test_run_contextual_preserves_state(self, env_setup, sample_graph_rag_state, sample_extracted_entities, sample_graph_results):
        """Test that contextual Cypher preserves existing state."""
        state = sample_graph_rag_state.copy()
        state["extracted_entities"] = sample_extracted_entities

        with patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_graph_results
            mock_neo4j.return_value = neo4j_instance

            result_state = run_contextual_cypher(state)

            assert result_state["user_question"] == state["user_question"]
            assert result_state["extracted_entities"] == state["extracted_entities"]
            assert result_state["query_path"] == state["query_path"]
