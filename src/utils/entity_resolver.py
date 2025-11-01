"""Entity resolution using dictionary lookup and fuzzy matching."""
import json
import sys
import re
from pathlib import Path
from typing import Dict, List
from fuzzywuzzy import process
import logging

logger = logging.getLogger(__name__)


class EntityResolver:
    """Resolve user input to canonical entity IDs."""

    def __init__(self):
        """Load entity dictionary."""
        dict_path = Path(__file__).parents[2] / "data/entities/mosar_entities.json"

        if not dict_path.exists():
            logger.warning(f"Entity dictionary not found: {dict_path}")
            self.entities = {}
            self.flat_dict = {}
            return

        with open(dict_path, 'r', encoding='utf-8') as f:
            self.entities = json.load(f)

        # Flatten for fast lookup
        self.flat_dict = {}
        for category, mappings in self.entities.items():
            for phrase, entity_info in mappings.items():
                self.flat_dict[phrase.lower()] = {
                    **entity_info,
                    "category": category
                }

        logger.info(f"Loaded {len(self.flat_dict)} entity mappings from dictionary")

    def resolve(self, text: str, threshold: int = 85) -> Dict[str, List[Dict]]:
        """
        Resolve entities in text.

        Args:
            text: Input text (question or chunk)
            threshold: Fuzzy match threshold (0-100)

        Returns:
            Dict mapping entity types to found entities
            Example: {"Component": [{"id": "R-ICU", "confidence": 1.0}]}
        """
        if not self.flat_dict:
            return {}

        results = {}
        text_lower = text.lower()

        # 0. Pattern matching for requirement IDs (NEW - highest priority)
        # Match patterns like FuncR_S110, DesR_A404, IntR_C302, PerfR_B203, SafR_X999
        req_pattern = r'\b(FuncR|DesR|IntR|PerfR|SafR)_([A-Z])(\d{3})\b'
        req_matches = re.finditer(req_pattern, text, re.IGNORECASE)

        for match in req_matches:
            req_id = match.group(0).upper()  # e.g., "FuncR_S110"
            req_category = match.group(1)    # e.g., "FuncR"

            entity_type = "Requirement"
            if entity_type not in results:
                results[entity_type] = []

            # Check if already added (avoid duplicates)
            if not any(e.get('id') == req_id for e in results[entity_type]):
                results[entity_type].append({
                    "id": req_id,
                    "type": "Requirement",
                    "category": req_category,
                    "matched_phrase": req_id,
                    "confidence": 1.0,
                    "source": "pattern_match"
                })
                logger.info(f"Pattern matched requirement ID: {req_id}")

        # 1. Exact match (fastest)
        for phrase, entity in self.flat_dict.items():
            if phrase in text_lower:
                entity_type = entity["type"]
                if entity_type not in results:
                    results[entity_type] = []

                # Check if already added (avoid duplicates)
                if not any(e.get('id') == entity.get('id') for e in results[entity_type]):
                    results[entity_type].append({
                        **entity,
                        "matched_phrase": phrase,
                        "confidence": 1.0
                    })

        # 2. Fuzzy match (if no exact match)
        if not results:
            best_matches = process.extract(
                text_lower,
                self.flat_dict.keys(),
                limit=3
            )

            for phrase, score in best_matches:
                if score >= threshold:
                    entity = self.flat_dict[phrase]
                    entity_type = entity["type"]

                    if entity_type not in results:
                        results[entity_type] = []

                    results[entity_type].append({
                        **entity,
                        "matched_phrase": phrase,
                        "confidence": score / 100.0
                    })

        return results

    def get_entity_by_id(self, entity_id: str) -> Dict:
        """
        Get entity information by ID.

        Args:
            entity_id: Entity ID (e.g., "R-ICU", "WM")

        Returns:
            Entity dictionary or None if not found
        """
        for phrase, entity in self.flat_dict.items():
            if entity.get('id') == entity_id:
                return entity
        return None

    def get_categories(self) -> List[str]:
        """
        Get all entity categories.

        Returns:
            List of category names
        """
        return list(self.entities.keys())

    def get_entities_by_category(self, category: str) -> Dict:
        """
        Get all entities in a category.

        Args:
            category: Category name (e.g., "components", "requirements")

        Returns:
            Dictionary of entities in that category
        """
        return self.entities.get(category, {})

    def resolve_entities_in_text(self, text: str, threshold: int = 85) -> Dict[str, List]:
        """
        Alias for resolve() method for compatibility.

        Args:
            text: Input text
            threshold: Fuzzy match threshold

        Returns:
            Dict mapping entity types to found entities
        """
        return self.resolve(text, threshold)

    def resolve_exact(self, entity_name: str, entity_type: str = None) -> Dict:
        """
        Try exact match for an entity.

        Args:
            entity_name: Entity name or phrase
            entity_type: Optional entity type filter

        Returns:
            Entity dict or None
        """
        entity_name_lower = entity_name.lower()

        for phrase, entity in self.flat_dict.items():
            if phrase == entity_name_lower:
                if entity_type is None or entity.get("type", "").lower() == entity_type.lower():
                    return {**entity, "confidence": 1.0}

        return None

    def resolve_fuzzy(self, entity_name: str, entity_type: str = None, threshold: int = 85) -> Dict:
        """
        Try fuzzy match for an entity.

        Args:
            entity_name: Entity name or phrase
            entity_type: Optional entity type filter
            threshold: Match threshold

        Returns:
            Best match entity dict or None
        """
        entity_name_lower = entity_name.lower()

        # Filter by type if provided
        candidates = self.flat_dict.keys()
        if entity_type:
            candidates = [
                phrase for phrase, entity in self.flat_dict.items()
                if entity.get("type", "").lower() == entity_type.lower()
            ]

        if not candidates:
            return None

        # Get best match
        best_matches = process.extract(entity_name_lower, candidates, limit=1)

        if best_matches and best_matches[0][1] >= threshold:
            phrase, score = best_matches[0]
            entity = self.flat_dict[phrase]
            return {**entity, "confidence": score / 100.0}

        return None


# Singleton instance
_resolver = None


def get_resolver() -> EntityResolver:
    """
    Get or create singleton EntityResolver.

    Returns:
        EntityResolver instance
    """
    global _resolver
    if _resolver is None:
        _resolver = EntityResolver()
    return _resolver


# Create module-level instance
entity_resolver = EntityResolver()


if __name__ == "__main__":
    # Test the entity resolver
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("=== Testing EntityResolver ===\n")

    resolver = EntityResolver()

    # Test 1: Exact match
    print("Test 1: Exact match")
    text1 = "The R-ICU component shall communicate via CAN bus"
    entities1 = resolver.resolve(text1)
    print(f"Text: '{text1}'")
    print(f"Found entities: {entities1}")

    # Test 2: Korean text
    print("\nTest 2: Korean text")
    text2 = "워킹 매니퓰레이터는 서비스 모듈과 통신한다"
    entities2 = resolver.resolve(text2)
    print(f"Text: '{text2}'")
    print(f"Found entities: {entities2}")

    # Test 3: Multiple entities
    print("\nTest 3: Multiple entities")
    text3 = "The Walking Manipulator uses SpaceWire protocol to connect to the Service Module"
    entities3 = resolver.resolve(text3)
    print(f"Text: '{text3}'")
    print(f"Found entities: {entities3}")

    # Test 4: Get by ID
    print("\nTest 4: Get entity by ID")
    entity = resolver.get_entity_by_id("R-ICU")
    print(f"Entity for 'R-ICU': {entity}")

    # Test 5: Get categories
    print("\nTest 5: Get categories")
    categories = resolver.get_categories()
    print(f"Categories: {categories}")

    # Test 6: Get entities by category
    print("\nTest 6: Get entities in 'components' category")
    components = resolver.get_entities_by_category("components")
    print(f"Found {len(components)} components")
    for name in list(components.keys())[:5]:
        print(f"  - {name}")

    print("\n✅ EntityResolver test complete!")
