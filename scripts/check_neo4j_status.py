"""
Check Neo4j database status and data completeness.

This script verifies:
1. Node counts by label
2. Relationship counts by type
3. Vector index status
4. Sample data quality
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def check_neo4j_status():
    """Check Neo4j database status."""

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            print("=" * 70)
            print("NEO4J DATABASE STATUS")
            print("=" * 70)

            # 1. Total node count
            result = session.run("MATCH (n) RETURN count(n) as total")
            total_nodes = result.single()["total"]
            print(f"\nTOTAL NODES: {total_nodes}")

            # 2. Node counts by label
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            print("\nNODES BY LABEL:")
            print("-" * 70)
            for record in result:
                print(f"  {record['label']:30s} : {record['count']:6d}")

            # 3. Total relationship count
            result = session.run("MATCH ()-[r]->() RETURN count(r) as total")
            total_rels = result.single()["total"]
            print(f"\nTOTAL RELATIONSHIPS: {total_rels}")

            # 4. Relationship counts by type
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
                LIMIT 20
            """)
            print("\nRELATIONSHIPS BY TYPE (Top 20):")
            print("-" * 70)
            for record in result:
                print(f"  {record['rel_type']:40s} : {record['count']:6d}")

            # 5. Check vector indexes
            result = session.run("""
                SHOW INDEXES
                WHERE type = 'VECTOR'
            """)
            print("\nVECTOR INDEXES:")
            print("-" * 70)
            indexes = list(result)
            if indexes:
                for record in indexes:
                    print(f"  Name: {record.get('name', 'N/A')}")
                    print(f"  State: {record.get('state', 'N/A')}")
                    print(f"  Population: {record.get('populationPercent', 'N/A')}")
                    print("-" * 70)
            else:
                print("  WARNING: No vector indexes found!")

            # 6. Check constraints
            result = session.run("SHOW CONSTRAINTS")
            print("\nCONSTRAINTS:")
            print("-" * 70)
            constraints = list(result)
            if constraints:
                for record in constraints:
                    print(f"  {record.get('name', 'N/A')} ({record.get('type', 'N/A')})")
            else:
                print("  WARNING: No constraints found!")

            # 7. Sample Requirements
            result = session.run("""
                MATCH (r:Requirement)
                RETURN r.id as id, r.type as type, r.statement as statement
                LIMIT 5
            """)
            print("\nSAMPLE REQUIREMENTS (First 5):")
            print("-" * 70)
            for i, record in enumerate(result, 1):
                print(f"{i}. [{record['id']}] ({record['type']})")
                print(f"   {record['statement'][:100]}...")
                print()

            # 8. Sample Components
            result = session.run("""
                MATCH (c:Component)
                RETURN c.id as id, c.name as name
                LIMIT 5
            """)
            print("\nSAMPLE COMPONENTS (First 5):")
            print("-" * 70)
            components = list(result)
            if components:
                for i, record in enumerate(components, 1):
                    print(f"{i}. [{record['id']}] {record['name']}")
            else:
                print("  WARNING: No components found!")

            # 9. Sample TextChunks with embeddings
            result = session.run("""
                MATCH (tc:TextChunk)
                WHERE tc.embedding IS NOT NULL
                RETURN count(tc) as count
            """)
            embedding_count = result.single()["count"]
            print(f"\nTEXT CHUNKS WITH EMBEDDINGS: {embedding_count}")

            # 10. Check for traceability relationships
            result = session.run("""
                MATCH (req:Requirement)-[r:VERIFIES|IMPLEMENTED_BY|REFINED_TO]->()
                RETURN type(r) as rel_type, count(r) as count
            """)
            print("\nTRACEABILITY RELATIONSHIPS:")
            print("-" * 70)
            trace_rels = list(result)
            if trace_rels:
                for record in trace_rels:
                    print(f"  {record['rel_type']:30s} : {record['count']:6d}")
            else:
                print("  WARNING: No traceability relationships found!")

            # Summary
            print("\n" + "=" * 70)
            print("SUMMARY")
            print("=" * 70)
            print(f"Total Nodes: {total_nodes}")
            print(f"Total Relationships: {total_rels}")
            print(f"Text Chunks with Embeddings: {embedding_count}")
            print(f"Vector Indexes: {len(indexes)}")
            print(f"Constraints: {len(constraints)}")

            # Recommendations
            print("\n" + "=" * 70)
            print("RECOMMENDATIONS")
            print("=" * 70)

            if total_nodes < 1000:
                print("WARNING: Node count is lower than expected (~3,000)")
                print("   -> Consider running: python scripts/load_documents.py")
            else:
                print("OK: Node count looks good")

            if embedding_count == 0:
                print("WARNING: No embeddings found!")
                print("   -> Vector search will not work")
            else:
                print(f"OK: Embeddings present ({embedding_count} chunks)")

            if len(indexes) == 0:
                print("WARNING: No vector indexes found!")
                print("   -> Run: python src/neo4j_schema/create_schema.py")
            else:
                print(f"OK: Vector indexes configured ({len(indexes)})")

            if not trace_rels:
                print("WARNING: No traceability relationships found!")
                print("   -> Requirements traceability may not work")
            else:
                print("OK: Traceability relationships exist")

    finally:
        driver.close()


if __name__ == "__main__":
    check_neo4j_status()
