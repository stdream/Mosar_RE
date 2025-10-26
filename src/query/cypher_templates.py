"""
Cypher Query Templates - Predefined queries for common patterns

Supports:
1. Requirements Traceability (V-Model)
2. Component Dependencies
3. Design Evolution (PDD → DDD)
4. Test Coverage
5. Unverified Requirements
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CypherTemplates:
    """
    Collection of predefined Cypher query templates for MOSAR GraphRAG.

    Each template is parameterized and can be used for Path A (Pure Cypher) queries.
    """

    # ===============================
    # 1. Requirements Traceability
    # ===============================

    @staticmethod
    def get_requirement_traceability(req_id: str) -> str:
        """
        Get full traceability chain for a requirement.

        Path: Requirement → DesignConcept → DetailedDesign → Component → TestCase

        Args:
            req_id: Requirement ID (e.g., 'FuncR_S110')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH path = (req:Requirement {{id: '{req_id}'}})
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        OPTIONAL MATCH (req)-[:RELATES_TO]->(c:Component)
        RETURN
            req.id AS requirement_id,
            req.statement AS requirement_statement,
            req.type AS requirement_type,
            req.level AS requirement_level,
            req.verification AS verification_method,
            collect(DISTINCT tc.id) AS test_cases,
            collect(DISTINCT c.id) AS related_components
        """

    @staticmethod
    def get_requirement_dependencies(req_id: str) -> str:
        """
        Get all requirements that this requirement derives from or covers.

        Args:
            req_id: Requirement ID

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (req:Requirement {{id: '{req_id}'}})
        OPTIONAL MATCH (req)-[:DERIVES_FROM]->(parent:Requirement)
        OPTIONAL MATCH (child:Requirement)-[:DERIVES_FROM]->(req)
        RETURN
            req.id AS requirement_id,
            req.statement AS statement,
            collect(DISTINCT parent.id) AS parent_requirements,
            collect(DISTINCT child.id) AS child_requirements
        """

    # ===============================
    # 2. Component Queries
    # ===============================

    @staticmethod
    def get_component_requirements(component_id: str) -> str:
        """
        Get all requirements related to a component.

        Args:
            component_id: Component ID (e.g., 'R-ICU')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (c:Component {{id: '{component_id}'}})<-[:RELATES_TO]-(req:Requirement)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        RETURN
            req.id AS requirement_id,
            req.type AS requirement_type,
            req.statement AS requirement_statement,
            req.verification AS verification_method,
            count(DISTINCT tc) AS test_case_count,
            collect(DISTINCT tc.id) AS test_cases
        ORDER BY req.type, req.id
        """

    @staticmethod
    def get_component_tests(component_id: str) -> str:
        """
        Get all test cases that verify a component.

        Args:
            component_id: Component ID

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (c:Component {{id: '{component_id}'}})<-[:RELATES_TO]-(req:Requirement)<-[:VERIFIES]-(tc:TestCase)
        RETURN
            tc.id AS test_case_id,
            tc.test_type AS test_type,
            tc.description AS description,
            tc.status AS status,
            collect(DISTINCT req.id) AS verified_requirements
        ORDER BY tc.test_type, tc.id
        """

    # ===============================
    # 3. Test Case Queries
    # ===============================

    @staticmethod
    def get_test_coverage() -> str:
        """
        Get overall test coverage statistics.

        Returns:
            Cypher query with coverage metrics
        """
        return """
        MATCH (req:Requirement)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        WITH
            count(DISTINCT req) AS total_requirements,
            count(DISTINCT CASE WHEN tc IS NOT NULL THEN req END) AS verified_requirements,
            count(DISTINCT tc) AS total_test_cases
        RETURN
            total_requirements,
            verified_requirements,
            total_requirements - verified_requirements AS unverified_requirements,
            total_test_cases,
            round(100.0 * verified_requirements / total_requirements, 2) AS coverage_percentage
        """

    @staticmethod
    def get_unverified_requirements(req_type: Optional[str] = None) -> str:
        """
        Get requirements without test cases.

        Args:
            req_type: Optional filter by requirement type (FuncR, SafR, PerfR, IntR)

        Returns:
            Cypher query string
        """
        type_filter = f"AND req.type = '{req_type}'" if req_type else ""

        return f"""
        MATCH (req:Requirement)
        WHERE NOT EXISTS {{ (req)<-[:VERIFIES]-(:TestCase) }}
        {type_filter}
        RETURN
            req.id AS requirement_id,
            req.type AS requirement_type,
            req.level_subsystem AS subsystem,
            req.statement AS requirement_statement,
            req.verification AS verification_method
        ORDER BY req.type, req.id
        """

    @staticmethod
    def get_test_case_details(test_case_id: str) -> str:
        """
        Get details of a specific test case.

        Args:
            test_case_id: Test case ID (e.g., 'CT-A-1')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (tc:TestCase {{id: '{test_case_id}'}})
        OPTIONAL MATCH (tc)-[:VERIFIES]->(req:Requirement)
        RETURN
            tc.id AS test_case_id,
            tc.test_type AS test_type,
            tc.description AS description,
            tc.status AS status,
            tc.procedure AS procedure,
            collect(DISTINCT req.id) AS verified_requirements,
            collect(DISTINCT req.statement) AS requirement_statements
        """

    # ===============================
    # 4. Protocol and Communication
    # ===============================

    @staticmethod
    def get_protocol_requirements(protocol_name: str) -> str:
        """
        Get requirements that use a specific protocol.

        Args:
            protocol_name: Protocol name (e.g., 'CAN', 'Ethernet', 'SpaceWire')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (p:Protocol {{name: '{protocol_name}'}})<-[:USES_PROTOCOL]-(req:Requirement)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)
        RETURN
            req.id AS requirement_id,
            req.type AS requirement_type,
            req.statement AS requirement_statement,
            p.name AS protocol,
            count(DISTINCT tc) AS test_count
        ORDER BY req.type, req.id
        """

    @staticmethod
    def get_all_protocols() -> str:
        """
        Get all communication protocols with usage statistics.

        Returns:
            Cypher query string
        """
        return """
        MATCH (p:Protocol)
        OPTIONAL MATCH (p)<-[:USES_PROTOCOL]-(req:Requirement)
        RETURN
            p.name AS protocol_name,
            p.category AS category,
            count(DISTINCT req) AS requirement_count,
            collect(DISTINCT req.type) AS requirement_types
        ORDER BY requirement_count DESC
        """

    # ===============================
    # 5. Document Section Queries
    # ===============================

    @staticmethod
    def search_sections_by_keyword(keyword: str, limit: int = 10) -> str:
        """
        Full-text search across document sections.

        Args:
            keyword: Search term
            limit: Max results

        Returns:
            Cypher query using fulltext index
        """
        return f"""
        CALL db.index.fulltext.queryNodes('section_fulltext', '{keyword}')
        YIELD node, score
        MATCH (doc:Document)-[:HAS_SECTION]->(node)
        RETURN
            node.id AS section_id,
            node.title AS section_title,
            node.content AS content,
            doc.title AS document,
            score
        ORDER BY score DESC
        LIMIT {limit}
        """

    @staticmethod
    def get_sections_mentioning_component(component_id: str, limit: int = 10) -> str:
        """
        Get document sections that mention a specific component.

        Args:
            component_id: Component ID
            limit: Max results

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (c:Component {{id: '{component_id}'}})<-[:MENTIONS]-(section:Section)
        MATCH (doc:Document)-[:HAS_SECTION]->(section)
        RETURN
            section.id AS section_id,
            section.title AS section_title,
            section.content AS content,
            doc.title AS document,
            doc.type AS doc_type
        ORDER BY doc.type, section.id
        LIMIT {limit}
        """

    # ===============================
    # 6. Statistics and Summaries
    # ===============================

    @staticmethod
    def get_requirements_by_type() -> str:
        """
        Get requirement count by type.

        Returns:
            Cypher query string
        """
        return """
        MATCH (req:Requirement)
        RETURN
            req.type AS requirement_type,
            count(*) AS count
        ORDER BY count DESC
        """

    @staticmethod
    def get_requirements_by_subsystem() -> str:
        """
        Get requirement count by subsystem.

        Returns:
            Cypher query string
        """
        return """
        MATCH (req:Requirement)
        RETURN
            req.level_subsystem AS subsystem,
            count(*) AS count
        ORDER BY count DESC
        """

    @staticmethod
    def get_database_stats() -> str:
        """
        Get overall database statistics.

        Returns:
            Cypher query string
        """
        return """
        MATCH (n)
        WITH labels(n) AS labels, count(*) AS count
        UNWIND labels AS label
        RETURN
            label AS node_type,
            sum(count) AS node_count
        ORDER BY node_count DESC
        """


class CypherTemplateExecutor:
    """
    Executes predefined Cypher templates against Neo4j database.
    """

    def __init__(self, neo4j_client):
        """
        Initialize executor.

        Args:
            neo4j_client: Neo4jClient instance
        """
        self.neo4j_client = neo4j_client
        self.templates = CypherTemplates()

    def execute_template(self, template_name: str, **params) -> List[Dict[str, Any]]:
        """
        Execute a named template with parameters.

        Args:
            template_name: Method name from CypherTemplates
            **params: Parameters for the template

        Returns:
            List of result records

        Raises:
            AttributeError: If template_name doesn't exist
        """
        # Get template method
        template_method = getattr(self.templates, template_name)

        # Generate query
        query = template_method(**params)

        logger.info(f"Executing template: {template_name} with params: {params}")
        logger.debug(f"Generated query:\n{query}")

        # Execute query
        results = self.neo4j_client.execute_query(query)

        logger.info(f"Query returned {len(results)} results")

        return results


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    templates = CypherTemplates()

    # Example: Get requirement traceability
    print("=== Requirement Traceability (FuncR_S110) ===")
    print(templates.get_requirement_traceability("FuncR_S110"))

    print("\n=== Component Requirements (R-ICU) ===")
    print(templates.get_component_requirements("R-ICU"))

    print("\n=== Test Coverage Stats ===")
    print(templates.get_test_coverage())

    print("\n=== Unverified SafR Requirements ===")
    print(templates.get_unverified_requirements("SafR"))
