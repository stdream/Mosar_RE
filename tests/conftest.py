"""
Pytest configuration and shared fixtures for MOSAR GraphRAG tests
"""

import pytest
import os
from unittest.mock import MagicMock, patch
from typing import Dict, List, Any

from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


@pytest.fixture
def mock_neo4j_client():
    """Mock Neo4j client for testing without database connection."""
    with patch('src.utils.neo4j_client.Neo4jClient') as mock:
        client_instance = MagicMock()
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing without API calls."""
    with patch('openai.OpenAI') as mock:
        client_instance = MagicMock()
        mock.return_value = client_instance
        yield client_instance


@pytest.fixture
def sample_graph_rag_state() -> GraphRAGState:
    """Create a sample GraphRAGState for testing."""
    return GraphRAGState(
        user_question="What hardware handles network communication?",
        language="en",
        session_id="test_session_123",
        user_id="test_user",
        query_path=QueryPath.HYBRID,
        routing_confidence=0.85,
        matched_entities={"Component": ["R-ICU"]},
        top_k_sections=None,
        extracted_entities=None,
        cypher_query=None,
        graph_results=None,
        final_answer="",
        citations=None,
        processing_time_ms=None,
        execution_path=None,
        cache_hit=None,
        error=None
    )


@pytest.fixture
def sample_vector_results() -> List[Dict[str, Any]]:
    """Sample vector search results."""
    return [
        {
            "section_id": "DDD-3.2",
            "title": "Network Architecture",
            "content": "The R-ICU (Reduced Instrument Control Unit) is responsible for network communication. It uses CAN bus at 1 Mbps for real-time communication and Ethernet at 100 Mbps for high-bandwidth data transfer. The component implements FuncR_S110 requirement for network redundancy.",
            "document": "DDD",
            "doc_type": "detailed_design",
            "score": 0.89
        },
        {
            "section_id": "PDD-2.1",
            "title": "Service Module Components",
            "content": "The Service Module (SM) contains the R-ICU, cPDU (Power Distribution Unit), and HOTDOCK interface. The WM (Walking Manipulator) connects via CAN bus.",
            "document": "PDD",
            "doc_type": "preliminary_design",
            "score": 0.78
        },
        {
            "section_id": "SRD-1.5",
            "title": "Communication Requirements",
            "content": "IntR_S102 specifies that all critical components must support redundant communication paths. The R-ICU implements both CAN and Ethernet interfaces to meet this requirement.",
            "document": "SRD",
            "doc_type": "requirements",
            "score": 0.72
        }
    ]


@pytest.fixture
def sample_extracted_entities() -> Dict[str, List[str]]:
    """Sample extracted entities from NER."""
    return {
        "Component": ["R-ICU", "WM", "SM"],
        "Requirement": ["FuncR_S110", "IntR_S102"],
        "Protocol": ["CAN", "Ethernet"]
    }


@pytest.fixture
def sample_graph_results() -> List[Dict[str, Any]]:
    """Sample graph query results."""
    return [
        {
            "component_id": "R-ICU",
            "component_name": "Reduced Instrument Control Unit",
            "protocols": ["CAN", "Ethernet"],
            "related_requirements": ["FuncR_S110", "IntR_S102"],
            "test_cases": ["CT-A-1", "IT1"]
        }
    ]


@pytest.fixture
def mock_embedding_response():
    """Mock OpenAI embedding response."""
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 3072)]
    return mock_response


@pytest.fixture
def mock_gpt4_response():
    """Mock OpenAI GPT-4 chat completion response."""
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "This is a test response from GPT-4."
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def mock_gpt4_json_response():
    """Mock OpenAI GPT-4 response with JSON entity extraction."""
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = '''```json
{
  "Component": ["R-ICU", "WM"],
  "Requirement": ["FuncR_S110"],
  "Protocol": ["CAN", "Ethernet"]
}
```'''
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.fixture
def env_setup(monkeypatch):
    """Setup environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USER", "neo4j")
    monkeypatch.setenv("NEO4J_PASSWORD", "test_password")
    monkeypatch.setenv("NEO4J_DATABASE", "neo4j")
