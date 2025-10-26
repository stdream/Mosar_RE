"""Load SRD (System Requirements Document) into Neo4j."""
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.ingestion.srd_parser import SRDParser
from src.ingestion.embedder import DocumentEmbedder
from src.ingestion.neo4j_loader import MOSARGraphLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Load SRD requirements into Neo4j with embeddings."""
    logger.info("="*60)
    logger.info("MOSAR GraphRAG - SRD Loading Pipeline")
    logger.info("="*60)

    # Step 1: Parse SRD
    logger.info("\n[Step 1/4] Parsing SRD document...")
    srd_path = Path(__file__).parents[1] / "Documents/SRD/System Requirements Document_MOSAR.md"

    if not srd_path.exists():
        logger.error(f"SRD file not found: {srd_path}")
        return 1

    parser = SRDParser()
    requirements = parser.parse(srd_path)

    stats = parser.get_statistics()
    logger.info(f"\nParsing Statistics:")
    logger.info(f"  Total requirements: {stats['total']}")
    logger.info(f"  By type: {stats['by_type']}")
    logger.info(f"  By subsystem: {stats['by_subsystem']}")
    logger.info(f"  By level: {stats['by_level']}")

    if not requirements:
        logger.error("No requirements parsed!")
        return 1

    # Step 2: Generate embeddings
    logger.info("\n[Step 2/4] Generating embeddings with OpenAI...")
    try:
        embedder = DocumentEmbedder()
        requirements = embedder.embed_requirements(requirements)
        logger.info("✓ Embeddings generated successfully")
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        logger.warning("Continuing without embeddings (will use null vectors)")
        # Add null embeddings
        for req in requirements:
            req['statement_embedding'] = [0.0] * 3072

    # Step 3: Load into Neo4j
    logger.info("\n[Step 3/4] Loading requirements into Neo4j...")
    try:
        loader = MOSARGraphLoader()
        loader.load_requirements(requirements)
        logger.info("✓ Requirements loaded successfully")

        # Step 4: Show statistics
        logger.info("\n[Step 4/4] Neo4j Database Statistics:")
        stats = loader.get_statistics()

        for category, items in stats.items():
            logger.info(f"\n  {category.upper()}:")
            for name, count in items.items():
                logger.info(f"    {name}: {count}")

        loader.close()

    except Exception as e:
        logger.error(f"Failed to load into Neo4j: {e}")
        import traceback
        traceback.print_exc()
        return 1

    logger.info("\n" + "="*60)
    logger.info("✅ SRD Loading Complete!")
    logger.info("="*60)
    logger.info(f"\nLoaded {len(requirements)} requirements into Neo4j Aura")
    logger.info("\nNext steps:")
    logger.info("  1. Verify data in Neo4j Browser: https://console.neo4j.io")
    logger.info("  2. Run sample queries to test the graph")
    logger.info("  3. Continue with Phase 2: PDD/DDD parsers")

    return 0


if __name__ == "__main__":
    sys.exit(main())
