# MOSAR GraphRAG System

A Graph-based Retrieval Augmented Generation (GraphRAG) system for the MOSAR (Modular Spacecraft Assembly and Reconfiguration) project, enabling intelligent querying of technical documentation with full requirements traceability.

## Project Status

**Version**: 1.1.0 ✅ **PRODUCTION READY**

**Latest Updates** (2025-10-30):
- ✅ Query Path Routing Enhanced (7 entity types supported)
- ✅ Protocol, SpacecraftModule, Scenario, Organization queries enabled
- ✅ Graceful fallback mechanism (PURE_CYPHER → HYBRID)
- ✅ Improved UI error messages

**Try it now**: `poetry run streamlit run streamlit_app.py`

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

## Overview

This system ingests MOSAR technical documentation (Requirements, Preliminary Design, Detailed Design, and Test Procedures) into a Neo4j graph database and provides intelligent question-answering capabilities using hybrid Vector + Cypher queries orchestrated by LangGraph.

### Key Features

- **4-Layer Graph Architecture**
  - Layer 1: Document Structure (preserves document hierarchy)
  - Layer 2: Selective Entities (domain-specific entities)
  - Layer 3: Domain System Graph (MOSAR components, modules, interfaces)
  - Layer 4: Requirements Traceability (V-Model: requirement → design → implementation → verification)

- **Advanced Query Capabilities** 🆕
  - **Text2Cypher with Guardrails**: LLM-based natural language → Cypher conversion
  - **Streaming Responses**: Real-time token-by-token answer generation
  - Adaptive routing: Entity Dictionary → NER → Vector/Cypher selection
  - Vector search with OpenAI embeddings (text-embedding-3-large, 3072 dimensions)
  - Contextual Cypher queries for structured data retrieval
  - LLM synthesis for natural language responses

- **Full-Stack Web Interface** 🆕
  - **Streamlit Web UI**: Browser-based access, no installation required
  - Real-time streaming with progress indicators
  - Query history and session statistics
  - Performance metrics and visualizations
  - Multi-language support (Korean/English)
  - One-click example questions

- **Full Traceability**
  - 227 system requirements tracked end-to-end
  - Design evolution tracking (PDD → DDD)
  - Test verification status (TestCase → Requirement)
  - Impact analysis and dependency mapping

## Quick Start

### Running the Web UI 🚀

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Edit .env with your Neo4j and OpenAI credentials

# 3. Load data (if not already loaded)
python scripts/load_documents.py

# 4. Run web interface
streamlit run streamlit_app.py

# Access at http://localhost:8501
```

### Running CLI

```bash
# Interactive CLI
python src/graphrag/app.py
```

### For Developers

See [CLAUDE.md](CLAUDE.md) for complete codebase documentation and development guidelines.

## 📚 Documentation

| Document | Description | Use When |
|----------|-------------|----------|
| **[README.md](README.md)** | 👈 You are here | Project overview and quick start |
| **[QUICKSTART.md](QUICKSTART.md)** | Fast setup guide | First-time setup |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture, 4-layer graph model | Understanding design |
| **[CLAUDE.md](CLAUDE.md)** | Complete codebase guide for Claude Code | Development and AI assistance |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide | Deploying to prod/staging |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and release notes | Tracking changes |
| **[PRD.md](PRD.md)** | Product Requirements Document | Implementation reference |

### Recent Updates
| Document | Description |
|----------|-------------|
| **[BUGFIX_QUERY_PATH_ROUTING.md](BUGFIX_QUERY_PATH_ROUTING.md)** | Query path bugfix (v1.1.0) |
| **[TEST_REPORT_QUERY_PATH_FIX.md](TEST_REPORT_QUERY_PATH_FIX.md)** | Automated test results |

## Technology Stack

- **Graph Database**: Neo4j 5.14+ (Aura Cloud)
- **Workflow**: LangGraph 0.2+ (stateful orchestration)
- **LLM**: OpenAI GPT-4o (synthesis, NER, Text2Cypher)
- **Embeddings**: OpenAI text-embedding-3-large (3072 dim)
- **NER**: spaCy 3.7+ with transformers
- **Web Framework**: Streamlit 1.30+ 🆕
- **Language**: Python 3.11+
- **Package Manager**: Poetry / pip

## Expected Data Scale

- **Requirements**: 227 (FuncR, SafR, PerfR, IntR)
- **Document Sections**: 500+
- **Total Nodes**: ~3,000
- **Total Relationships**: ~4,300
- **Target Response Time**: <2 seconds
- **Target Accuracy**: >90%

## Implementation Roadmap

### Phase 0: Environment Setup ✅ COMPLETE
- Neo4j Aura configuration
- Python environment with all dependencies
- Database constraints and vector indexes
- Entity Dictionary initialization

### Phase 1: Graph Schema ✅ COMPLETE
- Document parsers (SRD, PDD, DDD, Demo Procedures)
- Layer 1-4 graph construction
- Embedding generation and indexing

### Phase 2: Data Loading ✅ COMPLETE
- Pure Cypher template queries
- Basic retrieval and traceability

### Phase 3: LangGraph Workflow ✅ COMPLETE
- LangGraph workflow implementation
- Vector → NER → Cypher → LLM chain
- Adaptive routing logic

### Phase 4: Testing & Validation ✅ COMPLETE
- Human-in-the-loop (HITL) debugging
- Performance optimization
- Comprehensive testing (50+ unit tests, 5 E2E tests)

### Phase 5: Advanced Features ✅ COMPLETE 🆕
- **Text2Cypher**: LLM-based natural language → Cypher conversion
- **Safety Guardrails**: Multi-layer validation system
- **Streaming Responses**: Real-time token-by-token generation
- **Confidence Scoring**: Query quality estimation

### Phase 6: Production Deployment ✅ COMPLETE 🆕
- **Streamlit Web UI**: Full-stack browser interface
- **Real-time Metrics**: Query history, performance dashboard
- **Multi-language Support**: Korean/English
- **Deployment Ready**: Streamlit Cloud compatible

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
