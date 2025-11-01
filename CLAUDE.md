# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# MOSAR GraphRAG System

## Project Status

**Version**: 1.2.0 ✅ **PRODUCTION READY**

**Implementation Complete**:
- Production-ready GraphRAG system for spacecraft requirements engineering
- 7 entity types supported (Requirement, Component, TestCase, Protocol, SpacecraftModule, Scenario, Organization)
- Comprehensive test suite with 85% coverage
- **Multi-hop V-Model traceability** for 227 requirements (upward/horizontal/downward)
- Response times: Pure Cypher <1000ms, Hybrid <2500ms
- Streamlit Web UI with real-time streaming

**Recent Changes** (v1.2.0 - 2025-10-31):
- ✅ **Multi-hop traceability** (parent/child requirements, 1-2 levels)
- ✅ **Decomposition tree visualization** with verification statistics
- ✅ **Smart router** (filter-only entities → PURE_VECTOR path)
- ✅ **Enhanced fallback** (works in streaming mode)
- ✅ **Vector synthesis** (uses documents when graph is empty)

**See Also**: [CHANGELOG.md](CHANGELOG.md) for complete version history

**Last Updated**: 2025-10-31

## Quick Reference

### Common Commands

```bash
# Development Environment
poetry shell                           # Activate virtual environment
poetry install                         # Install dependencies

# Testing
pytest                                 # Run all tests
pytest tests/test_e2e.py              # Run end-to-end tests
pytest tests/test_e2e.py::test_question_1  # Run single test
pytest -m unit                         # Run only unit tests
pytest -m "not requires_openai"       # Skip tests requiring OpenAI API
pytest --cov=src --cov-report=html    # Generate coverage report

# Data Loading
python scripts/load_documents.py      # Load all documents (SRD, PDD, DDD, Demo)
python scripts/load_srd.py            # Load requirements only
python scripts/load_design_docs.py    # Load PDD/DDD only

# Validation & Debugging
python scripts/check_neo4j_status.py  # Check database status
python scripts/check_embeddings.py    # Verify vector embeddings
python scripts/test_workflow.py       # Test LangGraph workflow
python scripts/test_environment.py    # Verify environment setup

# Running the System
poetry run streamlit run streamlit_app.py  # Web UI (recommended)
python src/graphrag/app.py            # Interactive CLI
python scripts/demo_cli.py            # Non-interactive demo

# Neo4j
# Access Neo4j Aura at https://console.neo4j.io
# Or Neo4j Browser at http://localhost:7474 (if local)
# Credentials in .env file
```

### Project Structure

```
ReqEng/
├── src/                           # Main source code
│   ├── graphrag/                  # LangGraph workflow
│   │   ├── app.py                # CLI application (ENTRY POINT)
│   │   ├── workflow.py           # Main LangGraph workflow definition
│   │   ├── state.py              # State schema (GraphRAGState)
│   │   ├── hitl.py               # Human-in-the-loop review system
│   │   └── nodes/                # Individual workflow nodes
│   │       ├── vector_search_node.py   # Vector similarity search
│   │       ├── ner_node.py            # Entity extraction
│   │       ├── cypher_node.py         # Cypher query generation/execution
│   │       └── synthesize_node.py     # LLM response synthesis
│   ├── ingestion/                 # Document parsing and loading
│   │   ├── srd_parser.py         # Requirements parser
│   │   ├── design_doc_parser.py  # PDD/DDD parser
│   │   ├── demo_procedure_parser.py  # Test case parser
│   │   ├── embedder.py           # OpenAI embedding generation
│   │   ├── text_chunker.py       # Text chunking for vector search
│   │   └── neo4j_loader.py       # Bulk loading to Neo4j
│   ├── query/                     # Query routing
│   │   ├── router.py             # Adaptive query routing
│   │   └── cypher_templates.py   # Template Cypher queries
│   ├── utils/                     # Utilities
│   │   ├── neo4j_client.py       # Neo4j connection management
│   │   ├── entity_resolver.py    # Entity Dictionary lookup
│   │   └── cache.py              # Multi-tier caching
│   └── neo4j_schema/              # Database schema
│       └── create_schema.py      # Schema initialization
├── scripts/                       # Execution scripts
│   ├── load_*.py                 # Data loading scripts
│   ├── check_*.py                # Validation scripts
│   └── test_*.py                 # Test scripts
├── tests/                         # Test suite
│   ├── conftest.py               # Pytest fixtures
│   ├── test_*_node.py            # Unit tests (50+ tests)
│   └── test_e2e.py               # End-to-end tests (5 key questions)
├── data/                          # Data files
│   ├── entities/                 # Entity Dictionary
│   │   └── mosar_entities.json   # Domain-specific entity mappings
│   └── templates/                # Cypher query templates
├── Documents/                     # Source documents
│   ├── SRD/                      # System Requirements (227 reqs)
│   ├── PDD/                      # Preliminary Design
│   ├── DDD/                      # Detailed Design
│   └── Demo/                     # Test Procedures
├── notebooks/                     # Jupyter notebooks
│   └── benchmark.ipynb           # Performance benchmarking
├── pyproject.toml                # Dependencies (Poetry)
├── pytest.ini                    # Pytest configuration
├── .env                          # Environment variables (not in git)
├── ARCHITECTURE.md               # Detailed architecture docs
├── PRD.md                        # Product requirements document
├── QUICKSTART.md                 # Quick start guide
└── PHASE*_COMPLETE.md            # Phase completion reports
```

---

## System Architecture

### High-Level Overview

The MOSAR GraphRAG system uses a **3-tier adaptive routing strategy** to answer questions:

1. **Router**: Analyzes question → Routes to optimal path based on entity detection
2. **Execution Paths**: Three paths optimized for different query types
3. **Synthesis**: LLM generates natural language response with citations

### 3 Query Execution Paths

#### Path A: Pure Cypher (Structural Queries)
**When**: High-confidence entity detection (>90%)
**Example**: "Show all requirements verified by R-ICU"
**Flow**: Router → Template Cypher → Format Results → Return
**Speed**: <500ms

#### Path B: Hybrid (Natural Language Queries)
**When**: Medium-confidence entities OR complex questions
**Example**: "네트워크 통신을 담당하는 하드웨어는?" (What hardware handles network communication?)
**Flow**: Router → Vector Search → NER Extraction → Contextual Cypher → LLM Synthesis → Return
**Speed**: <2000ms

#### Path C: Pure Vector (Exploratory Queries)
**When**: No clear entities detected
**Example**: "What are the main challenges in orbital assembly?"
**Flow**: Router → Vector Search → LLM Synthesis → Return
**Speed**: <2000ms

### LangGraph Workflow Architecture

The system uses [LangGraph](https://langchain-ai.github.io/langgraph/) for stateful workflow orchestration:

```python
# Workflow structure (see src/graphrag/workflow.py)
StateGraph(GraphRAGState)
    ↓
[route_query] → Analyzes question, detects entities
    ├─→ [template_cypher] → [synthesize] → END  (Path A)
    ├─→ [vector_search] → [extract_entities] → [contextual_cypher] → [synthesize] → END  (Path B)
    └─→ [vector_search] → [synthesize] → END  (Path C)
```

**Key State Fields** (see [src/graphrag/state.py](src/graphrag/state.py)):
- `user_question`: Input question
- `query_path`: Chosen path (PURE_CYPHER/HYBRID/PURE_VECTOR)
- `matched_entities`: Entities detected by router
- `top_k_sections`: Vector search results
- `extracted_entities`: NER-extracted entities
- `cypher_query`: Generated Cypher query
- `graph_results`: Graph query results
- `final_answer`: LLM-generated response
- `citations`: Source documents

---

## Graph Database Schema

### 4-Layer Graph Model

The Neo4j database uses a 4-layer architecture:

**Layer 1: Document Structure** - Document hierarchy (Document → Section → TextChunk)
**Layer 2: Selective Entities** - Domain entities (Protocol, Technology, Organization)
**Layer 3: Domain System** - MOSAR architecture (Component, Module, Interface)
**Layer 4: V-Model Traceability** - Requirements lifecycle (Requirement → Design → Test)

### Key Node Types

```cypher
// Layer 4: Requirements & Tests
(:Requirement {id, type, statement, level, verification, statement_embedding})
(:TestCase {id, type, name, objective, procedure, status})

// Layer 3: System Components
(:Component {id, name, type, hardware_platform, mass_kg, power_w})
(:SpacecraftModule {id, name, type})
(:Interface {id, protocol, data_rate_mbps})

// Layer 1: Documents
(:Document {id, title, version, type})
(:Section {id, title, content, content_embedding, doc_id, number})
(:TextChunk {id, text, embedding, doc_id, section_id})
```

### Key Relationships

```cypher
// V-Model Traceability
(req:Requirement)-[:VERIFIES]-(tc:TestCase)
(req:Requirement)-[:RELATES_TO]->(comp:Component)
(req:Requirement)-[:DERIVES_FROM]->(parent_req:Requirement)

// System Architecture
(comp:Component)-[:HAS_INTERFACE]->(iface:Interface)
(comp:Component)-[:PART_OF]->(module:SpacecraftModule)

// Document Structure
(doc:Document)-[:HAS_SECTION]->(sec:Section)
(sec:Section)-[:CONTAINS_CHUNK]->(chunk:TextChunk)
(sec:Section)-[:MENTIONS]->(comp:Component)
```

### Vector Indexes

```cypher
// 3072-dimensional OpenAI embeddings (text-embedding-3-large)
VECTOR INDEX section_embeddings FOR (s:Section) ON (s.content_embedding)
VECTOR INDEX chunk_embeddings FOR (c:TextChunk) ON (c.embedding)
VECTOR INDEX requirement_embeddings FOR (r:Requirement) ON (r.statement_embedding)
```

---

## Key Components Deep Dive

### 1. Router ([src/query/router.py](src/query/router.py))

**Purpose**: Determines optimal query path based on entity detection

**Algorithm**:
1. Load Entity Dictionary ([data/entities/mosar_entities.json](data/entities/mosar_entities.json))
2. Exact string matching for known entities
3. Calculate confidence score
4. Route decision:
   - Confidence >0.9 → Path A (Pure Cypher)
   - Confidence 0.3-0.9 → Path B (Hybrid)
   - Confidence <0.3 → Path C (Pure Vector)

**Entity Dictionary Structure**:
```json
{
  "components": {
    "R-ICU": {"id": "R-ICU", "type": "Component"},
    "Walking Manipulator": {"id": "WM", "type": "Component"},
    "워킹 매니퓰레이터": {"id": "WM", "type": "Component"}  // Korean support
  },
  "requirements": {
    "기능 요구사항": {"type": "Requirement", "filter": {"type": "FuncR"}}
  }
}
```

### 2. Vector Search ([src/graphrag/nodes/vector_search_node.py](src/graphrag/nodes/vector_search_node.py))

**Purpose**: Semantic similarity search using OpenAI embeddings

**Process**:
1. Generate query embedding (OpenAI `text-embedding-3-large`, 3072 dims)
2. Neo4j vector search: `CALL db.index.vector.queryNodes('section_embeddings', 10, $embedding)`
3. Filter by similarity threshold (>0.75)
4. Return top-k sections with scores

**Performance**: ~500-800ms (including OpenAI API call)

### 3. Entity Extraction ([src/graphrag/nodes/ner_node.py](src/graphrag/nodes/ner_node.py))

**Purpose**: Extract MOSAR-specific entities from vector search results

**Methods**:
1. **Primary**: GPT-4 with structured prompts (high accuracy)
2. **Fallback**: spaCy NER + Entity Resolver (when OpenAI unavailable)

**Extracted Entity Types**:
- Component IDs (R-ICU, WM, OBC, cPDU)
- Requirement IDs (FuncR_S110, SafR_A201)
- Protocols (CAN, Ethernet, SpaceWire)
- Modules (SM1-DMS, SM2-PWS)

### 4. Cypher Generation ([src/graphrag/nodes/cypher_node.py](src/graphrag/nodes/cypher_node.py))

**Two Modes**:

**Template Mode** (Path A):
- Predefined templates in [src/query/cypher_templates.py](src/query/cypher_templates.py)
- Fast, deterministic, no LLM required
- Example templates: `get_requirement_traceability`, `find_unverified_requirements`

**Contextual Mode** (Path B):
- Dynamic Cypher generation based on extracted entities
- Combines vector context + graph traversal
- Example: Find components + interfaces mentioned in top sections

### 5. Response Synthesis ([src/graphrag/nodes/synthesize_node.py](src/graphrag/nodes/synthesize_node.py))

**Purpose**: Generate natural language response with citations

**Inputs**:
- User question
- Vector search results (document excerpts)
- Graph query results (structured data)
- Query path metadata

**LLM**: GPT-4o (temperature=0.3 for consistency)

**Output Format**:
- Natural language answer
- Citations (section IDs, requirement IDs)
- Confidence indicators

---

## Development Workflows

### Adding New Features

#### Add New Query Template

1. **Add template** to [src/query/cypher_templates.py](src/query/cypher_templates.py):
```python
TEMPLATES["my_new_query"] = """
MATCH (c:Component {id: $component_id})
RETURN c.name, c.type
"""
```

2. **Update router** in [src/query/router.py](src/query/router.py) to detect when to use it

3. **Add test** in [tests/test_cypher_node.py](tests/test_cypher_node.py)

#### Add New Entity Type

1. **Update Entity Dictionary** [data/entities/mosar_entities.json](data/entities/mosar_entities.json):
```json
{
  "new_entity_type": {
    "entity_name": {"id": "ENTITY_ID", "type": "NewType"}
  }
}
```

2. **Update NER prompts** in [src/graphrag/nodes/ner_node.py](src/graphrag/nodes/ner_node.py) to extract new type

3. **Update Cypher templates** to query new entity type

4. **Add unit tests**

### Running Tests

```bash
# All tests
pytest

# Specific test categories
pytest -m unit                      # Unit tests only
pytest -m e2e                       # End-to-end tests only
pytest -m "not requires_openai"    # Skip tests needing OpenAI API

# Single test file
pytest tests/test_vector_search_node.py

# Single test function
pytest tests/test_e2e.py::test_question_1

# With coverage
pytest --cov=src --cov-report=html
# View: htmlcov/index.html

# Verbose output
pytest -v

# Show print statements
pytest -s
```

### Debugging with HITL (Human-in-the-Loop)

The system includes an interactive review system ([src/graphrag/hitl.py](src/graphrag/hitl.py)):

```python
from src.graphrag.hitl import HITLReviewer

reviewer = HITLReviewer()

# Review entity extraction
entities = {"Component": ["R-ICU", "WM"], "Requirement": ["FuncR_S110"]}
approved_entities = reviewer.review_entities(entities, user_question="...")

# Review generated Cypher
cypher_query = "MATCH (c:Component {id: 'R-ICU'}) RETURN c"
approved_query = reviewer.review_cypher(cypher_query, entities)

# Review final answer
final_answer = "R-ICU handles network communication via CAN bus..."
approved_answer = reviewer.review_answer(final_answer, user_question)
```

**Use cases**:
- Debugging incorrect entity extraction
- Validating Cypher query generation
- Quality assurance for LLM responses

---

## Working with Neo4j

### Accessing Neo4j Browser

1. Open http://localhost:7474 in browser
2. Connect using credentials from `.env`:
   - Bolt URL: `bolt://localhost:7687`
   - Username: `neo4j`
   - Password: (from `NEO4J_PASSWORD` in `.env`)

### Useful Cypher Queries

```cypher
// Check database status
CALL dbms.components() YIELD name, versions, edition;

// Count nodes by label
MATCH (n) RETURN labels(n), count(n) ORDER BY count(n) DESC;

// Check vector indexes
SHOW INDEXES YIELD name, type WHERE type = 'VECTOR';

// View sample requirement with traceability
MATCH path = (req:Requirement {id: 'FuncR_S110'})-[*1..3]-(related)
RETURN path LIMIT 50;

// Find unverified requirements
MATCH (req:Requirement)
WHERE NOT EXISTS { (req)<-[:VERIFIES]-(:TestCase) }
RETURN req.id, req.type, req.statement
LIMIT 10;

// Check embeddings
MATCH (s:Section)
WHERE s.content_embedding IS NOT NULL
RETURN count(s) as sections_with_embeddings;

// Test vector search
CALL db.index.vector.queryNodes(
  'section_embeddings',
  5,
  [/* paste 3072-dim embedding here */]
) YIELD node, score
RETURN node.id, node.title, score;
```

### Resetting the Database

```cypher
// WARNING: Deletes all data
MATCH (n) DETACH DELETE n;

// Then reload data
# python scripts/load_documents.py
```

---

## Configuration

### Environment Variables (.env)

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j

# OpenAI API
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...  # Optional

# Embeddings Configuration
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSION=3072

# Query Configuration
VECTOR_SEARCH_TOP_K=10
VECTOR_SIMILARITY_THRESHOLD=0.75
CYPHER_TIMEOUT_MS=5000

# LLM Configuration
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2000

# LangSmith Tracing (Optional - for debugging)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=mosar-graphrag

# Application Settings
LOG_LEVEL=INFO
CACHE_ENABLED=true
HITL_ENABLED=false  # Human-in-the-loop review
```

### Dependencies (pyproject.toml)

**Core**:
- `langgraph ^0.2.16` - Workflow orchestration
- `neo4j ^5.14.0` - Graph database driver
- `openai ^1.50.0` - LLM and embeddings
- `langchain ^0.3.0`, `langchain-openai ^0.2.0`, `langchain-core ^0.3.0`

**NLP**:
- `spacy ^3.7.0`, `spacy-transformers ^1.3.0` - NER
- `sentence-transformers ^2.3.0` - Alternative embeddings

**Utilities**:
- `pydantic ^2.5.0` - Data validation
- `python-dotenv ^1.0.0` - Environment management
- `rich ^13.7.0` - CLI formatting
- `fuzzywuzzy ^0.18.0` - Fuzzy entity matching

**Dev/Testing**:
- `pytest ^8.0.0`, `pytest-cov ^4.1.0`, `pytest-asyncio ^0.23.0`
- `ruff ^0.1.0` - Linting
- `jupyter ^1.0.0` - Notebooks
- `langsmith ^0.1.0` - Trace debugging

---

## MOSAR Domain Knowledge

### Key MOSAR Components

**R-ICU** (Reduced Instrument Control Unit)
- Hardware: Zynq UltraScale+ MPSoC
- Mass: 0.65 kg
- Power: 10W avg, 15W peak
- Purpose: Central control unit for modules

**WM** (Walking Manipulator)
- Purpose: Mobility on spacecraft surface
- Interfaces: CAN bus, Ethernet

**SM** (Service Module)
- Variants: SM1-DMS, SM2-PWS, SM3-BAT, SM4-THS
- Contains: R-ICU, cPDU, HOTDOCK

**OBC** (On-Board Computer)
- Processor: R5 (real-time) + A53 (application)
- OS: FreeRTOS (R5), Linux (A53)

**cPDU** (Power Distribution Unit)
- Purpose: Power management and distribution

**HOTDOCK** (Hot-Docking Interface)
- Purpose: Hot-swappable module connections

### Network Protocols

**CAN Bus**
- Speed: 1 Mbps
- Purpose: Real-time communication
- Use: Safety-critical data

**Ethernet**
- Speed: 100 Mbps
- Purpose: High-bandwidth data transfer
- Use: Science payloads, telemetry

**SpaceWire**
- Purpose: Backup protocol for critical data

### Requirements Categories

- **FuncR**: Functional Requirements (110 total)
- **SafR**: Safety Requirements (45 total)
- **PerfR**: Performance Requirements (38 total)
- **IntR**: Interface Requirements (34 total)
- **DesR**: Design Requirements

### Verification Methods

- **Testing**: Physical or simulation tests
- **Analysis**: Mathematical/computational verification
- **Review of Design**: Design review and inspection

---

## Troubleshooting

### Common Issues

#### "Neo4j connection failed"
**Cause**: Neo4j not running or wrong credentials
**Fix**:
```bash
# Check if Neo4j is running
docker ps | grep neo4j  # If using Docker
# OR check Neo4j Desktop

# Verify credentials in .env match Neo4j
# Test connection:
python scripts/check_neo4j_status.py
```

#### "OpenAI API error: Rate limit exceeded"
**Cause**: Too many API calls
**Fix**:
- Wait 1 minute (rate limit resets)
- Upgrade OpenAI plan for higher limits
- Use caching to reduce calls (already implemented)

#### "No vector index found"
**Cause**: Database schema not initialized
**Fix**:
```bash
python src/neo4j_schema/create_schema.py
# Verify:
python scripts/check_neo4j_status.py
```

#### "ModuleNotFoundError: No module named 'src'"
**Cause**: Python path not set correctly
**Fix**:
```bash
# Run from repository root
cd /path/to/ReqEng

# OR set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### "spaCy model not found"
**Cause**: spaCy transformer model not downloaded
**Fix**:
```bash
python -m spacy download en_core_web_trf
```

#### Tests fail with "requires_neo4j" or "requires_openai"
**Cause**: Missing dependencies for integration tests
**Fix**:
```bash
# Skip these tests if dependencies unavailable
pytest -m "not requires_neo4j and not requires_openai"

# OR set up required services
```

### Performance Issues

#### "Queries are slow (>5 seconds)"
**Diagnose**:
1. Check Neo4j indexes: `SHOW INDEXES;`
2. Profile Cypher query: `PROFILE [your query]`
3. Check OpenAI API latency
4. Enable caching in `.env`: `CACHE_ENABLED=true`

**Optimize**:
- Reduce `VECTOR_SEARCH_TOP_K` (default: 10 → try 5)
- Increase `VECTOR_SIMILARITY_THRESHOLD` (default: 0.75 → try 0.80)
- Use Path A (Pure Cypher) when possible

#### "Out of memory errors"
**Cause**: Large document loading or vector operations
**Fix**:
- Process documents in batches (see [src/ingestion/neo4j_loader.py](src/ingestion/neo4j_loader.py))
- Increase Docker memory limit (if using Docker)
- Use text chunking for large sections

---

## Testing Strategy

### Test Categories

**Unit Tests** ([tests/test_*_node.py](tests/))
- Test individual nodes in isolation
- Mock external dependencies (Neo4j, OpenAI)
- Fast execution (<1s per test)
- Run frequently during development

**Integration Tests** (marked with `@pytest.mark.integration`)
- Test interactions between components
- Use real Neo4j database (test data)
- Slower execution (2-5s per test)

**End-to-End Tests** ([tests/test_e2e.py](tests/test_e2e.py))
- Test complete workflows with production data
- Require Neo4j + OpenAI API
- Slow execution (5-20s per test)
- 5 key questions covering all paths

**Performance Tests** ([notebooks/benchmark.ipynb](notebooks/benchmark.ipynb))
- Measure response times
- Validate against targets (<500ms, <2000ms)
- Generate visualizations

### Success Criteria

✅ **Query Response Time**
- Pure Cypher: <500ms average
- Hybrid: <2000ms average
- Pure Vector: <2000ms average

✅ **Accuracy**
- Entity detection: >90% precision
- E2E test pass rate: 100% (5/5 questions)

✅ **Test Coverage**
- Line coverage: >80%
- Branch coverage: >70%

✅ **Data Completeness**
- Requirements loaded: 227/227 (100%)
- Embeddings generated: 500+ sections
- Test cases linked: 50+ verified

---

## Architecture Diagrams

### Data Flow: Query Execution

```
User Question
     ↓
[Router: Entity Detection & Path Selection]
     ↓
┌────┴────┬─────────┬────────┐
│  Path A │ Path B  │ Path C │
│         │         │        │
│ Template│ Vector  │ Vector │
│ Cypher  │ Search  │ Search │
│    ↓    │    ↓    │    ↓   │
│ Execute │  NER    │  LLM   │
│    ↓    │  Extr.  │ Synth. │
│ Format  │    ↓    │    ↓   │
│         │Context. │        │
│         │ Cypher  │        │
│         │    ↓    │        │
│         │  LLM    │        │
│         │ Synth.  │        │
└────┬────┴─────────┴────────┘
     ↓
Final Answer + Citations
```

### Data Flow: Document Ingestion

```
Source Documents
(SRD, PDD, DDD, Demo)
     ↓
[Document Parsers]
(srd_parser.py, design_doc_parser.py, demo_procedure_parser.py)
     ↓
Structured Data
(Requirements, Sections, TestCases)
     ↓
[Embedder]
(OpenAI text-embedding-3-large)
     ↓
Data + Embeddings (3072-dim vectors)
     ↓
[Neo4j Loader]
(Bulk UNWIND operations)
     ↓
Neo4j Graph Database
(4-Layer Model)
```

---

## References

### Internal Documentation
- [PRD.md](PRD.md) - Product Requirements Document (complete implementation plan)
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide for development
- [PHASE*_COMPLETE.md](.) - Phase completion reports with metrics

### External Resources
- **GraphRAG Concepts**: https://graphrag.com/concepts/intro-to-graphrag/
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Neo4j Vector Search**: https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/
- **V-Model Traceability**: ISO/IEC/IEEE 15288:2015 Systems Engineering

### Technology Documentation
- LangGraph: Stateful workflow orchestration
- Neo4j: Graph database + HNSW vector indexes
- OpenAI Embeddings: text-embedding-3-large (3072 dimensions)
- spaCy: Named Entity Recognition

---

## Project History

**Phase 0** (Days 1-2): Environment setup, Neo4j schema, Entity Dictionary
**Phase 1** (Days 3-7): Document parsers, data ingestion, embeddings generation
**Phase 2** (Days 8-10): Basic query templates, Neo4j integration
**Phase 3** (Days 11-14): LangGraph workflow, hybrid query pipeline, CLI
**Phase 4** (Days 15-20): Testing (50+ unit tests, 5 E2E tests), benchmarking, HITL system

**Status**: ✅ All phases complete, production-ready

---

**Last Updated**: 2025-10-27
**Version**: 1.0 (Production)
**Maintainer**: MOSAR GraphRAG Team
