"""
Live CLI test - Simulates user interaction
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graphrag.app import GraphRAGCLI

def test_live_queries():
    """Test CLI with simulated user queries."""
    cli = GraphRAGCLI()

    # Show banner
    cli.show_banner()

    print("\n" + "="*80)
    print("LIVE CLI TEST - Processing Real Queries")
    print("="*80)

    # Test queries
    test_queries = [
        "Show all requirements verified by R-ICU",
        "What are the main challenges in orbital assembly?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*80}")
        print(f"TEST QUERY {i}/{len(test_queries)}")
        print(f"{'='*80}")
        print(f"Question: {query}")
        print("-"*80)

        cli.process_query(query)

    # Show final statistics
    print("\n\n" + "="*80)
    print("FINAL SESSION SUMMARY")
    print("="*80)

    cli.show_history()
    print()
    cli.show_stats()

    print("\n\n" + "="*80)
    print("CLI Test Complete!")
    print(f"Session ID: {cli.session_id}")
    print(f"Total Queries Processed: {cli.query_count}")
    print("="*80)

if __name__ == "__main__":
    test_live_queries()
