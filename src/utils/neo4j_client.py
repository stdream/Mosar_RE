"""Neo4j database client."""
import os
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j database connection and query execution."""

    def __init__(self):
        """Initialize Neo4j driver from environment variables."""
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            self.driver.verify_connectivity()
            logger.info(f"✓ Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        """Close the Neo4j driver connection."""
        if self.driver:
            self.driver.close()
            logger.info("✓ Neo4j connection closed")

    def execute(self, cypher: str, **params) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return results.

        Args:
            cypher: Cypher query string
            **params: Query parameters

        Returns:
            List of result dictionaries
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(cypher, **params)
            return [record.data() for record in result]

    def query(self, cypher: str, **params) -> List[Dict[str, Any]]:
        """
        Alias for execute() method.

        Args:
            cypher: Cypher query string
            **params: Query parameters

        Returns:
            List of result dictionaries
        """
        return self.execute(cypher, **params)

    def write_transaction(self, cypher: str, **params) -> List[Dict[str, Any]]:
        """
        Execute a write transaction.

        Args:
            cypher: Cypher query string
            **params: Query parameters

        Returns:
            List of result dictionaries
        """
        with self.driver.session(database=self.database) as session:
            result = session.execute_write(
                lambda tx: list(tx.run(cypher, **params))
            )
            return [record.data() for record in result]

    def verify_connection(self) -> bool:
        """
        Verify database connection is working.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.driver.verify_connectivity()
            result = self.execute("RETURN 1 AS test")
            return len(result) > 0 and result[0]["test"] == 1
        except Exception as e:
            logger.error(f"Connection verification failed: {e}")
            return False

    def get_constraints(self) -> List[str]:
        """
        Get all constraints in the database.

        Returns:
            List of constraint names
        """
        result = self.execute("SHOW CONSTRAINTS")
        return [record["name"] for record in result]

    def get_indexes(self) -> List[str]:
        """
        Get all indexes in the database.

        Returns:
            List of index names
        """
        result = self.execute("SHOW INDEXES")
        return [record["name"] for record in result]

    def count_nodes(self, label: Optional[str] = None) -> int:
        """
        Count nodes in the database.

        Args:
            label: Optional node label to filter

        Returns:
            Node count
        """
        if label:
            cypher = f"MATCH (n:{label}) RETURN count(n) AS count"
        else:
            cypher = "MATCH (n) RETURN count(n) AS count"

        result = self.execute(cypher)
        return result[0]["count"] if result else 0

    def count_relationships(self, rel_type: Optional[str] = None) -> int:
        """
        Count relationships in the database.

        Args:
            rel_type: Optional relationship type to filter

        Returns:
            Relationship count
        """
        if rel_type:
            cypher = f"MATCH ()-[r:{rel_type}]->() RETURN count(r) AS count"
        else:
            cypher = "MATCH ()-[r]->() RETURN count(r) AS count"

        result = self.execute(cypher)
        return result[0]["count"] if result else 0


# Singleton instance
_client = None


def get_client() -> Neo4jClient:
    """
    Get or create singleton Neo4j client.

    Returns:
        Neo4jClient instance
    """
    global _client
    if _client is None:
        _client = Neo4jClient()
    return _client


if __name__ == "__main__":
    # Test connection
    logging.basicConfig(level=logging.INFO)
    client = Neo4jClient()

    if client.verify_connection():
        print("✅ Neo4j connection successful!")
        print(f"Nodes: {client.count_nodes()}")
        print(f"Relationships: {client.count_relationships()}")
    else:
        print("❌ Neo4j connection failed!")

    client.close()
