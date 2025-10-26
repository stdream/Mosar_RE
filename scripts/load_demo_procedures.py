"""Load Demo Procedures test cases to Neo4j."""
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.ingestion.demo_procedure_parser import DemoProcedureParser
from src.ingestion.neo4j_loader import MOSARGraphLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Load Demo Procedures pipeline."""
    print("\n" + "="*70)
    print("MOSAR GraphRAG - Demo Procedures Loading Pipeline")
    print("="*70 + "\n")

    # File paths
    demo_path = Path(__file__).parents[1] / "Documents/Demo/MOSAR-WP3-D3.5-DLR_1.1.0-Demonstration-Procedures.md"

    if not demo_path.exists():
        print(f"❌ Demo Procedures file not found: {demo_path}")
        return

    # Step 1: Parse Demo Procedures
    print("Step 1/2: Parsing Demo Procedures")
    print("-" * 70)
    parser = DemoProcedureParser()
    test_cases = parser.parse(demo_path)

    stats = parser.get_statistics()
    print(f"\nParsing Statistics:")
    print(f"  Total test cases: {stats['total']}")
    print(f"  By type: {stats['by_type']}")
    print(f"  With covered requirements: {stats['with_requirements']}")

    # Step 2: Load to Neo4j
    print("\n\nStep 2/2: Loading to Neo4j")
    print("-" * 70)
    loader = MOSARGraphLoader()
    loader.load_test_cases(test_cases)

    # Show final statistics
    print("\n\nNeo4j Statistics:")
    print("-" * 70)
    neo4j_stats = loader.get_statistics()

    print("\nNodes:")
    for label, count in neo4j_stats["nodes"].items():
        print(f"  {label}: {count}")

    print("\nRelationships:")
    for rel_type, count in neo4j_stats["relationships"].items():
        print(f"  {rel_type}: {count}")

    loader.close()

    print("\n" + "="*70)
    print("SUCCESS: Demo Procedures loading complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
