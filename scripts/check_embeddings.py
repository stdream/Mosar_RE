"""Check if embeddings exist in Neo4j."""
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


def check_embeddings():
    """Check embeddings in Neo4j."""

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            print("="* 70)
            print("EMBEDDING STATUS CHECK")
            print("=" * 70)

            # Check Requirement embeddings
            result = session.run("""
                MATCH (r:Requirement)
                WHERE r.statement_embedding IS NOT NULL
                RETURN count(r) as count
            """)
            req_count = result.single()["count"]
            print(f"\nRequirements with embeddings: {req_count}")

            # Check Section embeddings
            result = session.run("""
                MATCH (s:Section)
                WHERE s.content_embedding IS NOT NULL
                RETURN count(s) as count
            """)
            sec_count = result.single()["count"]
            print(f"Sections with embeddings: {sec_count}")

            # Check TextChunk existence
            result = session.run("""
                MATCH (tc:TextChunk)
                RETURN count(tc) as count
            """)
            chunk_count = result.single()["count"]
            print(f"TextChunks: {chunk_count}")

            # Check Component embeddings
            result = session.run("""
                MATCH (c:Component)
                WHERE c.name_embedding IS NOT NULL
                RETURN count(c) as count
            """)
            comp_count = result.single()["count"]
            print(f"Components with embeddings: {comp_count}")

            # Sample embedding to verify dimension
            result = session.run("""
                MATCH (r:Requirement)
                WHERE r.statement_embedding IS NOT NULL
                RETURN r.id as id, size(r.statement_embedding) as dim
                LIMIT 1
            """)
            sample = result.single()
            if sample:
                print(f"\nSample embedding dimension: {sample['dim']} (expected: 3072)")
                print(f"Sample requirement: {sample['id']}")

            print("\n" + "=" * 70)
            print("SUMMARY")
            print("=" * 70)
            if req_count > 0 or sec_count > 0:
                print("OK: Embeddings are present in the database")
                print(f"  - Requirements: {req_count}")
                print(f"  - Sections: {sec_count}")
                print(f"  - Components: {comp_count}")
                if chunk_count > 0:
                    print(f"  - TextChunks: {chunk_count}")
            else:
                print("WARNING: No embeddings found!")
                print("  -> Vector search will not work")

    finally:
        driver.close()


if __name__ == "__main__":
    check_embeddings()
