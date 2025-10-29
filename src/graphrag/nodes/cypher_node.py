"""
Cypher Query Node - Execute Cypher queries against Neo4j

Supports:
1. Template-based Cypher (Path A: Pure Cypher)
2. Contextual Cypher (Path B: Hybrid with extracted entities)
3. Dynamic query generation (Text2Cypher with LLM)
"""

import logging
import os
from typing import Dict, List, Any, Optional

from src.graphrag.state import GraphRAGState
from src.utils.neo4j_client import Neo4jClient
from src.query.cypher_templates import CypherTemplates
from src.query.text2cypher import Text2CypherGenerator

logger = logging.getLogger(__name__)

# Global Text2Cypher generator (initialize once)
_text2cypher_generator = None

def get_text2cypher_generator() -> Text2CypherGenerator:
    """Get or create Text2Cypher generator (singleton pattern)."""
    global _text2cypher_generator
    if _text2cypher_generator is None:
        _text2cypher_generator = Text2CypherGenerator()
    return _text2cypher_generator


def run_template_cypher(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Execute predefined Cypher template (Path A).

    Uses matched entities from router to select and execute appropriate template.

    Args:
        state: Current GraphRAGState with 'matched_entities' populated

    Returns:
        Updated state with 'cypher_query' and 'graph_results'
    """
    matched_entities = state.get("matched_entities", {})

    if not matched_entities:
        logger.warning("No matched entities for template Cypher")
        state["graph_results"] = []
        return state

    logger.info(f"Running template Cypher with entities: {matched_entities}")

    # Select template based on entities
    templates = CypherTemplates()
    cypher_query = None
    results = []

    try:
        # Priority: Requirement → Component → TestCase → Protocol
        # Handle both "Requirement"/"requirements", "Component"/"components", etc.
        requirement_key = next((k for k in matched_entities.keys() if k.lower() in ["requirement", "requirements"]), None)
        component_key = next((k for k in matched_entities.keys() if k.lower() in ["component", "components"]), None)
        testcase_key = next((k for k in matched_entities.keys() if k.lower() in ["testcase", "test_case", "test_cases"]), None)

        if requirement_key and matched_entities[requirement_key]:
            req_data = matched_entities[requirement_key][0]
            req_id = req_data if isinstance(req_data, str) else req_data.get("id")
            cypher_query = templates.get_requirement_traceability(req_id)
            logger.info(f"Using requirement traceability template for {req_id}")

        elif component_key and matched_entities[component_key]:
            comp_data = matched_entities[component_key][0]
            comp_id = comp_data if isinstance(comp_data, str) else comp_data.get("id")
            cypher_query = templates.get_component_requirements(comp_id)
            logger.info(f"Using component requirements template for {comp_id}")

        elif testcase_key and matched_entities[testcase_key]:
            tc_data = matched_entities[testcase_key][0]
            tc_id = tc_data if isinstance(tc_data, str) else tc_data.get("id")
            cypher_query = templates.get_test_case_details(tc_id)
            logger.info(f"Using test case details template for {tc_id}")

        else:
            logger.warning("No suitable template found for matched entities")
            state["graph_results"] = []
            return state

        # Execute query
        neo4j_client = Neo4jClient()
        results = neo4j_client.execute(cypher_query)
        neo4j_client.close()

        logger.info(f"Template Cypher returned {len(results)} results")

        # Update state
        state["cypher_query"] = cypher_query
        state["graph_results"] = results

    except Exception as e:
        logger.error(f"Template Cypher execution failed: {e}")
        state["error"] = f"Cypher execution error: {str(e)}"
        state["graph_results"] = []

    return state


def run_contextual_cypher(state: GraphRAGState) -> GraphRAGState:
    """
    LangGraph Node: Generate and execute contextual Cypher (Path B).

    Uses two approaches:
    1. Text2Cypher (LLM-based) - Tries first if enabled
    2. Pattern-based fallback - Uses _build_contextual_query()

    Args:
        state: Current GraphRAGState with 'extracted_entities' populated

    Returns:
        Updated state with 'cypher_query' and 'graph_results'
    """
    extracted_entities = state.get("extracted_entities", {})
    user_question = state["user_question"]
    language = state.get("language", "en")

    if not extracted_entities:
        logger.warning("No extracted entities for contextual Cypher")
        state["graph_results"] = []
        return state

    logger.info(f"Building contextual Cypher with entities: {extracted_entities}")

    # Try Text2Cypher first (if enabled)
    use_text2cypher = os.getenv("USE_TEXT2CYPHER", "true").lower() == "true"
    cypher_query = None
    query_method = "pattern"  # Track which method was used

    if use_text2cypher:
        try:
            logger.info("Attempting Text2Cypher generation")
            generator = get_text2cypher_generator()
            cypher_query, confidence = generator.generate(
                user_question=user_question,
                extracted_entities=extracted_entities,
                language=language
            )
            query_method = f"text2cypher (confidence={confidence:.2f})"
            logger.info(f"Text2Cypher generated query with confidence {confidence:.2f}")

            # If confidence is too low, fall back to pattern-based
            if confidence < 0.5:
                logger.warning(f"Text2Cypher confidence too low ({confidence:.2f}), using pattern fallback")
                cypher_query = None  # Will trigger fallback below

        except Exception as e:
            logger.warning(f"Text2Cypher failed: {e}, falling back to pattern-based")
            cypher_query = None

    # Fallback to pattern-based query
    if cypher_query is None:
        logger.info("Using pattern-based query generation")
        cypher_query = _build_contextual_query(user_question, extracted_entities)
        query_method = "pattern"

    try:
        # Execute query
        neo4j_client = Neo4jClient()
        results = neo4j_client.execute(cypher_query)
        neo4j_client.close()

        logger.info(f"Contextual Cypher returned {len(results)} results (method={query_method})")

        # Update state
        state["cypher_query"] = cypher_query
        state["graph_results"] = results
        state["query_generation_method"] = query_method  # Track method used

    except Exception as e:
        logger.error(f"Contextual Cypher execution failed: {e}")
        logger.error(f"Query was:\n{cypher_query}")
        state["error"] = f"Cypher execution error: {str(e)}"
        state["graph_results"] = []

    return state


def _build_contextual_query(question: str, entities: Dict[str, List[str]]) -> str:
    """
    Build a contextual Cypher query based on extracted entities.

    Intelligently selects patterns based on entity combinations:
    - Component + Requirement → Traceability
    - Component + Protocol → Communication architecture
    - Requirement + TestCase → Verification status
    - Component only → Component details + requirements

    Args:
        question: User's question (for intent detection)
        entities: Extracted entities by type

    Returns:
        Cypher query string
    """
    question_lower = question.lower()

    # Extract entity lists
    components = entities.get("Component", [])
    requirements = entities.get("Requirement", [])
    test_cases = entities.get("TestCase", [])
    protocols = entities.get("Protocol", [])

    # Pattern 1: Component + Protocol → Communication query
    if components and protocols:
        component_ids = ", ".join([f"'{c}'" for c in components])
        protocol_names = ", ".join([f"'{p}'" for p in protocols])

        return f"""
        MATCH (c:Component)
        WHERE c.id IN [{component_ids}]
        OPTIONAL MATCH (c)<-[:RELATES_TO]-(req:Requirement)-[:USES_PROTOCOL]->(p:Protocol)
        WHERE p.name IN [{protocol_names}]
        OPTIONAL MATCH (c)-[:MENTIONS]-(section:Section)
        WHERE section.content CONTAINS '{protocols[0]}'
        RETURN
            c.id AS component_id,
            c.name AS component_name,
            collect(DISTINCT p.name) AS protocols,
            collect(DISTINCT req.id) AS related_requirements,
            collect(DISTINCT {{section_title: section.title, content: section.content}})[..3] AS relevant_sections
        """

    # Pattern 2: Component + Requirement → Traceability
    if components and requirements:
        component_ids = ", ".join([f"'{c}'" for c in components])
        requirement_ids = ", ".join([f"'{r}'" for r in requirements])

        return f"""
        MATCH (c:Component)
        WHERE c.id IN [{component_ids}]
        MATCH (req:Requirement)
        WHERE req.id IN [{requirement_ids}]
        OPTIONAL MATCH (req)-[:RELATES_TO]->(c)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        RETURN
            c.id AS component_id,
            c.name AS component_name,
            collect(DISTINCT req.id) AS requirements,
            collect(DISTINCT req.statement) AS requirement_statements,
            collect(DISTINCT tc.id) AS test_cases
        """

    # Pattern 3: Requirement + TestCase → Verification
    if requirements and test_cases:
        requirement_ids = ", ".join([f"'{r}'" for r in requirements])
        tc_ids = ", ".join([f"'{t}'" for t in test_cases])

        return f"""
        MATCH (req:Requirement)
        WHERE req.id IN [{requirement_ids}]
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        WHERE tc.id IN [{tc_ids}]
        OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)
        RETURN
            req.id AS requirement_id,
            req.statement AS requirement_statement,
            req.verification AS verification_method,
            collect(DISTINCT tc.id) AS test_cases,
            collect(DISTINCT tc.description) AS test_descriptions,
            collect(DISTINCT c.id) AS components
        """

    # Pattern 4: Component only → Full component info
    if components:
        component_ids = ", ".join([f"'{c}'" for c in components])

        # Check if question is about testing/verification
        if any(keyword in question_lower for keyword in ['test', 'verify', 'validation', '테스트', '검증']):
            return f"""
            MATCH (c:Component)
            WHERE c.id IN [{component_ids}]
            OPTIONAL MATCH (c)<-[:RELATES_TO]-(req:Requirement)<-[:VERIFIES]-(tc:TestCase)
            RETURN
                c.id AS component_id,
                c.name AS component_name,
                collect(DISTINCT req.id) AS requirements,
                collect(DISTINCT tc.id) AS test_cases,
                count(DISTINCT tc) AS test_count
            """

        # General component query
        return f"""
        MATCH (c:Component)
        WHERE c.id IN [{component_ids}]
        OPTIONAL MATCH (c)<-[:RELATES_TO]-(req:Requirement)
        OPTIONAL MATCH (req)-[:USES_PROTOCOL]->(p:Protocol)
        OPTIONAL MATCH (c)-[:MENTIONS]-(section:Section)<-[:HAS_SECTION]-(doc:Document)
        RETURN
            c.id AS component_id,
            c.name AS component_name,
            collect(DISTINCT req.id) AS requirements,
            collect(DISTINCT req.type) AS requirement_types,
            collect(DISTINCT p.name) AS protocols,
            collect(DISTINCT {{doc: doc.title, section: section.title, content: section.content}})[..5] AS design_sections
        """

    # Pattern 5: Requirement only → Requirement details
    if requirements:
        requirement_ids = ", ".join([f"'{r}'" for r in requirements])

        return f"""
        MATCH (req:Requirement)
        WHERE req.id IN [{requirement_ids}]
        OPTIONAL MATCH (req)-[:DERIVES_FROM]->(parent:Requirement)
        OPTIONAL MATCH (child:Requirement)-[:DERIVES_FROM]->(req)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)
        RETURN
            req.id AS requirement_id,
            req.statement AS requirement_statement,
            req.type AS requirement_type,
            req.verification AS verification_method,
            collect(DISTINCT parent.id) AS parent_requirements,
            collect(DISTINCT child.id) AS child_requirements,
            collect(DISTINCT tc.id) AS test_cases,
            collect(DISTINCT c.id) AS components
        """

    # Pattern 6: TestCase only
    if test_cases:
        tc_ids = ", ".join([f"'{t}'" for t in test_cases])

        return f"""
        MATCH (tc:TestCase)
        WHERE tc.id IN [{tc_ids}]
        OPTIONAL MATCH (tc)-[:VERIFIES]->(req:Requirement)
        OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)
        RETURN
            tc.id AS test_case_id,
            tc.description AS description,
            tc.status AS status,
            collect(DISTINCT req.id) AS verified_requirements,
            collect(DISTINCT c.id) AS tested_components
        """

    # Fallback: Generic entity search
    logger.warning("No specific pattern matched, using generic query")
    return """
    MATCH (n)
    WHERE n.id IN $entity_ids
    RETURN n
    LIMIT 10
    """


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test contextual query building
    test_cases = [
        {
            "question": "What hardware handles network communication?",
            "entities": {
                "Component": ["R-ICU"],
                "Protocol": ["CAN", "Ethernet"]
            }
        },
        {
            "question": "Show traceability for FuncR_S110",
            "entities": {
                "Requirement": ["FuncR_S110"],
                "Component": ["R-ICU"]
            }
        },
        {
            "question": "What tests verify R-ICU?",
            "entities": {
                "Component": ["R-ICU"]
            }
        }
    ]

    for case in test_cases:
        print(f"\nQuestion: {case['question']}")
        print(f"Entities: {case['entities']}")
        print("Generated Query:")
        print(_build_contextual_query(case['question'], case['entities']))
        print("="*80)
