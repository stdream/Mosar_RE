"""
HITL (Human-in-the-Loop) Module for GraphRAG

Allows human review and correction of:
1. Entity extraction results
2. Cypher query generation
3. Final answers before presentation

Usage in CLI:
- Set HITL_ENABLED=true in .env
- System will pause for approval at key decision points
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()


class HITLStage(Enum):
    """Stages where HITL intervention can occur."""
    ENTITY_EXTRACTION = "entity_extraction"
    CYPHER_GENERATION = "cypher_generation"
    FINAL_ANSWER = "final_answer"


class HITLManager:
    """Manages human-in-the-loop interactions."""

    def __init__(self, enabled: bool = False):
        """
        Initialize HITL manager.

        Args:
            enabled: Whether HITL is enabled (from .env or config)
        """
        self.enabled = enabled
        self.corrections = []  # Track corrections for learning

    def review_entities(
        self,
        user_question: str,
        extracted_entities: Dict[str, List[str]]
    ) -> Tuple[Dict[str, List[str]], bool]:
        """
        Review and correct extracted entities.

        Args:
            user_question: User's original question
            extracted_entities: Entities extracted by NER

        Returns:
            Tuple of (corrected_entities, approved)
        """
        if not self.enabled:
            return extracted_entities, True

        console.print("\n" + "="*60, style="yellow")
        console.print("🤔 HITL: Entity Extraction Review", style="bold yellow")
        console.print("="*60, style="yellow")

        console.print(f"\n[bold]Question:[/bold] {user_question}")

        # Display extracted entities
        if extracted_entities:
            table = Table(title="Extracted Entities", show_header=True)
            table.add_column("Type", style="cyan")
            table.add_column("Entities", style="green")

            for entity_type, entities in extracted_entities.items():
                table.add_row(entity_type, ", ".join(entities))

            console.print(table)
        else:
            console.print("\n[yellow]No entities extracted[/yellow]")

        # Ask for approval
        console.print("\n[bold]Options:[/bold]")
        console.print("  [1] Approve (continue)")
        console.print("  [2] Edit entities")
        console.print("  [3] Skip HITL for this query")

        choice = console.input("\n[yellow]Your choice (1-3):[/yellow] ").strip()

        if choice == "1":
            logger.info("HITL: Entities approved")
            return extracted_entities, True

        elif choice == "2":
            corrected_entities = self._edit_entities(extracted_entities)
            self._record_correction(HITLStage.ENTITY_EXTRACTION, {
                "original": extracted_entities,
                "corrected": corrected_entities
            })
            return corrected_entities, True

        elif choice == "3":
            logger.info("HITL: Skipped for this query")
            return extracted_entities, True

        else:
            console.print("[red]Invalid choice, using original entities[/red]")
            return extracted_entities, True

    def review_cypher(
        self,
        user_question: str,
        cypher_query: str,
        entities: Dict[str, List[str]]
    ) -> Tuple[str, bool]:
        """
        Review and correct generated Cypher query.

        Args:
            user_question: User's original question
            cypher_query: Generated Cypher query
            entities: Entities used in query generation

        Returns:
            Tuple of (corrected_query, approved)
        """
        if not self.enabled:
            return cypher_query, True

        console.print("\n" + "="*60, style="yellow")
        console.print("🔍 HITL: Cypher Query Review", style="bold yellow")
        console.print("="*60, style="yellow")

        console.print(f"\n[bold]Question:[/bold] {user_question}")
        console.print(f"\n[bold]Entities:[/bold] {entities}")

        # Display Cypher query with syntax highlighting
        console.print("\n[bold]Generated Cypher Query:[/bold]")
        syntax = Syntax(cypher_query, "cypher", theme="monokai", line_numbers=True)
        console.print(syntax)

        # Ask for approval
        console.print("\n[bold]Options:[/bold]")
        console.print("  [1] Approve (execute query)")
        console.print("  [2] Edit query")
        console.print("  [3] Reject (use vector search only)")

        choice = console.input("\n[yellow]Your choice (1-3):[/yellow] ").strip()

        if choice == "1":
            logger.info("HITL: Cypher query approved")
            return cypher_query, True

        elif choice == "2":
            corrected_query = self._edit_cypher(cypher_query)
            self._record_correction(HITLStage.CYPHER_GENERATION, {
                "original": cypher_query,
                "corrected": corrected_query,
                "entities": entities
            })
            return corrected_query, True

        elif choice == "3":
            logger.info("HITL: Cypher query rejected")
            return "", False  # Empty query = fall back to vector only

        else:
            console.print("[red]Invalid choice, using original query[/red]")
            return cypher_query, True

    def review_answer(
        self,
        user_question: str,
        final_answer: str,
        citations: Optional[List[Dict[str, str]]]
    ) -> Tuple[str, bool]:
        """
        Review and correct final answer before presentation.

        Args:
            user_question: User's original question
            final_answer: Generated answer
            citations: Source citations

        Returns:
            Tuple of (corrected_answer, approved)
        """
        if not self.enabled:
            return final_answer, True

        console.print("\n" + "="*60, style="yellow")
        console.print("📝 HITL: Final Answer Review", style="bold yellow")
        console.print("="*60, style="yellow")

        console.print(f"\n[bold]Question:[/bold] {user_question}")

        # Display answer
        console.print("\n[bold]Generated Answer:[/bold]")
        console.print(Panel(final_answer, border_style="blue"))

        # Display citations
        if citations:
            console.print("\n[bold]Citations:[/bold]")
            for i, citation in enumerate(citations, 1):
                console.print(f"  [{i}] {citation}")

        # Ask for approval
        console.print("\n[bold]Options:[/bold]")
        console.print("  [1] Approve (show to user)")
        console.print("  [2] Edit answer")
        console.print("  [3] Regenerate (try different path)")

        choice = console.input("\n[yellow]Your choice (1-3):[/yellow] ").strip()

        if choice == "1":
            logger.info("HITL: Answer approved")
            return final_answer, True

        elif choice == "2":
            corrected_answer = self._edit_answer(final_answer)
            self._record_correction(HITLStage.FINAL_ANSWER, {
                "original": final_answer,
                "corrected": corrected_answer
            })
            return corrected_answer, True

        elif choice == "3":
            logger.info("HITL: Answer rejected, requesting regeneration")
            return final_answer, False

        else:
            console.print("[red]Invalid choice, using original answer[/red]")
            return final_answer, True

    def _edit_entities(
        self,
        entities: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        """
        Interactive entity editing.

        Args:
            entities: Original entities

        Returns:
            Corrected entities
        """
        console.print("\n[bold]Entity Editing Mode[/bold]")
        console.print("Format: EntityType: entity1, entity2, ...")
        console.print("Example: Component: R-ICU, WM")
        console.print("(Press Enter with empty line to finish)\n")

        corrected = {}

        for entity_type in ["Component", "Requirement", "TestCase", "Protocol", "Scenario"]:
            current = entities.get(entity_type, [])
            current_str = ", ".join(current) if current else ""

            console.print(f"\n[cyan]{entity_type}:[/cyan] [{current_str}]")
            new_value = console.input("  New value (or Enter to keep): ").strip()

            if new_value:
                corrected[entity_type] = [e.strip() for e in new_value.split(",")]
            elif current:
                corrected[entity_type] = current

        return corrected

    def _edit_cypher(self, original_query: str) -> str:
        """
        Interactive Cypher query editing.

        Args:
            original_query: Original Cypher query

        Returns:
            Corrected Cypher query
        """
        console.print("\n[bold]Cypher Query Editing Mode[/bold]")
        console.print("Enter corrected query (end with empty line):\n")

        lines = []
        console.print("[dim](Original query shown above. Type your corrections below)[/dim]")

        while True:
            line = console.input()
            if line.strip() == "":
                break
            lines.append(line)

        corrected_query = "\n".join(lines)

        if not corrected_query.strip():
            console.print("[yellow]No changes made, using original query[/yellow]")
            return original_query

        return corrected_query

    def _edit_answer(self, original_answer: str) -> str:
        """
        Interactive answer editing.

        Args:
            original_answer: Original answer

        Returns:
            Corrected answer
        """
        console.print("\n[bold]Answer Editing Mode[/bold]")
        console.print("Enter corrected answer (end with '---' on new line):\n")

        lines = []
        while True:
            line = console.input()
            if line.strip() == "---":
                break
            lines.append(line)

        corrected_answer = "\n".join(lines)

        if not corrected_answer.strip():
            console.print("[yellow]No changes made, using original answer[/yellow]")
            return original_answer

        return corrected_answer

    def _record_correction(
        self,
        stage: HITLStage,
        correction_data: Dict[str, Any]
    ):
        """
        Record a correction for future learning.

        Args:
            stage: HITL stage where correction occurred
            correction_data: Correction details
        """
        self.corrections.append({
            "stage": stage.value,
            "data": correction_data
        })

        logger.info(f"HITL correction recorded at stage: {stage.value}")

    def get_correction_stats(self) -> Dict[str, Any]:
        """
        Get statistics about HITL corrections.

        Returns:
            Statistics dict
        """
        stats = {
            "total_corrections": len(self.corrections),
            "by_stage": {}
        }

        for stage in HITLStage:
            count = sum(1 for c in self.corrections if c["stage"] == stage.value)
            stats["by_stage"][stage.value] = count

        return stats

    def export_corrections(self, filepath: str):
        """
        Export corrections to JSON file for analysis.

        Args:
            filepath: Output file path
        """
        import json

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "corrections": self.corrections,
                "stats": self.get_correction_stats()
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"HITL corrections exported to {filepath}")


# Singleton instance
_hitl_manager: Optional[HITLManager] = None


def get_hitl_manager(enabled: Optional[bool] = None) -> HITLManager:
    """
    Get or create HITL manager singleton.

    Args:
        enabled: Override enabled state (reads from env if None)

    Returns:
        HITLManager instance
    """
    global _hitl_manager

    if _hitl_manager is None:
        if enabled is None:
            import os
            enabled = os.getenv("HITL_ENABLED", "false").lower() == "true"

        _hitl_manager = HITLManager(enabled=enabled)

    return _hitl_manager
