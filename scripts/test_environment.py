"""Test environment setup for Phase 0."""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.utils.neo4j_client import Neo4jClient
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def test_neo4j():
    """Test Neo4j connection."""
    logger.info("=== Testing Neo4j Connection ===")
    try:
        client = Neo4jClient()

        if client.verify_connection():
            logger.info("✓ Neo4j connection successful")

            # Get statistics
            nodes = client.count_nodes()
            rels = client.count_relationships()
            constraints = len(client.get_constraints())
            indexes = len(client.get_indexes())

            logger.info(f"  - Nodes: {nodes}")
            logger.info(f"  - Relationships: {rels}")
            logger.info(f"  - Constraints: {constraints}")
            logger.info(f"  - Indexes: {indexes}")

            client.close()
            return True
        else:
            logger.error("✗ Neo4j connection failed")
            return False

    except Exception as e:
        logger.error(f"✗ Neo4j test failed: {e}")
        return False


def test_openai():
    """Test OpenAI API connection."""
    logger.info("\n=== Testing OpenAI API ===")
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "sk-your-key-here":
            logger.error("✗ OpenAI API key not configured in .env")
            return False

        client = OpenAI(api_key=api_key)

        # Test embedding
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input="test",
            dimensions=3072
        )

        embedding = response.data[0].embedding

        if len(embedding) == 3072:
            logger.info("✓ OpenAI API connection successful")
            logger.info(f"  - Model: text-embedding-3-large")
            logger.info(f"  - Embedding dimensions: {len(embedding)}")
            return True
        else:
            logger.error(f"✗ Unexpected embedding dimensions: {len(embedding)}")
            return False

    except Exception as e:
        logger.error(f"✗ OpenAI test failed: {e}")
        return False


def test_entity_dictionary():
    """Test Entity Dictionary loading."""
    logger.info("\n=== Testing Entity Dictionary ===")
    try:
        import json

        dict_path = Path(__file__).parents[1] / "data/entities/mosar_entities.json"

        if not dict_path.exists():
            logger.error(f"✗ Entity Dictionary not found: {dict_path}")
            return False

        with open(dict_path, 'r', encoding='utf-8') as f:
            entities = json.load(f)

        categories = list(entities.keys())
        total_entities = sum(len(v) for v in entities.values())

        logger.info("✓ Entity Dictionary loaded successfully")
        logger.info(f"  - Categories: {', '.join(categories)}")
        logger.info(f"  - Total entities: {total_entities}")

        return True

    except Exception as e:
        logger.error(f"✗ Entity Dictionary test failed: {e}")
        return False


def test_python_packages():
    """Test critical Python packages."""
    logger.info("\n=== Testing Python Packages ===")

    packages = [
        "neo4j",
        "openai",
        "langgraph",
        "langchain",
        "spacy",
        "pydantic",
        "python-dotenv",
        "rich"
    ]

    success = True
    for package in packages:
        try:
            if package == "python-dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            logger.info(f"✓ {package}")
        except ImportError:
            logger.error(f"✗ {package} not installed")
            success = False

    return success


def main():
    """Run all environment tests."""
    logger.info("╔════════════════════════════════════════╗")
    logger.info("║  MOSAR GraphRAG - Phase 0 Validation  ║")
    logger.info("╚════════════════════════════════════════╝\n")

    results = {
        "Python Packages": test_python_packages(),
        "Neo4j Connection": test_neo4j(),
        "OpenAI API": test_openai(),
        "Entity Dictionary": test_entity_dictionary()
    }

    logger.info("\n" + "="*50)
    logger.info("SUMMARY")
    logger.info("="*50)

    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{test:.<30} {status}")

    all_passed = all(results.values())

    if all_passed:
        logger.info("\n✅ Phase 0 Environment Setup Complete!")
        logger.info("\nNext steps:")
        logger.info("  1. Review QUICKSTART.md for Phase 1 instructions")
        logger.info("  2. Start document ingestion: python scripts/load_documents.py")
        return 0
    else:
        logger.info("\n❌ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
