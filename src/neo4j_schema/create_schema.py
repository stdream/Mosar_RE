"""Neo4j schema creation script."""
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[2]))

from src.utils.neo4j_client import Neo4jClient

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_schema():
    """Execute schema.cypher to create constraints and indexes."""
    logger.info("=== MOSAR GraphRAG Schema Creation ===\n")

    try:
        client = Neo4jClient()
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
        logger.error("\nPlease ensure:")
        logger.error("1. Neo4j is running (Docker or Desktop)")
        logger.error("2. .env file is configured with correct credentials")
        logger.error("3. NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD are set")
        return False

    schema_file = Path(__file__).parent / "schema.cypher"

    if not schema_file.exists():
        logger.error(f"Schema file not found: {schema_file}")
        return False

    logger.info(f"Reading schema from: {schema_file}")

    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_cypher = f.read()

    # Split by semicolon or double newline (separate statements)
    # Cypher statements are separated by semicolons or blank lines
    statements = []
    current_statement = []

    for line in schema_cypher.split('\n'):
        line = line.strip()

        # Skip empty lines and comments when starting new statement
        if not line or line.startswith('//'):
            if current_statement:
                statements.append('\n'.join(current_statement))
                current_statement = []
            continue

        current_statement.append(line)

    # Add last statement
    if current_statement:
        statements.append('\n'.join(current_statement))

    logger.info(f"\nFound {len(statements)} statements to execute\n")

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, statement in enumerate(statements, 1):
        if not statement.strip():
            continue

        try:
            # Extract statement type for better logging
            stmt_type = "UNKNOWN"
            if "CREATE CONSTRAINT" in statement:
                stmt_type = "CONSTRAINT"
            elif "CREATE VECTOR INDEX" in statement:
                stmt_type = "VECTOR INDEX"
            elif "CREATE FULLTEXT INDEX" in statement:
                stmt_type = "FULLTEXT INDEX"
            elif "CREATE INDEX" in statement:
                stmt_type = "INDEX"

            client.execute(statement)
            success_count += 1
            logger.info(f"✓ [{i}/{len(statements)}] Created {stmt_type}")

        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg or "Equivalent" in error_msg:
                skip_count += 1
                logger.warning(f"⊙ [{i}/{len(statements)}] {stmt_type} already exists (skipped)")
            else:
                error_count += 1
                logger.error(f"✗ [{i}/{len(statements)}] Failed to create {stmt_type}: {e}")

    logger.info("\n=== Schema Creation Summary ===")
    logger.info(f"✓ Successfully created: {success_count}")
    logger.info(f"⊙ Already existed: {skip_count}")
    logger.info(f"✗ Errors: {error_count}")

    # Verify constraints and indexes
    logger.info("\n=== Verification ===")
    try:
        constraints = client.get_constraints()
        indexes = client.get_indexes()

        logger.info(f"Total constraints: {len(constraints)}")
        logger.info(f"Total indexes: {len(indexes)}")

        logger.info("\nConstraints:")
        for constraint in constraints:
            logger.info(f"  - {constraint}")

        logger.info("\nIndexes:")
        for index in indexes:
            logger.info(f"  - {index}")

    except Exception as e:
        logger.error(f"Verification failed: {e}")

    client.close()

    if error_count == 0:
        logger.info("\n✅ Schema creation completed successfully!")
        return True
    else:
        logger.warning(f"\n⚠ Schema creation completed with {error_count} errors")
        return False


if __name__ == "__main__":
    success = create_schema()
    sys.exit(0 if success else 1)
