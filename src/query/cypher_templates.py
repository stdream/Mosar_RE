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
        Get complete V-Model traceability for a requirement (multi-hop).

        Includes:
        - Upward: Parent requirements (System → Subsystem)
        - Horizontal: Test cases, Components, Interfaces
        - Downward: Child requirements with their tests/components

        Args:
            req_id: Requirement ID (e.g., 'FuncR_C104')

        Returns:
            Cypher query string with full V-Model traceability
        """
        return f"""
        // Main requirement
        MATCH (req:Requirement {{id: '{req_id}'}})

        // Upward traceability: Parent requirements
        OPTIONAL MATCH (req)-[:DERIVES_FROM*1..2]->(parent:Requirement)

        // Downward traceability: Child requirements
        OPTIONAL MATCH (req)<-[:DERIVES_FROM*1..2]-(child:Requirement)

        // Horizontal: Test cases (main requirement)
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)

        // Horizontal: Components (main requirement)
        OPTIONAL MATCH (req)-[:RELATES_TO]->(comp:Component)

        // Horizontal: Interfaces (via components)
        OPTIONAL MATCH (comp)-[:HAS_INTERFACE]->(iface:Interface)

        // Aggregate main requirement data
        WITH req,
             collect(DISTINCT parent.id) as parent_ids,
             collect(DISTINCT child) as child_nodes,
             collect(DISTINCT tc.id) as test_case_ids,
             collect(DISTINCT comp.id) as component_ids,
             collect(DISTINCT iface.id) as interface_ids

        // For each child, find their tests and components
        UNWIND CASE WHEN size(child_nodes) > 0 THEN child_nodes ELSE [null] END as child_node
        OPTIONAL MATCH (child_node)<-[:VERIFIES]-(child_tc:TestCase)
        OPTIONAL MATCH (child_node)-[:RELATES_TO]->(child_comp:Component)

        WITH req, parent_ids, test_case_ids, component_ids, interface_ids, child_node,
             collect(DISTINCT child_tc.id) as child_test_ids,
             collect(DISTINCT child_comp.id) as child_comp_ids

        // Aggregate child details
        WITH req, parent_ids, test_case_ids, component_ids, interface_ids,
             collect(DISTINCT CASE WHEN child_node IS NOT NULL THEN {{
                 id: child_node.id,
                 type: child_node.type,
                 statement: child_node.statement,
                 verification: child_node.verification,
                 level: child_node.level,
                 test_cases: child_test_ids,
                 components: child_comp_ids
             }} ELSE null END) as child_details_raw

        RETURN
            req.id AS requirement_id,
            req.statement AS requirement_statement,
            req.type AS requirement_type,
            req.level AS requirement_level,
            req.verification AS verification_method,
            test_case_ids AS test_cases,
            component_ids AS related_components,
            interface_ids AS related_interfaces,
            parent_ids AS parent_requirements,
            [item IN child_details_raw WHERE item IS NOT NULL] AS child_requirements
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

    @staticmethod
    def get_requirement_decomposition_tree(req_id: str) -> str:
        """
        Get complete decomposition tree for a requirement (multi-level).

        Shows:
        - Direct child requirements
        - Grandchildren requirements
        - Test cases for each leaf requirement
        - Components for each leaf requirement

        Args:
            req_id: Top-level requirement ID (e.g., 'FuncR_S110')

        Returns:
            Cypher query with complete decomposition structure
        """
        return f"""
        MATCH (parent:Requirement {{id: '{req_id}'}})

        // Get all descendants (children and grandchildren)
        OPTIONAL MATCH path = (parent)<-[:DERIVES_FROM*1..2]-(descendant:Requirement)

        WITH parent, descendant, length(path) as level
        ORDER BY level, descendant.id

        // Get tests and components for each descendant
        OPTIONAL MATCH (descendant)<-[:VERIFIES]-(tc:TestCase)
        OPTIONAL MATCH (descendant)-[:RELATES_TO]->(comp:Component)

        WITH parent,
             descendant,
             level,
             collect(DISTINCT tc.id) as test_cases,
             collect(DISTINCT comp.id) as components

        RETURN
            parent.id as parent_id,
            parent.statement as parent_statement,
            parent.type as parent_type,
            parent.level as parent_level,
            collect({{
                id: descendant.id,
                statement: descendant.statement,
                type: descendant.type,
                level: level,
                verification: descendant.verification,
                test_cases: test_cases,
                components: components,
                test_count: size(test_cases),
                component_count: size(components)
            }}) as descendants
        """

    # ===============================
    # 2. Component Queries
    # ===============================

    @staticmethod
    def get_component_requirements(component_id: str) -> str:
        """
        Get all requirements related to a component with multi-hop traceability.

        Multi-hop traceability includes:
        - Direct requirements (Component ← RELATES_TO ← Requirement)
        - Child requirements (Requirement ← DERIVES_FROM ← Child)
        - Parent requirements (Requirement → DERIVES_FROM → Parent)
        - Test cases (Requirement ← VERIFIES ← TestCase)

        Args:
            component_id: Component ID (e.g., 'R-ICU')

        Returns:
            Cypher query string with full traceability
        """
        return f"""
        // Step 1: Find direct requirements
        MATCH (c:Component {{id: '{component_id}'}})<-[:RELATES_TO]-(req:Requirement)

        // Step 2: Multi-hop parent requirements (upward traceability)
        OPTIONAL MATCH (req)-[:DERIVES_FROM*1..2]->(parent:Requirement)

        // Step 3: Multi-hop child requirements (downward traceability)
        OPTIONAL MATCH (req)<-[:DERIVES_FROM*1..2]-(child:Requirement)

        // Step 4: Test cases for direct requirements
        OPTIONAL MATCH (req)<-[:VERIFIES]-(tc:TestCase)

        // Aggregate per requirement
        WITH req,
             collect(DISTINCT parent.id) as parent_ids,
             collect(DISTINCT child.id) as child_ids,
             collect(DISTINCT tc.id) as test_case_ids,
             collect(DISTINCT child) as child_nodes

        // Step 5: For each child, find their test cases and components
        UNWIND CASE WHEN size(child_nodes) > 0 THEN child_nodes ELSE [null] END as child_node
        OPTIONAL MATCH (child_node)<-[:VERIFIES]-(child_tc:TestCase)
        OPTIONAL MATCH (child_node)-[:RELATES_TO]->(child_comp:Component)

        WITH req, parent_ids, child_ids, test_case_ids, child_node,
             collect(DISTINCT child_tc.id) as child_test_ids,
             collect(DISTINCT child_comp.id) as child_comp_ids

        // Group back per requirement with child details
        WITH req, parent_ids, child_ids, test_case_ids,
             collect(DISTINCT CASE WHEN child_node IS NOT NULL THEN {{
                 id: child_node.id,
                 type: child_node.type,
                 statement: child_node.statement,
                 verification: child_node.verification,
                 level: child_node.level,
                 test_cases: child_test_ids,
                 components: child_comp_ids
             }} ELSE null END) as child_details_raw

        RETURN
            req.id AS requirement_id,
            req.type AS requirement_type,
            req.statement AS requirement_statement,
            req.verification AS verification_method,
            req.level AS requirement_level,
            parent_ids AS parent_requirements,
            child_ids AS child_requirement_ids,
            [item IN child_details_raw WHERE item IS NOT NULL] AS child_requirements,
            size(test_case_ids) AS test_case_count,
            test_case_ids AS test_cases
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
    # 5. SpacecraftModule Queries
    # ===============================

    @staticmethod
    def get_module_details(module_id: str) -> str:
        """
        Get details of a spacecraft module including components and requirements.

        Args:
            module_id: Module ID (e.g., 'SM', 'SM1-DMS')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (sm:SpacecraftModule {{id: '{module_id}'}})
        OPTIONAL MATCH (sm)-[:CONTAINS]->(c:Component)
        OPTIONAL MATCH (c)<-[:RELATES_TO]-(req:Requirement)
        OPTIONAL MATCH (c)-[:HAS_INTERFACE]->(i:Interface)
        RETURN
            sm.id AS module_id,
            sm.name AS module_name,
            sm.description AS description,
            collect(DISTINCT c.id) AS components,
            collect(DISTINCT c.name) AS component_names,
            collect(DISTINCT req.id) AS related_requirements,
            collect(DISTINCT i.protocol) AS interface_protocols
        """

    @staticmethod
    def get_all_modules() -> str:
        """
        Get all spacecraft modules with component counts.

        Returns:
            Cypher query string
        """
        return """
        MATCH (sm:SpacecraftModule)
        OPTIONAL MATCH (sm)-[:CONTAINS]->(c:Component)
        RETURN
            sm.id AS module_id,
            sm.name AS module_name,
            count(DISTINCT c) AS component_count,
            collect(DISTINCT c.id) AS components
        ORDER BY component_count DESC
        """

    # ===============================
    # 6. Scenario Queries
    # ===============================

    @staticmethod
    def get_scenario_details(scenario_id: str) -> str:
        """
        Get details of a mission scenario.

        Args:
            scenario_id: Scenario ID (e.g., 'S1', 'S2')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (s:Scenario {{id: '{scenario_id}'}})
        OPTIONAL MATCH (s)-[:INVOLVES]->(c:Component)
        OPTIONAL MATCH (s)-[:REQUIRES]->(req:Requirement)
        OPTIONAL MATCH (s)<-[:DEFINED_IN]-(section:Section)<-[:HAS_SECTION]-(doc:Document)
        RETURN
            s.id AS scenario_id,
            s.name AS scenario_name,
            s.description AS description,
            collect(DISTINCT c.id) AS involved_components,
            collect(DISTINCT req.id) AS required_requirements,
            collect(DISTINCT {{doc: doc.title, section: section.title}}) AS documentation
        """

    @staticmethod
    def get_all_scenarios() -> str:
        """
        Get all mission scenarios.

        Returns:
            Cypher query string
        """
        return """
        MATCH (s:Scenario)
        OPTIONAL MATCH (s)-[:INVOLVES]->(c:Component)
        RETURN
            s.id AS scenario_id,
            s.name AS scenario_name,
            s.description AS description,
            count(DISTINCT c) AS component_count
        ORDER BY s.id
        """

    # ===============================
    # 7. Organization Queries
    # ===============================

    @staticmethod
    def get_organization_projects(org_id: str) -> str:
        """
        Get projects and contributions by an organization.

        Args:
            org_id: Organization ID (e.g., 'SPACEAPPS', 'TAS-UK')

        Returns:
            Cypher query string
        """
        return f"""
        MATCH (org:Organization {{id: '{org_id}'}})
        OPTIONAL MATCH (org)-[:DEVELOPS]->(c:Component)
        OPTIONAL MATCH (org)-[:CONTRIBUTES_TO]->(proj:Project)
        OPTIONAL MATCH (org)<-[:WORKS_FOR]-(p:Person)
        RETURN
            org.id AS organization_id,
            org.name AS organization_name,
            org.country AS country,
            collect(DISTINCT c.id) AS developed_components,
            collect(DISTINCT proj.name) AS projects,
            collect(DISTINCT p.name) AS team_members
        """

    @staticmethod
    def get_all_organizations() -> str:
        """
        Get all organizations with component counts.

        Returns:
            Cypher query string
        """
        return """
        MATCH (org:Organization)
        OPTIONAL MATCH (org)-[:DEVELOPS]->(c:Component)
        RETURN
            org.id AS organization_id,
            org.name AS organization_name,
            org.country AS country,
            count(DISTINCT c) AS component_count,
            collect(DISTINCT c.id) AS components
        ORDER BY component_count DESC
        """

    # ===============================
    # 8. Document Section Queries
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
    # 9. Statistics and Summaries
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
