"""
GraphRAG State Definition for LangGraph Workflow

Defines the state object passed between workflow nodes.
"""

from typing import TypedDict, List, Dict, Any, Optional
from src.query.router import QueryPath


class GraphRAGState(TypedDict):
    """
    State object for GraphRAG workflow.

    Passed between LangGraph nodes and updated at each step.
    """
    # Input
    user_question: str  # Original user question
    language: str  # Detected language (ko, en)

    # Session Management (for CLI/API)
    session_id: Optional[str]  # Unique session identifier
    user_id: Optional[str]  # User identifier

    # Routing
    query_path: QueryPath  # Selected path (pure_cypher, hybrid, pure_vector)
    routing_confidence: float  # 0.0-1.0
    matched_entities: Dict[str, List[str]]  # Entities detected by router

    # Vector Search Results (Path B, C)
    top_k_sections: Optional[List[Dict[str, Any]]]  # Top-k sections from vector search
    # Each dict: {section_id, title, content, score}

    # NER Results (Path B)
    extracted_entities: Optional[Dict[str, List[str]]]  # Entities from NER
    # Format: {"Component": ["R-ICU"], "Requirement": ["FuncR_S110"], ...}

    # Cypher Results (Path A, B)
    cypher_query: Optional[str]  # Generated or template Cypher query
    graph_results: Optional[List[Dict[str, Any]]]  # Results from Cypher execution

    # Final Answer
    final_answer: str  # Synthesized natural language response
    citations: Optional[List[Dict[str, str]]]  # Source citations
    # Format: [{source: "Section 3.2", content: "..."}]

    # Metadata
    processing_time_ms: Optional[float]  # Total processing time
    execution_path: Optional[List[str]]  # Path taken through workflow nodes
    cache_hit: Optional[bool]  # Whether result was cached
    error: Optional[str]  # Error message if any
