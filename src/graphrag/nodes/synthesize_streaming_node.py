"""
Streaming Response Synthesis Node - Generate answers with real-time streaming

Provides streaming responses for better UX:
- Real-time token-by-token display
- Early user engagement (don't wait for full response)
- Chunked processing for long answers

Usage:
    # In LangGraph workflow
    workflow.add_node("synthesize_streaming", synthesize_response_streaming)

    # Or standalone
    for chunk in stream_synthesis(question, context):
        print(chunk, end='', flush=True)
"""

import logging
import os
from typing import Dict, List, Any, Optional, Generator
from openai import OpenAI

from src.graphrag.state import GraphRAGState

logger = logging.getLogger(__name__)


def synthesize_response_streaming(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Synthesize final answer with streaming (non-blocking).

    NOTE: This node collects the full streamed response for LangGraph compatibility.
    For actual streaming to UI, use stream_synthesis() directly.

    Args:
        state: Current GraphRAGState

    Returns:
        Updated state with 'final_answer' and 'citations'
    """
    user_question = state["user_question"]
    language = state.get("language", "en")
    query_path = state.get("query_path")

    # Gather context
    context = _gather_context(state)

    logger.info(f"Synthesizing streaming response (language={language})")

    try:
        # Stream response and collect
        full_answer = ""
        citations = []

        for chunk in stream_synthesis(user_question, context, language, query_path):
            if isinstance(chunk, dict):
                # Metadata chunk (citations, etc.)
                if "citations" in chunk:
                    citations = chunk["citations"]
            else:
                # Text chunk
                full_answer += chunk

        # Update state
        state["final_answer"] = full_answer.strip()
        state["citations"] = citations

        logger.info(f"Streamed {len(full_answer)} characters")

    except Exception as e:
        logger.error(f"Streaming synthesis failed: {e}")
        state["final_answer"] = f"Error generating response: {str(e)}"
        state["citations"] = []
        state["error"] = str(e)

    return state


def stream_synthesis(
    user_question: str,
    context: Dict[str, Any],
    language: str = "en",
    query_path: Optional[str] = None
) -> Generator[str, None, None]:
    """
    Stream answer synthesis chunk by chunk.

    Args:
        user_question: User's question
        context: Context dict with vector_results, graph_results, etc.
        language: Language code
        query_path: Query execution path

    Yields:
        String chunks (text) or dict chunks (metadata)
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("LLM_MODEL", "gpt-4o")

    # Build prompt
    system_prompt = _build_system_prompt(language)
    user_prompt = _build_user_prompt(user_question, context, query_path)

    try:
        # Stream from OpenAI
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000,
            stream=True  # Enable streaming
        )

        # Yield chunks as they arrive
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                yield content

        # Yield citations as metadata (after streaming completes)
        citations = _extract_citations(context)
        if citations:
            yield {"citations": citations}

    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        yield f"\n\n[Error: {str(e)}]"


def _gather_context(state: GraphRAGState) -> Dict[str, Any]:
    """
    Gather all context for synthesis.

    Args:
        state: Current state

    Returns:
        Context dict
    """
    return {
        "vector_results": state.get("top_k_sections", []),
        "graph_results": state.get("graph_results", []),
        "cypher_query": state.get("cypher_query"),
        "extracted_entities": state.get("extracted_entities", {}),
        "matched_entities": state.get("matched_entities", {}),
        "query_generation_method": state.get("query_generation_method")
    }


def _build_system_prompt(language: str) -> str:
    """Build system prompt for synthesis."""
    if language == "ko":
        return """당신은 MOSAR 우주선 시스템의 요구사항과 설계 문서 전문가입니다.

주어진 정보를 바탕으로 정확하고 명확하게 답변하세요.

답변 규칙:
1. **정확성**: 제공된 데이터만 사용하고, 추측하지 마세요
2. **구조화**: 복잡한 답변은 bullet point로 정리하세요
3. **인용**: 요구사항 ID, 컴포넌트 ID 등을 명시하세요
4. **간결함**: 핵심만 전달하고, 불필요한 설명은 피하세요
5. **한글**: 자연스러운 한국어로 답변하세요"""
    else:
        return """You are an expert on MOSAR spacecraft system requirements and design documents.

Answer questions accurately and clearly based on the provided information.

Answer Guidelines:
1. **Accuracy**: Use only the provided data, don't speculate
2. **Structure**: Organize complex answers with bullet points
3. **Citations**: Mention requirement IDs, component IDs, etc.
4. **Brevity**: Focus on key information, avoid unnecessary details
5. **English**: Respond in clear, professional English"""


def _build_user_prompt(
    question: str,
    context: Dict[str, Any],
    query_path: Optional[str]
) -> str:
    """Build user prompt with context."""
    prompt_parts = []

    # Question
    prompt_parts.append(f"# Question\n{question}\n")

    # Graph results (most important)
    if context.get("graph_results"):
        prompt_parts.append("# Graph Database Results")
        results = context["graph_results"]
        if len(results) > 20:
            prompt_parts.append(f"(Showing first 20 of {len(results)} results)\n")
            results = results[:20]

        for i, record in enumerate(results, 1):
            prompt_parts.append(f"\n## Result {i}")
            for key, value in record.items():
                if value is not None:
                    # Format value nicely
                    if isinstance(value, list):
                        value_str = f"[{len(value)} items]" if len(value) > 5 else str(value)
                    else:
                        value_str = str(value)[:200]  # Truncate long strings
                    prompt_parts.append(f"- {key}: {value_str}")
        prompt_parts.append("")

    # Vector results (supplementary)
    if context.get("vector_results"):
        prompt_parts.append("# Document Context")
        for section in context["vector_results"][:3]:  # Top 3 only
            title = section.get("title", "Unknown")
            content_preview = section.get("content", "")[:300]
            prompt_parts.append(f"\n## {title}")
            prompt_parts.append(content_preview)
        prompt_parts.append("")

    # Cypher query (for transparency)
    if context.get("cypher_query"):
        prompt_parts.append("# Query Used")
        prompt_parts.append(f"```cypher\n{context['cypher_query']}\n```\n")

    # Task
    prompt_parts.append("# Task")
    prompt_parts.append("Answer the question based on the information above.")
    prompt_parts.append("Be specific and cite relevant IDs (requirements, components, test cases).")

    return "\n".join(prompt_parts)


def _extract_citations(context: Dict[str, Any]) -> List[str]:
    """Extract citation sources from context."""
    citations = []

    # From graph results
    if context.get("graph_results"):
        for record in context["graph_results"][:10]:  # Top 10
            # Extract IDs
            for key, value in record.items():
                if 'id' in key.lower() and value:
                    if isinstance(value, str):
                        citations.append(value)
                    elif isinstance(value, list):
                        citations.extend([str(v) for v in value if v])

    # From vector results
    if context.get("vector_results"):
        for section in context["vector_results"][:5]:
            section_id = section.get("id") or section.get("section_id")
            if section_id:
                citations.append(str(section_id))

    # Deduplicate and limit
    citations = list(dict.fromkeys(citations))[:20]  # Unique, max 20

    return citations


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Mock context
    test_context = {
        "graph_results": [
            {
                "requirement_id": "FuncR_S110",
                "requirement_statement": "The system shall support real-time communication",
                "components": ["R-ICU", "OBC"],
                "test_cases": ["TC_NET_001"]
            },
            {
                "requirement_id": "FuncR_S111",
                "requirement_statement": "The system shall use CAN bus protocol",
                "components": ["R-ICU"],
                "test_cases": []
            }
        ],
        "vector_results": [
            {
                "id": "DDD-4.1",
                "title": "Network Architecture",
                "content": "The R-ICU implements CAN bus communication at 1 Mbps..."
            }
        ],
        "cypher_query": "MATCH (c:Component {id: 'R-ICU'})<-[:RELATES_TO]-(req:Requirement) RETURN req"
    }

    print("="*80)
    print("Streaming Response Test")
    print("="*80)

    question = "What requirements are related to R-ICU?"

    print(f"\nQuestion: {question}\n")
    print("Streaming Answer:")
    print("-"*80)

    for chunk in stream_synthesis(question, test_context, language="en"):
        if isinstance(chunk, dict):
            print(f"\n\n[Citations: {chunk.get('citations', [])}]")
        else:
            print(chunk, end='', flush=True)

    print("\n" + "="*80)
