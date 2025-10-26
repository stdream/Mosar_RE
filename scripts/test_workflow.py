"""
Test GraphRAG Workflow - Phase 3 Validation

Tests all 3 query paths with sample questions in Korean and English.
"""

import sys
import os
import logging
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graphrag.workflow import GraphRAGWorkflow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_result(query: str, result: dict, query_num: int):
    """
    Pretty print query result.

    Args:
        query: Original question
        result: Result dict from workflow
        query_num: Query number
    """
    print("\n" + "="*100)
    print(f"[Query {query_num}] {query}")
    print("="*100)

    # Metadata
    metadata = result.get("metadata", {})
    print(f"\n[Metadata]")
    print(f"  - Path: {metadata.get('query_path', 'unknown')}")
    print(f"  - Routing Confidence: {metadata.get('routing_confidence', 0):.2f}")
    print(f"  - Language: {metadata.get('language', 'unknown')}")
    print(f"  - Processing Time: {metadata.get('processing_time_ms', 0):.0f}ms")

    if metadata.get('matched_entities'):
        print(f"  - Matched Entities: {metadata['matched_entities']}")

    if metadata.get('extracted_entities'):
        print(f"  - Extracted Entities (NER): {metadata['extracted_entities']}")

    if metadata.get('error'):
        print(f"  - Error: {metadata['error']}")

    # Answer
    print(f"\n[Answer]")
    print("-" * 100)
    print(result.get("answer", "No answer"))
    print("-" * 100)

    # Citations
    citations = result.get("citations", [])
    if citations:
        print(f"\n[Citations] ({len(citations)} sources)")
        for i, citation in enumerate(citations[:5], 1):
            if isinstance(citation, dict):
                citation_str = json.dumps(citation, ensure_ascii=False)
            else:
                citation_str = str(citation)
            print(f"  [{i}] {citation_str}")

    # Cypher Query (if available)
    if metadata.get('cypher_query'):
        print(f"\n[Cypher Query]")
        print("```cypher")
        print(metadata['cypher_query'])
        print("```")


def run_phase3_tests():
    """
    Run comprehensive Phase 3 tests.

    Tests all 3 query paths with various question types.
    """
    print("="*100)
    print("PHASE 3 TEST - GraphRAG Hybrid Query Workflow")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("="*100)

    # Initialize workflow
    logger.info("Initializing GraphRAGWorkflow...")
    workflow = GraphRAGWorkflow()
    logger.info("Workflow initialized successfully")

    # Test queries organized by path
    test_queries = {
        "Path A - Pure Cypher (High Confidence Entity Match)": [
            "Show all requirements verified by R-ICU",
            "FuncR_S110의 traceability를 보여줘",
            "What test cases verify requirement SafR_A201?",
            "CT-A-1 테스트는 어떤 요구사항을 검증하나요?",
        ],
        "Path B - Hybrid (Vector + NER + Cypher)": [
            "어떤 하드웨어가 네트워크 통신을 담당하나요?",
            "What hardware handles network communication?",
            "How does the Service Module handle real-time communication?",
            "R-ICU의 역할은 무엇인가요?",
            "Which components use CAN protocol?",
        ],
        "Path C - Pure Vector (Exploratory)": [
            "What are the main challenges in orbital assembly?",
            "Explain the MOSAR system architecture",
            "우주에서 모듈형 조립의 장점은 무엇인가요?",
        ]
    }

    # Execute tests
    total_queries = sum(len(queries) for queries in test_queries.values())
    query_num = 0
    success_count = 0
    error_count = 0

    for path_name, queries in test_queries.items():
        print("\n\n" + "="*100)
        print(f"Testing: {path_name}")
        print("="*100)

        for query in queries:
            query_num += 1

            try:
                logger.info(f"Executing query {query_num}/{total_queries}: {query[:50]}...")
                result = workflow.query(query)

                print_result(query, result, query_num)

                if not result["metadata"].get("error"):
                    success_count += 1
                else:
                    error_count += 1

            except Exception as e:
                logger.error(f"Query {query_num} failed: {e}", exc_info=True)
                print(f"\n[ERROR] Error executing query: {e}")
                error_count += 1

    # Summary
    print("\n\n" + "="*100)
    print("TEST SUMMARY")
    print("="*100)
    print(f"Total Queries: {total_queries}")
    print(f"[SUCCESS] Successful: {success_count}")
    print(f"[ERROR] Errors: {error_count}")
    print(f"Success Rate: {success_count / total_queries * 100:.1f}%")
    print("="*100)

    return success_count, error_count


def run_quick_test():
    """
    Quick test with 3 representative queries (one per path).
    """
    print("="*100)
    print("QUICK TEST - GraphRAG Workflow (One query per path)")
    print("="*100)

    workflow = GraphRAGWorkflow()

    quick_queries = [
        ("Path A", "Show all requirements verified by R-ICU"),
        ("Path B", "어떤 하드웨어가 네트워크 통신을 담당하나요?"),
        ("Path C", "What are the main challenges in orbital assembly?")
    ]

    for i, (path, query) in enumerate(quick_queries, 1):
        print(f"\n\n[{path}] {query}")
        print("-" * 100)

        try:
            result = workflow.query(query)
            print(f"[SUCCESS]")
            print(f"Path: {result['metadata'].get('query_path')}")
            print(f"Processing Time: {result['metadata'].get('processing_time_ms', 0):.0f}ms")
            print(f"Answer preview: {result['answer'][:200]}...")

        except Exception as e:
            print(f"[ERROR] {e}")

    print("\n" + "="*100)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test GraphRAG Workflow")
    parser.add_argument("--quick", action="store_true", help="Run quick test (3 queries)")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    args = parser.parse_args()

    if args.quick:
        run_quick_test()
    elif args.full:
        run_phase3_tests()
    else:
        # Default: run full tests
        run_phase3_tests()
