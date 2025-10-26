"""Load PDD and DDD design documents to Neo4j."""
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from src.ingestion.design_doc_parser import DesignDocParser
from src.ingestion.text_chunker import TextChunker
from src.ingestion.embedder import DocumentEmbedder
from src.ingestion.neo4j_loader import MOSARGraphLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Load PDD and DDD pipeline."""
    print("\n" + "="*70)
    print("MOSAR GraphRAG - Design Documents Loading Pipeline")
    print("="*70 + "\n")

    # File paths
    pdd_path = Path(__file__).parents[1] / "Documents/PDD/MOSAR-WP2-D2.4-SA_1.1.0-Preliminary-Design-Document.md"
    ddd_path = Path(__file__).parents[1] / "Documents/DDD/MOSAR-WP3-D3.6-SA_1.2.0-Detailed-Design-Document.md"

    # Initialize
    chunker = TextChunker(chunk_size=240, overlap=50)  # Tuned for 500+ target
    embedder = DocumentEmbedder()
    loader = MOSARGraphLoader()

    total_sections = 0

    # Process PDD
    if pdd_path.exists():
        print("="*70)
        print("PART 1: Preliminary Design Document (PDD)")
        print("="*70 + "\n")

        print("Step 1/4: Parsing PDD")
        print("-" * 70)
        pdd_parser = DesignDocParser("PDD")
        pdd_sections = pdd_parser.parse(pdd_path)

        stats = pdd_parser.get_statistics()
        print(f"\nParsing Statistics:")
        print(f"  Total sections: {stats['total']}")
        print(f"  By level: {stats['by_level']}")
        print(f"  Avg content length: {stats['avg_content_length']} chars")

        print("\n\nStep 2/4: Chunking large sections")
        print("-" * 70)
        pdd_sections = chunker.chunk_sections(pdd_sections)
        print(f"  After chunking: {len(pdd_sections)} sections/chunks")

        print("\n\nStep 3/4: Generating embeddings for PDD sections")
        print("-" * 70)
        pdd_sections = embedder.embed_sections(pdd_sections)

        print("\n\nStep 4/4: Loading PDD to Neo4j")
        print("-" * 70)
        loader.load_design_sections(pdd_sections, "PDD")

        total_sections += len(pdd_sections)
    else:
        print(f"PDD file not found: {pdd_path}")

    # Process DDD
    if ddd_path.exists():
        print("\n\n" + "="*70)
        print("PART 2: Detailed Design Document (DDD)")
        print("="*70 + "\n")

        print("Step 1/4: Parsing DDD")
        print("-" * 70)
        ddd_parser = DesignDocParser("DDD")
        ddd_sections = ddd_parser.parse(ddd_path)

        stats = ddd_parser.get_statistics()
        print(f"\nParsing Statistics:")
        print(f"  Total sections: {stats['total']}")
        print(f"  By level: {stats['by_level']}")
        print(f"  Avg content length: {stats['avg_content_length']} chars")

        print("\n\nStep 2/4: Chunking large sections")
        print("-" * 70)
        ddd_sections = chunker.chunk_sections(ddd_sections)
        print(f"  After chunking: {len(ddd_sections)} sections/chunks")

        print("\n\nStep 3/4: Generating embeddings for DDD sections")
        print("-" * 70)
        ddd_sections = embedder.embed_sections(ddd_sections)

        print("\n\nStep 4/4: Loading DDD to Neo4j")
        print("-" * 70)
        loader.load_design_sections(ddd_sections, "DDD")

        total_sections += len(ddd_sections)
    else:
        print(f"DDD file not found: {ddd_path}")

    # Show final statistics
    print("\n\n" + "="*70)
    print("FINAL STATISTICS")
    print("="*70 + "\n")

    print("Neo4j Graph Statistics:")
    print("-" * 70)
    neo4j_stats = loader.get_statistics()

    print("\nNodes:")
    for label, count in neo4j_stats["nodes"].items():
        print(f"  {label}: {count}")

    print("\nRelationships:")
    for rel_type, count in neo4j_stats["relationships"].items():
        print(f"  {rel_type}: {count}")

    loader.close()

    print("\n" + "="*70)
    print(f"SUCCESS: Loaded {total_sections} design document sections!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
