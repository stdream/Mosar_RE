"""
End-to-End Tests for MOSAR GraphRAG System

These tests require:
1. Neo4j database running (localhost:7687)
2. Documents loaded into Neo4j
3. OpenAI API key configured

Run with: pytest tests/test_e2e.py -v -m e2e
"""

import pytest
import time
from typing import Dict, Any

from src.graphrag.workflow import build_workflow
from src.graphrag.state import GraphRAGState
from src.query.router import QueryPath


# Mark all tests in this module as e2e and requires_neo4j
pytestmark = [pytest.mark.e2e, pytest.mark.requires_neo4j, pytest.mark.requires_openai]


@pytest.fixture(scope="module")
def graphrag_workflow():
    """Build GraphRAG workflow once for all tests."""
    workflow = build_workflow()
    return workflow


class TestKeyQuestions:
    """
    Test 5 key questions defined in PRD.

    Success Criteria:
    - Accuracy: >90% (answers contain correct entities)
    - Response time: <2000ms (hybrid/vector), <500ms (pure Cypher)
    - Complete execution path
    """

    def test_question_1_component_impact(self, graphrag_workflow):
        """
        Q1: R-ICU를 변경하면 어떤 요구사항이 영향받나요?

        Expected:
        - Query path: PURE_CYPHER or HYBRID
        - Should find requirements related to R-ICU
        - Response time: <500ms (pure Cypher) or <2000ms (hybrid)
        """
        question = "R-ICU를 변경하면 어떤 요구사항이 영향받나요?"

        start_time = time.time()

        result = graphrag_workflow.invoke({
            "user_question": question,
            "language": "ko",
            "session_id": "test_q1",
            "user_id": "test_user",
            "query_path": None,
            "routing_confidence": 0.0,
            "matched_entities": {},
            "top_k_sections": None,
            "extracted_entities": None,
            "cypher_query": None,
            "graph_results": None,
            "final_answer": "",
            "citations": None,
            "processing_time_ms": None,
            "execution_path": None,
            "cache_hit": None,
            "error": None
        })

        elapsed_ms = (time.time() - start_time) * 1000

        # Assertions
        assert result["final_answer"], "Answer should not be empty"
        assert result["error"] is None, f"Error occurred: {result.get('error')}"

        # Check entity detection
        answer_lower = result["final_answer"].lower()
        assert "r-icu" in answer_lower or "ICU" in result["final_answer"], \
            "Answer should mention R-ICU"

        # Check query path
        assert result["query_path"] in [QueryPath.PURE_CYPHER, QueryPath.HYBRID], \
            f"Expected PURE_CYPHER or HYBRID, got {result['query_path']}"

        # Check response time
        if result["query_path"] == QueryPath.PURE_CYPHER:
            assert elapsed_ms < 500, f"Pure Cypher should be <500ms, got {elapsed_ms:.0f}ms"
        else:
            assert elapsed_ms < 2000, f"Hybrid should be <2000ms, got {elapsed_ms:.0f}ms"

        # Check citations exist
        assert result.get("citations"), "Should have citations"

        print(f"\n✓ Q1 passed: {elapsed_ms:.0f}ms, Path: {result['query_path']}")
        print(f"  Answer preview: {result['final_answer'][:200]}...")

    def test_question_2_requirement_verification(self, graphrag_workflow):
        """
        Q2: FuncR_S110 요구사항을 검증하는 테스트는 무엇인가요?

        Expected:
        - Query path: PURE_CYPHER
        - Should find test cases that verify FuncR_S110
        - Should mention test case IDs
        """
        question = "FuncR_S110 요구사항을 검증하는 테스트는 무엇인가요?"

        start_time = time.time()

        result = graphrag_workflow.invoke({
            "user_question": question,
            "language": "ko",
            "session_id": "test_q2",
            "user_id": "test_user",
            "query_path": None,
            "routing_confidence": 0.0,
            "matched_entities": {},
            "top_k_sections": None,
            "extracted_entities": None,
            "cypher_query": None,
            "graph_results": None,
            "final_answer": "",
            "citations": None,
            "processing_time_ms": None,
            "execution_path": None,
            "cache_hit": None,
            "error": None
        })

        elapsed_ms = (time.time() - start_time) * 1000

        # Assertions
        assert result["final_answer"], "Answer should not be empty"
        assert result["error"] is None, f"Error occurred: {result.get('error')}"

        # Check requirement mention
        assert "FuncR_S110" in result["final_answer"] or "funcr" in result["final_answer"].lower(), \
            "Answer should mention FuncR_S110"

        # Check for test-related keywords
        answer_lower = result["final_answer"].lower()
        test_keywords = ["test", "테스트", "검증", "verify", "ct-", "it"]
        assert any(keyword in answer_lower for keyword in test_keywords), \
            "Answer should mention testing or test cases"

        # Response time check
        assert elapsed_ms < 2000, f"Should be <2000ms, got {elapsed_ms:.0f}ms"

        print(f"\n✓ Q2 passed: {elapsed_ms:.0f}ms, Path: {result['query_path']}")
        print(f"  Answer preview: {result['final_answer'][:200]}...")

    def test_question_3_network_communication(self, graphrag_workflow):
        """
        Q3: 어떤 하드웨어가 네트워크 통신을 담당하나요?

        Expected:
        - Query path: HYBRID (natural language)
        - Should find R-ICU and mention CAN/Ethernet
        - Should have both graph and vector results
        """
        question = "어떤 하드웨어가 네트워크 통신을 담당하나요?"

        start_time = time.time()

        result = graphrag_workflow.invoke({
            "user_question": question,
            "language": "ko",
            "session_id": "test_q3",
            "user_id": "test_user",
            "query_path": None,
            "routing_confidence": 0.0,
            "matched_entities": {},
            "top_k_sections": None,
            "extracted_entities": None,
            "cypher_query": None,
            "graph_results": None,
            "final_answer": "",
            "citations": None,
            "processing_time_ms": None,
            "execution_path": None,
            "cache_hit": None,
            "error": None
        })

        elapsed_ms = (time.time() - start_time) * 1000

        # Assertions
        assert result["final_answer"], "Answer should not be empty"
        assert result["error"] is None, f"Error occurred: {result.get('error')}"

        # Check hardware mention
        answer_lower = result["final_answer"].lower()
        assert "r-icu" in answer_lower or "icu" in answer_lower, \
            "Answer should mention R-ICU"

        # Check protocol mention
        assert "can" in answer_lower or "ethernet" in answer_lower, \
            "Answer should mention communication protocols"

        # Response time
        assert elapsed_ms < 2000, f"Should be <2000ms, got {elapsed_ms:.0f}ms"

        print(f"\n✓ Q3 passed: {elapsed_ms:.0f}ms, Path: {result['query_path']}")
        print(f"  Answer preview: {result['final_answer'][:200]}...")

    def test_question_4_design_evolution(self, graphrag_workflow):
        """
        Q4: PDD에서 DDD로 네트워크 설계가 어떻게 변경되었나요?

        Expected:
        - Query path: PURE_VECTOR or HYBRID
        - Should find sections from both PDD and DDD
        - Should mention design changes
        """
        question = "PDD에서 DDD로 네트워크 설계가 어떻게 변경되었나요?"

        start_time = time.time()

        result = graphrag_workflow.invoke({
            "user_question": question,
            "language": "ko",
            "session_id": "test_q4",
            "user_id": "test_user",
            "query_path": None,
            "routing_confidence": 0.0,
            "matched_entities": {},
            "top_k_sections": None,
            "extracted_entities": None,
            "cypher_query": None,
            "graph_results": None,
            "final_answer": "",
            "citations": None,
            "processing_time_ms": None,
            "execution_path": None,
            "cache_hit": None,
            "error": None
        })

        elapsed_ms = (time.time() - start_time) * 1000

        # Assertions
        assert result["final_answer"], "Answer should not be empty"
        assert result["error"] is None, f"Error occurred: {result.get('error')}"

        # Check document mentions
        answer = result["final_answer"]
        assert "PDD" in answer or "preliminary" in answer.lower() or "예비" in answer, \
            "Answer should mention PDD"
        assert "DDD" in answer or "detailed" in answer.lower() or "상세" in answer, \
            "Answer should mention DDD"

        # Response time
        assert elapsed_ms < 2000, f"Should be <2000ms, got {elapsed_ms:.0f}ms"

        print(f"\n✓ Q4 passed: {elapsed_ms:.0f}ms, Path: {result['query_path']}")
        print(f"  Answer preview: {result['final_answer'][:200]}...")

    def test_question_5_unverified_requirements(self, graphrag_workflow):
        """
        Q5: 아직 테스트가 없는 요구사항은 어떤 것들이 있나요?

        Expected:
        - Query path: PURE_CYPHER (structural query)
        - Should find requirements without test cases
        - Should list requirement IDs
        """
        question = "아직 테스트가 없는 요구사항은 어떤 것들이 있나요?"

        start_time = time.time()

        result = graphrag_workflow.invoke({
            "user_question": question,
            "language": "ko",
            "session_id": "test_q5",
            "user_id": "test_user",
            "query_path": None,
            "routing_confidence": 0.0,
            "matched_entities": {},
            "top_k_sections": None,
            "extracted_entities": None,
            "cypher_query": None,
            "graph_results": None,
            "final_answer": "",
            "citations": None,
            "processing_time_ms": None,
            "execution_path": None,
            "cache_hit": None,
            "error": None
        })

        elapsed_ms = (time.time() - start_time) * 1000

        # Assertions
        assert result["final_answer"], "Answer should not be empty"
        assert result["error"] is None, f"Error occurred: {result.get('error')}"

        # Check for requirement-related keywords
        answer_lower = result["final_answer"].lower()
        req_keywords = ["요구사항", "requirement", "funcr", "safr", "perfr", "intr"]
        assert any(keyword in answer_lower for keyword in req_keywords), \
            "Answer should mention requirements"

        # Response time
        assert elapsed_ms < 2000, f"Should be <2000ms, got {elapsed_ms:.0f}ms"

        print(f"\n✓ Q5 passed: {elapsed_ms:.0f}ms, Path: {result['query_path']}")
        print(f"  Answer preview: {result['final_answer'][:200]}...")


class TestAccuracyMetrics:
    """Calculate overall accuracy metrics."""

    def test_overall_accuracy(self, graphrag_workflow):
        """
        Test overall accuracy with multiple questions.

        Success Criteria: >90% accuracy
        """
        test_questions = [
            {
                "question": "R-ICU는 무엇인가요?",
                "expected_entities": ["R-ICU", "ICU"],
                "expected_keywords": ["reduced", "instrument", "control", "제어"]
            },
            {
                "question": "CAN 버스를 사용하는 컴포넌트는?",
                "expected_entities": ["CAN"],
                "expected_keywords": ["r-icu", "icu", "component"]
            },
            {
                "question": "Service Module에 포함된 구성요소는?",
                "expected_entities": ["SM", "Service Module"],
                "expected_keywords": ["r-icu", "cpdu", "hotdock"]
            }
        ]

        correct_count = 0
        total_count = len(test_questions)

        for i, test in enumerate(test_questions):
            result = graphrag_workflow.invoke({
                "user_question": test["question"],
                "language": "ko",
                "session_id": f"test_accuracy_{i}",
                "user_id": "test_user",
                "query_path": None,
                "routing_confidence": 0.0,
                "matched_entities": {},
                "top_k_sections": None,
                "extracted_entities": None,
                "cypher_query": None,
                "graph_results": None,
                "final_answer": "",
                "citations": None,
                "processing_time_ms": None,
                "execution_path": None,
                "cache_hit": None,
                "error": None
            })

            if result["error"]:
                print(f"  Question {i+1} ERROR: {result['error']}")
                continue

            answer_lower = result["final_answer"].lower()

            # Check if answer contains expected keywords
            keyword_match = any(
                keyword.lower() in answer_lower
                for keyword in test["expected_keywords"]
            )

            if keyword_match:
                correct_count += 1
                print(f"  ✓ Question {i+1} CORRECT")
            else:
                print(f"  ✗ Question {i+1} INCORRECT")
                print(f"    Expected keywords: {test['expected_keywords']}")
                print(f"    Answer: {result['final_answer'][:100]}...")

        accuracy = (correct_count / total_count) * 100
        print(f"\n{'='*60}")
        print(f"Overall Accuracy: {accuracy:.1f}% ({correct_count}/{total_count})")
        print(f"{'='*60}")

        assert accuracy >= 90, f"Accuracy {accuracy:.1f}% is below 90% threshold"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])
