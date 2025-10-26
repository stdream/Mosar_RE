# MOSAR GraphRAG System

## Project Overview

This repository contains the implementation of a **GraphRAG (Graph-based Retrieval Augmented Generation)** system for the MOSAR (Modular Spacecraft Assembly and Reconfiguration) project. The system ingests technical documentation (requirements, preliminary design, detailed design, and test procedures) into a Neo4j graph database and enables intelligent querying with hybrid vector + Cypher approaches.

**Key Metrics**:
- 227 system requirements tracked with complete V-Model traceability
- 500+ document sections from PDD, DDD, SRD, Demo Procedures
- ~3,000 nodes and ~4,300 relationships expected
- Target response time: <2 seconds
- Target accuracy: >90% for known entities

## Architecture

### 4-Layer Graph Model

The system uses a sophisticated 4-layer graph architecture where each layer serves a distinct purpose:

#### Layer 1: Document Structure Graph (Lexical)
Preserves the original document hierarchy and structure:
- **Nodes**: `Document`, `Section`, `Subsection`, `TextChunk`
- **Relationships**: `HAS_SECTION`, `HAS_SUBSECTION`, `CONTAINS_CHUNK`, `NEXT_SECTION`, `PARENT_SECTION`
- **Purpose**: Maintains document context, enables navigation, supports chunk-based vector search

```cypher
(:Document {id, title, version, type})-[:HAS_SECTION]->
(:Section {id, title, level, content_summary})-[:CONTAINS_CHUNK]->
(:TextChunk {id, text, embedding[3072], start_char, end_char})
```

#### Layer 2: Selective Entity Extraction
Domain-specific entities extracted from documents:
- **Nodes**: `Protocol`, `Technology`, `Organization`, `Person`, `Concept`
- **Relationships**: `MENTIONED_IN`, `RELATED_TO`
- **Purpose**: Entity-based navigation and relationship discovery

```cypher
(:Component {id, name, type})<-[:MENTIONS]-
(:Section)-[:MENTIONS]->
(:Technology {name, category})
```

#### Layer 3: Domain System Graph (MOSAR Architecture)
Models the actual MOSAR spacecraft system:
- **Nodes**: `Component`, `SpacecraftModule`, `Interface`, `SoftwareTask`, `Scenario`, `Protocol`
- **Relationships**: `HAS_INTERFACE`, `RUNS_ON`, `COMMUNICATES_VIA`, `PART_OF`, `EXECUTES`, `INTERACTS_WITH`
- **Purpose**: System architecture queries, dependency analysis, scenario modeling

```cypher
(:SpacecraftModule {id: "SM", name: "Service Module"})-[:CONTAINS]->
(:Component {id: "R-ICU", name: "Reduced Instrument Control Unit",
             hardware_platform: "Zynq UltraScale+ MPSoC", mass_kg: 0.65})-[:HAS_INTERFACE]->
(:Interface {id: "CAN-BUS-1", protocol: "CAN", data_rate_mbps: 1.0})
```

#### Layer 4: Requirements Traceability (V-Model)
Complete requirements lifecycle tracking:
- **Nodes**: `Requirement`, `DesignConcept`, `DetailedDesign`, `TestCase`, `VerificationMethod`
- **Relationships**: `PRELIMINARY_DESIGN`, `REFINED_TO`, `IMPLEMENTED_BY`, `VERIFIES`, `DEPENDS_ON`, `COVERS`
- **Purpose**: Requirements traceability, verification status, impact analysis

```cypher
(:Requirement {id: "FuncR_S110", type: "FuncR", statement: "...", status: "verified"})-[:PRELIMINARY_DESIGN]->
(:DesignConcept {id: "NET-ARCH-PDD", source: "PDD"})-[:REFINED_TO {changes: "...", completeness: 95}]->
(:DetailedDesign {id: "NET-ARCH-DDD", source: "DDD"})-[:IMPLEMENTED_BY]->
(:Component {id: "R-ICU"})<-[:VERIFIES]-
(:TestCase {id: "TC_NET_001", procedure: "Demo Procedure 3.2"})
```

### Cross-Layer Relationships

Critical relationships connecting the layers:
- `DEFINED_IN`: Requirements/Components → Document Sections
- `MENTIONS`: Sections → Components/Requirements
- `EVOLVED_TO`: PDD Sections → DDD Sections (design evolution tracking)

## Technology Stack

### Core Technologies
- **LangGraph (^0.2.0)**: Stateful workflow orchestration with conditional routing
- **Neo4j Python Driver (^5.14.0)**: Graph database interaction
- **OpenAI API (^1.3.0)**: LLM for NER, synthesis, and embeddings
  - Embeddings: `text-embedding-3-large` (3072 dimensions, cosine similarity)
  - LLM: `gpt-4o` for entity extraction and response synthesis
- **spaCy (^3.7.0)**: Named Entity Recognition (with transformers)

### Supporting Libraries
- **python-dotenv**: Environment configuration
- **pydantic**: Data validation
- **tiktoken**: Token counting for context management
- **markdown**: Document parsing
- **beautifulsoup4**: HTML cleaning

## Query Architecture: Hybrid Approach

The system uses a **3-tier adaptive routing strategy** that automatically selects the optimal query path:

### Query Routing Decision Tree

```
User Question
    ↓
[1] Check Entity Dictionary (Fast Lookup)
    ├─ High Confidence Match → Pure Cypher Query (Path A)
    ├─ Moderate Confidence → Hybrid Workflow (Path B)
    └─ No Match → Pure Vector Search (Path C)
```

### Path A: Pure Cypher (Template-Based)
**When**: Question contains explicit entity IDs or exact terminology
**Example**: "Show all requirements verified by R-ICU"

```python
MATCH (c:Component {id: $component_id})<-[:VERIFIES]-(tc:TestCase)-[:VERIFIES]->(req:Requirement)
RETURN req.id, req.statement, tc.id
```

**Advantages**: Fastest (<100ms), 100% accuracy for known entities

### Path B: Hybrid (Vector → NER → Cypher → LLM)
**When**: Question uses natural language or domain terminology
**Example**: "어떤 하드웨어가 네트워크 통신을 담당하나요?" (What hardware handles network communication?)

**5-Step Workflow**:

1. **Vector Search**: Find top-k relevant text chunks
```python
def run_vector_search(state: GraphRAGState) -> GraphRAGState:
    query_embedding = get_embedding(state["user_question"])
    cypher = """
    CALL db.index.vector.queryNodes('chunk_embeddings', $k, $embedding)
    YIELD node, score
    RETURN node.id AS chunk_id, node.text AS text, score
    ORDER BY score DESC LIMIT $k
    """
    return {"top_k_nodes": results}
```

2. **Entity Extraction (NER)**: Extract entities from retrieved context
```python
def extract_entities_from_context(state: GraphRAGState) -> GraphRAGState:
    context = "\n".join([node["text"] for node in state["top_k_nodes"]])
    prompt = f"""Extract MOSAR entities from this text:
    - Components (e.g., R-ICU, WM, SM)
    - Requirements (e.g., FuncR_S110)
    - Interfaces (e.g., CAN-BUS-1)

    Text: {context}

    Return JSON: {{"Component": [...], "Requirement": [...], "Interface": [...]}}
    """
    extracted = call_openai(prompt)
    return {"extracted_entities": extracted}
```

3. **Contextual Cypher**: Build Cypher query using extracted entities
```python
def run_contextual_cypher(state: GraphRAGState) -> GraphRAGState:
    entities = state["extracted_entities"]
    cypher = f"""
    MATCH (section:Section)-[:MENTIONS]->(c:Component)
    WHERE c.id IN $component_ids
    MATCH (c)-[:HAS_INTERFACE]->(i:Interface)
    WHERE i.protocol = 'Ethernet' OR i.protocol = 'CAN'
    RETURN c.id, c.name, i.protocol, i.data_rate_mbps
    """
    return {"graph_results": results}
```

4. **LLM Synthesis**: Generate natural language response
```python
def synthesize_hybrid_response(state: GraphRAGState) -> GraphRAGState:
    prompt = f"""Question: {state['user_question']}

    Retrieved Text:
    {state['top_k_nodes']}

    Graph Query Results:
    {state['graph_results']}

    Provide a comprehensive answer with citations."""
    return {"final_answer": call_openai(prompt)}
```

### Path C: Pure Vector Search
**When**: Exploratory questions without clear entities
**Example**: "What are the main challenges in orbital assembly?"

Uses only semantic similarity on text chunks with LLM synthesis.

## Entity Dictionary: Dual Usage

The `mosar_entities.json` file serves two critical purposes:

### 1. Query-Time Resolution (Real-Time)
Fast entity lookup to route queries correctly:
```json
{
  "components": {
    "Walking Manipulator": {"id": "WM", "type": "Component"},
    "워킹 매니퓰레이터": {"id": "WM", "type": "Component"},
    "R-ICU": {"id": "R-ICU", "type": "Component"}
  },
  "requirements": {
    "안전 요구사항": {"type": "Requirement", "filter": {"type": "SafR"}},
    "기능 요구사항": {"type": "Requirement", "filter": {"type": "FuncR"}}
  }
}
```

### 2. Load-Time Relationship Creation (Ingestion)
During data loading, the Entity Dictionary pre-creates `RELATES_TO` relationships:
```python
def _create_entity_relationships_from_requirements(self):
    """Use Entity Dictionary to create relationships during ingestion."""
    for req_text in requirement_statements:
        # Check if requirement text mentions known components
        for component_name, component_info in entity_dict["components"].items():
            if component_name in req_text:
                cypher = """
                MATCH (req:Requirement {id: $req_id})
                MATCH (c:Component {id: $component_id})
                MERGE (req)-[:RELATES_TO]->(c)
                """
```

**Benefit**: Reduces runtime NER dependency, improves query speed by 40-60%

## Implementation Phases

The project follows a 4-phase implementation plan (see [PRD.md](PRD.md) for full details):

### Phase 0: Environment Setup (Days 1-2)
- Neo4j database setup with constraints and vector indexes
- Python environment with LangGraph, spaCy models
- Entity Dictionary creation

### Phase 1: Data Ingestion (Days 3-7)
- Parse 4 document types: SRD, PDD, DDD, Demo Procedures
- Create Layer 1 (Document Structure) and Layer 2 (Entities)
- Build Layer 3 (Domain System Graph)
- Establish Layer 4 (Requirements Traceability)

**Critical**: Demo Procedures parser extracts test cases with `VERIFIES` relationships

### Phase 2: Basic Query (Days 8-10)
- Implement pure Cypher template queries
- Test basic retrieval and traceability queries

### Phase 3: Hybrid Query Workflow (Days 11-14)
- Implement 5-node LangGraph workflow (Vector → NER → Cypher → Synthesis)
- Add Entity Dictionary query-time resolution
- Build adaptive routing logic

### Phase 4: Advanced Features (Days 15-20)
- HITL (Human-in-the-Loop) for Text2Cypher debugging
- Query performance optimization
- Comprehensive testing and documentation

## Key Files and Directories

### Existing Files (Planning Phase)
- **[PRD.md](PRD.md)**: Complete Product Requirements Document with implementation details
- **[Documents/SRD/System Requirements Document_MOSAR.md](Documents/SRD/System Requirements Document_MOSAR.md)**: 227 requirements in table format
- **[Documents/PDD/MOSAR-WP2-D2.4-SA_1.1.0-Preliminary-Design-Document.md](Documents/PDD/MOSAR-WP2-D2.4-SA_1.1.0-Preliminary-Design-Document.md)**: Preliminary design specifications
- **[Documents/DDD/MOSAR-WP3-D3.6-SA_1.2.0-Detailed-Design-Document.md](Documents/DDD/MOSAR-WP3-D3.6-SA_1.2.0-Detailed-Design-Document.md)**: Detailed design specifications

### Planned Structure (After Implementation)
```
ReqEng/
├── src/
│   ├── ingestion/
│   │   ├── srd_parser.py          # Requirements table parser
│   │   ├── pdd_parser.py          # Preliminary design parser
│   │   ├── ddd_parser.py          # Detailed design parser
│   │   ├── demo_procedure_parser.py  # Test case extraction
│   │   └── neo4j_loader.py        # Graph database loader
│   ├── query/
│   │   ├── langgraph_workflow.py  # Main LangGraph workflow
│   │   ├── cypher_templates.py    # Predefined Cypher queries
│   │   ├── entity_resolver.py     # Entity Dictionary lookup
│   │   └── hybrid_chain.py        # Vector → NER → Cypher chain
│   └── utils/
│       ├── embeddings.py          # OpenAI embedding utilities
│       └── graph_utils.py         # Neo4j connection pool
├── data/
│   └── entities/
│       └── mosar_entities.json    # Entity Dictionary (dual usage)
├── tests/
│   ├── test_ingestion.py
│   └── test_query_workflow.py
├── notebooks/
│   └── explore_graph.ipynb        # Neo4j Browser queries
├── .env                           # API keys, Neo4j credentials
├── pyproject.toml                 # Dependencies
└── README.md                      # Setup instructions
```

## MOSAR Domain Knowledge

### Key Components
- **R-ICU**: Reduced Instrument Control Unit (Zynq UltraScale+ MPSoC, 0.65kg, 10W avg)
- **OBC**: On-Board Computer (R5 processor for real-time tasks)
- **cPDU**: Power Distribution Unit
- **HOTDOCK**: Hot-swappable docking interface
- **WM**: Walking Manipulator (mobility on spacecraft surface)
- **SM**: Service Module (contains R-ICU, cPDU, HOTDOCK)

### Network Architecture
- **CAN Bus**: 1 Mbps, real-time communication (SafR requirements)
- **Ethernet**: 100 Mbps, high-bandwidth data (science payloads)
- **SpaceWire**: Backup protocol for critical data

### Requirements Categories
- **FuncR**: Functional Requirements (110 total)
- **SafR**: Safety Requirements (45 total)
- **PerfR**: Performance Requirements (38 total)
- **IntR**: Interface Requirements (34 total)

### Design Evolution
- **PDD → DDD Tracking**: Each `DesignConcept` node has a `REFINED_TO` relationship showing:
  - What changed from preliminary to detailed design
  - Completeness percentage
  - Open issues for next revision

## Common Query Patterns

### 1. Requirements Traceability
"Show the full traceability chain for requirement FuncR_S110"
```cypher
MATCH path = (req:Requirement {id: 'FuncR_S110'})-[:PRELIMINARY_DESIGN]->
             (pdd:DesignConcept)-[:REFINED_TO]->(ddd:DetailedDesign)-[:IMPLEMENTED_BY]->
             (c:Component)<-[:VERIFIES]-(tc:TestCase)
RETURN path
```

### 2. Unverified Requirements
"Which requirements don't have test cases yet?"
```cypher
MATCH (req:Requirement)
WHERE NOT EXISTS { (req)<-[:VERIFIES]-(:TestCase) }
RETURN req.id, req.type, req.statement
ORDER BY req.type, req.id
```

### 3. Component Dependencies
"What components does R-ICU interact with?"
```cypher
MATCH (c:Component {id: 'R-ICU'})-[:HAS_INTERFACE]->(i:Interface)<-[:HAS_INTERFACE]-(other:Component)
RETURN other.id, other.name, i.protocol, i.data_rate_mbps
```

### 4. Design Evolution
"How did the network architecture evolve from PDD to DDD?"
```cypher
MATCH (pdd:Section {id: 'PDD-3.2'})-[:EVOLVED_TO {category: 'network'}]->(ddd:Section {id: 'DDD-4.1'})
MATCH (pdd)-[:MENTIONS]->(concept:DesignConcept)-[:REFINED_TO]->(detail:DetailedDesign)
RETURN pdd.title, ddd.title, concept.decision, detail.final_choice
```

### 5. Hybrid Natural Language Query
"서비스 모듈에서 실시간 통신을 어떻게 처리하나요?" (How does the Service Module handle real-time communication?)

**Workflow**:
1. Vector search finds relevant sections about SM and real-time communication
2. NER extracts entities: `Component:SM`, `Protocol:CAN`
3. Cypher query:
```cypher
MATCH (sm:SpacecraftModule {id: 'SM'})-[:CONTAINS]->(c:Component)-[:HAS_INTERFACE]->(i:Interface)
WHERE i.protocol = 'CAN'
MATCH (c)-[:RUNS_ON]->(task:SoftwareTask)
WHERE task.realtime = true
RETURN c.name, i.data_rate_mbps, task.name, task.priority
```
4. LLM synthesizes: "The Service Module uses the R-ICU component connected to a 1 Mbps CAN bus for real-time communication. The OBC runs real-time tasks on the R5 processor with priorities managed by FreeRTOS..."

## Development Guidelines

### Adding New Document Types
1. Create parser in `src/ingestion/` following the pattern in `srd_parser.py`
2. Define document-specific node types and relationships
3. Update Entity Dictionary with new domain terms
4. Add vector indexes if full-text search needed

### Extending the Graph Schema
1. Update constraints in Phase 0 setup script
2. Document new node properties in this CLAUDE.md file
3. Create migration script if modifying existing nodes
4. Update Cypher templates if query patterns change

### Testing Queries
1. Use `notebooks/explore_graph.ipynb` for interactive Cypher testing
2. Test all 3 query paths (Cypher, Hybrid, Vector) for each question type
3. Verify Entity Dictionary coverage (aim for >80% of domain terms)
4. Check response time (<2s target) and accuracy (>90% target)

### Performance Optimization
- **Vector Index Tuning**: Adjust `m` and `efConstruction` for HNSW algorithm
- **Cypher Optimization**: Use `EXPLAIN` and `PROFILE` for slow queries
- **Entity Dictionary Expansion**: Add frequently missed terms from NER logs
- **Caching**: Cache frequently accessed subgraphs (e.g., component hierarchy)

## Troubleshooting

### "Entity not found" errors
- Check Entity Dictionary coverage in `mosar_entities.json`
- Review NER extraction quality (use HITL to debug)
- Verify entity IDs match between documents and graph

### Slow query performance
- Check if vector index is being used (`PROFILE` in Neo4j Browser)
- Reduce top-k parameter for vector search (try k=5 instead of k=10)
- Use Entity Dictionary more aggressively to skip vector search

### Incorrect traceability chains
- Verify parsers correctly extract requirement IDs (regex patterns)
- Check `VERIFIES` relationships created by Demo Procedures parser
- Validate PDD→DDD `REFINED_TO` relationships for completeness

## References

- **GraphRAG Concepts**: https://graphrag.com/concepts/intro-to-graphrag/
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Neo4j Vector Search**: https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/
- **V-Model Traceability**: ISO/IEC/IEEE 15288:2015 Systems Engineering

## Future Enhancements

1. **Multi-hop Reasoning**: Implement graph traversal for complex questions requiring 3+ hops
2. **Temporal Queries**: Track design changes over time with version-aware queries
3. **Impact Analysis**: "If we change Component X, what requirements are affected?"
4. **Auto-generated Test Cases**: Suggest test cases for unverified requirements
5. **Cross-project Traceability**: Link MOSAR to related ESA/JAXA missions

---

**Status**: Planning phase complete. Implementation ready to begin with Phase 0.

**Last Updated**: 2025-10-26

**Contact**: See [PRD.md](PRD.md) for detailed implementation schedule and acceptance criteria.
