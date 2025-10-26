"""
Query Router - Adaptive routing for GraphRAG queries

Determines the optimal query path based on entity detection:
- Path A: Pure Cypher (high confidence entity match)
- Path B: Hybrid (moderate confidence, needs vector + NER)
- Path C: Pure Vector (no entity match, exploratory)
"""

import re
from typing import Dict, List, Tuple, Optional
from enum import Enum
import logging

from src.utils.entity_resolver import EntityResolver

logger = logging.getLogger(__name__)


class QueryPath(str, Enum):
    """Query routing paths"""
    PURE_CYPHER = "pure_cypher"
    HYBRID = "hybrid"
    PURE_VECTOR = "pure_vector"


class QueryRouter:
    """
    Routes user queries to the optimal execution path based on entity detection.

    Uses Entity Dictionary for fast entity lookup and confidence scoring.
    """

    def __init__(self, entity_dict_path: str = "data/entities/mosar_entities.json"):
        """
        Initialize query router.

        Args:
            entity_dict_path: Path to Entity Dictionary JSON (not used, kept for API compatibility)
        """
        self.entity_resolver = EntityResolver()

        # Confidence thresholds
        self.HIGH_CONFIDENCE_THRESHOLD = 0.9  # Path A: Pure Cypher
        self.MODERATE_CONFIDENCE_THRESHOLD = 0.6  # Path B: Hybrid
        # Below moderate → Path C: Pure Vector

        # Known requirement ID patterns
        self.req_pattern = re.compile(r'\b(FuncR|SafR|PerfR|IntR)_[A-Z]\d{3}\b', re.IGNORECASE)

        # Known component ID patterns
        self.component_pattern = re.compile(r'\b(R-ICU|WM|SM|OBC|cPDU|HOTDOCK)\b', re.IGNORECASE)

        # Known test case patterns
        self.testcase_pattern = re.compile(r'\b(CT-[A-Z]-\d+|IT\d+|S\d+)\b', re.IGNORECASE)

    def route(self, user_question: str) -> Tuple[QueryPath, Dict]:
        """
        Determine optimal query path for the user's question.

        Args:
            user_question: User's natural language question

        Returns:
            (query_path, routing_info) where routing_info contains:
                - path: QueryPath enum
                - confidence: 0.0-1.0
                - matched_entities: Dict of detected entities
                - reasoning: str explanation
        """
        logger.info(f"Routing query: {user_question[:100]}...")

        # Step 1: Check for explicit entity IDs (highest confidence)
        explicit_entities = self._detect_explicit_entities(user_question)
        if explicit_entities:
            return self._route_to_pure_cypher(explicit_entities)

        # Step 2: Use Entity Dictionary for fuzzy matching
        resolved_entities = self.entity_resolver.resolve_entities_in_text(user_question)

        # Calculate overall confidence
        confidence = self._calculate_confidence(resolved_entities)

        # Step 3: Route based on confidence
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            return self._route_to_pure_cypher(resolved_entities)
        elif confidence >= self.MODERATE_CONFIDENCE_THRESHOLD:
            return self._route_to_hybrid(resolved_entities, confidence)
        else:
            return self._route_to_pure_vector(confidence)

    def _detect_explicit_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Detect explicit entity IDs using regex patterns.

        Returns:
            Dict with keys: 'requirements', 'components', 'test_cases'
        """
        entities = {
            'requirements': self.req_pattern.findall(text),
            'components': self.component_pattern.findall(text),
            'test_cases': self.testcase_pattern.findall(text)
        }

        # Remove empty lists
        entities = {k: v for k, v in entities.items() if v}

        if entities:
            logger.info(f"Detected explicit entities: {entities}")

        return entities

    def _calculate_confidence(self, resolved_entities: Dict) -> float:
        """
        Calculate overall confidence score from resolved entities.

        Args:
            resolved_entities: Output from EntityResolver.resolve_entities_in_text()

        Returns:
            Confidence score 0.0-1.0
        """
        if not resolved_entities:
            return 0.0

        # Extract confidence scores from resolved entities
        confidences = []

        for entity_type, entities in resolved_entities.items():
            for entity in entities:
                if isinstance(entity, dict) and 'confidence' in entity:
                    confidences.append(entity['confidence'])

        if not confidences:
            # If entities found but no confidence scores, assume moderate confidence
            return 0.7

        # Use max confidence (most confident entity match)
        return max(confidences)

    def _route_to_pure_cypher(self, entities: Dict) -> Tuple[QueryPath, Dict]:
        """Route to Path A: Pure Cypher with known entities."""
        routing_info = {
            'path': QueryPath.PURE_CYPHER,
            'confidence': 1.0,
            'matched_entities': entities,
            'reasoning': f"High confidence entity match detected. Using template-based Cypher query. Entities: {entities}"
        }

        logger.info(f"→ Path A (Pure Cypher): {routing_info['reasoning']}")
        return QueryPath.PURE_CYPHER, routing_info

    def _route_to_hybrid(self, entities: Dict, confidence: float) -> Tuple[QueryPath, Dict]:
        """Route to Path B: Hybrid workflow (Vector + NER + Cypher)."""
        routing_info = {
            'path': QueryPath.HYBRID,
            'confidence': confidence,
            'matched_entities': entities,
            'reasoning': f"Moderate confidence (conf={confidence:.2f}). Using hybrid workflow with vector search + NER + contextual Cypher."
        }

        logger.info(f"→ Path B (Hybrid): {routing_info['reasoning']}")
        return QueryPath.HYBRID, routing_info

    def _route_to_pure_vector(self, confidence: float) -> Tuple[QueryPath, Dict]:
        """Route to Path C: Pure Vector search (exploratory)."""
        routing_info = {
            'path': QueryPath.PURE_VECTOR,
            'confidence': confidence,
            'matched_entities': {},
            'reasoning': f"Low confidence (conf={confidence:.2f}). No clear entities detected. Using pure vector search for exploratory retrieval."
        }

        logger.info(f"→ Path C (Pure Vector): {routing_info['reasoning']}")
        return QueryPath.PURE_VECTOR, routing_info


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    router = QueryRouter()

    # Test queries
    test_queries = [
        "Show all requirements verified by R-ICU",  # Path A (explicit component ID)
        "FuncR_S110의 traceability를 보여줘",  # Path A (explicit requirement ID)
        "어떤 하드웨어가 네트워크 통신을 담당하나요?",  # Path B (domain term: 네트워크 통신)
        "What hardware handles network communication?",  # Path B (domain term: network communication)
        "What are the main challenges in orbital assembly?",  # Path C (exploratory)
        "CT-A-1 테스트는 어떤 요구사항을 검증하나요?",  # Path A (explicit test case ID)
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        path, info = router.route(query)
        print(f"  → Path: {path.value}")
        print(f"  → Confidence: {info['confidence']:.2f}")
        print(f"  → Entities: {info['matched_entities']}")
        print(f"  → Reasoning: {info['reasoning']}")
