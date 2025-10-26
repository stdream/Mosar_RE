"""
NER (Named Entity Recognition) Node - Extract MOSAR entities from context

Uses OpenAI GPT-4 to extract domain-specific entities from retrieved text.
Combines with Entity Dictionary for validation and confidence scoring.
"""

import logging
import json
import re
import os
from typing import Dict, List, Any
from openai import OpenAI

from src.graphrag.state import GraphRAGState
from src.utils.entity_resolver import EntityResolver

logger = logging.getLogger(__name__)


def extract_entities_from_context(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Extract MOSAR entities from vector search results.

    Uses GPT-4 to identify:
    - Component IDs (e.g., R-ICU, WM, SM)
    - Requirement IDs (e.g., FuncR_S110)
    - Test Case IDs (e.g., CT-A-1)
    - Protocols (e.g., CAN, Ethernet)
    - Scenarios (e.g., S1, S2)

    Args:
        state: Current GraphRAGState with 'top_k_sections' populated

    Returns:
        Updated state with 'extracted_entities' populated
    """
    top_k_sections = state.get("top_k_sections", [])

    if not top_k_sections:
        logger.warning("No sections available for NER extraction")
        state["extracted_entities"] = {}
        return state

    logger.info(f"Extracting entities from {len(top_k_sections)} sections...")

    # Combine section content
    combined_context = "\n\n".join([
        f"[Section: {sec['title']}]\n{sec['content']}"
        for sec in top_k_sections[:5]  # Use top 5 for context window
    ])

    # Truncate to avoid token limit (max ~4000 tokens)
    max_chars = 16000
    if len(combined_context) > max_chars:
        combined_context = combined_context[:max_chars] + "\n... [truncated]"
        logger.info(f"Context truncated to {max_chars} chars")

    # Extract entities using GPT-4
    extracted_entities = _extract_entities_with_gpt4(
        context=combined_context,
        user_question=state["user_question"]
    )

    # Validate with Entity Dictionary
    validated_entities = _validate_with_entity_dict(extracted_entities)

    logger.info(f"Extracted entities: {validated_entities}")

    # Update state
    state["extracted_entities"] = validated_entities

    return state


def _extract_entities_with_gpt4(context: str, user_question: str) -> Dict[str, List[str]]:
    """
    Use GPT-4 to extract MOSAR entities from context.

    Args:
        context: Combined section content
        user_question: Original user question (for context)

    Returns:
        Dict with entity types as keys
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""You are an expert in MOSAR (Modular Spacecraft Assembly and Reconfiguration) system.

Extract all relevant entities from the provided context that would help answer the user's question.

**Entity Types to Extract**:
1. **Component** - Hardware/software components (e.g., R-ICU, WM, SM, OBC, cPDU, HOTDOCK)
2. **Requirement** - Requirement IDs (e.g., FuncR_S110, SafR_A201, PerfR_B305, IntR_S102)
3. **TestCase** - Test case IDs (e.g., CT-A-1, IT1, S1)
4. **Protocol** - Communication protocols (e.g., CAN, Ethernet, SpaceWire, I2C)
5. **Scenario** - Demonstration scenarios (e.g., S1, S2, S3)

**User Question**:
{user_question}

**Context**:
{context}

**Instructions**:
- Extract only entities that appear in the context
- Use exact IDs when available (e.g., "R-ICU", not "Reduced ICU")
- For requirements, use full ID format (e.g., "FuncR_S110")
- Return entities as a JSON object with entity types as keys and lists of entity IDs as values
- If no entities of a type are found, omit that key
- Be precise - only extract entities directly relevant to answering the question

**Output Format** (JSON only, no explanation):
{{
  "Component": ["R-ICU", "WM"],
  "Requirement": ["FuncR_S110"],
  "Protocol": ["CAN", "Ethernet"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a technical entity extraction assistant. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,  # Deterministic extraction
            max_tokens=1000
        )

        # Parse JSON response
        response_text = response.choices[0].message.content.strip()

        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        elif response_text.startswith('```'):
            # Remove code block markers
            response_text = re.sub(r'```\w*\s*|\s*```', '', response_text).strip()

        entities = json.loads(response_text)

        logger.info(f"GPT-4 extracted entities: {entities}")

        return entities

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse GPT-4 response as JSON: {e}")
        logger.error(f"Response: {response_text}")
        return {}

    except Exception as e:
        logger.error(f"Entity extraction with GPT-4 failed: {e}")
        return {}


def _validate_with_entity_dict(entities: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Validate extracted entities against Entity Dictionary.

    Args:
        entities: Extracted entities from GPT-4

    Returns:
        Validated entities with standardized IDs
    """
    entity_resolver = EntityResolver()
    validated = {}

    for entity_type, entity_list in entities.items():
        validated_list = []

        for entity_id in entity_list:
            # Try exact match first
            resolved = entity_resolver.resolve_exact(entity_id, entity_type.lower())

            if resolved:
                validated_list.append(resolved["id"])
                logger.debug(f"Validated {entity_type}: {entity_id} → {resolved['id']}")
            else:
                # Try fuzzy match
                resolved = entity_resolver.resolve_fuzzy(entity_id, entity_type.lower())
                if resolved and resolved["confidence"] > 0.8:
                    validated_list.append(resolved["id"])
                    logger.debug(f"Fuzzy matched {entity_type}: {entity_id} → {resolved['id']} (conf={resolved['confidence']:.2f})")
                else:
                    # Keep original if no match
                    validated_list.append(entity_id)
                    logger.debug(f"No validation for {entity_type}: {entity_id} (keeping original)")

        if validated_list:
            validated[entity_type] = list(set(validated_list))  # Remove duplicates

    return validated


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Mock state with sample sections
    state = GraphRAGState(
        user_question="What hardware handles network communication?",
        language="en",
        query_path=None,
        routing_confidence=0.0,
        matched_entities={},
        top_k_sections=[
            {
                "section_id": "DDD-3.2",
                "title": "Network Architecture",
                "content": "The R-ICU (Reduced Instrument Control Unit) is responsible for network communication. It uses CAN bus at 1 Mbps for real-time communication and Ethernet at 100 Mbps for high-bandwidth data transfer. The component implements FuncR_S110 requirement for network redundancy.",
                "document": "DDD",
                "doc_type": "detailed_design",
                "score": 0.85
            },
            {
                "section_id": "PDD-2.1",
                "title": "Service Module Components",
                "content": "The Service Module (SM) contains the R-ICU, cPDU (Power Distribution Unit), and HOTDOCK interface. The WM (Walking Manipulator) connects via CAN bus.",
                "document": "PDD",
                "doc_type": "preliminary_design",
                "score": 0.78
            }
        ],
        extracted_entities=None,
        cypher_query=None,
        graph_results=None,
        final_answer="",
        citations=None,
        processing_time_ms=None,
        error=None
    )

    result_state = extract_entities_from_context(state)

    print("Extracted Entities:")
    print(json.dumps(result_state["extracted_entities"], indent=2))
