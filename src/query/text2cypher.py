"""
Text2Cypher - LLM-based Natural Language to Cypher Query Generation

Converts natural language questions to safe Cypher queries using:
1. Schema-aware prompting
2. Few-shot examples
3. Safety guardrails
4. Validation before execution

Usage:
    generator = Text2CypherGenerator()
    cypher = generator.generate(
        question="What requirements are related to R-ICU?",
        context={"entities": {"Component": ["R-ICU"]}}
    )
"""

import logging
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI

from src.utils.schema_inspector import SchemaInspector

logger = logging.getLogger(__name__)


class Text2CypherGenerator:
    """
    Generate safe Cypher queries from natural language using LLM.

    Features:
    - Schema-aware: Automatically includes database schema in prompt
    - Few-shot learning: Uses examples for better accuracy
    - Safety guardrails: Validates queries before execution
    - Entity-aware: Incorporates extracted entities for precision
    """

    def __init__(self):
        """Initialize Text2Cypher generator."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.schema_inspector = SchemaInspector()
        self.model = os.getenv("LLM_MODEL", "gpt-4o")

        # Get schema description once
        self.schema_description = self.schema_inspector.get_schema_description()

        logger.info("Text2Cypher generator initialized")

    def generate(
        self,
        user_question: str,
        extracted_entities: Optional[Dict[str, List[str]]] = None,
        language: str = "en"
    ) -> tuple[str, float]:
        """
        Generate Cypher query from natural language question.

        Args:
            user_question: User's natural language question
            extracted_entities: Optional dict of extracted entities by type
            language: Language code ('en' or 'ko')

        Returns:
            Tuple of (cypher_query, confidence_score)
        """
        logger.info(f"Generating Cypher for: {user_question}")

        # Build prompt
        prompt = self._build_prompt(user_question, extracted_entities, language)

        try:
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for deterministic queries
                max_tokens=1000
            )

            # Extract Cypher from response
            generated_text = response.choices[0].message.content.strip()
            cypher_query = self._extract_cypher(generated_text)

            logger.info(f"Generated Cypher ({len(cypher_query)} chars)")

            # Validate query
            is_valid, error = self.schema_inspector.validate_cypher(cypher_query)

            if not is_valid:
                logger.error(f"Generated query failed validation: {error}")
                logger.error(f"Query was:\n{cypher_query}")
                # Return fallback query
                return self._get_fallback_query(extracted_entities), 0.3

            # Estimate confidence based on entity match
            confidence = self._estimate_confidence(cypher_query, extracted_entities)

            return cypher_query, confidence

        except Exception as e:
            logger.error(f"Text2Cypher generation failed: {e}")
            # Return fallback query
            return self._get_fallback_query(extracted_entities), 0.2

    def _get_system_prompt(self) -> str:
        """Get system prompt for Text2Cypher."""
        return """You are an expert Neo4j Cypher query generator for the MOSAR spacecraft requirements database.

Your task is to convert natural language questions into accurate, safe Cypher queries.

IMPORTANT RULES:
1. **READ-ONLY**: Only generate MATCH and RETURN queries. Never use CREATE, DELETE, SET, REMOVE, or MERGE.
2. **USE SCHEMA**: Only use node labels, relationships, and properties that exist in the provided schema.
3. **BE PRECISE**: Match the user's intent exactly. Don't return unnecessary data.
4. **USE PARAMETERS**: When entities are provided, use them directly in the query.
5. **RETURN CLAUSE**: Always include a RETURN clause with meaningful data.
6. **LIMIT RESULTS**: Add LIMIT clause when returning large collections.
7. **FORMAT**: Return ONLY the Cypher query, no explanation or markdown.

OUTPUT FORMAT:
Return the Cypher query directly without ```cypher``` code blocks or explanations.
"""

    def _build_prompt(
        self,
        question: str,
        entities: Optional[Dict[str, List[str]]],
        language: str
    ) -> str:
        """
        Build complete prompt for LLM.

        Args:
            question: User question
            entities: Extracted entities
            language: Language code

        Returns:
            Formatted prompt string
        """
        prompt_parts = []

        # 1. Schema information
        prompt_parts.append("# Database Schema")
        prompt_parts.append(self.schema_description)
        prompt_parts.append("")

        # 2. Few-shot examples
        prompt_parts.append("# Example Queries")
        prompt_parts.extend(self._get_few_shot_examples(language))
        prompt_parts.append("")

        # 3. Extracted entities (if available)
        if entities:
            prompt_parts.append("# Extracted Entities")
            for entity_type, entity_list in entities.items():
                prompt_parts.append(f"- {entity_type}: {', '.join(entity_list)}")
            prompt_parts.append("")

        # 4. User question
        prompt_parts.append("# Question")
        prompt_parts.append(question)
        prompt_parts.append("")

        # 5. Instruction
        prompt_parts.append("# Task")
        prompt_parts.append("Generate a Cypher query that answers the question above.")
        prompt_parts.append("Use the extracted entities if provided.")
        prompt_parts.append("Return ONLY the Cypher query, no explanation.")

        return "\n".join(prompt_parts)

    def _get_few_shot_examples(self, language: str) -> List[str]:
        """
        Get few-shot examples for in-context learning.

        Args:
            language: Language code ('en' or 'ko')

        Returns:
            List of example strings
        """
        if language == "ko":
            return [
                "## Example 1",
                "질문: FuncR_S110의 추적성을 보여줘",
                "엔티티: Requirement: FuncR_S110",
                "Cypher:",
                "MATCH (req:Requirement {id: 'FuncR_S110'})",
                "OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)",
                "OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)",
                "RETURN req.id, req.statement, collect(tc.id) AS test_cases, collect(c.id) AS components",
                "",
                "## Example 2",
                "질문: R-ICU와 관련된 요구사항은?",
                "엔티티: Component: R-ICU",
                "Cypher:",
                "MATCH (c:Component {id: 'R-ICU'})<-[:RELATES_TO]-(req:Requirement)",
                "RETURN req.id, req.type, req.statement",
                "ORDER BY req.id",
                "",
                "## Example 3",
                "질문: 테스트되지 않은 요구사항은?",
                "엔티티: 없음",
                "Cypher:",
                "MATCH (req:Requirement)",
                "WHERE NOT EXISTS { (req)<-[:VERIFIES]-(:TestCase) }",
                "RETURN req.id, req.type, req.statement",
                "LIMIT 20",
            ]
        else:
            return [
                "## Example 1",
                "Question: Show traceability for FuncR_S110",
                "Entities: Requirement: FuncR_S110",
                "Cypher:",
                "MATCH (req:Requirement {id: 'FuncR_S110'})",
                "OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)",
                "OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)",
                "RETURN req.id, req.statement, collect(tc.id) AS test_cases, collect(c.id) AS components",
                "",
                "## Example 2",
                "Question: What requirements are related to R-ICU?",
                "Entities: Component: R-ICU",
                "Cypher:",
                "MATCH (c:Component {id: 'R-ICU'})<-[:RELATES_TO]-(req:Requirement)",
                "RETURN req.id, req.type, req.statement",
                "ORDER BY req.id",
                "",
                "## Example 3",
                "Question: Which requirements have no test cases?",
                "Entities: None",
                "Cypher:",
                "MATCH (req:Requirement)",
                "WHERE NOT EXISTS { (req)<-[:VERIFIES]-(:TestCase) }",
                "RETURN req.id, req.type, req.statement",
                "LIMIT 20",
                "",
                "## Example 4",
                "Question: What components use the CAN protocol?",
                "Entities: Protocol: CAN",
                "Cypher:",
                "MATCH (p:Protocol {name: 'CAN'})<-[:USES_PROTOCOL]-(req:Requirement)-[:RELATES_TO]->(c:Component)",
                "RETURN DISTINCT c.id, c.name",
                "",
                "## Example 5",
                "Question: Show the design sections that mention R-ICU",
                "Entities: Component: R-ICU",
                "Cypher:",
                "MATCH (c:Component {id: 'R-ICU'})<-[:MENTIONS]-(sec:Section)<-[:HAS_SECTION]-(doc:Document)",
                "RETURN doc.title, sec.title, sec.number",
                "ORDER BY doc.title, sec.number",
                "LIMIT 10",
            ]

    def _extract_cypher(self, llm_response: str) -> str:
        """
        Extract Cypher query from LLM response.

        Handles various response formats:
        - Pure Cypher
        - Markdown code blocks
        - With explanations

        Args:
            llm_response: Raw LLM response

        Returns:
            Clean Cypher query
        """
        # Remove markdown code blocks
        if "```cypher" in llm_response:
            start = llm_response.find("```cypher") + 9
            end = llm_response.find("```", start)
            cypher = llm_response[start:end].strip()
        elif "```" in llm_response:
            start = llm_response.find("```") + 3
            end = llm_response.find("```", start)
            cypher = llm_response[start:end].strip()
        else:
            # Assume entire response is Cypher
            cypher = llm_response.strip()

        # Remove leading/trailing whitespace and newlines
        cypher = "\n".join(line.strip() for line in cypher.split("\n") if line.strip())

        return cypher

    def _estimate_confidence(
        self,
        cypher_query: str,
        entities: Optional[Dict[str, List[str]]]
    ) -> float:
        """
        Estimate confidence score for generated query.

        Based on:
        - Entity incorporation (0.3)
        - Query complexity (0.3)
        - Schema alignment (0.4)

        Args:
            cypher_query: Generated Cypher query
            entities: Extracted entities

        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Base confidence

        # Check entity incorporation
        if entities:
            entity_count = sum(len(v) for v in entities.values())
            entities_in_query = 0

            for entity_list in entities.values():
                for entity in entity_list:
                    if entity in cypher_query:
                        entities_in_query += 1

            if entity_count > 0:
                entity_score = entities_in_query / entity_count
                confidence += 0.3 * entity_score

        # Check for OPTIONAL MATCH (better handling of missing data)
        if "OPTIONAL MATCH" in cypher_query.upper():
            confidence += 0.1

        # Check for LIMIT (prevents overwhelming results)
        if "LIMIT" in cypher_query.upper():
            confidence += 0.05

        # Check for ORDER BY (organized results)
        if "ORDER BY" in cypher_query.upper():
            confidence += 0.05

        # Cap at 1.0
        return min(confidence, 1.0)

    def _get_fallback_query(self, entities: Optional[Dict[str, List[str]]]) -> str:
        """
        Get fallback query when generation fails.

        Args:
            entities: Extracted entities (if any)

        Returns:
            Safe fallback Cypher query
        """
        if entities:
            # Try to build simple query from entities
            if "Requirement" in entities and entities["Requirement"]:
                req_id = entities["Requirement"][0]
                return f"""
                MATCH (req:Requirement {{id: '{req_id}'}})
                RETURN req.id, req.statement, req.type
                """

            elif "Component" in entities and entities["Component"]:
                comp_id = entities["Component"][0]
                return f"""
                MATCH (c:Component {{id: '{comp_id}'}})
                OPTIONAL MATCH (c)<-[:RELATES_TO]-(req:Requirement)
                RETURN c.id, c.name, collect(req.id) AS requirements
                """

        # Generic fallback
        return """
        MATCH (req:Requirement)
        RETURN req.id, req.type, req.statement
        LIMIT 10
        """

    def close(self):
        """Close resources."""
        if self.schema_inspector:
            self.schema_inspector.close()


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    generator = Text2CypherGenerator()

    # Test cases
    test_cases = [
        {
            "question": "Show all requirements verified by test cases",
            "entities": None,
            "language": "en"
        },
        {
            "question": "R-ICU를 변경하면 어떤 요구사항이 영향받나요?",
            "entities": {"Component": ["R-ICU"]},
            "language": "ko"
        },
        {
            "question": "What components communicate via CAN bus?",
            "entities": {"Protocol": ["CAN"]},
            "language": "en"
        },
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {i}")
        print(f"{'='*80}")
        print(f"Question: {case['question']}")
        print(f"Entities: {case['entities']}")
        print(f"Language: {case['language']}")

        cypher, confidence = generator.generate(
            case['question'],
            case['entities'],
            case['language']
        )

        print(f"\nGenerated Cypher (confidence={confidence:.2f}):")
        print(cypher)

    generator.close()
