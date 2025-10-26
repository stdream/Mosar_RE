"""System Requirements Document parser."""
import re
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SRDParser:
    """Parse System Requirements Document (table format)."""

    def __init__(self):
        """Initialize parser."""
        self.requirements = []

    def parse(self, file_path: Path) -> List[Dict]:
        """
        Extract requirements from SRD markdown.

        Returns:
            List of requirement dicts with fields:
            - id: e.g., "FuncR_S101"
            - title: e.g., "Satellite repair and update"
            - statement: Full requirement text
            - level: Mandatory/Desirable/Optional
            - covers: Referenced requirements/documents
            - comment: Additional notes
            - type: e.g., "FuncR"
            - subsystem: e.g., "S" (Space), "A" (System), "B" (WM)
        """
        logger.info(f"Parsing SRD file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all requirement IDs in the document
        # Pattern: FuncR_S101, PerfR_A201, SafR_B301, etc.
        req_pattern = re.compile(
            r'\|\s*([A-Z][a-z]+R_[A-Z]\d+)\s*\|(.+?)\|(.*?)\|',
            re.MULTILINE
        )

        matches = req_pattern.finditer(content)

        for match in matches:
            req_id = match.group(1).strip()
            title = match.group(2).strip()
            level = match.group(3).strip()

            # Find the requirement block (everything until the next requirement or section)
            req_start = match.start()

            # Find the end of this requirement block
            # Look for the next requirement ID or a page separator
            next_req_match = req_pattern.search(content, match.end())
            page_separator = content.find('{', match.end())

            if next_req_match and page_separator != -1:
                req_end = min(next_req_match.start(), page_separator)
            elif next_req_match:
                req_end = next_req_match.start()
            elif page_separator != -1:
                req_end = page_separator
            else:
                req_end = len(content)

            req_block = content[req_start:req_end]

            # Parse the requirement block
            req_data = self._parse_requirement_block(req_id, title, level, req_block)
            if req_data:
                self.requirements.append(req_data)

        logger.info(f"✓ Parsed {len(self.requirements)} requirements from SRD")
        return self.requirements

    def _parse_requirement_block(
        self,
        req_id: str,
        title: str,
        level: str,
        block: str
    ) -> Optional[Dict]:
        """
        Parse individual requirement block.

        Args:
            req_id: Requirement ID (e.g., "FuncR_S101")
            title: Requirement title
            level: Mandatory/Desirable/Optional
            block: Text block containing the requirement details

        Returns:
            Dictionary with requirement data
        """
        req = {
            "id": req_id,
            "title": title,
            "level": level,
            "statement": "",
            "covers": "",
            "comment": "",
            "verification": "",
            "responsible": ""
        }

        # Extract STATEMENT field
        statement_match = re.search(
            r'\|\s*STATEMENT\s*\|(.*?)(?=\|\s*(?:COVERS|VERIFICATION|COMMENT|$))',
            block,
            re.DOTALL | re.MULTILINE
        )
        if statement_match:
            statement = statement_match.group(1).strip()
            # Clean up table formatting
            statement = re.sub(r'\|', '', statement)
            statement = re.sub(r'<br>', ' ', statement)
            statement = re.sub(r'\s+', ' ', statement)
            req['statement'] = statement.strip()

        # Extract COVERS field
        covers_match = re.search(
            r'\|\s*COVERS\s*\|(.*?)(?=\|\s*(?:COMMENT|VERIFICATION|$))',
            block,
            re.DOTALL | re.MULTILINE
        )
        if covers_match:
            covers = covers_match.group(1).strip()
            covers = re.sub(r'\|', '', covers)
            covers = re.sub(r'<br>', ' ', covers)
            covers = re.sub(r'\s+', ' ', covers)
            req['covers'] = covers.strip()

        # Extract VERIFICATION field
        verification_match = re.search(
            r'\|\s*VERIFICATION\s*\|(.*?)(?=\|\s*(?:COVERS|COMMENT|$))',
            block,
            re.DOTALL | re.MULTILINE
        )
        if verification_match:
            verification = verification_match.group(1).strip()
            verification = re.sub(r'\|', '', verification)
            verification = re.sub(r'<br>', ' ', verification)
            verification = re.sub(r'\s+', ' ', verification)
            req['verification'] = verification.strip()

        # Extract COMMENT field
        comment_match = re.search(
            r'\|\s*COMMENT\s*\|(.*?)$',
            block,
            re.DOTALL | re.MULTILINE
        )
        if comment_match:
            comment = comment_match.group(1).strip()
            comment = re.sub(r'\|', '', comment)
            comment = re.sub(r'<br>', ' ', comment)
            comment = re.sub(r'\s+', ' ', comment)
            req['comment'] = comment.strip()

        # Infer type and subsystem from ID
        # Format: TypeR_SubsystemNumber (e.g., FuncR_S101)
        if '_' in req_id:
            req_type, rest = req_id.split('_', 1)
            req['type'] = req_type  # e.g., "FuncR"

            # Extract subsystem letter
            subsystem_match = re.match(r'([A-Z])', rest)
            if subsystem_match:
                req['subsystem'] = subsystem_match.group(1)  # e.g., "S", "A", "B"
            else:
                req['subsystem'] = ""
        else:
            req['type'] = ""
            req['subsystem'] = ""

        # Only return if we have a statement (core requirement)
        if req['statement']:
            return req
        else:
            logger.warning(f"Skipping {req_id}: No statement found")
            return None

    def get_statistics(self) -> Dict:
        """
        Get parsing statistics.

        Returns:
            Dictionary with statistics
        """
        if not self.requirements:
            return {
                "total": 0,
                "by_type": {},
                "by_subsystem": {},
                "by_level": {}
            }

        # Count by type
        by_type = {}
        for req in self.requirements:
            req_type = req.get('type', 'Unknown')
            by_type[req_type] = by_type.get(req_type, 0) + 1

        # Count by subsystem
        by_subsystem = {}
        for req in self.requirements:
            subsystem = req.get('subsystem', 'Unknown')
            by_subsystem[subsystem] = by_subsystem.get(subsystem, 0) + 1

        # Count by level
        by_level = {}
        for req in self.requirements:
            level = req.get('level', 'Unknown')
            by_level[level] = by_level.get(level, 0) + 1

        return {
            "total": len(self.requirements),
            "by_type": by_type,
            "by_subsystem": by_subsystem,
            "by_level": by_level
        }


if __name__ == "__main__":
    # Test the parser
    logging.basicConfig(level=logging.INFO)

    srd_path = Path(__file__).parents[2] / "Documents/SRD/System Requirements Document_MOSAR.md"

    if not srd_path.exists():
        print(f"❌ SRD file not found: {srd_path}")
    else:
        parser = SRDParser()
        requirements = parser.parse(srd_path)

        print(f"\n✅ Parsed {len(requirements)} requirements")

        stats = parser.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total: {stats['total']}")
        print(f"  By Type: {stats['by_type']}")
        print(f"  By Subsystem: {stats['by_subsystem']}")
        print(f"  By Level: {stats['by_level']}")

        # Show first few requirements
        print(f"\nFirst 3 requirements:")
        for req in requirements[:3]:
            print(f"\n  {req['id']}: {req['title']}")
            print(f"    Type: {req['type']}, Subsystem: {req['subsystem']}, Level: {req['level']}")
            print(f"    Statement: {req['statement'][:100]}...")
