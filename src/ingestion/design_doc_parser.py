"""Parser for PDD and DDD documents."""
import re
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DesignDocParser:
    """Parse Preliminary/Detailed Design Documents (section-based)."""

    def __init__(self, doc_type: str = "PDD"):
        """
        Initialize parser.

        Args:
            doc_type: "PDD" or "DDD"
        """
        self.doc_type = doc_type
        self.sections = []

    def parse(self, file_path: Path) -> List[Dict]:
        """
        Extract sections from design document.

        Returns:
            List of section dicts with fields:
            - id: Unique section ID (e.g., "PDD-2.1")
            - doc_id: Document type ("PDD" or "DDD")
            - number: Section number (e.g., "2.1")
            - title: Section title
            - level: Section level (1, 2, 3, etc.)
            - content: Section content text
            - chapter: Main chapter number
        """
        logger.info(f"Parsing {self.doc_type} file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all sections with headers
        # Pattern: ## Section Title or ### Subsection Title
        # Also match numbered sections: 2.1, 3.2.1, etc.

        # Split by page separators first
        pages = content.split('{')

        section_pattern = re.compile(
            r'^#+\s+(.+?)$|'  # Markdown headers
            r'^\s*(\d+(?:\.\d+)*)\s+(.+?)$',  # Numbered sections
            re.MULTILINE
        )

        for page in pages:
            matches = section_pattern.finditer(page)

            for match in matches:
                if match.group(1):  # Markdown header
                    header_text = match.group(1).strip()
                    level = page[match.start():match.start()+10].count('#')

                    # Try to extract number from header
                    number_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)', header_text)
                    if number_match:
                        number = number_match.group(1)
                        title = number_match.group(2)
                    else:
                        number = ""
                        title = header_text

                elif match.group(2):  # Numbered section
                    number = match.group(2).strip()
                    title = match.group(3).strip()
                    level = number.count('.') + 1
                else:
                    continue

                # Extract content (everything until next section)
                content_start = match.end()
                next_match = section_pattern.search(page, content_start)

                if next_match:
                    content_end = next_match.start()
                else:
                    content_end = len(page)

                section_content = page[content_start:content_end].strip()

                # Clean content
                section_content = self._clean_content(section_content)

                # Skip very short sections (likely TOC or page numbers)
                if len(section_content) < 50:
                    continue

                # Create section dict
                section_id = f"{self.doc_type}-{number}" if number else f"{self.doc_type}-{title[:20]}"
                chapter = number.split('.')[0] if '.' in number else number

                section = {
                    "id": section_id,
                    "doc_id": self.doc_type,
                    "number": number,
                    "title": title,
                    "level": level,
                    "content": section_content,
                    "chapter": chapter
                }

                self.sections.append(section)

        # Remove duplicates by ID
        seen = set()
        unique_sections = []
        for sec in self.sections:
            if sec['id'] not in seen:
                seen.add(sec['id'])
                unique_sections.append(sec)

        self.sections = unique_sections

        logger.info(f"✓ Parsed {len(self.sections)} sections from {self.doc_type}")
        return self.sections

    def _clean_content(self, text: str) -> str:
        """
        Clean section content.

        Args:
            text: Raw section text

        Returns:
            Cleaned text
        """
        # Remove image references
        text = re.sub(r'!\[\]\([^)]+\)', '', text)

        # Remove page separators
        text = re.sub(r'\{\d+\}[-]+', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # Remove table formatting artifacts
        text = re.sub(r'\|[-:]+\|', '', text)

        return text.strip()

    def get_statistics(self) -> Dict:
        """
        Get parsing statistics.

        Returns:
            Dictionary with statistics
        """
        if not self.sections:
            return {
                "total": 0,
                "by_level": {},
                "by_chapter": {},
                "avg_content_length": 0
            }

        # Count by level
        by_level = {}
        for sec in self.sections:
            level = sec.get('level', 0)
            by_level[level] = by_level.get(level, 0) + 1

        # Count by chapter
        by_chapter = {}
        for sec in self.sections:
            chapter = sec.get('chapter', 'Unknown')
            by_chapter[chapter] = by_chapter.get(chapter, 0) + 1

        # Average content length
        total_length = sum(len(sec.get('content', '')) for sec in self.sections)
        avg_length = total_length // len(self.sections) if self.sections else 0

        return {
            "total": len(self.sections),
            "by_level": by_level,
            "by_chapter": by_chapter,
            "avg_content_length": avg_length
        }


if __name__ == "__main__":
    # Test the parser
    logging.basicConfig(level=logging.INFO)

    # Test PDD
    print("=== Testing PDD Parser ===\n")
    pdd_path = Path(__file__).parents[2] / "Documents/PDD/MOSAR-WP2-D2.4-SA_1.1.0-Preliminary-Design-Document.md"

    if pdd_path.exists():
        parser = DesignDocParser("PDD")
        sections = parser.parse(pdd_path)

        print(f"Parsed {len(sections)} sections")

        stats = parser.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total: {stats['total']}")
        print(f"  By level: {stats['by_level']}")
        print(f"  Avg content length: {stats['avg_content_length']} chars")

        # Show first few sections
        print(f"\nFirst 3 sections:")
        for sec in sections[:3]:
            print(f"\n  [{sec['id']}] {sec['title']}")
            print(f"    Level: {sec['level']}, Chapter: {sec['chapter']}")
            print(f"    Content: {sec['content'][:100]}...")
    else:
        print(f"PDD file not found: {pdd_path}")

    # Test DDD
    print("\n\n=== Testing DDD Parser ===\n")
    ddd_path = Path(__file__).parents[2] / "Documents/DDD/MOSAR-WP3-D3.6-SA_1.2.0-Detailed-Design-Document.md"

    if ddd_path.exists():
        parser = DesignDocParser("DDD")
        sections = parser.parse(ddd_path)

        print(f"Parsed {len(sections)} sections")

        stats = parser.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total: {stats['total']}")
        print(f"  By level: {stats['by_level']}")
        print(f"  Avg content length: {stats['avg_content_length']} chars")
    else:
        print(f"DDD file not found: {ddd_path}")
