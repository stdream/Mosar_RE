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
import json
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
    # CRITICAL: Check for empty graph results (hallucination bug fix)
    graph_results = context.get("graph_results", [])
    graph_is_empty = not graph_results or len(graph_results) == 0

    vector_results = context.get("vector_results", [])
    vector_is_empty = not vector_results or len(vector_results) == 0

    # If query_path is pure_cypher AND graph results are empty, return clear message
    # For hybrid path, allow fallback to vector results if graph is empty
    if query_path == "pure_cypher" and graph_is_empty:
        logger.warning(f"Empty graph results for query: {user_question}")

        # Extract entity information for error message
        matched_entities = context.get("matched_entities", {})
        entity_info = ""
        if matched_entities:
            entity_list = []
            for entity_type, entity_data in matched_entities.items():
                if isinstance(entity_data, dict) and 'id' in entity_data:
                    entity_list.append(f"{entity_type}: {entity_data['id']}")
                elif isinstance(entity_data, list):
                    entity_list.extend([f"{entity_type}: {e}" for e in entity_data])
                elif isinstance(entity_data, str):
                    entity_list.append(f"{entity_type}: {entity_data}")
            if entity_list:
                entity_info = ", ".join(entity_list)

        # Yield empty results message
        if language == "ko":
            empty_message = f"""데이터베이스에서 요청하신 정보를 찾을 수 없습니다.

**쿼리 정보**:
- 검색 엔티티: {entity_info if entity_info else '알 수 없음'}
- 실행된 Cypher 쿼리: 성공적으로 실행됨
- 반환된 결과: 0개

**가능한 원인**:
1. 요청하신 엔티티가 데이터베이스에 존재하지 않습니다
2. 엔티티는 존재하지만 관련 관계(RELATES_TO, VERIFIES, USES_PROTOCOL 등)가 생성되지 않았습니다
3. 데이터 ingestion 중 일부 관계가 누락되었을 수 있습니다

**도움말**:
- 엔티티 ID 형식을 확인해주세요 (예: FuncR_A101, R-ICU, CT-A-1)
- 다른 검색어로 시도해보세요
- 벡터 검색을 통해 문서에서 관련 내용을 찾아볼 수 있습니다"""
        else:
            empty_message = f"""No information found in the database for your query.

**Query Information**:
- Searched Entity: {entity_info if entity_info else 'Unknown'}
- Cypher Query: Successfully executed
- Results Returned: 0

**Possible Causes**:
1. The requested entity does not exist in the database
2. The entity exists but lacks relationships (RELATES_TO, VERIFIES, USES_PROTOCOL, etc.)
3. Some relationships may have been missed during data ingestion

**Suggestions**:
- Verify the entity ID format (e.g., FuncR_A101, R-ICU, CT-A-1)
- Try different search terms
- Use vector search to find related information in documents"""

        yield empty_message
        yield {"citations": []}  # Empty citations
        return  # Stop here, don't call LLM

    # For hybrid path, check if BOTH graph and vector results are empty
    if query_path == "hybrid" and graph_is_empty and vector_is_empty:
        logger.warning(f"Both graph and vector results are empty for query: {user_question}")

        if language == "ko":
            empty_message = """데이터베이스와 문서에서 관련 정보를 찾을 수 없습니다.

**시도한 검색**:
- 지식 그래프 쿼리: 결과 없음
- 문서 벡터 검색: 유사한 내용 없음

**제안**:
- 다른 검색어나 키워드로 시도해보세요
- 질문을 더 구체적으로 작성해보세요
- 존재하는 엔티티 ID를 확인하고 질문해보세요 (예: FuncR_A101, R-ICU)"""
        else:
            empty_message = """No relevant information found in database or documents.

**Search Attempted**:
- Knowledge graph query: No results
- Document vector search: No similar content

**Suggestions**:
- Try different keywords or search terms
- Make your question more specific
- Verify entity IDs exist and try again (e.g., FuncR_A101, R-ICU)"""

        yield empty_message
        yield {"citations": []}
        return

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("LLM_MODEL", "gpt-4o")

    # Build prompt (pass query_path for context-aware system prompt)
    system_prompt = _build_system_prompt(language, query_path)
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


def _build_system_prompt(language: str, query_path: Optional[str] = None) -> str:
    """Build system prompt for synthesis.

    Args:
        language: Language code (ko/en)
        query_path: Query path (pure_cypher, hybrid, pure_vector)
    """
    # Pure Vector path uses different instructions (document-based search)
    if query_path == "pure_vector":
        if language == "ko":
            return """당신은 MOSAR 우주선 시스템의 요구사항과 설계 문서 전문가입니다.

**답변 방식**:
- 제공된 문서 내용(Document Context)을 기반으로 답변하세요
- 문서에 명시된 내용을 요약하고 설명하세요
- 관련 섹션의 정보를 종합하여 포괄적인 답변을 제공하세요
- 문서에 없는 정보는 "문서에서 찾을 수 없습니다"라고 밝히세요

답변 규칙:
1. **정확성**: 문서에 명시된 내용만 사용
2. **종합**: 여러 문서 섹션의 정보를 통합하여 설명
3. **맥락**: 각 정보의 출처(문서명, 섹션)를 언급
4. **구조화**: 명확한 구조로 정리 (개요, 상세 내용, 요약)
5. **한글**: 자연스러운 한국어로 답변하세요"""
        else:
            return """You are an expert on MOSAR spacecraft system requirements and design documents.

**Answer Approach**:
- Base your answer on the provided Document Context
- Summarize and explain what is explicitly mentioned in the documents
- Synthesize information from multiple sections for comprehensive answers
- If information is not in the documents, state "This information is not found in the documents"

Answer Guidelines:
1. **Accuracy**: Use only what is explicitly stated in documents
2. **Synthesis**: Integrate information from multiple document sections
3. **Context**: Mention sources (document name, section) for each piece of information
4. **Structure**: Organize clearly (overview, details, summary)
5. **English**: Respond in clear, professional English"""

    # Pure Cypher / Hybrid paths use graph-based instructions
    if language == "ko":
        return """당신은 MOSAR 우주선 시스템의 요구사항과 설계 문서 전문가입니다.

**중요 제약사항**:
- 반드시 제공된 그래프 데이터베이스 결과만을 사용하여 답변하세요
- 그래프 결과에 없는 요구사항 ID, 테스트 케이스 ID, 컴포넌트 ID를 절대 생성하거나 추측하지 마세요
- 정보가 불충분하면 "데이터베이스에 해당 정보가 없습니다"라고 명확히 밝히세요
- 허위 정보를 생성하는 것은 엄격히 금지됩니다

답변 규칙:
1. **정확성**: 오직 "Graph Database Results"에 있는 정보만 사용
2. **ID 인용**: 그래프 결과에 명시된 ID만 인용 (req1, TC1 같은 임의 ID 생성 금지)
3. **완전성**: 모든 요구사항 ID를 빠짐없이 포함하세요 (일부만 선택하지 말 것)
4. **구조화**:
   - 주요 항목은 자세히 설명
   - 나머지는 카테고리별로 나열
   - bullet point 사용
5. **명확성**: 각 요구사항의 의미와 중요성을 설명하세요
6. **한글**: 자연스러운 한국어로 답변하세요"""
    else:
        return """You are an expert on MOSAR spacecraft system requirements and design documents.

**CRITICAL CONSTRAINTS**:
- Answer ONLY using the provided graph database results
- NEVER generate, fabricate, or guess requirement IDs, test case IDs, or component IDs not in the graph results
- If information is insufficient, clearly state "This information is not available in the database"
- Generating false information is strictly prohibited

Answer Guidelines:
1. **Accuracy**: Use ONLY information from "Graph Database Results"
2. **Citations**: Cite only IDs explicitly in graph results (never generate fake IDs like req1, TC1)
3. **Completeness**: Include ALL requirement IDs without omission (do not select only a few)
4. **Structure**:
   - Explain major items in detail
   - List remaining items by category
   - Use bullet points
5. **Clarity**: Explain the meaning and importance of each requirement
6. **English**: Respond in clear, professional English"""


def _build_user_prompt(
    question: str,
    context: Dict[str, Any],
    query_path: Optional[str]
) -> str:
    """Build user prompt with context."""
    prompt_parts = []

    # Question
    prompt_parts.append(f"# Question\n{question}\n")

    # Graph results (most important) - Use formatted version for special queries
    if context.get("graph_results"):
        results = context["graph_results"]

        # Check if this is a decomposition tree or other special format
        if len(results) == 1 and 'descendants' in results[0]:
            # Use formatted tree output
            prompt_parts.append("# Graph Database Results (Decomposition Tree)")
            formatted = _format_graph_results(results)
            prompt_parts.append(formatted)
        else:
            # Default format for regular queries
            prompt_parts.append("# Graph Database Results")
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

    # Task - with explicit structured template based on result count
    prompt_parts.append("# Task")
    prompt_parts.append("Answer the question based on the information above.")

    # Extract all requirement IDs from graph results for verification
    num_results = len(context.get("graph_results", []))
    if num_results > 0:
        # Collect all IDs by category
        all_ids_by_category = {}
        for record in context.get("graph_results", []):
            req_id = record.get("requirement_id")
            if req_id:
                # Extract category (e.g., FuncR, DesR, IntR, PerfR)
                category = req_id.split('_')[0] if '_' in req_id else "Other"
                if category not in all_ids_by_category:
                    all_ids_by_category[category] = []
                all_ids_by_category[category].append(req_id)

        # Build structured template
        if num_results <= 5:
            prompt_parts.append(f"\n**필수 답변 형식** (총 {num_results}개 결과):")
            prompt_parts.append("\n1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시")
            prompt_parts.append("2. 모든 요구사항을 자세히 설명")
        elif num_results <= 15:
            prompt_parts.append(f"\n**필수 답변 형식** (총 {num_results}개 결과):")
            prompt_parts.append("\n1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시")
            prompt_parts.append("2. 주요 요구사항 상세 설명 (5-7개)")
            prompt_parts.append("3. 전체 요구사항 목록 (카테고리별)")
        else:
            prompt_parts.append(f"\n**필수 답변 형식** (총 {num_results}개 결과):")
            prompt_parts.append("\n1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시")
            prompt_parts.append("2. 주요 요구사항 상세 설명 (7-10개)")
            prompt_parts.append("3. 전체 요구사항 목록 (카테고리별)")

        # Provide explicit ID list for verification
        if all_ids_by_category:
            prompt_parts.append(f"\n**검증용 전체 ID 목록** (반드시 모두 포함):")
            for category in sorted(all_ids_by_category.keys()):
                ids = all_ids_by_category[category]
                prompt_parts.append(f"- {category}: {len(ids)}개 - {', '.join(sorted(ids))}")

            prompt_parts.append(f"\n**합계 검증**: 모든 카테고리 개수를 합산하면 정확히 {num_results}개가 되어야 합니다.")

    prompt_parts.append("\n**중요**: 위의 전체 ID 목록에 있는 모든 요구사항을 빠짐없이 답변에 포함해야 합니다.")

    return "\n".join(prompt_parts)


def _format_graph_results(graph_results: List[Dict[str, Any]]) -> str:
    """
    Format graph query results as readable text.

    Special handling for:
    - Decomposition tree (parent + descendants)
    - Traceability queries
    - General results

    Args:
        graph_results: List of Neo4j query results

    Returns:
        Formatted string
    """
    if not graph_results:
        return "No graph results available."

    # Check if this is a decomposition tree result
    if len(graph_results) == 1 and 'descendants' in graph_results[0]:
        return _format_decomposition_tree(graph_results[0])

    # Default: Convert to JSON for structured display
    formatted = json.dumps(graph_results, indent=2, ensure_ascii=False)

    # Truncate if too long
    max_chars = 8000
    if len(formatted) > max_chars:
        formatted = formatted[:max_chars] + "\n... [truncated]"

    return formatted


def _format_decomposition_tree(result: Dict[str, Any]) -> str:
    """
    Format requirements decomposition tree for clear visualization.

    Args:
        result: Single decomposition tree result

    Returns:
        Formatted tree structure as string
    """
    parent_id = result.get('parent_id')
    parent_statement = result.get('parent_statement', '')
    parent_type = result.get('parent_type', '')
    parent_level = result.get('parent_level', 'System')
    descendants = result.get('descendants', [])

    # Group descendants by level
    level1 = [d for d in descendants if d.get('level') == 1]
    level2 = [d for d in descendants if d.get('level') == 2]

    output = f"""
요구사항 분해 구조 (Requirements Decomposition Tree)
=====================================================

📋 상위 요구사항 (Parent Requirement)
  ID: {parent_id}
  Type: {parent_type}
  Level: {parent_level}
  Statement: {parent_statement[:200]}{'...' if len(parent_statement) > 200 else ''}

└─ 하위 요구사항 ({len(level1)} Level-1 children, {len(level2)} Level-2 grandchildren)
"""

    # Level 1 children
    if level1:
        output += "\n   📍 Level 1 (Direct Children - Subsystem Level):\n"
        for i, child in enumerate(level1, 1):
            output += f"""
   {i}. {child.get('id')} ({child.get('type')})
      Statement: {child.get('statement', '')[:150]}{'...' if len(child.get('statement', '')) > 150 else ''}
      Verification: {child.get('verification', 'N/A')}
      Tests: {len(child.get('test_cases', []))} | Components: {len(child.get('components', []))}
"""

    # Level 2 grandchildren
    if level2:
        output += "\n   📍 Level 2 (Grandchildren - Component Level):\n"
        for i, gc in enumerate(level2, 1):
            test_info = f"{gc.get('test_count', 0)} tests: {gc.get('test_cases', [])}" if gc.get('test_count', 0) > 0 else "No tests"
            comp_info = f"{gc.get('component_count', 0)} components: {gc.get('components', [])}" if gc.get('component_count', 0) > 0 else "No components"

            output += f"""
   {i}. {gc.get('id')} ({gc.get('type')})
      Statement: {gc.get('statement', '')[:150]}{'...' if len(gc.get('statement', '')) > 150 else ''}
      Verification: {gc.get('verification', 'N/A')}
      {test_info}
      {comp_info}
"""

    # Summary statistics
    total_verified = sum(1 for d in descendants if d.get('test_count', 0) > 0)
    total_unverified = len(descendants) - total_verified

    output += f"""
📊 검증 상태 요약 (Verification Summary)
  - 총 하위 요구사항: {len(descendants)}개
  - 테스트 완료: {total_verified}개
  - 미검증: {total_unverified}개
  - 검증률: {(total_verified/len(descendants)*100) if descendants else 0:.1f}%
"""

    return output


def _extract_citations(context: Dict[str, Any]) -> List[str]:
    """Extract citation sources from context.

    IMPORTANT: Extract ALL citations from graph results to ensure completeness.
    """
    citations = []

    # From graph results - include ALL results (no limit)
    if context.get("graph_results"):
        for record in context["graph_results"]:  # All records, not just [:10]
            # Extract IDs
            for key, value in record.items():
                if 'id' in key.lower() and value:
                    if isinstance(value, str):
                        citations.append(value)
                    elif isinstance(value, list):
                        citations.extend([str(v) for v in value if v])

    # From vector results - use document name + section title for readability
    if context.get("vector_results"):
        for section in context["vector_results"][:5]:
            # Use document name and section title instead of technical section_id
            doc_name = section.get("document", "Unknown Document")
            doc_type = section.get("doc_type", "")
            section_title = section.get("title", "Untitled Section")

            # Format: "Document Type: Section Title" or "Document Name: Section Title"
            if doc_type:
                citation = f"{doc_type}: {section_title}"
            else:
                citation = f"{doc_name}: {section_title}"

            citations.append(citation)

    # Deduplicate but don't limit
    citations = list(dict.fromkeys(citations))  # Unique, no max limit

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
