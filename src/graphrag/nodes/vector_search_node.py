"""
Vector Search Node - Semantic similarity search using Neo4j vector index

Retrieves top-k most relevant document sections based on embedding similarity.
"""

import logging
from typing import List, Dict, Any
import os
from openai import OpenAI

from src.graphrag.state import GraphRAGState
from src.utils.neo4j_client import Neo4jClient

logger = logging.getLogger(__name__)


def get_embedding(text: str, model: str = "text-embedding-3-large") -> List[float]:
    """
    Generate OpenAI embedding for text.

    Args:
        text: Input text
        model: OpenAI embedding model

    Returns:
        3072-dimensional embedding vector
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding

    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        # Return zero vector as fallback
        return [0.0] * 3072


def run_vector_search(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Perform vector similarity search on document sections.

    Uses Neo4j vector index 'section_embeddings' to find top-k relevant sections.

    Args:
        state: Current GraphRAGState

    Returns:
        Updated state with 'top_k_sections' populated
    """
    user_question = state["user_question"]
    k = 10  # Top-k sections to retrieve

    logger.info(f"Running vector search for: {user_question[:100]}...")

    # Generate query embedding
    query_embedding = get_embedding(user_question)

    # Neo4j vector search query
    cypher = """
    CALL db.index.vector.queryNodes('section_embeddings', $k, $embedding)
    YIELD node, score
    MATCH (doc:Document)-[:HAS_SECTION]->(node)
    RETURN
        node.id AS section_id,
        node.title AS title,
        node.content AS content,
        doc.title AS document,
        doc.type AS doc_type,
        score
    ORDER BY score DESC
    LIMIT $k
    """

    # Execute query
    neo4j_client = Neo4jClient()
    try:
        results = neo4j_client.execute(
            cypher,
            k=k,
            embedding=query_embedding
        )

        logger.info(f"Vector search returned {len(results)} sections")

        # Format results
        top_k_sections = [
            {
                "section_id": rec["section_id"],
                "title": rec["title"],
                "content": rec["content"],
                "document": rec["document"],
                "doc_type": rec["doc_type"],
                "score": float(rec["score"])
            }
            for rec in results
        ]

        # Log top results
        for i, section in enumerate(top_k_sections[:3]):
            logger.debug(f"  [{i+1}] {section['title']} (score={section['score']:.3f})")

        # Update state
        state["top_k_sections"] = top_k_sections

    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        state["top_k_sections"] = []
        state["error"] = f"Vector search error: {str(e)}"

    finally:
        neo4j_client.close()

    return state


# Standalone function for testing
def test_vector_search(question: str, k: int = 10):
    """
    Test vector search standalone.

    Args:
        question: User question
        k: Number of results
    """
    state = GraphRAGState(
        user_question=question,
        language="en",
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
        error=None
    )

    result_state = run_vector_search(state)

    print(f"Question: {question}\n")
    print(f"Top {k} Results:")
    for i, section in enumerate(result_state["top_k_sections"][:k]):
        print(f"\n[{i+1}] {section['title']}")
        print(f"    Document: {section['document']} ({section['doc_type']})")
        print(f"    Score: {section['score']:.3f}")
        print(f"    Content: {section['content'][:200]}...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test with sample questions
    test_questions = [
        "What hardware handles network communication?",
        "어떤 하드웨어가 네트워크 통신을 담당하나요?",
        "How does the Service Module handle real-time communication?",
    ]

    for q in test_questions:
        test_vector_search(q, k=5)
        print("\n" + "="*80 + "\n")
