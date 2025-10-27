"""
Unified Document Loader for MOSAR GraphRAG System

Loads all MOSAR documents into Neo4j in the correct order:
1. System Requirements (SRD)
2. Design Documents (PDD + DDD)
3. Demonstration Procedures (Test Cases)

Usage:
    python scripts/load_documents.py [--skip-srd] [--skip-design] [--skip-demo]

Environment Variables Required:
    - NEO4J_URI
    - NEO4J_USER
    - NEO4J_PASSWORD
    - OPENAI_API_KEY
"""

import sys
import logging
import time
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ingestion.srd_parser import SRDParser
from src.ingestion.design_doc_parser import DesignDocParser
from src.ingestion.demo_procedure_parser import DemoProcedureParser
from src.ingestion.embedder import DocumentEmbedder
from src.ingestion.neo4j_loader import MOSARGraphLoader
from src.utils.neo4j_client import Neo4jClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Use ASCII-only output for Windows compatibility
console = Console()


class DocumentLoadManager:
    """Manages the complete document loading pipeline."""

    def __init__(self):
        """Initialize parsers and loaders."""
        self.srd_parser = SRDParser()
        self.design_parser = DesignDocParser()
        self.demo_parser = DemoProcedureParser()
        self.embedder = DocumentEmbedder()
        self.loader = MOSARGraphLoader()

        # Document paths
        self.docs_dir = project_root / "Documents"
        self.srd_path = self.docs_dir / "SRD" / "System Requirements Document_MOSAR.md"
        self.pdd_path = self.docs_dir / "PDD" / "MOSAR-WP2-D2.4-SA_1.1.0-Preliminary-Design-Document.md"
        self.ddd_path = self.docs_dir / "DDD" / "MOSAR-WP3-D3.6-SA_1.2.0-Detailed-Design-Document.md"
        self.demo_path = self.docs_dir / "Demo" / "MOSAR-WP3-D3.5-DLR_1.1.0-Demonstration-Procedures.md"

        # Statistics
        self.stats = {
            "requirements": 0,
            "sections": 0,
            "test_cases": 0,
            "embeddings": 0,
            "errors": 0
        }

    def verify_environment(self):
        """Verify Neo4j connection and required files."""
        console.print("\n[bold cyan]Verifying Environment...[/bold cyan]")

        # Check Neo4j connection
        try:
            client = Neo4jClient()
            client.close()
            console.print("[OK] Neo4j connection successful", style="green")
        except Exception as e:
            console.print(f"[ERROR] Neo4j connection failed: {e}", style="red")
            raise

        # Check document files
        missing_files = []
        for path in [self.srd_path, self.pdd_path, self.ddd_path, self.demo_path]:
            if not path.exists():
                missing_files.append(str(path))
            else:
                console.print(f"[OK] Found: {path.name}", style="green")

        if missing_files:
            console.print(f"\n[red][ERROR] Missing files:[/red]")
            for f in missing_files:
                console.print(f"  - {f}", style="red")
            raise FileNotFoundError(f"Missing {len(missing_files)} document files")

        console.print("\n[bold green][OK] Environment verification complete[/bold green]\n")

    def load_srd(self):
        """Load System Requirements Document."""
        console.print("\n" + "="*60, style="cyan")
        console.print("[bold cyan]Step 1: Loading System Requirements (SRD)[/bold cyan]")
        console.print("="*60, style="cyan")

        try:
            with console.status("[bold green]Parsing SRD..."):
                requirements = self.srd_parser.parse(self.srd_path)
                self.stats["requirements"] = len(requirements)

            console.print(f"[OK] Parsed {len(requirements)} requirements", style="green")

            with console.status("[bold green]Generating embeddings..."):
                requirements_with_embeddings = self.embedder.embed_requirements(requirements)
                self.stats["embeddings"] += len(requirements)

            console.print(f"[OK] Generated {len(requirements)} requirement embeddings", style="green")

            with console.status("[bold green]Loading to Neo4j..."):
                self.loader.load_requirements(requirements_with_embeddings)

            console.print(f"[OK] Loaded {len(requirements)} requirements to Neo4j", style="green")

        except Exception as e:
            console.print(f"[ERROR] SRD loading failed: {e}", style="red")
            self.stats["errors"] += 1
            raise

    def load_design_docs(self):
        """Load PDD and DDD design documents."""
        console.print("\n" + "="*60, style="cyan")
        console.print("[bold cyan]Step 2: Loading Design Documents (PDD + DDD)[/bold cyan]")
        console.print("="*60, style="cyan")

        try:
            # Parse PDD
            with console.status("[bold green]Parsing PDD..."):
                pdd_parser = DesignDocParser(doc_type="PDD")
                pdd_sections = pdd_parser.parse(self.pdd_path)
                console.print(f"[OK] Parsed {len(pdd_sections)} PDD sections", style="green")

            # Parse DDD
            with console.status("[bold green]Parsing DDD..."):
                ddd_parser = DesignDocParser(doc_type="DDD")
                ddd_sections = ddd_parser.parse(self.ddd_path)
                console.print(f"[OK] Parsed {len(ddd_sections)} DDD sections", style="green")

            all_sections = pdd_sections + ddd_sections
            self.stats["sections"] = len(all_sections)

            # Generate embeddings
            with console.status("[bold green]Generating embeddings..."):
                sections_with_embeddings = self.embedder.embed_sections(all_sections)
                self.stats["embeddings"] += len(sections_with_embeddings)

            console.print(f"[OK] Generated {len(sections_with_embeddings)} section embeddings", style="green")

            # Load PDD sections
            with console.status("[bold green]Loading PDD to Neo4j..."):
                pdd_sections_with_emb = [s for s in sections_with_embeddings if s.get("doc_type") == "PDD"]
                self.loader.load_design_sections(pdd_sections_with_emb, doc_type="PDD")

            # Load DDD sections
            with console.status("[bold green]Loading DDD to Neo4j..."):
                ddd_sections_with_emb = [s for s in sections_with_embeddings if s.get("doc_type") == "DDD"]
                self.loader.load_design_sections(ddd_sections_with_emb, doc_type="DDD")

            console.print(f"[OK] Loaded {len(all_sections)} design sections to Neo4j", style="green")

        except Exception as e:
            console.print(f"[ERROR] Design documents loading failed: {e}", style="red")
            self.stats["errors"] += 1
            raise

    def load_demo_procedures(self):
        """Load Demonstration Procedures (test cases)."""
        console.print("\n" + "="*60, style="cyan")
        console.print("[bold cyan]Step 3: Loading Demonstration Procedures (Test Cases)[/bold cyan]")
        console.print("="*60, style="cyan")

        try:
            with console.status("[bold green]Parsing Demo Procedures..."):
                test_cases = self.demo_parser.parse(self.demo_path)
                self.stats["test_cases"] = len(test_cases)

            console.print(f"[OK] Parsed {len(test_cases)} test cases", style="green")

            with console.status("[bold green]Loading to Neo4j..."):
                self.loader.load_test_cases(test_cases)

            console.print(f"[OK] Loaded {len(test_cases)} test cases to Neo4j", style="green")

        except Exception as e:
            console.print(f"[ERROR] Demo procedures loading failed: {e}", style="red")
            self.stats["errors"] += 1
            raise

    def print_summary(self, elapsed_time: float):
        """Print loading summary."""
        console.print("\n" + "="*60, style="green")
        console.print("[bold green]Loading Complete![/bold green]")
        console.print("="*60, style="green")

        table = Table(title="Loading Summary", show_header=True, header_style="bold cyan")
        table.add_column("Item", style="cyan")
        table.add_column("Count", justify="right", style="green")

        table.add_row("Requirements", str(self.stats["requirements"]))
        table.add_row("Design Sections", str(self.stats["sections"]))
        table.add_row("Test Cases", str(self.stats["test_cases"]))
        table.add_row("Embeddings Generated", str(self.stats["embeddings"]))
        table.add_row("Errors", str(self.stats["errors"]), style="red" if self.stats["errors"] > 0 else "green")
        table.add_row("Total Time", f"{elapsed_time:.1f}s", style="yellow")

        console.print(table)

        # Next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. Verify data loaded correctly:")
        console.print("   [cyan]python scripts/check_phase2_criteria.py[/cyan]")
        console.print("\n2. Test the GraphRAG workflow:")
        console.print("   [cyan]python src/graphrag/app.py[/cyan]")
        console.print("\n3. Run E2E tests:")
        console.print("   [cyan]pytest tests/test_e2e.py -v -m e2e[/cyan]")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Load MOSAR documents into Neo4j")
    parser.add_argument("--skip-srd", action="store_true", help="Skip SRD loading")
    parser.add_argument("--skip-design", action="store_true", help="Skip design documents loading")
    parser.add_argument("--skip-demo", action="store_true", help="Skip demo procedures loading")
    args = parser.parse_args()

    # Print header
    console.print(Panel.fit(
        "[bold cyan]MOSAR GraphRAG Document Loader[/bold cyan]\n"
        "Loads System Requirements, Design Documents, and Test Cases",
        border_style="cyan"
    ))

    manager = DocumentLoadManager()

    try:
        # Verify environment
        manager.verify_environment()

        start_time = time.time()

        # Load documents in order
        if not args.skip_srd:
            manager.load_srd()
        else:
            console.print("\n[yellow]⚠ Skipping SRD loading[/yellow]")

        if not args.skip_design:
            manager.load_design_docs()
        else:
            console.print("\n[yellow]⚠ Skipping Design Documents loading[/yellow]")

        if not args.skip_demo:
            manager.load_demo_procedures()
        else:
            console.print("\n[yellow]⚠ Skipping Demo Procedures loading[/yellow]")

        elapsed_time = time.time() - start_time

        # Print summary
        manager.print_summary(elapsed_time)

        if manager.stats["errors"] > 0:
            console.print("\n[yellow]⚠ Loading completed with errors[/yellow]")
            sys.exit(1)
        else:
            console.print("\n[bold green][OK] All documents loaded successfully![/bold green]")
            sys.exit(0)

    except Exception as e:
        console.print(f"\n[bold red][ERROR] Fatal error: {e}[/bold red]")
        logger.exception("Fatal error during document loading")
        sys.exit(1)


if __name__ == "__main__":
    main()
