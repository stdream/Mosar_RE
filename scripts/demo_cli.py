"""
Demo script to show CLI capabilities without interactive input.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graphrag.app import GraphRAGCLI

def demo():
    """Run CLI demo with pre-defined queries."""
    cli = GraphRAGCLI()

    # Show banner
    cli.show_banner()

    # Show help
    print("\n\n=== Testing /help command ===")
    cli.show_help()

    # Process a sample query
    print("\n\n=== Testing sample query ===")
    test_questions = [
        "Show all requirements verified by R-ICU",
    ]

    for question in test_questions:
        print(f"\n\nProcessing: {question}")
        cli.process_query(question)

    # Show history
    print("\n\n=== Testing /history command ===")
    cli.show_history()

    # Show stats
    print("\n\n=== Testing /stats command ===")
    cli.show_stats()

    print("\n\nCLI Demo Complete!")

if __name__ == "__main__":
    demo()
