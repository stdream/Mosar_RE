# MOSAR GraphRAG System - Product Requirements Document (PRD)

**Version**: 1.0
**Date**: 2025-01-26
**Project**: MOSAR Requirements Engineering GraphRAG System
**Status**: Approved for Implementation

---

## 📋 Executive Summary

### Vision
MOSAR 프로젝트 문서(SRD, PDD, DDD, Demo Procedures)를 Neo4j 기반 GraphRAG 시스템으로 구축하여 요구사항 추적성(Traceability), 설계 검증, 영향 분석을 지원하는 AI 기반 지식 관리 시스템.

### Core Objectives
1. **요구사항 추적성**: 요구사항 → 설계 → 구현 → 검증 전체 경로 추적
2. **영향 분석**: 설계 변경 시 파급 효과 즉시 파악 (분석 시간 90% 단축)
3. **지능형 검색**: 자연어 질문에 대한 정확한 답변 (정확도 90%+)
4. **설계 검증**: PDD→DDD 진화 과정에서 요구사항 이탈 조기 발견

### Success Metrics
- ✅ 227개 요구사항 100% 그래프화
- ✅ 500+ 문서 섹션 임베딩 완료
- ✅ 5가지 핵심 질문 정확도 90%+
- ✅ 평균 응답 시간 < 2초
- ✅ 테스트 커버리지 80%+

---

## 🏗️ System Architecture

### Technology Stack

```yaml
Orchestration:
  - LangGraph v0.2.16+: Stateful workflow orchestration
  - LangChain v0.3+: LLM integrations & chains

Graph Database:
  - Neo4j v5.14+: Graph storage & Cypher queries
  - neo4j-driver (Python): Database connectivity
  - Neo4j Vector Index: Integrated vector search

LLM & Embeddings:
  - OpenAI GPT-4o: Text2Cypher, response synthesis
  - OpenAI text-embedding-3-large (3072d): Semantic search
  - Alternative: Ollama/LM Studio (local deployment)

NER & Entity Resolution:
  - spaCy v3.7+: Named Entity Recognition
  - spacy-transformers: Enhanced NER models
  - FuzzyWuzzy: String fuzzy matching
  - Custom Entity Dictionary: MOSAR-specific terms

Development:
  - Python 3.11+
  - Poetry: Dependency management
  - Pytest: Testing framework
  - Ruff: Linting & formatting
  - LangSmith: Trace debugging
```

### Graph Schema (4-Layer Architecture)

```
Layer 4: Requirements Traceability
  ↕ (DERIVES_FROM, IMPLEMENTED_BY, VALIDATED_BY)
Layer 3: Domain System Graph
  ↕ (CONNECTS_TO, HAS_INTERFACE, RUNS_TASK)
Layer 1: Document Structure
  ↕ (HAS_CHAPTER, HAS_SECTION, CONTAINS)
Layer 2: Entities (Selective)
  ↕ (MENTIONS, RELATES_TO)
```

---

## 📐 Implementation Phases

### **Phase 0: Environment Setup (Day 1-2)**

#### Deliverables
- [x] Project structure
- [x] `pyproject.toml` with all dependencies
- [x] `.env.example` template
- [x] Neo4j database setup
- [x] `README.md` with setup instructions

#### Project Structure
```
ReqEng/
├── Documents/              # Existing documents (SRD, PDD, DDD, Demo)
├── src/
│   ├── graphrag/          # LangGraph workflows
│   │   ├── state.py       # State definitions
│   │   ├── nodes/         # Workflow nodes
│   │   │   ├── query_classifier.py
│   │   │   ├── cypher_executor.py
│   │   │   ├── vector_search.py
│   │   │   ├── entity_extractor.py
│   │   │   ├── contextual_cypher.py
│   │   │   └── response_synthesizer.py
│   │   ├── workflow.py    # Graph assembly
│   │   └── app.py         # CLI interface
│   ├── ingestion/         # Document parsing & embedding
│   │   ├── markdown_parser.py
│   │   ├── srd_parser.py
│   │   ├── pdd_parser.py
│   │   ├── ddd_parser.py
│   │   ├── demo_procedure_parser.py  # NEW: Test case extraction
│   │   ├── embedder.py
│   │   └── neo4j_loader.py
│   ├── neo4j_schema/      # Graph schema
│   │   ├── schema.cypher
│   │   └── create_schema.py
│   └── utils/             # Common utilities
│       ├── entity_resolver.py
│       └── neo4j_client.py
├── data/
│   ├── entities/          # Entity Dictionary
│   │   └── mosar_entities.json
│   └── templates/         # Cypher query templates
│       └── cypher_templates.yaml
├── scripts/               # Execution scripts
│   ├── load_documents.py
│   └── run_graphrag.py
├── tests/                 # Unit & E2E tests
│   ├── test_nodes.py
│   ├── test_e2e.py
│   └── fixtures/
├── notebooks/             # Jupyter experiments
│   └── benchmark.ipynb
├── .env.example
├── pyproject.toml
├── pytest.ini
└── README.md
```

#### Dependencies (pyproject.toml)
```toml
[tool.poetry]
name = "mosar-graphrag"
version = "0.1.0"
description = "MOSAR Requirements Engineering GraphRAG System"
python = "^3.11"

[tool.poetry.dependencies]
# Core
python = "^3.11"
neo4j = "^5.14.0"
langgraph = "^0.2.16"
langchain = "^0.3.0"
langchain-openai = "^0.2.0"
langchain-core = "^0.3.0"

# NLP & Embeddings
openai = "^1.50.0"
spacy = "^3.7.0"
spacy-transformers = "^1.3.0"
sentence-transformers = "^2.3.0"  # Optional: local embeddings

# Entity Resolution
fuzzywuzzy = "^0.18.0"
python-levenshtein = "^0.25.0"

# Utilities
pydantic = "^2.5.0"
python-dotenv = "^1.0.0"
pyyaml = "^6.0"
rich = "^13.7.0"  # Pretty console output

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.23.0"
ruff = "^0.1.0"
jupyter = "^1.0.0"
ipykernel = "^6.28.0"
langsmith = "^0.1.0"  # Trace debugging
```

#### Environment Variables (.env.example)
```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=mosar-graphrag

# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_ORG_ID=org-your-org-id  # Optional

# LangSmith (Optional - for debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-your-key-here
LANGCHAIN_PROJECT=mosar-graphrag

# Application
LOG_LEVEL=INFO
CACHE_ENABLED=true
```

#### Success Criteria
- ✅ Neo4j connection successful
- ✅ All dependencies installed
- ✅ Python environment activated
- ✅ Sample Cypher query executes

---

### **Phase 1: Graph Schema Construction (Day 3-7)**

#### Task 1.1: Neo4j Schema Definition

**File**: `src/neo4j_schema/schema.cypher`

```cypher
// ==========================================
// CONSTRAINTS (Uniqueness & Data Integrity)
// ==========================================

// Documents
CREATE CONSTRAINT unique_document_id IF NOT EXISTS
FOR (d:Document) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT unique_section_id IF NOT EXISTS
FOR (s:Section) REQUIRE (s.doc_id, s.number) IS UNIQUE;

// Requirements (Layer 4)
CREATE CONSTRAINT unique_requirement_id IF NOT EXISTS
FOR (r:Requirement) REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT unique_requirement_version_id IF NOT EXISTS
FOR (rv:RequirementVersion) REQUIRE rv.id IS UNIQUE;

// Components (Layer 3)
CREATE CONSTRAINT unique_component_id IF NOT EXISTS
FOR (c:Component) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT unique_spacecraft_module_id IF NOT EXISTS
FOR (sm:SpacecraftModule) REQUIRE sm.id IS UNIQUE;

// Test Cases (NEW - Demo Procedures)
CREATE CONSTRAINT unique_test_case_id IF NOT EXISTS
FOR (tc:TestCase) REQUIRE tc.id IS UNIQUE;

// Organizations
CREATE CONSTRAINT unique_organization_name IF NOT EXISTS
FOR (o:Organization) REQUIRE o.name IS UNIQUE;

// Scenarios
CREATE CONSTRAINT unique_scenario_id IF NOT EXISTS
FOR (s:Scenario) REQUIRE s.id IS UNIQUE;


// ==========================================
// INDEXES (Query Performance)
// ==========================================

// Requirements
CREATE INDEX requirement_level_subsystem IF NOT EXISTS
FOR (r:Requirement) ON (r.level, r.subsystem);

CREATE INDEX requirement_type IF NOT EXISTS
FOR (r:Requirement) ON (r.type);

// Components
CREATE INDEX component_type_name IF NOT EXISTS
FOR (c:Component) ON (c.type, c.name);

// Test Cases (NEW)
CREATE INDEX test_case_status IF NOT EXISTS
FOR (tc:TestCase) REQUIRE (tc.status, tc.type);

// Sections
CREATE INDEX section_doc_chapter IF NOT EXISTS
FOR (s:Section) ON (s.doc_id, s.chapter);


// ==========================================
// FULLTEXT INDEXES (Keyword Search)
// ==========================================

CREATE FULLTEXT INDEX requirement_fulltext IF NOT EXISTS
FOR (r:Requirement)
ON EACH [r.title, r.statement, r.comment];

CREATE FULLTEXT INDEX component_fulltext IF NOT EXISTS
FOR (c:Component)
ON EACH [c.name, c.description];

CREATE FULLTEXT INDEX section_fulltext IF NOT EXISTS
FOR (s:Section)
ON EACH [s.title, s.content];


// ==========================================
// VECTOR INDEXES (Semantic Search)
// ==========================================

// Requirements (statement embeddings)
CREATE VECTOR INDEX requirement_embeddings IF NOT EXISTS
FOR (r:Requirement) ON (r.statement_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
};

// Document Sections (content embeddings)
CREATE VECTOR INDEX section_embeddings IF NOT EXISTS
FOR (s:Section) ON (s.content_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
};

// Text Chunks (Layer 1 - optional, for fine-grained search)
CREATE VECTOR INDEX chunk_embeddings IF NOT EXISTS
FOR (c:TextChunk) ON (c.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
};

// Components (description embeddings - optional)
CREATE VECTOR INDEX component_embeddings IF NOT EXISTS
FOR (c:Component) ON (c.description_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
};
```

**Implementation**: `src/neo4j_schema/create_schema.py`

```python
"""Neo4j schema creation script."""
from pathlib import Path
from src.utils.neo4j_client import Neo4jClient
import logging

logger = logging.getLogger(__name__)

def create_schema():
    """Execute schema.cypher to create constraints and indexes."""
    client = Neo4jClient()
    schema_file = Path(__file__).parent / "schema.cypher"

    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_cypher = f.read()

    # Split by double newline (separate statements)
    statements = [s.strip() for s in schema_cypher.split('\n\n') if s.strip()]

    for i, statement in enumerate(statements):
        if statement.startswith('//') or not statement:
            continue

        try:
            client.execute(statement)
            logger.info(f"✓ Executed statement {i+1}/{len(statements)}")
        except Exception as e:
            logger.warning(f"⚠ Statement {i+1} failed (may already exist): {e}")

    logger.info("✅ Schema creation complete!")

if __name__ == "__main__":
    create_schema()
```

#### Task 1.2: Entity Dictionary Creation

**File**: `data/entities/mosar_entities.json`

```json
{
  "components": {
    "Walking Manipulator": {"id": "WM", "type": "Component"},
    "Reduced Instrument Control Unit": {"id": "R-ICU", "type": "Component"},
    "R-ICU": {"id": "R-ICU", "type": "Component"},
    "우주선 제어 유닛": {"id": "OBC-S", "type": "Component"},
    "On-Board Computer": {"id": "OBC-S", "type": "Component"},
    "OBC-S": {"id": "OBC-S", "type": "Component"},
    "OBC-C": {"id": "OBC-C", "type": "Component"},
    "cPDU": {"id": "cPDU", "type": "Component"},
    "HOTDOCK": {"id": "HOTDOCK", "type": "Component"},
    "SM1-DMS": {"id": "SM1-DMS", "type": "SpacecraftModule"},
    "SM2-PWS": {"id": "SM2-PWS", "type": "SpacecraftModule"},
    "SM3-BAT": {"id": "SM3-BAT", "type": "SpacecraftModule"},
    "SM4-THS": {"id": "SM4-THS", "type": "SpacecraftModule"}
  },

  "requirements": {
    "안전 요구사항": {"type": "Requirement", "filter": {"type": "SafR"}},
    "기능 요구사항": {"type": "Requirement", "filter": {"type": "FuncR"}},
    "성능 요구사항": {"type": "Requirement", "filter": {"type": "PerfR"}},
    "인터페이스 요구사항": {"type": "Requirement", "filter": {"type": "IntR"}},
    "설계 요구사항": {"type": "Requirement", "filter": {"type": "DesR"}}
  },

  "scenarios": {
    "첫 번째 시나리오": {"id": "S1", "type": "Scenario"},
    "두 번째 시나리오": {"id": "S2", "type": "Scenario"},
    "세 번째 시나리오": {"id": "S3", "type": "Scenario"},
    "Scenario 1": {"id": "S1", "type": "Scenario"},
    "Scenario 2": {"id": "S2", "type": "Scenario"},
    "Scenario 3": {"id": "S3", "type": "Scenario"},
    "SM 조립 시나리오": {"id": "S1", "type": "Scenario"},
    "SM 교체 시나리오": {"id": "S2", "type": "Scenario"}
  },

  "organizations": {
    "스페이스앱스": {"id": "SPACEAPPS", "type": "Organization"},
    "SPACEAPPS": {"id": "SPACEAPPS", "type": "Organization"},
    "TAS-UK": {"id": "TAS-UK", "type": "Organization"},
    "GMV": {"id": "GMV", "type": "Organization"},
    "DLR": {"id": "DLR", "type": "Organization"},
    "SITAEL": {"id": "SITAEL", "type": "Organization"}
  },

  "protocols": {
    "SpaceWire": {"id": "SpaceWire", "type": "Protocol"},
    "RMAP": {"id": "RMAP", "type": "Protocol"},
    "CAN": {"id": "CAN", "type": "Protocol"},
    "CAN bus": {"id": "CAN", "type": "Protocol"}
  }
}
```

**Implementation**: `src/utils/entity_resolver.py`

```python
"""Entity resolution using dictionary lookup and fuzzy matching."""
import json
from pathlib import Path
from typing import Dict, List, Optional
from fuzzywuzzy import process
import logging

logger = logging.getLogger(__name__)

class EntityResolver:
    """Resolve user input to canonical entity IDs."""

    def __init__(self):
        """Load entity dictionary."""
        dict_path = Path(__file__).parents[2] / "data/entities/mosar_entities.json"
        with open(dict_path, 'r', encoding='utf-8') as f:
            self.entities = json.load(f)

        # Flatten for fast lookup
        self.flat_dict = {}
        for category, mappings in self.entities.items():
            for phrase, entity_info in mappings.items():
                self.flat_dict[phrase.lower()] = {
                    **entity_info,
                    "category": category
                }

    def resolve(self, text: str, threshold: int = 85) -> Dict[str, List[Dict]]:
        """
        Resolve entities in text.

        Args:
            text: Input text (question or chunk)
            threshold: Fuzzy match threshold (0-100)

        Returns:
            Dict mapping entity types to found entities
            Example: {"Component": [{"id": "R-ICU", "confidence": 1.0}]}
        """
        results = {}

        # 1. Exact match (fastest)
        for phrase, entity in self.flat_dict.items():
            if phrase in text.lower():
                entity_type = entity["type"]
                if entity_type not in results:
                    results[entity_type] = []

                results[entity_type].append({
                    **entity,
                    "matched_phrase": phrase,
                    "confidence": 1.0
                })

        # 2. Fuzzy match (if no exact match)
        if not results:
            best_matches = process.extract(
                text.lower(),
                self.flat_dict.keys(),
                limit=3
            )

            for phrase, score in best_matches:
                if score >= threshold:
                    entity = self.flat_dict[phrase]
                    entity_type = entity["type"]

                    if entity_type not in results:
                        results[entity_type] = []

                    results[entity_type].append({
                        **entity,
                        "matched_phrase": phrase,
                        "confidence": score / 100.0
                    })

        return results

# Singleton
entity_resolver = EntityResolver()
```

#### Success Criteria
- ✅ Neo4j schema created (all constraints & indexes)
- ✅ Entity Dictionary loaded (100+ mappings)
- ✅ Entity resolver unit tests pass

---

### **Phase 2: Document Parsing & Data Loading (Day 8-14)**

#### Task 2.1: Document Parsers Implementation

**File**: `src/ingestion/srd_parser.py`

```python
"""System Requirements Document parser."""
import re
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SRDParser:
    """Parse System Requirements Document (table format)."""

    def parse(self, file_path: Path) -> List[Dict]:
        """
        Extract requirements from SRD markdown.

        Returns:
            List of requirement dicts with fields:
            - id: e.g., "FuncR_S101"
            - title: e.g., "Satellite repair and update"
            - statement: Full requirement text
            - level: Mandatory/Desirable/Optional
            - verification: Testing/Review of Design/Analysis
            - responsible: Organization(s)
            - covers: Referenced requirements/documents
            - comment: Additional notes
        """
        requirements = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to match requirement tables
        # Pattern: | FuncR_XXX | Title | ... |
        req_pattern = re.compile(
            r'\|\s*([A-Z][a-z]+R_[A-Z]\d+)\s*\|',
            re.MULTILINE
        )

        matches = req_pattern.finditer(content)

        for match in matches:
            req_id = match.group(1)

            # Extract table block
            table_start = match.start()
            table_end = content.find('\n\n', table_start)
            table_block = content[table_start:table_end]

            # Parse table rows
            req_data = self._parse_requirement_table(req_id, table_block)
            if req_data:
                requirements.append(req_data)

        logger.info(f"✓ Parsed {len(requirements)} requirements from SRD")
        return requirements

    def _parse_requirement_table(self, req_id: str, table_block: str) -> Dict:
        """Parse individual requirement table."""
        lines = table_block.split('\n')

        req = {"id": req_id}

        for line in lines:
            if '| STATEMENT' in line:
                req['statement'] = self._extract_cell_value(line, 1)
            elif '| VERIFICATION' in line:
                req['verification'] = self._extract_cell_value(line, 1)
                req['covers'] = self._extract_cell_value(line, 3)  # COVERS column
            elif '| RESPONSIBLE' in line:
                req['responsible'] = self._extract_cell_value(line, 1)
            elif '| COMMENT' in line:
                req['comment'] = self._extract_cell_value(line, 1)
            elif req_id in line and 'STATEMENT' not in line:
                # Title row: | FuncR_XXX | Title | ... | Level |
                cells = [c.strip() for c in line.split('|')]
                if len(cells) >= 4:
                    req['title'] = cells[1]
                    req['level'] = cells[-2]  # Mandatory/Desirable/Optional

        # Infer type from ID
        req['type'] = req_id.split('_')[0]  # e.g., "FuncR"
        req['subsystem'] = req_id.split('_')[1][0]  # e.g., "S"

        return req

    def _extract_cell_value(self, line: str, index: int) -> str:
        """Extract cell value from table row."""
        cells = [c.strip() for c in line.split('|')]
        return cells[index] if len(cells) > index else ""
```

**File**: `src/ingestion/demo_procedure_parser.py` (NEW)

```python
"""Demonstration Procedures parser - extracts test cases."""
import re
from typing import List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DemoProcedureParser:
    """Parse test cases from Demonstration Procedures document."""

    def parse(self, file_path: Path) -> List[Dict]:
        """
        Extract test cases and their covered requirements.

        Returns:
            List of test case dicts:
            - id: e.g., "CT-A-1", "IT1", "S2"
            - type: "Component Test", "Integration Test", "Scenario"
            - name: Test description
            - objective: What it tests
            - procedure: Test steps
            - covered_requirements: List of requirement IDs
        """
        test_cases = []

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern 1: Component Tests (CT-X-Y)
        ct_pattern = re.compile(r'#### (CT-[A-Z]-\d+):\s*(.+)', re.MULTILINE)

        for match in ct_pattern.finditer(content):
            tc_id = match.group(1)
            tc_name = match.group(2)

            # Extract covered requirements section
            tc_start = match.end()
            tc_end = content.find('####', tc_start)
            tc_block = content[tc_start:tc_end]

            covered_reqs = self._extract_covered_requirements(tc_block)

            test_cases.append({
                "id": tc_id,
                "type": "Component Test",
                "name": tc_name,
                "covered_requirements": covered_reqs,
                "objective": self._extract_objective(tc_block),
                "procedure": self._extract_procedure(tc_block)
            })

        # Pattern 2: Integration Tests (IT1, IT2...)
        it_pattern = re.compile(r'#### (IT\d+):\s*(.+)', re.MULTILINE)

        for match in it_pattern.finditer(content):
            tc_id = match.group(1)
            tc_name = match.group(2)

            tc_start = match.end()
            tc_end = content.find('####', tc_start)
            tc_block = content[tc_start:tc_end]

            covered_reqs = self._extract_covered_requirements(tc_block)

            test_cases.append({
                "id": tc_id,
                "type": "Integration Test",
                "name": tc_name,
                "covered_requirements": covered_reqs,
                "objective": self._extract_objective(tc_block),
                "procedure": self._extract_procedure(tc_block)
            })

        # Pattern 3: Scenarios (S1, S2, S3)
        scenario_pattern = re.compile(r'### Scenario (S\d+):\s*(.+)', re.MULTILINE)

        for match in scenario_pattern.finditer(content):
            tc_id = match.group(1)
            tc_name = match.group(2)

            tc_start = match.end()
            tc_end = content.find('###', tc_start)
            tc_block = content[tc_start:tc_end]

            covered_reqs = self._extract_covered_requirements(tc_block)

            test_cases.append({
                "id": tc_id,
                "type": "Scenario",
                "name": tc_name,
                "covered_requirements": covered_reqs,
                "objective": self._extract_objective(tc_block),
                "procedure": self._extract_procedure(tc_block)
            })

        logger.info(f"✓ Parsed {len(test_cases)} test cases from Demo Procedures")
        return test_cases

    def _extract_covered_requirements(self, text: str) -> List[str]:
        """Extract requirement IDs from 'Covered Requirements' section."""
        # Pattern: FuncR_XXX, PerfR_XXX, etc.
        req_pattern = re.compile(r'\b([A-Z][a-z]+R_[A-Z]\d+)\b')

        matches = req_pattern.findall(text)
        return list(set(matches))  # Remove duplicates

    def _extract_objective(self, text: str) -> str:
        """Extract objective section."""
        match = re.search(r'Objective:(.+?)(?:\n\n|\Z)', text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _extract_procedure(self, text: str) -> str:
        """Extract procedure section."""
        match = re.search(r'Procedure:(.+?)(?:\n\n|\Z)', text, re.DOTALL)
        return match.group(1).strip() if match else ""
```

#### Task 2.2: Embeddings Generation

**File**: `src/ingestion/embedder.py`

```python
"""Document embedding using OpenAI API."""
from typing import List, Dict
from openai import OpenAI
import numpy as np
import logging
import os

logger = logging.getLogger(__name__)

class DocumentEmbedder:
    """Generate embeddings for semantic search."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-large"
        self.dimensions = 3072

    def embed_requirements(self, requirements: List[Dict]) -> List[Dict]:
        """
        Add embeddings to requirement dicts.

        Args:
            requirements: List of requirement dicts from SRDParser

        Returns:
            Same list with 'statement_embedding' field added
        """
        texts = [req['statement'] for req in requirements]
        embeddings = self._batch_embed(texts)

        for req, embedding in zip(requirements, embeddings):
            req['statement_embedding'] = embedding

        logger.info(f"✓ Generated embeddings for {len(requirements)} requirements")
        return requirements

    def embed_sections(self, sections: List[Dict]) -> List[Dict]:
        """
        Add embeddings to section dicts.

        Args:
            sections: List of section dicts from PDDParser/DDDParser

        Returns:
            Same list with 'content_embedding' field added
        """
        texts = [sec.get('content', sec.get('title', '')) for sec in sections]
        embeddings = self._batch_embed(texts)

        for sec, embedding in zip(sections, embeddings):
            sec['content_embedding'] = embedding

        logger.info(f"✓ Generated embeddings for {len(sections)} sections")
        return sections

    def _batch_embed(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Batch embed texts with OpenAI API.

        Args:
            texts: List of text strings
            batch_size: Max texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]

            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    dimensions=self.dimensions
                )

                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

                logger.info(f"✓ Embedded batch {i//batch_size + 1} ({len(batch)} texts)")

            except Exception as e:
                logger.error(f"✗ Batch {i//batch_size + 1} failed: {e}")
                # Fallback: zero vectors
                all_embeddings.extend([[0.0] * self.dimensions] * len(batch))

        return all_embeddings
```

#### Task 2.3: Neo4j Loader (Enhanced)

**File**: `src/ingestion/neo4j_loader.py`

```python
"""Load parsed documents into Neo4j."""
from typing import List, Dict
from src.utils.neo4j_client import Neo4jClient
from src.utils.entity_resolver import entity_resolver
import logging

logger = logging.getLogger(__name__)

class MOSARGraphLoader:
    """Load MOSAR documents into Neo4j graph."""

    def __init__(self):
        """Initialize Neo4j client."""
        self.client = Neo4jClient()

    def load_srd(self, requirements: List[Dict]):
        """
        Load requirements from SRD.

        Creates:
        - Requirement nodes
        - RequirementType classification
        - Organization nodes
        - ASSIGNED_TO relationships
        """
        cypher = """
        UNWIND $requirements AS req

        // Create Requirement node
        MERGE (r:Requirement {id: req.id})
        SET r.title = req.title,
            r.statement = req.statement,
            r.type = req.type,
            r.subsystem = req.subsystem,
            r.level = req.level,
            r.verification_method = req.verification,
            r.comment = req.comment,
            r.statement_embedding = req.statement_embedding

        // Create Organization nodes
        WITH r, req
        UNWIND split(req.responsible, ',') AS org_name
        WITH r, trim(org_name) AS org_name
        WHERE org_name <> ''

        MERGE (org:Organization {name: org_name})
        MERGE (r)-[:ASSIGNED_TO]->(org)
        """

        self.client.execute(cypher, requirements=requirements)
        logger.info(f"✅ Loaded {len(requirements)} requirements to Neo4j")

        # Create COVERS relationships
        self._create_covers_relationships(requirements)

        # Create entity relationships (Phase 2 dual usage)
        self._create_entity_relationships_from_requirements(requirements)

    def _create_covers_relationships(self, requirements: List[Dict]):
        """Create DERIVES_FROM relationships from COVERS field."""
        cypher = """
        UNWIND $requirements AS req
        MATCH (child:Requirement {id: req.id})

        WITH child, req.covers AS covers_str
        WHERE covers_str IS NOT NULL AND covers_str <> ''

        // Extract parent requirement IDs
        WITH child, split(covers_str, ',') AS parent_ids
        UNWIND parent_ids AS parent_id
        WITH child, trim(parent_id) AS parent_id
        WHERE parent_id =~ '[A-Z][a-z]+R_[A-Z]\\d+'

        MATCH (parent:Requirement {id: parent_id})
        MERGE (child)-[:DERIVES_FROM]->(parent)
        """

        self.client.execute(cypher, requirements=requirements)
        logger.info("✓ Created DERIVES_FROM relationships")

    def _create_entity_relationships_from_requirements(self, requirements: List[Dict]):
        """
        Phase 2 dual usage of Entity Dictionary:
        Pre-create RELATES_TO relationships from requirement text to entities.
        """
        for req in requirements:
            text = req['statement'] + ' ' + req.get('comment', '')
            entities = entity_resolver.resolve(text)

            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    if entity_type == "Component":
                        self._link_requirement_to_component(req['id'], entity['id'])
                    elif entity_type == "Scenario":
                        self._link_requirement_to_scenario(req['id'], entity['id'])

        logger.info("✓ Created entity relationships from requirements")

    def _link_requirement_to_component(self, req_id: str, component_id: str):
        """Create RELATES_TO relationship."""
        cypher = """
        MATCH (req:Requirement {id: $req_id})
        MERGE (comp:Component {id: $component_id})
        MERGE (req)-[:RELATES_TO]->(comp)
        """
        self.client.execute(cypher, req_id=req_id, component_id=component_id)

    def _link_requirement_to_scenario(self, req_id: str, scenario_id: str):
        """Create VALIDATED_BY relationship."""
        cypher = """
        MATCH (req:Requirement {id: $req_id})
        MERGE (scenario:Scenario {id: $scenario_id})
        MERGE (req)-[:VALIDATED_BY]->(scenario)
        """
        self.client.execute(cypher, req_id=req_id, scenario_id=scenario_id)

    def load_demo_procedures(self, test_cases: List[Dict]):
        """
        Load test cases from Demonstration Procedures.

        Creates:
        - TestCase nodes
        - VERIFIED_BY relationships (TestCase → Requirement)
        """
        cypher = """
        UNWIND $test_cases AS tc

        // Create TestCase node
        MERGE (t:TestCase {id: tc.id})
        SET t.type = tc.type,
            t.name = tc.name,
            t.objective = tc.objective,
            t.procedure = tc.procedure,
            t.status = 'Planned'

        // Create VERIFIED_BY relationships
        WITH t, tc
        UNWIND tc.covered_requirements AS req_id

        MATCH (req:Requirement {id: req_id})
        MERGE (t)-[:VERIFIES]->(req)
        """

        self.client.execute(cypher, test_cases=test_cases)
        logger.info(f"✅ Loaded {len(test_cases)} test cases to Neo4j")
```

#### Success Criteria
- ✅ 227 requirements loaded
- ✅ Test cases loaded with VERIFIES relationships
- ✅ 500+ sections embedded
- ✅ Entity relationships created
- ✅ Sample Cypher queries work

---

### **Phase 3: LangGraph Workflow Construction (Day 15-24)**

#### Task 3.1: State Definition

**File**: `src/graphrag/state.py`

```python
"""LangGraph state definitions."""
from typing import TypedDict, Literal, List, Dict, Optional

class GraphRAGState(TypedDict):
    """State for GraphRAG workflow."""

    # Input
    question: str
    user_id: str
    session_id: str

    # Query Analysis
    query_type: Literal["structural", "semantic", "hybrid"]
    entities: Dict[str, List[Dict]]  # {"Component": [{"id": "R-ICU", "confidence": 0.9}]}
    confidence: float

    # Cypher Path
    cypher_query: Optional[str]
    cypher_results: List[Dict]

    # Vector Path
    vector_context: List[Dict]  # [{"chunk": str, "score": float, "section": str}]
    top_k_nodes: List[str]  # Node IDs from vector search

    # Hybrid Path (NEW)
    extracted_entities: Dict[str, List[str]]  # Entities from NER on vector results
    graph_context: Dict[str, List[Dict]]  # {"requirements": [...], "components": [...]}

    # Response
    answer: str
    sources: List[Dict]

    # Metadata
    execution_path: List[str]
    cache_hit: bool
    error: Optional[str]
```

#### Task 3.2: Core Nodes Implementation

**File**: `src/graphrag/nodes/query_classifier.py`

```python
"""Query classification and routing."""
from src.graphrag.state import GraphRAGState
from src.utils.entity_resolver import entity_resolver
import logging

logger = logging.getLogger(__name__)

def classify_query(state: GraphRAGState) -> GraphRAGState:
    """
    Analyze question and determine query strategy.

    Routes to:
    - "structural": Clear entities → Template Cypher
    - "semantic": No entities → Vector search
    - "hybrid": Partial entities → Vector → Cypher
    """
    question = state["question"]

    # Step 1: Entity Dictionary Lookup
    entities = entity_resolver.resolve(question, threshold=85)

    # Step 2: Decision Logic
    if entities:
        # Calculate average confidence
        all_entities = [e for elist in entities.values() for e in elist]
        avg_confidence = sum(e['confidence'] for e in all_entities) / len(all_entities)

        if avg_confidence > 0.9:
            # High confidence → Direct structural query
            query_type = "structural"
            logger.info(f"✓ Classified as STRUCTURAL (confidence: {avg_confidence:.2f})")
        else:
            # Moderate confidence → Hybrid approach
            query_type = "hybrid"
            logger.info(f"✓ Classified as HYBRID (confidence: {avg_confidence:.2f})")

        confidence = avg_confidence
    else:
        # No entities found → Semantic search
        query_type = "semantic"
        confidence = 0.3
        logger.info("✓ Classified as SEMANTIC (no entities)")

    return {
        **state,
        "query_type": query_type,
        "entities": entities,
        "confidence": confidence,
        "execution_path": state.get("execution_path", []) + [f"classify→{query_type}"]
    }
```

**File**: `src/graphrag/nodes/vector_search.py` (NEW)

```python
"""Vector similarity search in Neo4j."""
from src.graphrag.state import GraphRAGState
from src.utils.neo4j_client import Neo4jClient
from openai import OpenAI
import os
import logging

logger = logging.getLogger(__name__)

client_neo4j = Neo4jClient()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_vector_search(state: GraphRAGState) -> GraphRAGState:
    """
    Perform vector similarity search.

    Returns top-k most similar sections/requirements.
    """
    question = state["question"]

    # Generate query embedding
    response = client_openai.embeddings.create(
        model="text-embedding-3-large",
        input=question,
        dimensions=3072
    )
    query_embedding = response.data[0].embedding

    # Neo4j vector search
    cypher = """
    CALL db.index.vector.queryNodes(
        'section_embeddings',
        10,
        $embedding
    ) YIELD node, score
    WHERE score > 0.75

    RETURN
        node.id AS node_id,
        node.title AS title,
        node.content AS content,
        node.doc_id AS doc_id,
        node.number AS section_number,
        score
    ORDER BY score DESC
    """

    results = client_neo4j.query(cypher, embedding=query_embedding)

    logger.info(f"✓ Vector search found {len(results)} relevant sections")

    return {
        **state,
        "vector_context": results,
        "top_k_nodes": [r["node_id"] for r in results[:5]],
        "execution_path": state["execution_path"] + ["vector_search"]
    }
```

**File**: `src/graphrag/nodes/entity_extractor.py` (NEW)

```python
"""Extract entities from vector search results using NER."""
from src.graphrag.state import GraphRAGState
import spacy
import logging

logger = logging.getLogger(__name__)

# Load spaCy model (assumes installed: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_entities_from_context(state: GraphRAGState) -> GraphRAGState:
    """
    Run NER on vector search results to extract entities.

    Extracts: Component names, Requirement IDs, Protocol names
    """
    vector_context = state["vector_context"]

    # Combine top-3 results
    combined_text = "\n\n".join([
        ctx["content"][:1000]  # Limit to 1000 chars per section
        for ctx in vector_context[:3]
    ])

    # Run spaCy NER
    doc = nlp(combined_text)

    # Extract entities (customize based on your NER model)
    extracted = {
        "Component": [],
        "Requirement": [],
        "Protocol": []
    }

    # Simple regex for requirement IDs
    import re
    req_ids = re.findall(r'\b([A-Z][a-z]+R_[A-Z]\d+)\b', combined_text)
    extracted["Requirement"] = list(set(req_ids))

    # TODO: Train custom NER for Components/Protocols
    # For now, use entity_resolver on text chunks
    from src.utils.entity_resolver import entity_resolver
    resolved = entity_resolver.resolve(combined_text)

    if "Component" in resolved:
        extracted["Component"] = [e["id"] for e in resolved["Component"]]
    if "Protocol" in resolved:
        extracted["Protocol"] = [e["id"] for e in resolved["Protocol"]]

    logger.info(f"✓ Extracted entities: {extracted}")

    return {
        **state,
        "extracted_entities": extracted,
        "execution_path": state["execution_path"] + ["entity_extraction"]
    }
```

**File**: `src/graphrag/nodes/contextual_cypher.py` (NEW - Key for Hybrid)

```python
"""Execute contextual Cypher based on extracted entities."""
from src.graphrag.state import GraphRAGState
from src.utils.neo4j_client import Neo4jClient
import logging

logger = logging.getLogger(__name__)

client = Neo4jClient()

def run_contextual_cypher(state: GraphRAGState) -> GraphRAGState:
    """
    Build and execute Cypher query based on extracted entities.

    This is the "Vector → Cypher" bridge in hybrid mode.
    """
    extracted_entities = state["extracted_entities"]
    top_k_nodes = state["top_k_nodes"]

    # Build dynamic Cypher
    cypher_parts = []
    params = {}

    # Start from vector-found sections
    cypher_parts.append("""
    MATCH (section:Section)
    WHERE section.id IN $section_ids
    """)
    params["section_ids"] = top_k_nodes

    # Find related requirements
    if extracted_entities.get("Requirement"):
        cypher_parts.append("""
        MATCH (section)-[:MENTIONS|DEFINED_IN]-(req:Requirement)
        WHERE req.id IN $req_ids
        """)
        params["req_ids"] = extracted_entities["Requirement"]

    # Find related components
    if extracted_entities.get("Component"):
        cypher_parts.append("""
        OPTIONAL MATCH (req)-[:IMPLEMENTED_BY]->(comp:Component)
        WHERE comp.id IN $comp_ids
        """)
        params["comp_ids"] = extracted_entities["Component"]

    # Final return
    cypher_parts.append("""
    RETURN
        section.id AS section_id,
        section.title AS section_title,
        collect(DISTINCT req.id) AS requirements,
        collect(DISTINCT comp.id) AS components
    LIMIT 20
    """)

    cypher = "\n".join(cypher_parts)

    # Execute
    results = client.query(cypher, **params)

    # Organize results
    graph_context = {
        "requirements": [],
        "components": []
    }

    for row in results:
        graph_context["requirements"].extend(row.get("requirements", []))
        graph_context["components"].extend(row.get("components", []))

    # Deduplicate
    graph_context["requirements"] = list(set(graph_context["requirements"]))
    graph_context["components"] = list(set(graph_context["components"]))

    logger.info(f"✓ Contextual Cypher found: {len(graph_context['requirements'])} reqs, {len(graph_context['components'])} comps")

    return {
        **state,
        "graph_context": graph_context,
        "execution_path": state["execution_path"] + ["contextual_cypher"]
    }
```

**File**: `src/graphrag/nodes/response_synthesizer.py`

```python
"""Synthesize final response using LLM."""
from src.graphrag.state import GraphRAGState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import logging

logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def synthesize_hybrid_response(state: GraphRAGState) -> GraphRAGState:
    """
    Synthesize response from vector + graph context.

    Uses LLM to combine:
    - Vector search results (document excerpts)
    - Graph traversal results (structured entities)
    """
    question = state["question"]
    vector_context = state.get("vector_context", [])
    graph_context = state.get("graph_context", {})

    # Prepare vector snippets
    vector_snippets = "\n\n".join([
        f"**[{ctx['doc_id']} {ctx['section_number']}] {ctx['title']}** (relevance: {ctx['score']:.2f})\n"
        f"{ctx['content'][:500]}..."
        for ctx in vector_context[:3]
    ])

    # Prepare graph info
    graph_info = f"""
    Related Requirements: {', '.join(graph_context.get('requirements', [])[:10])}
    Related Components: {', '.join(graph_context.get('components', [])[:10])}
    """

    # LLM prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a technical documentation assistant for the MOSAR spacecraft project.

        Answer questions using BOTH:
        1. Document excerpts (from vector search)
        2. Structured knowledge graph relationships (from Cypher queries)

        Cite specific requirement IDs and component names.
        If information is incomplete, state what is known and what is missing."""),
        ("user", """Question: {question}

        === Document Context (Vector Search) ===
        {vector_context}

        === Related Graph Entities (Cypher Query) ===
        {graph_context}

        Provide a comprehensive answer with citations.""")
    ])

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "vector_context": vector_snippets,
        "graph_context": graph_info
    })

    return {
        **state,
        "answer": response.content,
        "sources": [
            {"type": "vector", "count": len(vector_context)},
            {"type": "graph", "entities": graph_context}
        ],
        "execution_path": state["execution_path"] + ["hybrid_synthesis"]
    }
```

#### Task 3.3: Workflow Assembly (Enhanced)

**File**: `src/graphrag/workflow.py`

```python
"""LangGraph workflow assembly."""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.graphrag.state import GraphRAGState
from src.graphrag.nodes.query_classifier import classify_query
from src.graphrag.nodes.cypher_executor import run_cypher_template
from src.graphrag.nodes.vector_search import run_vector_search
from src.graphrag.nodes.entity_extractor import extract_entities_from_context
from src.graphrag.nodes.contextual_cypher import run_contextual_cypher
from src.graphrag.nodes.response_synthesizer import (
    generate_simple_response,
    synthesize_hybrid_response
)

import logging

logger = logging.getLogger(__name__)

def build_workflow():
    """Construct LangGraph workflow with 3 paths."""

    # Create graph
    workflow = StateGraph(GraphRAGState)

    # Add nodes
    workflow.add_node("classify_query", classify_query)
    workflow.add_node("run_cypher_template", run_cypher_template)
    workflow.add_node("run_vector_search", run_vector_search)
    workflow.add_node("extract_entities_from_context", extract_entities_from_context)
    workflow.add_node("run_contextual_cypher", run_contextual_cypher)
    workflow.add_node("generate_simple_response", generate_simple_response)
    workflow.add_node("synthesize_hybrid_response", synthesize_hybrid_response)

    # Define routing function
    def route_query(state: GraphRAGState) -> str:
        """Route based on query_type."""
        query_type = state["query_type"]

        if query_type == "structural":
            return "run_cypher_template"
        elif query_type == "semantic":
            return "run_vector_search"
        else:  # hybrid
            return "run_vector_search"  # Start with vector, then graph

    # Set entry point
    workflow.set_entry_point("classify_query")

    # Add conditional routing
    workflow.add_conditional_edges(
        "classify_query",
        route_query,
        {
            "run_cypher_template": "run_cypher_template",
            "run_vector_search": "run_vector_search"
        }
    )

    # Path 1: Structural (Cypher only)
    workflow.add_edge("run_cypher_template", "generate_simple_response")
    workflow.add_edge("generate_simple_response", END)

    # Path 2 & 3: Semantic/Hybrid (Vector → Entity → Cypher → Synthesis)
    workflow.add_edge("run_vector_search", "extract_entities_from_context")
    workflow.add_edge("extract_entities_from_context", "run_contextual_cypher")
    workflow.add_edge("run_contextual_cypher", "synthesize_hybrid_response")
    workflow.add_edge("synthesize_hybrid_response", END)

    # Compile with checkpointing
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    logger.info("✅ LangGraph workflow compiled")
    return app

# Singleton
graphrag_app = build_workflow()
```

#### Task 3.4: CLI Interface

**File**: `src/graphrag/app.py`

```python
"""Command-line interface for GraphRAG."""
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from src.graphrag.workflow import graphrag_app
import uuid

console = Console()

def main():
    """Interactive CLI."""
    console.print(Panel.fit(
        "[bold cyan]MOSAR GraphRAG System[/bold cyan]\n"
        "Ask questions about requirements, design, and tests.",
        border_style="cyan"
    ))

    session_id = str(uuid.uuid4())

    while True:
        # Get question
        console.print("\n[bold yellow]Your question[/bold yellow] (or 'quit'):")
        question = input("> ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            console.print("[green]Goodbye![/green]")
            break

        if not question:
            continue

        # Execute workflow
        try:
            result = graphrag_app.invoke(
                {
                    "question": question,
                    "user_id": "cli_user",
                    "session_id": session_id,
                    "execution_path": []
                },
                config={"configurable": {"thread_id": session_id}}
            )

            # Display answer
            console.print("\n[bold green]Answer:[/bold green]")
            console.print(Markdown(result["answer"]))

            # Display metadata
            console.print(f"\n[dim]Execution path: {' → '.join(result['execution_path'])}[/dim]")
            console.print(f"[dim]Sources: {result.get('sources', [])}[/dim]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
```

#### Success Criteria
- ✅ 3 query paths work (structural, semantic, hybrid)
- ✅ CLI accepts questions and returns answers
- ✅ LangSmith traces show execution flow
- ✅ Response time < 2 seconds for structural queries
- ✅ Hybrid queries successfully combine vector + graph

---

### **Phase 4: Testing & Validation (Day 25-29)**

#### Task 4.1: Unit Tests

**File**: `tests/test_nodes.py`

```python
"""Unit tests for LangGraph nodes."""
import pytest
from src.graphrag.nodes.query_classifier import classify_query
from src.graphrag.state import GraphRAGState

def test_classify_query_structural():
    """Test structural query classification."""
    state = {
        "question": "R-ICU를 변경하면 어떤 요구사항이 영향받나?",
        "execution_path": []
    }

    result = classify_query(state)

    assert result["query_type"] == "structural"
    assert "Component" in result["entities"]
    assert result["entities"]["Component"][0]["id"] == "R-ICU"
    assert result["confidence"] > 0.9

def test_classify_query_semantic():
    """Test semantic query classification."""
    state = {
        "question": "열 관리 시스템은 어떻게 설계되었나?",
        "execution_path": []
    }

    result = classify_query(state)

    # No clear entities → semantic
    assert result["query_type"] in ["semantic", "hybrid"]
    assert result["confidence"] < 0.9
```

#### Task 4.2: End-to-End Tests

**File**: `tests/test_e2e.py`

```python
"""End-to-end tests for 5 key questions."""
import pytest
from src.graphrag.workflow import graphrag_app

@pytest.fixture
def session_config():
    """Test session configuration."""
    return {"configurable": {"thread_id": "test_session"}}

def test_question_1_component_impact(session_config):
    """Q1: R-ICU 변경 시 영향받는 요구사항?"""
    result = graphrag_app.invoke(
        {
            "question": "R-ICU 하드웨어를 변경하면 어떤 요구사항이 영향받나?",
            "user_id": "test_user",
            "session_id": "test",
            "execution_path": []
        },
        config=session_config
    )

    # Assertions
    assert result["answer"]  # Non-empty answer
    assert "structural" in result["execution_path"][0]  # Should use structural path
    assert len(result.get("cypher_results", [])) > 0  # Found requirements

def test_question_2_scenario_failure(session_config):
    """Q2: Scenario S2 실패 시 대안 검증 방법?"""
    result = graphrag_app.invoke(
        {
            "question": "Scenario S2가 실패했을 때 대안 검증 방법은?",
            "user_id": "test_user",
            "session_id": "test",
            "execution_path": []
        },
        config=session_config
    )

    assert result["answer"]
    assert any("S2" in str(s) for s in result.get("sources", []))

# ... More E2E tests for questions 3-5
```

#### Task 4.3: Benchmark

**File**: `notebooks/benchmark.ipynb`

```python
"""Performance benchmarking."""
import time
from src.graphrag.workflow import graphrag_app

questions = [
    ("structural", "FuncR_A101을 구현한 컴포넌트는?"),
    ("semantic", "열 관리 인터페이스 관련 내용은?"),
    ("hybrid", "WM의 안전 요구사항과 테스트는?")
]

results = []

for query_type, question in questions:
    start = time.time()

    result = graphrag_app.invoke({
        "question": question,
        "user_id": "benchmark",
        "session_id": f"bench_{query_type}",
        "execution_path": []
    })

    elapsed = time.time() - start

    results.append({
        "type": query_type,
        "question": question,
        "time_ms": elapsed * 1000,
        "path": result["execution_path"]
    })

# Analysis
import pandas as pd
df = pd.DataFrame(results)
print(df)
print(f"\nAverage response time: {df['time_ms'].mean():.0f}ms")
```

#### Success Criteria
- ✅ All unit tests pass
- ✅ 5 E2E tests pass with 90%+ accuracy
- ✅ Average response time < 2000ms
- ✅ Structural queries < 500ms
- ✅ Test coverage > 80%

---

## 📦 Final Deliverables

### Codebase
```
src/
├── graphrag/          # LangGraph workflows (7 files)
├── ingestion/         # Document parsers (5 files)
├── neo4j_schema/      # Schema scripts (2 files)
└── utils/             # Helpers (2 files)

data/
├── entities/          # Entity Dictionary (1 file)
└── templates/         # Cypher templates (1 file)

tests/                 # Unit & E2E tests (3 files)
notebooks/             # Benchmarks (1 file)
scripts/               # Execution scripts (2 files)
```

### Documentation
- ✅ `README.md`: Setup & usage guide
- ✅ `PRD.md`: This document
- ✅ `ARCHITECTURE.md`: System architecture
- ✅ API documentation (auto-generated from docstrings)

### Data Assets
- ✅ Neo4j database with ~800 nodes
- ✅ 227 requirements with embeddings
- ✅ Test cases with VERIFIES relationships
- ✅ Entity Dictionary (100+ mappings)

---

## 📊 Success Metrics Summary

| Metric | Target | Measurement |
|--------|--------|-------------|
| Requirements loaded | 227 | `MATCH (r:Requirement) RETURN count(r)` |
| Test cases loaded | 50+ | `MATCH (tc:TestCase) RETURN count(tc)` |
| Embeddings generated | 500+ | `MATCH (n) WHERE n.content_embedding IS NOT NULL RETURN count(n)` |
| Query accuracy | 90%+ | E2E test pass rate |
| Response time (structural) | < 500ms | Benchmark results |
| Response time (hybrid) | < 2s | Benchmark results |
| Test coverage | 80%+ | `pytest --cov` |

---

## ⏱️ Timeline

| Phase | Duration | Completion Criteria |
|-------|----------|---------------------|
| **Phase 0** | Day 1-2 | Neo4j connected, dependencies installed |
| **Phase 1** | Day 3-7 | Schema created, Entity Dictionary ready |
| **Phase 2** | Day 8-14 | Documents parsed, Neo4j loaded, embeddings generated |
| **Phase 3** | Day 15-24 | LangGraph workflow operational, CLI working |
| **Phase 4** | Day 25-29 | Tests passing, benchmarks complete |
| **Total** | **~4 weeks** | Production-ready system |

---

## 🚨 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Document parsing errors | Medium | Medium | Manual validation + regex refinement |
| OpenAI API cost overrun | Low | Medium | Use local embeddings (sentence-transformers) |
| LangGraph bugs | Low | High | Fallback to LlamaIndex if needed |
| Neo4j performance issues | Medium | Medium | Index optimization + query tuning |
| NER accuracy issues | Medium | Low | Rely on Entity Dictionary primarily |

---

## 🔧 Development Setup

### Prerequisites
```bash
# Python 3.11+
python --version

# Neo4j Desktop or Docker
docker run --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.14
```

### Installation
```bash
# Clone repo
cd C:\Hee\SpaceAI\ReqEng

# Install Poetry
pip install poetry

# Install dependencies
poetry install

# Activate environment
poetry shell

# Setup environment
cp .env.example .env
# Edit .env with your keys

# Create Neo4j schema
python src/neo4j_schema/create_schema.py

# Load documents
python scripts/load_documents.py

# Run CLI
python src/graphrag/app.py
```

---

## 📚 References

### Documents
- System Requirements Document (SRD)
- Preliminary Design Document (PDD)
- Detailed Design Document (DDD)
- Demonstration Procedures (Demo)

### Technologies
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/)
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [spaCy NLP](https://spacy.io/)

---

## 🎯 Next Steps After Phase 4

### Phase 5 (Optional): Advanced Features
- [ ] Text2Cypher with guardrails
- [ ] Human-in-the-loop (HITL) approval
- [ ] Multi-turn dialogue support
- [ ] Streaming responses
- [ ] Parallel query execution

### Phase 6 (Optional): Production Deployment
- [ ] FastAPI REST API
- [ ] Web UI (React/Streamlit)
- [ ] Authentication & authorization
- [ ] Monitoring & logging (Prometheus/Grafana)
- [ ] Docker Compose deployment

---

**Document Status**: ✅ Ready for Implementation
**Approved By**: Project Team
**Date**: 2025-01-26
**Version**: 1.0
