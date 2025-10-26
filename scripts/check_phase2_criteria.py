"""Check Phase 2 success criteria."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.utils.neo4j_client import Neo4jClient


def main():
    client = Neo4jClient()

    print("\n" + "="*70)
    print("Phase 2 Success Criteria Check")
    print("="*70 + "\n")

    # Criteria from PRD
    reqs = client.count_nodes('Requirement')
    tcs = client.count_nodes('TestCase')
    verifies = client.count_relationships('VERIFIES')
    secs = client.count_nodes('Section')
    relates_to = client.count_relationships('RELATES_TO')
    mentions = client.count_relationships('MENTIONS')
    total_entity_rels = relates_to + mentions

    print("Criteria:")
    print("-" * 70)
    print(f"1. Requirements loaded: {reqs} / 227 target")
    print(f"2. Test cases loaded: {tcs}")
    print(f"   VERIFIES relationships: {verifies}")
    print(f"3. Sections embedded: {secs} / 500+ target")
    print(f"4. Entity relationships: {total_entity_rels}")
    print(f"   - RELATES_TO: {relates_to}")
    print(f"   - MENTIONS: {mentions}")

    print("\n" + "="*70)
    print("Assessment:")
    print("-" * 70)

    req_pass = reqs >= 220
    tc_pass = tcs > 0 and verifies > 0
    sec_pass = secs >= 500
    entity_pass = total_entity_rels > 0

    print(f"1. Requirements (>= 220): {'PASS' if req_pass else 'FAIL'}")
    print(f"2. Test cases with VERIFIES: {'PASS' if tc_pass else 'FAIL'}")
    print(f"3. Sections (>= 500): {'PASS' if sec_pass else f'WARNING - Need {500 - secs} more sections'}")
    print(f"4. Entity relationships: {'PASS' if entity_pass else 'FAIL'}")

    overall_pass = req_pass and tc_pass and sec_pass and entity_pass

    print("\n" + "="*70)
    if overall_pass:
        print("RESULT: Phase 2 SUCCESS - All criteria met!")
    else:
        print("RESULT: Phase 2 PARTIAL - Some criteria need attention")
        if not sec_pass:
            print(f"\nNOTE: Sections target not met. Options:")
            print(f"  - Improve parser to extract more granular sections")
            print(f"  - Add chunking for large sections")
            print(f"  - Current {secs} sections may be sufficient for MVP")
    print("="*70 + "\n")

    client.close()


if __name__ == "__main__":
    main()
