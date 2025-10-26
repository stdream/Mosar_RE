"""
MOSAR GraphRAG CLI - Interactive Command-Line Interface

Rich-powered beautiful CLI for querying the MOSAR GraphRAG system.
"""

import sys
import os
import uuid
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich import box

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.graphrag.workflow import GraphRAGWorkflow
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Console (force UTF-8 encoding for Windows)
try:
    console = Console(force_terminal=True, legacy_windows=False)
except:
    console = Console()


class GraphRAGCLI:
    """
    Interactive CLI for MOSAR GraphRAG system.

    Features:
    - Rich formatted output
    - Session management
    - Query history
    - Syntax highlighting for Cypher queries
    - Citation display
    """

    def __init__(self):
        """Initialize CLI."""
        self.workflow = GraphRAGWorkflow()
        self.session_id = str(uuid.uuid4())[:8]
        self.user_id = "cli-user"
        self.query_count = 0
        self.history = []

    def show_banner(self):
        """Display welcome banner."""
        banner = """
[bold cyan]================================================================[/bold cyan]
[bold white]          MOSAR GraphRAG System - Interactive CLI[/bold white]
[bold cyan]================================================================[/bold cyan]

[dim]Modular Spacecraft Assembly and Reconfiguration[/dim]
[dim]Knowledge Graph Query System[/dim]

[yellow]Session ID:[/yellow] [cyan]{session_id}[/cyan]
[yellow]Ready to answer questions about:[/yellow]
  - System Requirements (227 requirements)
  - Design Documents (PDD, DDD, 515 sections)
  - Test Cases (45 test cases)
  - Components, Protocols, and Traceability

[bold green]Type your question or:[/bold green]
  [cyan]/help[/cyan]    - Show help
  [cyan]/history[/cyan] - Show query history
  [cyan]/stats[/cyan]   - Show session statistics
  [cyan]/clear[/cyan]   - Clear screen
  [cyan]/exit[/cyan]    - Exit CLI

[bold cyan]================================================================[/bold cyan]
        """.format(session_id=self.session_id)

        console.print(banner)

    def show_help(self):
        """Display help information."""
        help_text = """[bold cyan]Available Commands:[/bold cyan]

[yellow]Questions:[/yellow]
  Just type your question in natural language (Korean or English)

  Examples:
    - Show all requirements verified by R-ICU
    - 어떤 하드웨어가 네트워크 통신을 담당하나요?
    - What are the main challenges in orbital assembly?
    - FuncR_S110의 traceability를 보여줘

[yellow]Commands:[/yellow]
  [cyan]/help[/cyan]     - Show this help message
  [cyan]/history[/cyan]  - Show query history for this session
  [cyan]/stats[/cyan]    - Show session statistics
  [cyan]/clear[/cyan]    - Clear the console screen
  [cyan]/exit[/cyan]     - Exit the CLI (or Ctrl+C)

[yellow]Query Paths:[/yellow]
  [green]Path A (Pure Cypher)[/green]   - Direct graph queries for known entities
  [blue]Path B (Hybrid)[/blue]         - Vector search + NER + Cypher
  [magenta]Path C (Pure Vector)[/magenta]  - Semantic search for exploratory questions
"""
        console.print("[cyan]" + "="*60 + "[/cyan]")
        console.print(help_text)
        console.print("[cyan]" + "="*60 + "[/cyan]")

    def show_history(self):
        """Display query history."""
        if not self.history:
            console.print("[yellow]No queries in this session yet.[/yellow]")
            return

        table = Table(title="Query History", box=box.ROUNDED)
        table.add_column("#", style="cyan", width=4)
        table.add_column("Question", style="white", width=50)
        table.add_column("Path", style="green", width=12)
        table.add_column("Time (ms)", style="yellow", width=10)
        table.add_column("Status", style="magenta", width=10)

        for i, item in enumerate(self.history, 1):
            status = "[green]OK[/green]" if not item.get("error") else "[red]ERR[/red]"
            question = item["question"][:47] + "..." if len(item["question"]) > 50 else item["question"]

            table.add_row(
                str(i),
                question,
                item["path"],
                f"{item['time']:.0f}",
                status
            )

        console.print(table)

    def show_stats(self):
        """Display session statistics."""
        if not self.history:
            console.print("[yellow]No queries in this session yet.[/yellow]")
            return

        total_queries = len(self.history)
        successful_queries = sum(1 for q in self.history if not q.get("error"))
        failed_queries = total_queries - successful_queries
        avg_time = sum(q["time"] for q in self.history) / total_queries

        # Path distribution
        path_counts = {}
        for q in self.history:
            path = q["path"]
            path_counts[path] = path_counts.get(path, 0) + 1

        stats_text = f"""[bold cyan]Session Statistics[/bold cyan]

[yellow]Session ID:[/yellow] {self.session_id}
[yellow]Total Queries:[/yellow] {total_queries}
[yellow]Successful:[/yellow] [green]{successful_queries}[/green]
[yellow]Failed:[/yellow] [red]{failed_queries}[/red]
[yellow]Average Response Time:[/yellow] {avg_time:.0f} ms

[bold cyan]Query Path Distribution:[/bold cyan]
{self._format_path_stats(path_counts)}
"""
        console.print("[cyan]" + "="*60 + "[/cyan]")
        console.print(stats_text)
        console.print("[cyan]" + "="*60 + "[/cyan]")

    def _format_path_stats(self, path_counts):
        """Format path statistics."""
        lines = []
        for path, count in path_counts.items():
            bar = "#" * (count * 2)
            lines.append(f"  [cyan]{path:15s}[/cyan] {bar} [yellow]{count}[/yellow]")
        return "\n".join(lines) if lines else "  [dim]No data[/dim]"

    def display_result(self, result: dict, question: str):
        """
        Display query result in rich format.

        Args:
            result: Result dict from workflow
            question: Original question
        """
        metadata = result.get("metadata", {})

        # Header
        console.print("\n[bold cyan]" + "="*63 + "[/bold cyan]")

        # Question
        console.print(f"[bold yellow]Question:[/bold yellow] {question}")

        # Metadata table
        meta_table = Table(show_header=False, box=None, padding=(0, 1))
        meta_table.add_column("Key", style="cyan")
        meta_table.add_column("Value", style="white")

        meta_table.add_row("Query Path", self._format_path(metadata.get("query_path", "unknown")))
        meta_table.add_row("Confidence", f"{metadata.get('routing_confidence', 0):.2f}")
        meta_table.add_row("Language", metadata.get("language", "unknown"))
        meta_table.add_row("Processing Time", f"{metadata.get('processing_time_ms', 0):.0f} ms")

        if metadata.get("matched_entities"):
            entities_str = ", ".join([
                f"{k}: {v}" for k, v in metadata["matched_entities"].items()
            ])
            meta_table.add_row("Matched Entities", entities_str[:60])

        console.print(meta_table)
        console.print()

        # Answer
        console.print("\n[bold green]Answer:[/bold green]")
        console.print("[green]" + "="*60 + "[/green]")
        # Use plain text instead of Markdown to avoid Windows encoding issues
        answer_text = result.get("answer", "No answer available")
        console.print(answer_text, markup=False, highlight=False)
        console.print("[green]" + "="*60 + "[/green]")

        # Citations
        citations = result.get("citations", [])
        if citations:
            console.print(f"\n[bold cyan]Citations[/bold cyan] ([dim]{len(citations)} sources[/dim]):")
            for i, citation in enumerate(citations[:5], 1):
                if isinstance(citation, dict):
                    source = citation.get("source", "Unknown")
                    ctype = citation.get("type", "unknown")
                    console.print(f"  [{i}] [cyan]{ctype}[/cyan]: {source}")
                else:
                    console.print(f"  [{i}] {citation}")

        # Cypher Query (if available)
        if metadata.get("cypher_query"):
            console.print(f"\n[bold cyan]Cypher Query:[/bold cyan]")
            syntax = Syntax(
                metadata["cypher_query"],
                "cypher",
                theme="monokai",
                line_numbers=False,
                word_wrap=True
            )
            console.print(syntax)

        # Error (if any)
        if metadata.get("error"):
            console.print(f"\n[bold red]Error:[/bold red] {metadata['error']}")

        console.print("[bold cyan]" + "="*63 + "[/bold cyan]\n")

    def _format_path(self, path: str) -> str:
        """Format query path with color."""
        if path == "pure_cypher":
            return "[green]Path A (Pure Cypher)[/green]"
        elif path == "hybrid":
            return "[blue]Path B (Hybrid)[/blue]"
        elif path == "pure_vector":
            return "[magenta]Path C (Pure Vector)[/magenta]"
        else:
            return f"[dim]{path}[/dim]"

    def process_query(self, question: str):
        """
        Process a user query.

        Args:
            question: User's question
        """
        self.query_count += 1

        # Show processing message (no spinner to avoid encoding issues)
        console.print("[bold green]Processing query...[/bold green]")

        try:
            result = self.workflow.query(
                question,
                session_id=self.session_id,
                user_id=self.user_id
            )

            # Record in history
            self.history.append({
                "question": question,
                "path": result["metadata"].get("query_path", "unknown"),
                "time": result["metadata"].get("processing_time_ms", 0),
                "error": result["metadata"].get("error")
            })

            # Display result
            self.display_result(result, question)

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            self.history.append({
                "question": question,
                "path": "error",
                "time": 0,
                "error": str(e)
            })

    def run(self):
        """Main CLI loop."""
        self.show_banner()

        while True:
            try:
                # Get user input
                user_input = Prompt.ask(
                    f"\n[bold cyan][Q{self.query_count + 1}][/bold cyan]",
                    default=""
                ).strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                    if Confirm.ask("\n[yellow]Are you sure you want to exit?[/yellow]"):
                        console.print("\n[bold cyan]Thank you for using MOSAR GraphRAG![/bold cyan]")
                        console.print(f"[dim]Session: {self.session_id} | Queries: {self.query_count}[/dim]\n")
                        break
                    else:
                        continue

                elif user_input.lower() == "/help":
                    self.show_help()

                elif user_input.lower() == "/history":
                    self.show_history()

                elif user_input.lower() == "/stats":
                    self.show_stats()

                elif user_input.lower() == "/clear":
                    console.clear()
                    self.show_banner()

                else:
                    # Process as query
                    self.process_query(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use /exit to quit gracefully[/yellow]")
                continue

            except Exception as e:
                console.print(f"\n[bold red]Unexpected error:[/bold red] {e}")
                continue


def main():
    """Entry point for CLI."""
    try:
        cli = GraphRAGCLI()
        cli.run()
    except Exception as e:
        console.print(f"[bold red]Fatal error:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
