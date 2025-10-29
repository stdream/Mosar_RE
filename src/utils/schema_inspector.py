"""
Neo4j Schema Inspector - Extract schema information for Text2Cypher

Provides schema details to LLM for safe Cypher generation:
- Node labels and their properties
- Relationship types
- Constraints and indexes
- Sample data patterns
"""

import logging
from typing import Dict, List, Any, Optional
from src.utils.neo4j_client import Neo4jClient

logger = logging.getLogger(__name__)


class SchemaInspector:
    """
    Inspects Neo4j database schema and provides information for LLM-based Text2Cypher.

    This enables:
    1. Safe Cypher generation (only use valid labels/properties)
    2. Context-aware query construction
    3. Schema validation before execution
    """

    def __init__(self):
        """Initialize schema inspector."""
        self.client = Neo4jClient()
        self._schema_cache = None

    def get_schema_description(self) -> str:
        """
        Get human-readable schema description for LLM prompt.

        Returns:
            Formatted schema description string
        """
        if self._schema_cache is None:
            self._schema_cache = self._fetch_schema()

        return self._format_schema_for_llm(self._schema_cache)

    def _fetch_schema(self) -> Dict[str, Any]:
        """
        Fetch complete schema information from Neo4j.

        Returns:
            Dict containing:
            - node_labels: List of node types with properties
            - relationships: List of relationship types
            - constraints: List of constraints
            - indexes: List of indexes
            - sample_patterns: Common graph patterns
        """
        schema = {
            "node_labels": self._get_node_labels(),
            "relationships": self._get_relationships(),
            "constraints": self._get_constraints(),
            "indexes": self._get_indexes(),
            "sample_patterns": self._get_common_patterns()
        }

        logger.info(f"Fetched schema: {len(schema['node_labels'])} node labels, "
                   f"{len(schema['relationships'])} relationship types")

        return schema

    def _get_node_labels(self) -> List[Dict[str, Any]]:
        """
        Get all node labels and their properties.

        Returns:
            List of dicts with 'label' and 'properties'
        """
        query = """
        CALL db.schema.nodeTypeProperties()
        YIELD nodeType, nodeLabels, propertyName, propertyTypes, mandatory
        RETURN
            nodeLabels[0] AS label,
            collect({
                name: propertyName,
                types: propertyTypes,
                mandatory: mandatory
            }) AS properties
        ORDER BY label
        """

        try:
            results = self.client.execute(query)

            # Group by label
            labels_dict = {}
            for record in results:
                label = record['label']
                if label not in labels_dict:
                    labels_dict[label] = []
                labels_dict[label].extend(record['properties'])

            # Convert to list
            node_labels = []
            for label, properties in labels_dict.items():
                node_labels.append({
                    "label": label,
                    "properties": properties
                })

            return node_labels

        except Exception as e:
            logger.warning(f"Failed to get node labels: {e}")
            # Fallback to known labels
            return [
                {"label": "Requirement", "properties": [{"name": "id"}, {"name": "statement"}]},
                {"label": "Component", "properties": [{"name": "id"}, {"name": "name"}]},
                {"label": "TestCase", "properties": [{"name": "id"}, {"name": "description"}]},
                {"label": "Section", "properties": [{"name": "id"}, {"name": "title"}, {"name": "content"}]},
            ]

    def _get_relationships(self) -> List[Dict[str, str]]:
        """
        Get all relationship types with their source and target labels.

        Returns:
            List of dicts with 'type', 'from_label', 'to_label'
        """
        query = """
        CALL db.schema.relTypeProperties()
        YIELD relType, sourceNodeLabels, targetNodeLabels
        RETURN DISTINCT
            relType AS type,
            sourceNodeLabels[0] AS from_label,
            targetNodeLabels[0] AS to_label
        ORDER BY type
        """

        try:
            results = self.client.execute(query)
            return [
                {
                    "type": r['type'],
                    "from_label": r.get('from_label', 'Any'),
                    "to_label": r.get('to_label', 'Any')
                }
                for r in results
            ]

        except Exception as e:
            logger.warning(f"Failed to get relationships: {e}")
            # Fallback to known relationships
            return [
                {"type": "RELATES_TO", "from_label": "Requirement", "to_label": "Component"},
                {"type": "VERIFIES", "from_label": "TestCase", "to_label": "Requirement"},
                {"type": "DERIVES_FROM", "from_label": "Requirement", "to_label": "Requirement"},
                {"type": "MENTIONS", "from_label": "Section", "to_label": "Component"},
            ]

    def _get_constraints(self) -> List[str]:
        """Get all constraints."""
        query = "SHOW CONSTRAINTS"

        try:
            results = self.client.execute(query)
            return [r.get('name', 'unknown') for r in results]
        except Exception as e:
            logger.warning(f"Failed to get constraints: {e}")
            return []

    def _get_indexes(self) -> List[str]:
        """Get all indexes."""
        query = "SHOW INDEXES"

        try:
            results = self.client.execute(query)
            return [r.get('name', 'unknown') for r in results]
        except Exception as e:
            logger.warning(f"Failed to get indexes: {e}")
            return []

    def _get_common_patterns(self) -> List[str]:
        """
        Get common graph patterns for examples.

        Returns:
            List of example Cypher patterns
        """
        return [
            # Requirements traceability
            "(req:Requirement)-[:VERIFIES]-(tc:TestCase)",
            "(req:Requirement)-[:RELATES_TO]->(comp:Component)",
            "(req:Requirement)-[:DERIVES_FROM]->(parent:Requirement)",

            # Design evolution
            "(sec:Section)-[:MENTIONS]->(comp:Component)",
            "(doc:Document)-[:HAS_SECTION]->(sec:Section)",

            # Component architecture
            "(comp:Component)-[:USES_PROTOCOL]->(proto:Protocol)",
            "(comp:Component)-[:PART_OF]->(module:SpacecraftModule)",
        ]

    def _format_schema_for_llm(self, schema: Dict[str, Any]) -> str:
        """
        Format schema information for LLM prompt.

        Args:
            schema: Schema dict from _fetch_schema()

        Returns:
            Formatted string for LLM context
        """
        lines = ["# Neo4j Database Schema", ""]

        # Node labels
        lines.append("## Node Labels")
        for node in schema['node_labels']:
            label = node['label']
            props = node['properties']

            lines.append(f"### :{label}")
            if props:
                lines.append("Properties:")
                for prop in props[:5]:  # Limit to top 5 properties
                    prop_name = prop.get('name', 'unknown')
                    prop_types = prop.get('types', ['Any'])
                    mandatory = " (required)" if prop.get('mandatory', False) else ""
                    lines.append(f"  - {prop_name}: {', '.join(prop_types)}{mandatory}")
            lines.append("")

        # Relationships
        lines.append("## Relationships")
        for rel in schema['relationships']:
            rel_type = rel['type']
            from_label = rel['from_label']
            to_label = rel['to_label']
            lines.append(f"- ({from_label})-[:{rel_type}]->({to_label})")
        lines.append("")

        # Common patterns
        lines.append("## Common Query Patterns")
        for pattern in schema['sample_patterns']:
            lines.append(f"- {pattern}")
        lines.append("")

        # Constraints
        if schema['constraints']:
            lines.append(f"## Constraints ({len(schema['constraints'])} total)")
            for constraint in schema['constraints'][:5]:
                lines.append(f"- {constraint}")
            lines.append("")

        return "\n".join(lines)

    def validate_cypher(self, cypher_query: str) -> tuple[bool, Optional[str]]:
        """
        Validate generated Cypher query before execution.

        Args:
            cypher_query: Generated Cypher query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Safety checks
        cypher_lower = cypher_query.lower()

        # 1. Prevent destructive operations
        forbidden_keywords = ['delete', 'detach delete', 'remove', 'set', 'create', 'merge']
        for keyword in forbidden_keywords:
            if keyword in cypher_lower:
                return False, f"Destructive operation '{keyword}' not allowed in read-only queries"

        # 2. Ensure RETURN clause exists
        if 'return' not in cypher_lower:
            return False, "Query must have a RETURN clause"

        # 3. Check for balanced brackets
        if cypher_query.count('(') != cypher_query.count(')'):
            return False, "Unbalanced parentheses in query"

        if cypher_query.count('[') != cypher_query.count(']'):
            return False, "Unbalanced brackets in query"

        if cypher_query.count('{') != cypher_query.count('}'):
            return False, "Unbalanced braces in query"

        # 4. Try EXPLAIN query (dry run)
        try:
            explain_query = f"EXPLAIN {cypher_query}"
            self.client.execute(explain_query)
            return True, None
        except Exception as e:
            return False, f"Query validation failed: {str(e)}"

    def close(self):
        """Close Neo4j connection."""
        if self.client:
            self.client.close()


# Standalone testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    inspector = SchemaInspector()

    print("="*80)
    print("Neo4j Schema Description")
    print("="*80)
    print(inspector.get_schema_description())

    print("\n" + "="*80)
    print("Testing Query Validation")
    print("="*80)

    # Test valid query
    valid_query = """
    MATCH (req:Requirement {id: 'FuncR_S110'})
    RETURN req.statement
    """
    is_valid, error = inspector.validate_cypher(valid_query)
    print(f"\nValid query: {is_valid}")
    if error:
        print(f"Error: {error}")

    # Test invalid query (destructive)
    invalid_query = """
    MATCH (req:Requirement)
    DELETE req
    """
    is_valid, error = inspector.validate_cypher(invalid_query)
    print(f"\nDestructive query blocked: {not is_valid}")
    if error:
        print(f"Error: {error}")

    inspector.close()
