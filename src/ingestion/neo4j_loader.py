"""Load parsed documents into Neo4j."""
import sys
from pathlib import Path
from typing import List, Dict
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[2]))

from src.utils.neo4j_client import Neo4jClient
from src.utils.entity_resolver import EntityResolver

logger = logging.getLogger(__name__)


class MOSARGraphLoader:
    """Load MOSAR documents into Neo4j graph."""

    def __init__(self):
        """Initialize Neo4j client and entity resolver."""
        self.client = Neo4jClient()
        self.entity_resolver = EntityResolver()
        logger.info("Initialized MOSARGraphLoader")

    def load_requirements(self, requirements: List[Dict]):
        """
        Load requirements from SRD.

        Creates:
        - Requirement nodes
        - Organization nodes
        - ASSIGNED_TO relationships
        - DERIVES_FROM relationships (from COVERS field)
        - Entity relationships (from Entity Dictionary)

        Args:
            requirements: List of requirement dicts from SRDParser
        """
        logger.info(f"Loading {len(requirements)} requirements to Neo4j...")

        # Create Requirement nodes
        cypher = """
        UNWIND $requirements AS req

        // Create Requirement node
        MERGE (r:Requirement {id: req.id})
        SET r.title = req.title,
            r.statement = req.statement,
            r.type = req.type,
            r.subsystem = req.subsystem,
            r.level = req.level,
            r.verification = req.verification,
            r.covers = req.covers,
            r.comment = req.comment,
            r.statement_embedding = req.statement_embedding,
            r.updated_at = datetime()

        RETURN count(r) AS created_count
        """

        result = self.client.execute(cypher, requirements=requirements)
        created_count = result[0]['created_count'] if result else 0

        logger.info(f"  ✓ Created/updated {created_count} requirement nodes")

        # Create DERIVES_FROM relationships from COVERS field
        self._create_covers_relationships(requirements)

        # Create entity relationships using Entity Dictionary
        self._create_entity_relationships(requirements)

        logger.info(f"✅ Loaded {len(requirements)} requirements to Neo4j")

    def _create_covers_relationships(self, requirements: List[Dict]):
        """
        Create DERIVES_FROM relationships from COVERS field.

        Args:
            requirements: List of requirement dicts
        """
        logger.info("  Creating DERIVES_FROM relationships from COVERS field...")

        cypher = """
        UNWIND $requirements AS req

        // Match the child requirement
        MATCH (child:Requirement {id: req.id})

        // Extract parent requirement IDs from COVERS field
        WITH child, req.covers AS covers_str
        WHERE covers_str IS NOT NULL AND covers_str <> ''

        // Split by comma and extract requirement IDs
        WITH child, split(covers_str, ',') AS covers_parts
        UNWIND covers_parts AS part

        WITH child, trim(part) AS part_trimmed
        WHERE part_trimmed =~ '.*[A-Z][a-z]+R_[A-Z]\\d+.*'

        // Extract the requirement ID pattern
        WITH child, part_trimmed
        WHERE part_trimmed <> ''

        // Match patterns like "FuncR_S101" in the text
        WITH child,
             [x IN split(part_trimmed, ' ') WHERE x =~ '[A-Z][a-z]+R_[A-Z]\\d+'][0] AS parent_id
        WHERE parent_id IS NOT NULL

        // Create relationship if parent exists
        MATCH (parent:Requirement {id: parent_id})
        MERGE (child)-[:DERIVES_FROM]->(parent)

        RETURN count(*) AS rel_count
        """

        result = self.client.execute(cypher, requirements=requirements)
        rel_count = result[0]['rel_count'] if result else 0

        logger.info(f"  ✓ Created {rel_count} DERIVES_FROM relationships")

    def _create_entity_relationships(self, requirements: List[Dict]):
        """
        Create relationships from requirements to entities using Entity Dictionary.

        Args:
            requirements: List of requirement dicts
        """
        logger.info("  Creating entity relationships from Entity Dictionary...")

        relationship_count = 0

        for req in requirements:
            # Combine all text fields for entity resolution
            text = f"{req.get('title', '')} {req.get('statement', '')} {req.get('comment', '')}"

            # Resolve entities
            entities = self.entity_resolver.resolve(text)

            # Create relationships for each entity type
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    if entity_type == "Component":
                        self._link_requirement_to_component(req['id'], entity['id'])
                        relationship_count += 1
                    elif entity_type == "Scenario":
                        self._link_requirement_to_scenario(req['id'], entity['id'])
                        relationship_count += 1
                    elif entity_type == "Protocol":
                        self._link_requirement_to_protocol(req['id'], entity['id'])
                        relationship_count += 1

        logger.info(f"  ✓ Created {relationship_count} entity relationships")

    def _link_requirement_to_component(self, req_id: str, component_id: str):
        """Create RELATES_TO relationship between requirement and component."""
        cypher = """
        MATCH (req:Requirement {id: $req_id})
        MERGE (comp:Component {id: $component_id})
        MERGE (req)-[:RELATES_TO]->(comp)
        """
        self.client.execute(cypher, req_id=req_id, component_id=component_id)

    def _link_requirement_to_scenario(self, req_id: str, scenario_id: str):
        """Create VALIDATED_BY relationship between requirement and scenario."""
        cypher = """
        MATCH (req:Requirement {id: $req_id})
        MERGE (scenario:Scenario {id: $scenario_id})
        MERGE (req)-[:VALIDATED_BY]->(scenario)
        """
        self.client.execute(cypher, req_id=req_id, scenario_id=scenario_id)

    def _link_requirement_to_protocol(self, req_id: str, protocol_id: str):
        """Create USES_PROTOCOL relationship between requirement and protocol."""
        cypher = """
        MATCH (req:Requirement {id: $req_id})
        MERGE (protocol:Protocol {id: $protocol_id})
        MERGE (req)-[:USES_PROTOCOL]->(protocol)
        """
        self.client.execute(cypher, req_id=req_id, protocol_id=protocol_id)

    def load_test_cases(self, test_cases: List[Dict]):
        """
        Load test cases from Demo Procedures.

        Creates:
        - TestCase nodes
        - VERIFIES relationships (TestCase -> Requirement)

        Args:
            test_cases: List of test case dicts from DemoProcedureParser
        """
        logger.info(f"Loading {len(test_cases)} test cases to Neo4j...")

        # Create TestCase nodes
        cypher = """
        UNWIND $test_cases AS tc

        // Create TestCase node
        MERGE (t:TestCase {id: tc.id})
        SET t.name = tc.name,
            t.type = tc.type,
            t.objective = tc.objective,
            t.procedure = tc.procedure,
            t.status = tc.status,
            t.updated_at = datetime()

        RETURN count(t) AS created_count
        """

        result = self.client.execute(cypher, test_cases=test_cases)
        created_count = result[0]['created_count'] if result else 0

        logger.info(f"  ✓ Created/updated {created_count} test case nodes")

        # Create VERIFIES relationships
        self._create_verifies_relationships(test_cases)

        logger.info(f"✅ Loaded {len(test_cases)} test cases to Neo4j")

    def _create_verifies_relationships(self, test_cases: List[Dict]):
        """
        Create VERIFIES relationships from test cases to requirements.

        Args:
            test_cases: List of test case dicts
        """
        logger.info("  Creating VERIFIES relationships...")

        cypher = """
        UNWIND $test_cases AS tc

        // Match the test case
        MATCH (t:TestCase {id: tc.id})

        // For each covered requirement
        UNWIND tc.covered_requirements AS req_id

        // Match the requirement
        MATCH (req:Requirement {id: req_id})

        // Create VERIFIES relationship
        MERGE (t)-[:VERIFIES]->(req)

        RETURN count(*) AS rel_count
        """

        result = self.client.execute(cypher, test_cases=test_cases)
        rel_count = result[0]['rel_count'] if result else 0

        logger.info(f"  ✓ Created {rel_count} VERIFIES relationships")

    def load_design_sections(self, sections: List[Dict], doc_type: str):
        """
        Load design document sections (PDD or DDD).

        Creates:
        - Section nodes with embeddings
        - Document nodes
        - HAS_SECTION relationships

        Args:
            sections: List of section dicts from DesignDocParser
            doc_type: "PDD" or "DDD"
        """
        logger.info(f"Loading {len(sections)} {doc_type} sections to Neo4j...")

        # Create Document node first
        doc_id = f"{doc_type}-MOSAR-v1.0"
        doc_title = "Preliminary Design Document" if doc_type == "PDD" else "Detailed Design Document"

        doc_cypher = """
        MERGE (d:Document {id: $doc_id})
        SET d.title = $title,
            d.type = $doc_type,
            d.version = '1.0',
            d.updated_at = datetime()
        """
        self.client.execute(doc_cypher, doc_id=doc_id, title=doc_title, doc_type=doc_type)

        # Create Section nodes
        section_cypher = """
        UNWIND $sections AS sec

        // Create Section node
        MERGE (s:Section {id: sec.id})
        SET s.doc_id = sec.doc_id,
            s.number = sec.number,
            s.title = sec.title,
            s.level = sec.level,
            s.content = sec.content,
            s.chapter = sec.chapter,
            s.content_embedding = sec.content_embedding,
            s.updated_at = datetime()

        // Link to Document
        WITH s, sec
        MATCH (d:Document {id: $doc_id})
        MERGE (d)-[:HAS_SECTION]->(s)

        RETURN count(s) AS created_count
        """

        result = self.client.execute(section_cypher, sections=sections, doc_id=doc_id)
        created_count = result[0]['created_count'] if result else 0

        logger.info(f"  ✓ Created/updated {created_count} section nodes")

        # Create entity relationships for sections
        self._create_section_entity_relationships(sections)

        logger.info(f"✅ Loaded {len(sections)} {doc_type} sections to Neo4j")

    def _create_section_entity_relationships(self, sections: List[Dict]):
        """
        Create MENTIONS relationships from sections to entities.

        Args:
            sections: List of section dicts
        """
        logger.info("  Creating MENTIONS relationships from sections...")

        relationship_count = 0

        for sec in sections:
            # Use section content for entity resolution
            text = f"{sec.get('title', '')} {sec.get('content', '')}"

            # Resolve entities
            entities = self.entity_resolver.resolve(text)

            # Create relationships for each entity type
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    if entity_type == "Component":
                        self._link_section_to_component(sec['id'], entity['id'])
                        relationship_count += 1
                    elif entity_type == "Requirement":
                        # Link section to requirement if requirement type mentioned
                        if 'filter' in entity:
                            # This is a requirement type, not a specific requirement
                            continue
                    elif entity_type == "Protocol":
                        self._link_section_to_protocol(sec['id'], entity['id'])
                        relationship_count += 1

        logger.info(f"  ✓ Created {relationship_count} MENTIONS relationships")

    def _link_section_to_component(self, section_id: str, component_id: str):
        """Create MENTIONS relationship between section and component."""
        cypher = """
        MATCH (sec:Section {id: $section_id})
        MERGE (comp:Component {id: $component_id})
        MERGE (sec)-[:MENTIONS]->(comp)
        """
        self.client.execute(cypher, section_id=section_id, component_id=component_id)

    def _link_section_to_protocol(self, section_id: str, protocol_id: str):
        """Create MENTIONS relationship between section and protocol."""
        cypher = """
        MATCH (sec:Section {id: $section_id})
        MERGE (protocol:Protocol {id: $protocol_id})
        MERGE (sec)-[:MENTIONS]->(protocol)
        """
        self.client.execute(cypher, section_id=section_id, protocol_id=protocol_id)

    def get_statistics(self) -> Dict:
        """
        Get loading statistics from Neo4j.

        Returns:
            Dictionary with node and relationship counts
        """
        stats = {
            "nodes": {},
            "relationships": {}
        }

        # Count nodes by label
        node_labels = ["Requirement", "Component", "Scenario", "Protocol", "Organization", "TestCase", "Section", "Document"]
        for label in node_labels:
            count = self.client.count_nodes(label)
            stats["nodes"][label] = count

        # Count relationships by type
        rel_types = ["DERIVES_FROM", "RELATES_TO", "VALIDATED_BY", "USES_PROTOCOL", "VERIFIES", "HAS_SECTION", "MENTIONS"]
        for rel_type in rel_types:
            count = self.client.count_relationships(rel_type)
            stats["relationships"][rel_type] = count

        return stats

    def close(self):
        """Close Neo4j connection."""
        self.client.close()


if __name__ == "__main__":
    # Test the loader
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("=== Testing MOSARGraphLoader ===\n")

    try:
        loader = MOSARGraphLoader()

        # Get current statistics
        print("Current Neo4j statistics:")
        stats = loader.get_statistics()

        for category, items in stats.items():
            print(f"\n{category.upper()}:")
            for name, count in items.items():
                print(f"  {name}: {count}")

        loader.close()

        print("\n✅ Loader test complete!")

    except Exception as e:
        print(f"\n❌ Loader test failed: {e}")
        import traceback
        traceback.print_exc()
