"""
LangGraph Workflow - Main GraphRAG query execution workflow

Implements adaptive routing with 3 paths:
- Path A: Pure Cypher (high confidence entity match)
- Path B: Hybrid (vector + NER + Cypher)
- Path C: Pure Vector (exploratory)

Features:
- Text2Cypher (LLM-based Cypher generation)
- Streaming responses (real-time token streaming)
- HITL (Human-in-the-Loop) review
"""

import logging
import os
import time
from typing import Dict, Any, Optional, Generator
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
from src.graphrag.nodes.synthesize_streaming_node import (
    synthesize_response_streaming,
    stream_synthesis
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

        # Path A: Pure Cypher → Synthesize OR Fallback to Hybrid
        workflow.add_conditional_edges(
            "template_cypher",
            self._template_cypher_decision,
            {
                "success": "synthesize",
                "fallback_to_hybrid": "vector_search"
            }
        )

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

    def _template_cypher_decision(self, state: GraphRAGState) -> str:
        """
        Conditional edge: Check if template Cypher succeeded or needs fallback.

        Args:
            state: Current state

        Returns:
            "success" if template executed successfully
            "fallback_to_hybrid" if template not found or failed
        """
        # Check if template selection failed
        if state.get("template_selection_error"):
            logger.warning(
                f"Template selection failed: {state['template_selection_error']}. "
                "Falling back to Hybrid path."
            )
            state["query_path"] = QueryPath.HYBRID  # Update path
            state["fallback_reason"] = state["template_selection_error"]
            return "fallback_to_hybrid"

        # Check if query was generated but execution failed
        if state.get("cypher_query") is None or not state.get("graph_results"):
            logger.warning("Template Cypher produced no results. Falling back to Hybrid path.")
            state["query_path"] = QueryPath.HYBRID
            state["fallback_reason"] = "No results from template query"
            return "fallback_to_hybrid"

        logger.info("✓ Template Cypher succeeded, proceeding to synthesis")
        return "success"

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
                    "error": final_state.get("error"),
                    "query_generation_method": final_state.get("query_generation_method"),
                    "template_selection_error": final_state.get("template_selection_error"),
                    "fallback_reason": final_state.get("fallback_reason"),
                    "template_entity": final_state.get("template_entity"),
                    "graph_results": final_state.get("graph_results", [])
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

    def query_stream(
        self,
        user_question: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Execute GraphRAG query with streaming response.

        Args:
            user_question: User's natural language question
            session_id: Optional session identifier
            user_id: Optional user identifier

        Yields:
            Dicts with:
            - {"type": "status", "message": "..."}  # Status updates
            - {"type": "chunk", "content": "..."}   # Answer chunks
            - {"type": "metadata", "data": {...}}   # Final metadata
        """
        logger.info(f"Processing streaming query: {user_question}")
        start_time = time.time()

        try:
            # Step 1: Route query
            yield {"type": "status", "message": "Routing query..."}
            language = self._detect_language(user_question)
            query_path, routing_info = self.router.route(user_question)

            yield {
                "type": "status",
                "message": f"Path selected: {query_path.value} (confidence={routing_info['confidence']:.2f})"
            }

            # Step 2: Execute retrieval (vector search + Cypher)
            # Build state manually for streaming
            state = {
                "user_question": user_question,
                "language": language,
                "query_path": query_path,
                "routing_confidence": routing_info["confidence"],
                "matched_entities": routing_info["matched_entities"]
            }

            # Run vector search if needed
            if query_path in [QueryPath.HYBRID, QueryPath.PURE_VECTOR]:
                yield {"type": "status", "message": "Searching documents..."}
                state_obj = GraphRAGState(**state)
                state_obj = run_vector_search(state_obj)
                state.update(state_obj)

                # Extract entities for hybrid
                if query_path == QueryPath.HYBRID:
                    yield {"type": "status", "message": "Extracting entities..."}
                    state_obj = extract_entities_from_context(state_obj)
                    state.update(state_obj)

                    # Run contextual Cypher
                    yield {"type": "status", "message": "Querying knowledge graph..."}
                    state_obj = run_contextual_cypher(state_obj)
                    state.update(state_obj)

            # Run template Cypher for pure Cypher path
            elif query_path == QueryPath.PURE_CYPHER:
                yield {"type": "status", "message": "Querying knowledge graph..."}
                state_obj = GraphRAGState(**state)
                state_obj = run_template_cypher(state_obj)
                state.update(state_obj)

            # Step 3: Stream synthesis
            yield {"type": "status", "message": "Generating answer..."}

            # Gather context for streaming
            context = {
                "vector_results": state.get("top_k_sections", []),
                "graph_results": state.get("graph_results", []),
                "cypher_query": state.get("cypher_query"),
                "extracted_entities": state.get("extracted_entities", {}),
                "matched_entities": state.get("matched_entities", {}),
                "query_generation_method": state.get("query_generation_method")
            }

            # Stream answer chunks
            citations = []
            for chunk in stream_synthesis(user_question, context, language, query_path):
                if isinstance(chunk, dict):
                    # Metadata (citations)
                    citations = chunk.get("citations", [])
                else:
                    # Text chunk
                    yield {"type": "chunk", "content": chunk}

            # Step 4: Send final metadata
            processing_time_ms = (time.time() - start_time) * 1000

            yield {
                "type": "metadata",
                "data": {
                    "citations": citations,
                    "query_path": query_path.value,
                    "routing_confidence": routing_info["confidence"],
                    "matched_entities": routing_info["matched_entities"],
                    "extracted_entities": state.get("extracted_entities"),
                    "cypher_query": state.get("cypher_query"),
                    "query_generation_method": state.get("query_generation_method"),
                    "template_selection_error": state.get("template_selection_error"),
                    "fallback_reason": state.get("fallback_reason"),
                    "template_entity": state.get("template_entity"),
                    "graph_results": state.get("graph_results", []),
                    "processing_time_ms": processing_time_ms,
                    "language": language
                }
            }

            logger.info(f"Streaming query completed in {processing_time_ms:.0f}ms")

        except Exception as e:
            logger.error(f"Streaming workflow failed: {e}", exc_info=True)
            yield {
                "type": "error",
                "message": f"Error processing query: {str(e)}"
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
