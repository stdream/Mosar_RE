# MOSAR GraphRAG System - Architecture Documentation

**Version**: 1.0
**Date**: 2025-10-27
**Project**: MOSAR Requirements Engineering GraphRAG System
**Status**: Production Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [4-Layer Graph Model](#4-layer-graph-model)
3. [Query Architecture](#query-architecture)
4. [Technology Stack](#technology-stack)
5. [Component Architecture](#component-architecture)
6. [Data Flow](#data-flow)
7. [Deployment Architecture](#deployment-architecture)
8. [Performance Considerations](#performance-considerations)

---

## System Overview

### Vision

MOSAR GraphRAG is an AI-powered knowledge management system that enables intelligent querying of spacecraft system documentation through a hybrid approach combining:
- **Graph Database** (Neo4j) for structured relationships
- **Vector Search** for semantic similarity
- **LLM** (GPT-4) for natural language understanding and synthesis

### Core Capabilities

1. **Requirements Traceability**: Track requirements → design → implementation → testing
2. **Impact Analysis**: Understand ripple effects of design changes
3. **Intelligent Search**: Natural language queries with 90%+ accuracy
4. **Design Verification**: Validate PDD→DDD evolution against requirements

### Key Metrics

- **227 system requirements** with complete V-Model traceability
- **500+ document sections** with semantic embeddings
- **~3,000 nodes** and **~4,300 relationships** in graph
- **<2 second** average response time
- **>90%** accuracy on known entities

---

## 4-Layer Graph Model

The system uses a sophisticated 4-layer graph architecture where each layer serves a distinct purpose while maintaining cross-layer relationships.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 4: V-Model                          │
│  Requirements ──► Design Concept ──► Detailed Design ──► Test│
│  ┌──────────┐     ┌────────────┐    ┌──────────┐  ┌───────┐│
│  │FuncR_S110│────►│NET-ARCH-PDD│───►│NET-ARCH-DD││  │ TC-A-1││
│  └──────────┘     └────────────┘    └──────────┘  └───────┘│
│      ▲                                                        │
│      │ RELATES_TO                                            │
├──────┼───────────────────────────────────────────────────────┤
│      │              Layer 3: Domain System                    │
│      │  ┌───────────┐    ┌───────────┐    ┌─────────┐      │
│      └─►│ Component │◄──►│ Interface │◄──►│Protocol │      │
│         │  (R-ICU)  │    │ (CAN-BUS) │    │  (CAN)  │      │
│         └───────────┘    └───────────┘    └─────────┘      │
│              ▲                                                │
│              │ MENTIONS                                       │
├──────────────┼───────────────────────────────────────────────┤
│              │          Layer 1: Document Structure           │
│              │  ┌────────┐    ┌─────────┐   ┌──────────┐    │
│              └──│Document│───►│ Section │──►│TextChunk │    │
│                 │ (DDD)  │    │  (3.2)  │   │(embedded)│    │
│                 └────────┘    └─────────┘   └──────────┘    │
│                                      ▲                         │
│                                      │ EXTRACTED_FROM         │
├──────────────────────────────────────┼───────────────────────┤
│                    Layer 2: Entities                          │
│                      ┌─────────┐                              │
│                      │Protocol │ Technology  Organization    │
│                      │ Concept │ Person      etc.            │
│                      └─────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Document Structure (Lexical)

**Purpose**: Preserve original document hierarchy for navigation and context

**Nodes**:
- `Document`: Top-level document (SRD, PDD, DDD, Demo)
- `Section`: Major sections with embeddings
- `Subsection`: Hierarchical subsections
- `TextChunk`: Chunked text for fine-grained vector search

**Relationships**:
- `HAS_SECTION`: Document → Section
- `HAS_SUBSECTION`: Section → Subsection
- `CONTAINS_CHUNK`: Section → TextChunk
- `NEXT_SECTION`: Sequential navigation
- `PARENT_SECTION`: Hierarchical navigation

**Properties**:
```cypher
(:Section {
  id: "DDD-3.2",
  title: "Network Architecture",
  content: "...",
  content_embedding: [3072 floats],
  doc_id: "DDD",
  number: "3.2",
  level: 1
})
```

**Use Cases**:
- Browse document hierarchy
- Find related sections
- Chunk-based semantic search

---

### Layer 2: Selective Entity Extraction

**Purpose**: Domain-specific entities for entity-based navigation

**Nodes**:
- `Protocol`: Communication protocols (CAN, Ethernet, SpaceWire)
- `Technology`: Technologies used (Zynq, FreeRTOS)
- `Organization`: Responsible parties (SPACEAPPS, TAS-UK, GMV)
- `Person`: Key personnel
- `Concept`: Abstract concepts (modularity, fault-tolerance)

**Relationships**:
- `MENTIONED_IN`: Entity → Section
- `RELATED_TO`: Entity ← → Entity

**Properties**:
```cypher
(:Protocol {
  name: "CAN",
  category: "bus",
  data_rate_mbps: 1.0
})
```

**Use Cases**:
- Find all mentions of a technology
- Track organizations responsible for features
- Cross-reference related concepts

---

### Layer 3: Domain System Graph (MOSAR Architecture)

**Purpose**: Model the actual MOSAR spacecraft system architecture

**Nodes**:
- `Component`: Hardware/software components (R-ICU, WM, OBC, cPDU)
- `SpacecraftModule`: Top-level modules (SM1-DMS, SM2-PWS, etc.)
- `Interface`: Communication interfaces (CAN-BUS-1, ETH-1)
- `SoftwareTask`: Running tasks (NetworkManager, TelemetryHandler)
- `Scenario`: Operational scenarios (S1, S2, S3)
- `Protocol`: Communication protocols

**Relationships**:
- `HAS_INTERFACE`: Component → Interface
- `RUNS_ON`: SoftwareTask → Component
- `COMMUNICATES_VIA`: Component → Protocol
- `PART_OF`: Component → SpacecraftModule
- `EXECUTES`: Scenario → Component
- `INTERACTS_WITH`: Component ← → Component

**Properties**:
```cypher
(:Component {
  id: "R-ICU",
  name: "Reduced Instrument Control Unit",
  hardware_platform: "Zynq UltraScale+ MPSoC",
  mass_kg: 0.65,
  power_avg_w: 10.0,
  power_peak_w: 15.0
})

(:Interface {
  id: "CAN-BUS-1",
  protocol: "CAN",
  data_rate_mbps: 1.0,
  redundant: true
})
```

**Use Cases**:
- System architecture queries
- Dependency analysis
- Communication path tracing
- Scenario modeling

---

### Layer 4: Requirements Traceability (V-Model)

**Purpose**: Complete requirements lifecycle tracking

**Nodes**:
- `Requirement`: System requirements (FuncR, SafR, PerfR, IntR, DesR)
- `DesignConcept`: Preliminary design decisions (from PDD)
- `DetailedDesign`: Detailed design specifications (from DDD)
- `TestCase`: Verification tests (CT-A-1, IT1, S1, S2, S3)
- `VerificationMethod`: Testing/Analysis/Review of Design

**Relationships**:
- `PRELIMINARY_DESIGN`: Requirement → DesignConcept
- `REFINED_TO`: DesignConcept → DetailedDesign
- `IMPLEMENTED_BY`: DetailedDesign → Component
- `VERIFIES`: TestCase → Requirement
- `DEPENDS_ON`: Requirement → Requirement
- `DERIVES_FROM`: Requirement → Requirement (parent-child)
- `COVERS`: Requirement → Requirement (coverage)

**Properties**:
```cypher
(:Requirement {
  id: "FuncR_S110",
  type: "FuncR",
  subsystem: "S",
  title: "Network Redundancy",
  statement: "The system shall provide redundant communication paths...",
  level: "Mandatory",
  verification: "Testing",
  responsible: "SPACEAPPS, GMV",
  covers: "FuncR_A101, FuncR_A102",
  comment: "Critical for fault tolerance",
  statement_embedding: [3072 floats],
  status: "verified"
})

(:TestCase {
  id: "CT-A-1",
  type: "Component Test",
  description: "Test R-ICU network failover",
  objective: "Verify redundant CAN/Ethernet switching",
  procedure: "1. Disconnect CAN bus...",
  status: "Passed",
  date_executed: "2025-01-15"
})
```

**Use Cases**:
- Full V-Model traceability
- Unverified requirements detection
- Impact analysis (what tests break if requirement changes)
- Coverage analysis

---

### Cross-Layer Relationships

Critical relationships connecting the layers:

```cypher
// Layer 4 ← → Layer 1
(:Requirement)-[:DEFINED_IN]->(:Section)
(:Section)-[:MENTIONS]->(:Requirement)

// Layer 4 ← → Layer 3
(:Requirement)-[:RELATES_TO]->(:Component)
(:TestCase)-[:TESTS]->(:Component)

// Layer 3 ← → Layer 1
(:Section)-[:MENTIONS]->(:Component)
(:Component)-[:DESCRIBED_IN]->(:Section)

// Layer 1 → Layer 1 (Design Evolution)
(:Section {doc_id: "PDD"})-[:EVOLVED_TO {
  changes: "Added Ethernet interface",
  completeness: 95
}]->(:Section {doc_id: "DDD"})
```

---

## Query Architecture

### 3-Tier Adaptive Routing Strategy

The system automatically selects the optimal query path based on entity detection confidence:

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Entity Dictionary Lookup       │
│  (Fast string matching)         │
└────────┬────────────────────────┘
         │
    ┌────┴────┬─────────────┬────────────┐
    │         │             │            │
High Conf.  Medium Conf.  Low Conf.   No Match
    │         │             │            │
    ▼         ▼             ▼            ▼
┌────────┐ ┌────────┐   ┌────────┐  ┌────────┐
│Path A  │ │Path B  │   │Path B  │  │Path C  │
│Pure    │ │Hybrid  │   │Hybrid  │  │Pure    │
│Cypher  │ │        │   │        │  │Vector  │
└────────┘ └────────┘   └────────┘  └────────┘
   <500ms    <2000ms      <2000ms     <2000ms
```

### Path A: Pure Cypher (Template-Based)

**When**: Question contains explicit entity IDs or exact terminology
**Example**: "FuncR_S110을 구현한 컴포넌트는?", "What requirements use CAN protocol?"

**Workflow**:
1. Entity Dictionary lookup → High confidence match
2. Select template via **ENTITY_TYPE_CONFIG** (configuration-driven)
3. Execute parameterized Cypher query
4. Format results (no LLM synthesis needed)
5. **Graceful fallback**: If template not found, automatically switches to Hybrid path

**Supported Entity Types** (2025-10-30 Update):
- ✅ **Requirement** (FuncR_*, SafR_*, PerfR_*, IntR_*)
- ✅ **Component** (R-ICU, WM, OBC-S, etc.)
- ✅ **TestCase** (CT-A-1, CT-B-2, etc.)
- ✅ **Protocol** (CAN, Ethernet, SpaceWire, RMAP)
- ✅ **SpacecraftModule** (SM, SM1-DMS, SM2-PWS, etc.)
- ✅ **Scenario** (S1, S2, S3)
- ✅ **Organization** (SPACEAPPS, TAS-UK, GMV, DLR)

**Advantages**:
- **Fastest**: <500ms (no embedding, no LLM)
- **Deterministic**: 100% accuracy for known entities
- **Cost-effective**: No OpenAI API calls
- **Extensible**: Easy to add new entity types via config

**Example**:
```python
# Router detects "FuncR_S110" with 100% confidence
template = templates["requirement_traceability"]
query = template.format(req_id="FuncR_S110")

# Execute Cypher
results = neo4j.execute(query)

# Simple formatting (no LLM)
answer = format_traceability_results(results)
```

---

### Path B: Hybrid (Vector → NER → Cypher → LLM)

**When**: Question uses natural language or domain terminology
**Example**: "네트워크 통신을 담당하는 하드웨어는?"

**5-Step Workflow**:

#### Step 1: Vector Search
```python
# Generate query embedding
query_embedding = openai.embeddings.create(
    model="text-embedding-3-large",
    input=user_question
)

# Neo4j vector search
cypher = """
CALL db.index.vector.queryNodes('section_embeddings', 10, $embedding)
YIELD node, score
WHERE score > 0.75
RETURN node, score
ORDER BY score DESC
"""
top_k_sections = execute(cypher, embedding=query_embedding)
```

#### Step 2: Entity Extraction (NER)
```python
# Extract entities from retrieved context
context = "\n".join([sec["content"] for sec in top_k_sections[:5]])

# GPT-4 entity extraction
prompt = f"""Extract MOSAR entities from this text:
- Components (e.g., R-ICU, WM, SM)
- Requirements (e.g., FuncR_S110)
- Interfaces (e.g., CAN-BUS-1)

Text: {context}

Return JSON: {{"Component": [...], "Requirement": [...]}}
"""
extracted_entities = gpt4(prompt)
```

#### Step 3: Contextual Cypher
```python
# Build Cypher query using extracted entities
cypher = f"""
MATCH (c:Component)
WHERE c.id IN $component_ids
MATCH (c)-[:HAS_INTERFACE]->(i:Interface)
WHERE i.protocol IN ['Ethernet', 'CAN']
RETURN c.id, c.name, i.protocol, i.data_rate_mbps
"""
graph_results = execute(cypher, component_ids=extracted_entities["Component"])
```

#### Step 4: LLM Synthesis
```python
# Combine vector + graph results
prompt = f"""Question: {user_question}

Retrieved Text:
{top_k_sections}

Graph Query Results:
{graph_results}

Provide a comprehensive answer with citations."""

final_answer = gpt4(prompt)
```

**Advantages**:
- **Flexible**: Handles natural language
- **Comprehensive**: Combines semantic + structural information
- **Accurate**: Validated entities via Entity Dictionary

**Performance**: <2000ms

---

### Path C: Pure Vector Search

**When**: Exploratory questions without clear entities
**Example**: "우주 환경에서의 열 관리 방법은?"

**Workflow**:
1. Vector search only (no entity extraction)
2. LLM synthesis from top-k sections
3. No Cypher queries

**Advantages**:
- **Simple**: Straightforward pipeline
- **Exploratory**: Good for broad questions

**Performance**: <2000ms

---

## Technology Stack

### Core Technologies

#### 1. LangGraph (v0.2.16+)
**Role**: Workflow orchestration

**Features Used**:
- StateGraph for stateful workflows
- Conditional routing
- Checkpointing for conversation history
- Error recovery

**Architecture**:
```python
workflow = StateGraph(GraphRAGState)

# Add nodes
workflow.add_node("classify_query", classify_query)
workflow.add_node("run_vector_search", run_vector_search)
workflow.add_node("extract_entities", extract_entities)
workflow.add_node("run_cypher", run_cypher)
workflow.add_node("synthesize_response", synthesize_response)

# Conditional routing
workflow.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "pure_cypher": "run_cypher",
        "hybrid": "run_vector_search",
        "pure_vector": "run_vector_search"
    }
)

app = workflow.compile(checkpointer=MemorySaver())
```

#### 2. Neo4j (v5.14+)
**Role**: Graph database + vector index

**Indexes**:
- **Vector Index**: HNSW algorithm, 3072 dimensions, cosine similarity
- **Full-text Index**: Requirements, Components, Sections
- **Composite Index**: (level, subsystem), (type, name)

**Configuration**:
```cypher
CREATE VECTOR INDEX section_embeddings
FOR (s:Section) ON (s.content_embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
}
```

#### 3. OpenAI API
**Role**: Embeddings + LLM

**Models**:
- **Embeddings**: `text-embedding-3-large` (3072d)
- **LLM**: `gpt-4o` (temperature=0.3)

**Usage**:
- ~500 embedding calls (one-time, during data loading)
- ~2-3 LLM calls per hybrid query
- Cost: ~$0.01 per hybrid query

#### 4. spaCy (v3.7+)
**Role**: Named Entity Recognition (backup for GPT-4)

**Model**: `en_core_web_sm` with transformers

**Use Case**: Offline NER when OpenAI API unavailable

---

### Supporting Libraries

- **python-dotenv**: Environment configuration
- **pydantic**: Data validation
- **tiktoken**: Token counting
- **markdown**: Document parsing
- **beautifulsoup4**: HTML cleaning
- **rich**: CLI formatting
- **pytest**: Testing framework

---

## Component Architecture

### High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI / API Layer                       │
│  ┌──────────┐    ┌──────────┐    ┌────────────┐           │
│  │ CLI App  │    │ REST API │    │  Web UI    │           │
│  └────┬─────┘    └────┬─────┘    └─────┬──────┘           │
└───────┼───────────────┼──────────────────┼─────────────────┘
        │               │                  │
        └───────────────┼──────────────────┘
                        │
┌───────────────────────┼─────────────────────────────────────┐
│                   LangGraph Workflow                         │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐             │
│  │   Router   │─►│ Vector     │─►│  NER     │             │
│  │ (classify) │  │ Search     │  │ Extract  │             │
│  └────────────┘  └────────────┘  └──────────┘             │
│         │              │                │                    │
│         ▼              ▼                ▼                    │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐             │
│  │Template    │  │Contextual  │  │Response  │             │
│  │Cypher      │  │Cypher      │  │Synthesis │             │
│  └────────────┘  └────────────┘  └──────────┘             │
└──────────┬───────────────┬─────────────┬──────────────────┘
           │               │             │
┌──────────┼───────────────┼─────────────┼──────────────────┐
│          │          Cache Layer        │                   │
│  ┌───────▼────┐  ┌─────▼──────┐  ┌───▼──────┐           │
│  │Vector Cache│  │Cypher Cache│  │Answer    │           │
│  │(LRU+TTL)   │  │(LRU+TTL)   │  │Cache     │           │
│  └────────────┘  └────────────┘  └──────────┘           │
└──────────┬───────────────┬─────────────┬──────────────────┘
           │               │             │
┌──────────┼───────────────┼─────────────┼──────────────────┐
│     Data Access Layer                  │                   │
│  ┌────────▼──────┐  ┌─────▼──────┐  ┌─▼──────────┐       │
│  │ Neo4j Client  │  │  OpenAI    │  │  Entity    │       │
│  │  (pooling)    │  │  Client    │  │  Resolver  │       │
│  └───────────────┘  └────────────┘  └────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Module Breakdown

#### 1. Ingestion Pipeline
```
Documents (MD) → Parsers → Embedder → Neo4j Loader → Graph DB
```

**Components**:
- `srd_parser.py`: Requirements table extraction
- `design_doc_parser.py`: PDD/DDD section extraction
- `demo_procedure_parser.py`: Test case extraction
- `embedder.py`: OpenAI embedding generation
- `neo4j_loader.py`: Bulk loading to Neo4j

#### 2. Query Pipeline
```
User Question → Router → [Path A/B/C] → Synthesis → Answer
```

**Components**:
- `router.py`: Entity Dictionary lookup + routing decision
- `vector_search_node.py`: Neo4j vector search
- `ner_node.py`: GPT-4 entity extraction
- `cypher_node.py`: Template/contextual Cypher execution
- `synthesize_node.py`: LLM-based response generation

#### 3. Utilities
- `neo4j_client.py`: Connection pooling, error handling
- `entity_resolver.py`: Entity Dictionary + fuzzy matching
- `cache.py`: Multi-tier LRU cache with TTL
- `hitl.py`: Human-in-the-loop review system

---

## Data Flow

### 1. Data Loading Flow

```
┌─────────────┐
│   SRD.md    │──┐
└─────────────┘  │
┌─────────────┐  │  Parse
│   PDD.md    │──┼─────────►┌─────────────┐
└─────────────┘  │          │  Parsers    │
┌─────────────┐  │          └──────┬──────┘
│   DDD.md    │──┤                 │
└─────────────┘  │                 ▼
┌─────────────┐  │          ┌─────────────┐
│   Demo.md   │──┘          │ Structured  │
└─────────────┘             │   Data      │
                            └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │  OpenAI     │
                            │ Embeddings  │
                            └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │  Neo4j      │
                            │  Loader     │
                            └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   Neo4j     │
                            │  Graph DB   │
                            └─────────────┘
```

### 2. Query Execution Flow (Hybrid Path Example)

```
User: "네트워크 통신 하드웨어는?"
         │
         ▼
   ┌────────────┐
   │   Router   │ Entity lookup → Low confidence
   └─────┬──────┘
         │
    [Hybrid Path]
         │
         ▼
   ┌────────────┐
   │  Vector    │ Embedding + Neo4j vector search
   │  Search    │ → Top-5 sections about networking
   └─────┬──────┘
         │
         ▼
   ┌────────────┐
   │    NER     │ GPT-4 extracts: {Component: [R-ICU], Protocol: [CAN, Ethernet]}
   └─────┬──────┘
         │
         ▼
   ┌────────────┐
   │ Contextual │ Build Cypher with entities
   │  Cypher    │ → Query graph for R-ICU + protocols
   └─────┬──────┘
         │
         ▼
   ┌────────────┐
   │    LLM     │ Synthesize: vector context + graph results
   │ Synthesis  │ → "R-ICU handles network communication..."
   └─────┬──────┘
         │
         ▼
   Final Answer + Citations
```

---

## Deployment Architecture

### Development Environment

```
Developer Machine
├── Python 3.11+ (Poetry)
├── Neo4j Desktop (localhost:7687)
└── .env (OPENAI_API_KEY)
```

### Production Environment (Recommended)

```
┌────────────────────────────────────────────────────┐
│                  Load Balancer                      │
└───────────────────┬────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼─────┐         ┌──────▼──────┐
│   FastAPI   │         │   FastAPI   │
│  Instance 1 │         │  Instance 2 │
└───────┬─────┘         └──────┬──────┘
        │                      │
        └──────────┬───────────┘
                   │
        ┌──────────▼───────────┐
        │     Redis Cache      │
        │   (Shared Session)   │
        └──────────┬───────────┘
                   │
        ┌──────────┴───────────┐
        │                      │
┌───────▼─────┐      ┌────────▼─────┐
│   Neo4j     │      │   OpenAI     │
│   Cluster   │      │     API      │
│ (3 nodes)   │      └──────────────┘
└─────────────┘
```

### Docker Compose (Quick Start)

```yaml
version: '3.8'
services:
  neo4j:
    image: neo4j:5.14
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
    volumes:
      - neo4j_data:/data

  graphrag:
    build: .
    ports:
      - "8000:8000"
    environment:
      NEO4J_URI: bolt://neo4j:7687
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      - neo4j

volumes:
  neo4j_data:
```

---

## Performance Considerations

### Response Time Targets

| Query Type | Target | Typical | Bottleneck |
|------------|--------|---------|------------|
| Pure Cypher | <500ms | 200-400ms | Neo4j query execution |
| Hybrid | <2000ms | 1200-1800ms | OpenAI API latency |
| Pure Vector | <2000ms | 1000-1500ms | Embedding generation |

### Optimization Strategies

#### 1. Caching
- **Vector Cache**: Cache embeddings by question text (LRU, 100 entries, 1h TTL)
- **Cypher Cache**: Cache query results by query+params (LRU, 100 entries, 1h TTL)
- **Answer Cache**: Cache final answers by question+path (LRU, 100 entries, 1h TTL)

**Impact**: 40-60% faster for repeated questions

#### 2. Neo4j Indexing
```cypher
// HNSW index for vector search
CREATE VECTOR INDEX section_embeddings ...

// Composite indexes for filtering
CREATE INDEX requirement_level_subsystem
FOR (r:Requirement) ON (r.level, r.subsystem)

// Full-text index for keyword search
CREATE FULLTEXT INDEX requirement_fulltext ...
```

#### 3. Connection Pooling
- Neo4j: Connection pool (min=5, max=50)
- OpenAI: Connection reuse with keep-alive

#### 4. Batch Processing
- Embeddings: Batch 100 texts per API call
- Neo4j inserts: UNWIND for bulk operations

### Scalability

**Current Capacity**:
- ~800 nodes, ~1200 relationships
- 10-20 concurrent users
- <2s 95th percentile latency

**Scaling to 10,000+ users**:
1. Horizontal scaling (multiple FastAPI instances)
2. Neo4j cluster (3-node setup)
3. Redis cache (shared across instances)
4. CDN for static assets
5. Rate limiting (10 queries/min per user)

---

## Security Considerations

### API Key Management
- Store OpenAI API key in secrets manager (AWS Secrets Manager, Azure Key Vault)
- Rotate keys quarterly
- Monitor usage for anomalies

### Data Access Control
- Neo4j authentication (username/password)
- Role-based access control (RBAC)
- Audit logging for all queries

### Input Validation
- Sanitize user inputs before Cypher queries
- Parameterized queries only (prevent injection)
- Rate limiting on API endpoints

---

## Monitoring & Observability

### Key Metrics

1. **Performance**:
   - Response time (p50, p95, p99)
   - Cache hit rate
   - OpenAI API latency

2. **Accuracy**:
   - Entity detection success rate
   - Query path distribution
   - User satisfaction (thumbs up/down)

3. **System Health**:
   - Neo4j connection pool usage
   - Memory usage
   - Error rate

### Tools

- **LangSmith**: LangGraph trace debugging
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **Sentry**: Error tracking

---

## Conclusion

The MOSAR GraphRAG system combines the strengths of graph databases, vector search, and large language models to create a powerful requirements engineering knowledge management system. The 4-layer graph model provides rich structural knowledge, while the 3-tier query architecture ensures optimal performance across different query types.

**Key Strengths**:
- ✅ Complete V-Model traceability
- ✅ Sub-2-second response times
- ✅ 90%+ accuracy on structured queries
- ✅ Natural language query support
- ✅ Production-ready architecture

---

**Document Version**: 1.0
**Last Updated**: 2025-10-27
**Maintainer**: MOSAR GraphRAG Team
