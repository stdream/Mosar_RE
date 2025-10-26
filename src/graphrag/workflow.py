"""
LangGraph Workflow - Main GraphRAG query execution workflow

Implements adaptive routing with 3 paths:
- Path A: Pure Cypher (high confidence entity match)
- Path B: Hybrid (vector + NER + Cypher)
- Path C: Pure Vector (exploratory)
"""

import logging
import time
from typing import Dict, Any
from langgraph.graph import StateGraph, END

from src.graphrag.state import GraphRAGState
from src.query.router import QueryRouter, QueryPath
from src.graphrag.nodes import (
    run_vector_search,
    extract_entities_from_context,
    run_contextual_cypher,
    run_template_cypher,
    synthesize_response
)

logger = logging.getLogger(__name__)


class GraphRAGWorkflow:
    """
    LangGraph-based workflow for GraphRAG queries.

    Workflow structure:
    1. Router → determine path
    2. Path A: Template Cypher → Synthesize
    3. Path B: Vector → NER → Contextual Cypher → Synthesize
    4. Path C: Vector → Synthesize
    """

    def __init__(self, entity_dict_path: str = "data/entities/mosar_entities.json"):
        """
        Initialize workflow.

        Args:
            entity_dict_path: Path to Entity Dictionary
        """
        self.router = QueryRouter(entity_dict_path)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build LangGraph workflow with conditional routing.

        Returns:
            Compiled StateGraph
        """
        # Create graph
        workflow = StateGraph(GraphRAGState)

        # Add nodes
        workflow.add_node("route_query", self._route_query_node)
        workflow.add_node("vector_search", run_vector_search)
        workflow.add_node("extract_entities", extract_entities_from_context)
        workflow.add_node("template_cypher", run_template_cypher)
        workflow.add_node("contextual_cypher", run_contextual_cypher)
        workflow.add_node("synthesize", synthesize_response)

        # Set entry point
        workflow.set_entry_point("route_query")

        # Add conditional edges from router
        workflow.add_conditional_edges(
            "route_query",
            self._route_decision,
            {
                "path_a": "template_cypher",
                "path_b": "vector_search",
                "path_c": "vector_search"
            }
        )

        # Path A: Pure Cypher → Synthesize → END
        workflow.add_edge("template_cypher", "synthesize")

        # Path B: Vector → NER → Contextual Cypher → Synthesize
        workflow.add_conditional_edges(
            "vector_search",
            self._after_vector_decision,
            {
                "path_b": "extract_entities",
                "path_c": "synthesize"
            }
        )
        workflow.add_edge("extract_entities", "contextual_cypher")
        workflow.add_edge("contextual_cypher", "synthesize")

        # All paths converge at synthesize → END
        workflow.add_edge("synthesize", END)

        # Compile graph
        return workflow.compile()

    def _route_query_node(self, state: GraphRAGState) -> GraphRAGState:
        """
        Node: Route user query to appropriate path.

        Args:
            state: Current state

        Returns:
            Updated state with routing info
        """
        user_question = state["user_question"]

        # Detect language
        language = self._detect_language(user_question)
        state["language"] = language

        # Route query
        query_path, routing_info = self.router.route(user_question)

        # Update state
        state["query_path"] = query_path
        state["routing_confidence"] = routing_info["confidence"]
        state["matched_entities"] = routing_info["matched_entities"]

        logger.info(f"Query routed to: {query_path.value} (confidence={routing_info['confidence']:.2f})")

        return state

    def _route_decision(self, state: GraphRAGState) -> str:
        """
        Conditional edge: Determine next node based on query_path.

        Args:
            state: Current state

        Returns:
            Next node key
        """
        query_path = state["query_path"]

        if query_path == QueryPath.PURE_CYPHER:
            return "path_a"
        elif query_path == QueryPath.HYBRID:
            return "path_b"
        else:  # PURE_VECTOR
            return "path_c"

    def _after_vector_decision(self, state: GraphRAGState) -> str:
        """
        Conditional edge: After vector search, determine if NER is needed.

        Args:
            state: Current state

        Returns:
            Next node key
        """
        query_path = state["query_path"]

        if query_path == QueryPath.HYBRID:
            return "path_b"  # Continue to NER
        else:
            return "path_c"  # Skip to synthesis

    def _detect_language(self, text: str) -> str:
        """
        Simple language detection (Korean vs English).

        Args:
            text: Input text

        Returns:
            'ko' or 'en'
        """
        # Check for Korean characters (Hangul)
        korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7a3')
        total_chars = len(text)

        if total_chars == 0:
            return "en"

        korean_ratio = korean_chars / total_chars

        return "ko" if korean_ratio > 0.3 else "en"

    def query(self, user_question: str, session_id: str = None, user_id: str = None) -> Dict[str, Any]:
        """
        Execute GraphRAG query.

        Args:
            user_question: User's natural language question
            session_id: Optional session identifier for tracking
            user_id: Optional user identifier

        Returns:
            Result dict with answer, citations, metadata
        """
        logger.info(f"Processing query: {user_question}")

        start_time = time.time()

        # Initialize state
        initial_state = GraphRAGState(
            user_question=user_question,
            language="en",
            session_id=session_id,
            user_id=user_id,
            query_path=None,
            routing_confidence=0.0,
            matched_entities={},
            top_k_sections=None,
            extracted_entities=None,
            cypher_query=None,
            graph_results=None,
            final_answer="",
            citations=None,
            processing_time_ms=None,
            execution_path=[],
            cache_hit=False,
            error=None
        )

        try:
            # Execute workflow
            final_state = self.graph.invoke(initial_state)

            # Calculate processing time
            processing_time_ms = (time.time() - start_time) * 1000
            final_state["processing_time_ms"] = processing_time_ms

            logger.info(f"Query completed in {processing_time_ms:.0f}ms")

            # Return result
            return {
                "answer": final_state["final_answer"],
                "citations": final_state.get("citations", []),
                "metadata": {
                    "query_path": final_state["query_path"].value if final_state["query_path"] else "unknown",
                    "routing_confidence": final_state["routing_confidence"],
                    "matched_entities": final_state["matched_entities"],
                    "extracted_entities": final_state.get("extracted_entities"),
                    "cypher_query": final_state.get("cypher_query"),
                    "processing_time_ms": processing_time_ms,
                    "language": final_state["language"],
                    "error": final_state.get("error")
                }
            }

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}", exc_info=True)

            return {
                "answer": f"Error processing query: {str(e)}",
                "citations": [],
                "metadata": {
                    "error": str(e),
                    "processing_time_ms": (time.time() - start_time) * 1000
                }
            }


# Standalone usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize workflow
    workflow = GraphRAGWorkflow()

    # Test queries
    test_queries = [
        "Show all requirements verified by R-ICU",  # Path A
        "어떤 하드웨어가 네트워크 통신을 담당하나요?",  # Path B
        "What are the main challenges in orbital assembly?",  # Path C
        "FuncR_S110의 traceability를 보여줘",  # Path A
    ]

    for query in test_queries:
        print("\n" + "="*80)
        print(f"Query: {query}")
        print("="*80)

        result = workflow.query(query)

        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nMetadata:")
        print(f"  - Path: {result['metadata'].get('query_path')}")
        print(f"  - Confidence: {result['metadata'].get('routing_confidence', 0):.2f}")
        print(f"  - Language: {result['metadata'].get('language')}")
        print(f"  - Processing Time: {result['metadata'].get('processing_time_ms', 0):.0f}ms")

        if result['citations']:
            print(f"\nCitations ({len(result['citations'])} sources):")
            for i, citation in enumerate(result['citations'][:5], 1):
                print(f"  [{i}] {citation}")
