"""
Unit tests for Vector Search Node
"""

import pytest
from unittest.mock import MagicMock, patch

from src.graphrag.nodes.vector_search_node import run_vector_search, get_embedding
from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


class TestGetEmbedding:
    """Test embedding generation function."""

    def test_get_embedding_success(self, env_setup, mock_embedding_response):
        """Test successful embedding generation."""
        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.embeddings.create.return_value = mock_embedding_response
            mock_openai.return_value = client_instance

            embedding = get_embedding("test query")

            assert len(embedding) == 3072
            assert all(isinstance(x, float) for x in embedding)
            client_instance.embeddings.create.assert_called_once()

    def test_get_embedding_failure(self, env_setup):
        """Test embedding generation with API failure."""
        with patch('openai.OpenAI') as mock_openai:
            client_instance = MagicMock()
            client_instance.embeddings.create.side_effect = Exception("API Error")
            mock_openai.return_value = client_instance

            embedding = get_embedding("test query")

            # Should return zero vector on failure
            assert len(embedding) == 3072
            assert all(x == 0.0 for x in embedding)


class TestVectorSearchNode:
    """Test vector search node functionality."""

    def test_run_vector_search_success(self, env_setup, sample_graph_rag_state, sample_vector_results):
        """Test successful vector search execution."""
        with patch('openai.OpenAI') as mock_openai, \
             patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:

            # Mock embedding
            client_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
            client_instance.embeddings.create.return_value = mock_response
            mock_openai.return_value = client_instance

            # Mock Neo4j
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_vector_results
            mock_neo4j.return_value = neo4j_instance

            # Run vector search
            result_state = run_vector_search(sample_graph_rag_state)

            # Assertions
            assert result_state["top_k_sections"] is not None
            assert len(result_state["top_k_sections"]) == 3
            assert result_state["top_k_sections"][0]["section_id"] == "DDD-3.2"
            assert result_state["top_k_sections"][0]["score"] == 0.89

            # Verify Neo4j was called
            neo4j_instance.execute.assert_called_once()
            neo4j_instance.close.assert_called_once()

    def test_run_vector_search_empty_results(self, env_setup, sample_graph_rag_state):
        """Test vector search with no results."""
        with patch('openai.OpenAI') as mock_openai, \
             patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:

            # Mock embedding
            client_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
            client_instance.embeddings.create.return_value = mock_response
            mock_openai.return_value = client_instance

            # Mock Neo4j with empty results
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = []
            mock_neo4j.return_value = neo4j_instance

            # Run vector search
            result_state = run_vector_search(sample_graph_rag_state)

            # Assertions
            assert result_state["top_k_sections"] == []

    def test_run_vector_search_neo4j_error(self, env_setup, sample_graph_rag_state):
        """Test vector search with Neo4j error."""
        with patch('openai.OpenAI') as mock_openai, \
             patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:

            # Mock embedding
            client_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
            client_instance.embeddings.create.return_value = mock_response
            mock_openai.return_value = client_instance

            # Mock Neo4j with error
            neo4j_instance = MagicMock()
            neo4j_instance.execute.side_effect = Exception("Database connection failed")
            mock_neo4j.return_value = neo4j_instance

            # Run vector search
            result_state = run_vector_search(sample_graph_rag_state)

            # Assertions
            assert result_state["top_k_sections"] == []
            assert "Vector search error" in result_state["error"]

    def test_run_vector_search_preserves_state(self, env_setup, sample_graph_rag_state, sample_vector_results):
        """Test that vector search preserves existing state."""
        with patch('openai.OpenAI') as mock_openai, \
             patch('src.utils.neo4j_client.Neo4jClient') as mock_neo4j:

            # Mock embedding
            client_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
            client_instance.embeddings.create.return_value = mock_response
            mock_openai.return_value = client_instance

            # Mock Neo4j
            neo4j_instance = MagicMock()
            neo4j_instance.execute.return_value = sample_vector_results
            mock_neo4j.return_value = neo4j_instance

            # Run vector search
            result_state = run_vector_search(sample_graph_rag_state)

            # Check that original state fields are preserved
            assert result_state["user_question"] == sample_graph_rag_state["user_question"]
            assert result_state["language"] == sample_graph_rag_state["language"]
            assert result_state["query_path"] == sample_graph_rag_state["query_path"]
