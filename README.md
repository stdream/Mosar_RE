# MOSAR GraphRAG System

A Graph-based Retrieval Augmented Generation (GraphRAG) system for the MOSAR (Modular Spacecraft Assembly and Reconfiguration) project, enabling intelligent querying of technical documentation with full requirements traceability.

## Project Status

**Current Phase**: Planning Complete ✅
**Next Phase**: Phase 0 - Environment Setup ⏳

## Overview

This system ingests MOSAR technical documentation (Requirements, Preliminary Design, Detailed Design, and Test Procedures) into a Neo4j graph database and provides intelligent question-answering capabilities using hybrid Vector + Cypher queries orchestrated by LangGraph.

### Key Features

- **4-Layer Graph Architecture**
  - Layer 1: Document Structure (preserves document hierarchy)
  - Layer 2: Selective Entities (domain-specific entities)
  - Layer 3: Domain System Graph (MOSAR components, modules, interfaces)
  - Layer 4: Requirements Traceability (V-Model: requirement → design → implementation → verification)

- **Hybrid Query Strategy**
  - Adaptive routing: Entity Dictionary → NER → Vector/Cypher selection
  - Vector search with OpenAI embeddings (text-embedding-3-large, 3072 dimensions)
  - Contextual Cypher queries for structured data retrieval
  - LLM synthesis for natural language responses

- **Full Traceability**
  - 227 system requirements tracked end-to-end
  - Design evolution tracking (PDD → DDD)
  - Test verification status (TestCase → Requirement)
  - Impact analysis and dependency mapping

## Quick Start

**New to this project?** Start here:

1. Read [QUICKSTART.md](QUICKSTART.md) for immediate next steps
2. Review [CLAUDE.md](CLAUDE.md) for architecture details
3. Check [PRD.md](PRD.md) for complete implementation plan

**Resuming development?**

```bash
# Next session command:
# "QUICKSTART.md를 읽고 Phase 0 시작해줘"
```

## Documentation

| Document | Description | Use When |
|----------|-------------|----------|
| [QUICKSTART.md](QUICKSTART.md) | Development start guide, Phase 0 checklist | Starting a new session |
| [CLAUDE.md](CLAUDE.md) | Architecture guide, query patterns, troubleshooting | Understanding system design |
| [PRD.md](PRD.md) | Complete implementation plan with code examples | Implementing phases |

## Technology Stack

- **Graph Database**: Neo4j 5.14+ with APOC plugin
- **Workflow**: LangGraph 0.2+ (stateful orchestration)
- **LLM**: OpenAI GPT-4o (synthesis + NER)
- **Embeddings**: OpenAI text-embedding-3-large (3072 dim)
- **NER**: spaCy 3.7+ with transformers
- **Language**: Python 3.11+
- **Package Manager**: Poetry

## Expected Data Scale

- **Requirements**: 227 (FuncR, SafR, PerfR, IntR)
- **Document Sections**: 500+
- **Total Nodes**: ~3,000
- **Total Relationships**: ~4,300
- **Target Response Time**: <2 seconds
- **Target Accuracy**: >90%

## Implementation Roadmap

### Phase 0: Environment Setup (Days 1-2) ⏳ NEXT
- Neo4j installation and configuration
- Python environment with all dependencies
- Database constraints and vector indexes
- Entity Dictionary initialization

### Phase 1: Data Ingestion (Days 3-7)
- Document parsers (SRD, PDD, DDD, Demo Procedures)
- Layer 1-4 graph construction
- Embedding generation and indexing

### Phase 2: Basic Query (Days 8-10)
- Pure Cypher template queries
- Basic retrieval and traceability

### Phase 3: Hybrid Query Workflow (Days 11-14)
- LangGraph workflow implementation
- Vector → NER → Cypher → LLM chain
- Adaptive routing logic

### Phase 4: Advanced Features (Days 15-20)
- Human-in-the-loop (HITL) debugging
- Performance optimization
- Comprehensive testing

## Repository Structure

```
ReqEng/
├── README.md              # ← You are here
├── QUICKSTART.md          # Development start guide
├── CLAUDE.md              # Architecture documentation
├── PRD.md                 # Product Requirements Document
├── .gitignore
├── Documents/             # Source documents
│   ├── SRD/              # System Requirements (227 reqs)
│   ├── PDD/              # Preliminary Design
│   ├── DDD/              # Detailed Design
│   └── Demo/             # Demonstration Procedures
└── [Future: src/, data/, scripts/, tests/]
```

## MOSAR Domain

The MOSAR project focuses on modular spacecraft assembly and reconfiguration in orbit.

**Key Components**:
- **R-ICU**: Reduced Instrument Control Unit (Zynq UltraScale+ MPSoC)
- **OBC**: On-Board Computer (R5 real-time processor)
- **cPDU**: Power Distribution Unit
- **HOTDOCK**: Hot-swappable docking interface
- **WM**: Walking Manipulator
- **SM**: Service Module

**Network Protocols**:
- CAN Bus (1 Mbps) - Real-time communication
- Ethernet (100 Mbps) - High-bandwidth data
- SpaceWire - Backup protocol

## Contributing

This is a research/planning repository. Implementation follows the 4-phase plan in [PRD.md](PRD.md).

## License

[To be determined]

## Contact

For questions about the implementation plan or architecture, refer to:
- [QUICKSTART.md](QUICKSTART.md#-tips) - Troubleshooting tips
- [CLAUDE.md](CLAUDE.md#troubleshooting) - Common issues
- [PRD.md](PRD.md) - Detailed specifications

---

**Last Updated**: 2025-10-26
**Git Commit**: Initial commit (Planning phase complete)
**Next Action**: Start Phase 0 - Environment Setup
