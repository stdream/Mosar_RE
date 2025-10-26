"""Demonstration Procedures parser - extracts test cases."""
import re
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DemoProcedureParser:
    """Parse test cases from Demonstration Procedures document."""

    def __init__(self):
        """Initialize parser."""
        self.test_cases = []

    def parse(self, file_path: Path) -> List[Dict]:
        """
        Extract test cases and their covered requirements.

        Returns:
            List of test case dicts:
            - id: e.g., "CT-A-1", "IT1", "S1"
            - type: "Component Test", "Integration Test", "Scenario"
            - name: Test description
            - objective: What it tests
            - procedure: Test steps
            - covered_requirements: List of requirement IDs
        """
        logger.info(f"Parsing Demo Procedures file: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse Component Tests (CT-X-Y)
        self._parse_component_tests(content)

        # Parse Integration Tests (ITX)
        self._parse_integration_tests(content)

        # Parse Scenarios (S1, S2, S3, etc.)
        self._parse_scenarios(content)

        logger.info(f"✓ Parsed {len(self.test_cases)} test cases from Demo Procedures")
        return self.test_cases

    def _parse_component_tests(self, content: str):
        """Parse Component Tests (CT-X-Y format)."""
        # Pattern: | ID | CT-A-1 | Title | ... |
        ct_pattern = re.compile(
            r'\|\s*ID\s*\|\s*(CT-[A-Z]-\d+)\s*\|(?:\s*Title\s*\|)?\s*([^|]+)',
            re.IGNORECASE
        )

        for match in ct_pattern.finditer(content):
            tc_id = match.group(1).strip()
            tc_name = match.group(2).strip()

            # Find the test case block
            tc_start = match.start()
            # Look for next test case or section
            next_match = ct_pattern.search(content, match.end())
            section_sep = content.find('{', match.end())

            if next_match and section_sep != -1:
                tc_end = min(next_match.start(), section_sep)
            elif next_match:
                tc_end = next_match.start()
            elif section_sep != -1:
                tc_end = section_sep
            else:
                tc_end = match.end() + 2000  # Reasonable chunk size

            tc_block = content[tc_start:tc_end]

            # Extract covered requirements
            covered_reqs = self._extract_covered_requirements(tc_block)

            # Extract objective/purpose
            objective = self._extract_field(tc_block, 'Purpose|Expected Result|Objective')

            # Extract procedure
            procedure = self._extract_field(tc_block, 'Procedure')

            self.test_cases.append({
                "id": tc_id,
                "type": "Component Test",
                "name": tc_name,
                "objective": objective,
                "procedure": procedure,
                "covered_requirements": covered_reqs,
                "status": "Planned"
            })

    def _parse_integration_tests(self, content: str):
        """Parse Integration Tests (IT1, IT2, etc.)."""
        # Pattern: IT1, IT2, IT3 in headers or tables
        it_pattern = re.compile(
            r'(IT\d+)\s*[–-]\s*([^\n|]+)',
            re.IGNORECASE
        )

        for match in it_pattern.finditer(content):
            tc_id = match.group(1).strip()
            tc_name = match.group(2).strip()

            # Skip if already added
            if any(tc['id'] == tc_id for tc in self.test_cases):
                continue

            # Find the test case block
            tc_start = match.start()
            next_match = it_pattern.search(content, match.end())
            section_sep = content.find('{', match.end())

            if next_match and section_sep != -1:
                tc_end = min(next_match.start(), section_sep)
            elif next_match:
                tc_end = next_match.start()
            elif section_sep != -1:
                tc_end = section_sep
            else:
                tc_end = match.end() + 2000

            tc_block = content[tc_start:tc_end]

            # Extract covered requirements
            covered_reqs = self._extract_covered_requirements(tc_block)

            # Extract objective
            objective = self._extract_field(tc_block, 'Purpose|Objective|Description')

            # Extract procedure
            procedure = self._extract_field(tc_block, 'Procedure|Sequence')

            self.test_cases.append({
                "id": tc_id,
                "type": "Integration Test",
                "name": tc_name,
                "objective": objective,
                "procedure": procedure,
                "covered_requirements": covered_reqs,
                "status": "Planned"
            })

    def _parse_scenarios(self, content: str):
        """Parse Demonstration Scenarios (S1, S2, S3, etc.)."""
        # Pattern: Scenario 1 (S1): Description
        scenario_pattern = re.compile(
            r'Scenario\s+\d+\s*\(?(S\d+)\)?:\s*([^\n]+)',
            re.IGNORECASE
        )

        for match in scenario_pattern.finditer(content):
            tc_id = match.group(1).strip()
            tc_name = match.group(2).strip()

            # Skip if already added
            if any(tc['id'] == tc_id for tc in self.test_cases):
                continue

            # Find the scenario block
            tc_start = match.start()
            next_match = scenario_pattern.search(content, match.end())
            section_sep = content.find('{', match.end())

            if next_match and section_sep != -1:
                tc_end = min(next_match.start(), section_sep)
            elif next_match:
                tc_end = next_match.start()
            elif section_sep != -1:
                tc_end = section_sep
            else:
                tc_end = match.end() + 3000

            tc_block = content[tc_start:tc_end]

            # Extract covered requirements
            covered_reqs = self._extract_covered_requirements(tc_block)

            # Extract scenario description
            objective = self._extract_field(tc_block, 'Description|Scenario Description')

            # Extract sequence of operations
            procedure = self._extract_field(tc_block, 'Sequence of Operations|Procedure')

            self.test_cases.append({
                "id": tc_id,
                "type": "Scenario",
                "name": tc_name,
                "objective": objective if objective else tc_name,
                "procedure": procedure,
                "covered_requirements": covered_reqs,
                "status": "Planned"
            })

    def _extract_covered_requirements(self, text: str) -> List[str]:
        """
        Extract requirement IDs from 'Covered Requirements' section.

        Returns:
            List of requirement IDs (e.g., ["FuncR_S101", "PerfR_B201"])
        """
        # Pattern: FuncR_XXX, PerfR_XXX, SafR_XXX, etc.
        req_pattern = re.compile(r'\b([A-Z][a-z]+R_[A-Z]\d+)\b')

        matches = req_pattern.findall(text)
        # Remove duplicates and return
        return list(set(matches))

    def _extract_field(self, text: str, field_pattern: str) -> str:
        """
        Extract field content (Purpose, Procedure, etc.).

        Args:
            text: Text block to search
            field_pattern: Regex pattern for field name (e.g., 'Purpose|Objective')

        Returns:
            Extracted field content
        """
        # Pattern: **Field Name** content or | Field Name | content
        pattern = re.compile(
            rf'(?:\*\*|##\s*|\|\s*)({field_pattern})(?:\*\*|:|\s*\|)\s*(.+?)(?=\*\*|##|\||$)',
            re.IGNORECASE | re.DOTALL
        )

        match = pattern.search(text)
        if match:
            content = match.group(2).strip()
            # Clean up
            content = re.sub(r'\|', '', content)  # Remove table separators
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            # Limit length
            if len(content) > 500:
                content = content[:500] + "..."
            return content

        return ""

    def get_statistics(self) -> Dict:
        """
        Get parsing statistics.

        Returns:
            Dictionary with statistics
        """
        if not self.test_cases:
            return {
                "total": 0,
                "by_type": {},
                "with_requirements": 0
            }

        # Count by type
        by_type = {}
        for tc in self.test_cases:
            tc_type = tc.get('type', 'Unknown')
            by_type[tc_type] = by_type.get(tc_type, 0) + 1

        # Count test cases with covered requirements
        with_reqs = sum(1 for tc in self.test_cases if tc.get('covered_requirements'))

        return {
            "total": len(self.test_cases),
            "by_type": by_type,
            "with_requirements": with_reqs
        }


if __name__ == "__main__":
    # Test the parser
    logging.basicConfig(level=logging.INFO)

    demo_path = Path(__file__).parents[2] / "Documents/Demo/MOSAR-WP3-D3.5-DLR_1.1.0-Demonstration-Procedures.md"

    if not demo_path.exists():
        print(f"Demo Procedures file not found: {demo_path}")
    else:
        parser = DemoProcedureParser()
        test_cases = parser.parse(demo_path)

        print(f"\nParsed {len(test_cases)} test cases")

        stats = parser.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total: {stats['total']}")
        print(f"  By Type: {stats['by_type']}")
        print(f"  With Requirements: {stats['with_requirements']}")

        # Show first few test cases
        print(f"\nFirst 5 test cases:")
        for tc in test_cases[:5]:
            print(f"\n  {tc['id']}: {tc['name']}")
            print(f"    Type: {tc['type']}")
            print(f"    Covered Requirements: {tc['covered_requirements']}")
            if tc['objective']:
                print(f"    Objective: {tc['objective'][:100]}...")
