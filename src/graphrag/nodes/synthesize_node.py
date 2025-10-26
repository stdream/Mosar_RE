"""
Response Synthesis Node - Generate natural language responses using GPT-4

Combines vector search results and graph query results to produce
coherent, cited answers in Korean or English.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI

from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath

logger = logging.getLogger(__name__)


def synthesize_response(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Synthesize final response using GPT-4.

    Combines:
    - User question
    - Vector search results (semantic context)
    - Graph query results (structured data)
    - Query path information

    Args:
        state: Current GraphRAGState with results populated

    Returns:
        Updated state with 'final_answer' and 'citations'
    """
    user_question = state["user_question"]
    query_path = state.get("query_path")
    language = state.get("language", "en")

    logger.info(f"Synthesizing response for query path: {query_path}")

    # Build synthesis prompt based on available data
    if query_path == QueryPath.PURE_CYPHER or query_path == QueryPath.HYBRID:
        # Use graph results as primary source
        response = _synthesize_from_graph(state, language)
    else:
        # Pure vector - use section results
        response = _synthesize_from_vectors(state, language)

    # Update state
    state["final_answer"] = response["answer"]
    state["citations"] = response["citations"]

    return state


def _synthesize_from_graph(state: GraphRAGState, language: str) -> Dict[str, Any]:
    """
    Synthesize response from graph query results.

    Args:
        state: GraphRAGState
        language: Target language (ko/en)

    Returns:
        Dict with 'answer' and 'citations'
    """
    user_question = state["user_question"]
    graph_results = state.get("graph_results", [])
    top_k_sections = state.get("top_k_sections", [])
    cypher_query = state.get("cypher_query", "")

    if not graph_results and not top_k_sections:
        return {
            "answer": "죄송합니다. 관련 정보를 찾을 수 없습니다." if language == "ko" else "I couldn't find relevant information to answer your question.",
            "citations": []
        }

    # Build context from graph results
    graph_context = _format_graph_results(graph_results)

    # Build context from vector results (supplementary)
    vector_context = ""
    if top_k_sections:
        vector_context = "\n\n".join([
            f"[{sec['document']} - {sec['title']}]\n{sec['content'][:500]}"
            for sec in top_k_sections[:3]
        ])

    # Language-specific prompts
    if language == "ko":
        system_prompt = "당신은 MOSAR (Modular Spacecraft Assembly and Reconfiguration) 시스템 전문가입니다. 기술 문서와 그래프 데이터베이스 쿼리 결과를 바탕으로 정확하고 상세한 답변을 제공하세요."
        instruction = """아래 질문에 대해 제공된 데이터를 바탕으로 답변해주세요.

**답변 요구사항**:
1. 정확하고 기술적으로 상세하게 답변
2. 그래프 데이터베이스 결과를 우선적으로 사용
3. 구체적인 컴포넌트 ID, 요구사항 ID, 테스트 케이스 ID 등을 명시
4. 출처를 명확히 표시 (예: "PDD 3.2절에 따르면...")
5. 관련 요구사항이나 테스트가 있으면 함께 언급
6. 마크다운 형식으로 작성 (리스트, 테이블 등 활용)
"""
    else:
        system_prompt = "You are an expert in MOSAR (Modular Spacecraft Assembly and Reconfiguration) system. Provide accurate and detailed technical answers based on documentation and graph database query results."
        instruction = """Answer the question below based on the provided data.

**Answer Requirements**:
1. Be accurate and technically detailed
2. Prioritize graph database results
3. Include specific component IDs, requirement IDs, test case IDs
4. Clearly cite sources (e.g., "According to PDD Section 3.2...")
5. Mention related requirements or tests if applicable
6. Use markdown formatting (lists, tables, etc.)
"""

    prompt = f"""{instruction}

**Question**:
{user_question}

**Graph Query Results**:
{graph_context}

**Additional Context (from documents)**:
{vector_context if vector_context else "N/A"}

**Cypher Query Used**:
```cypher
{cypher_query}
```

Provide a comprehensive answer:
"""

    # Call GPT-4
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Slightly creative but mostly factual
            max_tokens=2000
        )

        if response and response.choices and len(response.choices) > 0:
            answer = response.choices[0].message.content.strip()
        else:
            logger.error("GPT-4 response is empty or invalid")
            answer = "Error: Empty response from GPT-4"

        # Extract citations
        citations = _extract_citations(graph_results, top_k_sections)

        return {
            "answer": answer,
            "citations": citations
        }

    except Exception as e:
        logger.error(f"Response synthesis failed: {e}", exc_info=True)
        return {
            "answer": f"Error generating response: {str(e)}",
            "citations": []
        }


def _synthesize_from_vectors(state: GraphRAGState, language: str) -> Dict[str, Any]:
    """
    Synthesize response from vector search results only.

    Args:
        state: GraphRAGState
        language: Target language (ko/en)

    Returns:
        Dict with 'answer' and 'citations'
    """
    user_question = state["user_question"]
    top_k_sections = state.get("top_k_sections", [])

    if not top_k_sections:
        return {
            "answer": "관련 문서를 찾을 수 없습니다." if language == "ko" else "No relevant documents found.",
            "citations": []
        }

    # Build context
    context = "\n\n---\n\n".join([
        f"**Source**: {sec['document']} - {sec['title']}\n\n{sec['content']}"
        for sec in top_k_sections[:5]
    ])

    # Language-specific prompts
    if language == "ko":
        system_prompt = "당신은 MOSAR 시스템 기술 문서 전문가입니다. 제공된 문서를 바탕으로 질문에 답변하세요."
        instruction = "아래 문서를 참고하여 질문에 답변해주세요. 출처를 명시하고 마크다운 형식으로 작성하세요."
    else:
        system_prompt = "You are a MOSAR system technical documentation expert. Answer questions based on provided documents."
        instruction = "Answer the question based on the documents below. Cite sources and use markdown formatting."

    prompt = f"""{instruction}

**Question**:
{user_question}

**Relevant Documents**:
{context}

Provide a comprehensive answer:
"""

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        if response and response.choices and len(response.choices) > 0:
            answer = response.choices[0].message.content.strip()
        else:
            logger.error("GPT-4 response is empty or invalid")
            answer = "Error: Empty response from GPT-4"

        citations = _extract_citations([], top_k_sections)

        return {
            "answer": answer,
            "citations": citations
        }

    except Exception as e:
        logger.error(f"Response synthesis failed: {e}", exc_info=True)
        return {
            "answer": f"Error: {str(e)}",
            "citations": []
        }


def _format_graph_results(graph_results: List[Dict[str, Any]]) -> str:
    """
    Format graph query results as readable text.

    Args:
        graph_results: List of Neo4j query results

    Returns:
        Formatted string
    """
    if not graph_results:
        return "No graph results available."

    # Convert to JSON for structured display
    formatted = json.dumps(graph_results, indent=2, ensure_ascii=False)

    # Truncate if too long
    max_chars = 8000
    if len(formatted) > max_chars:
        formatted = formatted[:max_chars] + "\n... [truncated]"

    return formatted


def _extract_citations(graph_results: List[Dict], sections: List[Dict]) -> List[Dict[str, str]]:
    """
    Extract citation information from results.

    Args:
        graph_results: Graph query results
        sections: Vector search sections

    Returns:
        List of citation dicts
    """
    citations = []

    # Citations from graph results
    for result in graph_results[:5]:
        if "requirement_id" in result:
            citations.append({
                "type": "requirement",
                "id": result["requirement_id"],
                "source": "SRD"
            })
        elif "component_id" in result:
            citations.append({
                "type": "component",
                "id": result["component_id"],
                "source": "MOSAR System"
            })

    # Citations from sections
    if sections:
        for sec in sections[:5]:
            if sec and isinstance(sec, dict):
                citations.append({
                    "type": "document_section",
                    "source": f"{sec.get('document', 'Unknown')} - {sec.get('title', 'Unknown')}",
                    "score": f"{sec.get('score', 0.0):.3f}"
                })

    return citations


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Mock state with sample results
    state = GraphRAGState(
        user_question="What hardware handles network communication?",
        language="en",
        query_path=QueryPath.HYBRID,
        routing_confidence=0.85,
        matched_entities={"Component": ["R-ICU"]},
        top_k_sections=[
            {
                "section_id": "DDD-3.2",
                "title": "Network Architecture",
                "content": "The R-ICU is responsible for network communication using CAN and Ethernet protocols.",
                "document": "DDD",
                "doc_type": "detailed_design",
                "score": 0.89
            }
        ],
        extracted_entities={"Component": ["R-ICU"], "Protocol": ["CAN", "Ethernet"]},
        cypher_query="MATCH (c:Component {id: 'R-ICU'}) RETURN c",
        graph_results=[
            {
                "component_id": "R-ICU",
                "component_name": "Reduced Instrument Control Unit",
                "protocols": ["CAN", "Ethernet"],
                "related_requirements": ["FuncR_S110", "IntR_S102"]
            }
        ],
        final_answer="",
        citations=None,
        processing_time_ms=None,
        error=None
    )

    result = synthesize_response(state)

    print("=== Synthesized Response ===")
    print(result["final_answer"])
    print("\n=== Citations ===")
    print(json.dumps(result["citations"], indent=2))
