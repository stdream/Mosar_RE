"""Text chunking for large sections."""
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """Split long sections into chunks for better vector search."""

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        """
        Initialize chunker.

        Args:
            chunk_size: Target chunk size in tokens (approximate)
            overlap: Overlap between chunks in tokens
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_sections(self, sections: List[Dict]) -> List[Dict]:
        """
        Split sections into chunks if they exceed chunk_size.

        Args:
            sections: List of section dicts

        Returns:
            List of section/chunk dicts
        """
        logger.info(f"Chunking sections (chunk_size={self.chunk_size}, overlap={self.overlap})...")

        chunked_sections = []

        for sec in sections:
            content = sec.get('content', '')

            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            estimated_tokens = len(content) // 4

            if estimated_tokens <= self.chunk_size:
                # Section is small enough, keep as is
                chunked_sections.append(sec)
            else:
                # Split into chunks
                chunks = self._split_text(content, sec)
                chunked_sections.extend(chunks)

        logger.info(f"✓ Expanded {len(sections)} sections into {len(chunked_sections)} chunks")
        return chunked_sections

    def _split_text(self, text: str, section: Dict) -> List[Dict]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to split
            section: Original section dict

        Returns:
            List of chunk dicts
        """
        chunks = []

        # Character-based chunking (approx 4 chars = 1 token)
        char_chunk_size = self.chunk_size * 4
        char_overlap = self.overlap * 4

        # Split by sentences first for cleaner breaks
        sentences = re.split(r'(?<=[.!?])\s+', text)

        current_chunk = ""
        chunk_idx = 0

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= char_chunk_size:
                current_chunk += sentence + " "
            else:
                # Save current chunk
                if current_chunk.strip():
                    chunks.append(self._create_chunk_dict(
                        section, current_chunk.strip(), chunk_idx
                    ))
                    chunk_idx += 1

                # Start new chunk with overlap
                if char_overlap > 0 and current_chunk:
                    # Take last N characters as overlap
                    overlap_text = current_chunk[-char_overlap:]
                    current_chunk = overlap_text + sentence + " "
                else:
                    current_chunk = sentence + " "

        # Save last chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk_dict(
                section, current_chunk.strip(), chunk_idx
            ))

        return chunks

    def _create_chunk_dict(self, section: Dict, chunk_text: str, chunk_idx: int) -> Dict:
        """
        Create a chunk dictionary from section.

        Args:
            section: Original section dict
            chunk_text: Chunk content
            chunk_idx: Chunk index

        Returns:
            Chunk dict
        """
        return {
            "id": f"{section['id']}_chunk_{chunk_idx}",
            "doc_id": section['doc_id'],
            "number": section.get('number', ''),
            "title": f"{section.get('title', '')} (Part {chunk_idx + 1})",
            "level": section.get('level', 1),
            "content": chunk_text,
            "chapter": section.get('chapter', ''),
            "parent_section_id": section['id'],  # Link to original section
            "chunk_index": chunk_idx
        }


if __name__ == "__main__":
    # Test chunker
    logging.basicConfig(level=logging.INFO)

    chunker = TextChunker(chunk_size=500, overlap=100)

    # Create test section
    long_text = " ".join([f"Sentence {i} about MOSAR technology." for i in range(200)])
    test_section = {
        "id": "PDD-3.2",
        "doc_id": "PDD",
        "number": "3.2",
        "title": "System Architecture",
        "level": 2,
        "content": long_text,
        "chapter": "3"
    }

    print(f"\nOriginal section length: {len(test_section['content'])} chars")
    print(f"Estimated tokens: {len(test_section['content']) // 4}")

    chunks = chunker._split_text(test_section['content'], test_section)

    print(f"\nGenerated {len(chunks)} chunks:")
    for chunk in chunks:
        print(f"  {chunk['id']}: {len(chunk['content'])} chars ({len(chunk['content']) // 4} tokens)")
