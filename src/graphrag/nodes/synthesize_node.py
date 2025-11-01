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
    matched_entities = state.get("matched_entities", {})

    # CRITICAL: Check if graph results are empty (fix for hallucination bug)
    graph_is_empty = not graph_results or len(graph_results) == 0

    if graph_is_empty:
        # Graph query returned 0 results - provide clear empty results message
        logger.warning(f"Empty graph results for query: {user_question}")

        # Extract entity information for better error message
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

        if language == "ko":
            answer = f"""데이터베이스에서 요청하신 정보를 찾을 수 없습니다.

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
            answer = f"""No information found in the database for your query.

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

        return {
            "answer": answer,
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
        system_prompt = """당신은 MOSAR (Modular Spacecraft Assembly and Reconfiguration) 시스템 전문가입니다.

**중요 제약사항**:
- 반드시 제공된 그래프 데이터베이스 결과만을 사용하여 답변하세요
- 그래프 결과에 없는 요구사항 ID, 테스트 케이스 ID, 컴포넌트 ID를 절대 생성하거나 추측하지 마세요
- 정보가 불충분하면 "데이터베이스에 해당 정보가 없습니다"라고 명확히 밝히세요
- 허위 정보를 생성하는 것은 엄격히 금지됩니다"""
        instruction = """아래 질문에 대해 제공된 데이터를 바탕으로 답변해주세요.

**답변 요구사항**:
1. **오직 "Graph Query Results"에 있는 정보만 사용**
2. 그래프 결과에 명시된 ID만 인용 (RQ-001 같은 임의의 ID 생성 금지)
3. **모든 요구사항 ID를 빠짐없이 포함** (일부만 선택하지 말 것)
4. 주요 항목은 자세히 설명하고, 나머지는 카테고리별로 나열
5. 정보가 부족하면 "데이터베이스에 추가 정보 없음"이라고 명시
6. 출처를 명확히 표시 (실제로 존재하는 문서 섹션만)
7. 마크다운 형식으로 작성 (리스트, 테이블 등 활용)

**절대 금지**:
- 그래프 결과에 없는 요구사항/테스트 케이스 ID 생성
- 추측이나 일반적인 지식으로 답변 작성
- 플레이스홀더나 예시 데이터 생성
"""
    else:
        system_prompt = """You are an expert in MOSAR (Modular Spacecraft Assembly and Reconfiguration) system.

**CRITICAL CONSTRAINTS**:
- Answer ONLY using the provided graph database results
- NEVER generate, fabricate, or guess requirement IDs, test case IDs, or component IDs not in the graph results
- If information is insufficient, clearly state "This information is not available in the database"
- Generating false information is strictly prohibited"""
        instruction = """Answer the question below based on the provided data.

**Answer Requirements**:
1. **Use ONLY information from "Graph Query Results"**
2. Cite only IDs explicitly present in graph results (never generate fake IDs like RQ-001)
3. **Include ALL requirement IDs without omission** (do not select only a few)
4. Explain major items in detail, list remaining items by category
5. If information is missing, state "Additional information not available in database"
6. Cite sources clearly (only actual document sections that exist)
7. Use markdown formatting (lists, tables, etc.)

**STRICTLY PROHIBITED**:
- Generating requirement/test case IDs not in graph results
- Answering based on guesses or general knowledge
- Creating placeholder or example data
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
"""

    # Add structured template for multiple results
    if graph_results and len(graph_results) > 0:
        # Collect all IDs by category
        all_ids_by_category = {}
        for record in graph_results:
            req_id = record.get("requirement_id")
            if req_id:
                # Extract category (e.g., FuncR, DesR, IntR, PerfR)
                category = req_id.split('_')[0] if '_' in req_id else "Other"
                if category not in all_ids_by_category:
                    all_ids_by_category[category] = []
                all_ids_by_category[category].append(req_id)

        if all_ids_by_category:
            num_results = len(graph_results)
            prompt += f"\n\n**필수 답변 형식** (총 {num_results}개 결과):\n"
            if num_results <= 5:
                prompt += "1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시\n"
                prompt += "2. 모든 요구사항을 자세히 설명\n"
            elif num_results <= 15:
                prompt += "1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시\n"
                prompt += "2. 주요 요구사항 상세 설명 (5-7개)\n"
                prompt += "3. 전체 요구사항 목록 (카테고리별)\n"
            else:
                prompt += "1. 개요: 총 몇 개의 요구사항이 영향을 받는지 명시\n"
                prompt += "2. 주요 요구사항 상세 설명 (7-10개)\n"
                prompt += "3. 전체 요구사항 목록 (카테고리별)\n"

            prompt += "\n**검증용 전체 ID 목록** (반드시 모두 포함):\n"
            for category in sorted(all_ids_by_category.keys()):
                ids = all_ids_by_category[category]
                prompt += f"- {category}: {len(ids)}개 - {', '.join(sorted(ids))}\n"

            prompt += f"\n**합계 검증**: 모든 카테고리 개수를 합산하면 정확히 {num_results}개가 되어야 합니다.\n"
            prompt += "\n**중요**: 위의 전체 ID 목록에 있는 모든 요구사항을 빠짐없이 답변에 포함해야 합니다.\n"

    prompt += "\nProvide a comprehensive answer:\n"

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


def _extract_citations(graph_results: List[Dict], sections: List[Dict]) -> List[Dict[str, str]]:
    """
    Extract citation information from results.

    IMPORTANT: Extract ALL citations from graph results to ensure completeness.

    Args:
        graph_results: Graph query results
        sections: Vector search sections

    Returns:
        List of citation dicts
    """
    citations = []

    # Citations from graph results - include ALL results (no limit)
    for result in graph_results:  # All results, not just [:5]
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
