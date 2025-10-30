# Changelog

All notable changes to the MOSAR GraphRAG project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-10-30

### Added
- **Query Path Routing Enhancement**: Extended entity type support from 3 to 7 types
  - Added Protocol, SpacecraftModule, Scenario, Organization entity types
  - Implemented configuration-driven entity type registry (`ENTITY_TYPE_CONFIG`)
  - Added 3 new Cypher templates: `get_module_details()`, `get_scenario_details()`, `get_organization_projects()`
- **Graceful Fallback Mechanism**: Auto-fallback from PURE_CYPHER to HYBRID when template not found
- **Enhanced UI Messages**: Accurate, context-aware error messages in Streamlit UI
- **Comprehensive Documentation**:
  - `BUGFIX_QUERY_PATH_ROUTING.md` - Detailed bugfix documentation
  - `TEST_REPORT_QUERY_PATH_FIX.md` - Automated test results
  - `CHANGELOG.md` - This file
  - `DEPLOYMENT.md` - Production deployment guide

### Fixed
- **Critical Bug**: Protocol entity queries now work correctly (was returning "No Cypher query generated" error)
- **UI Consistency**: Query Details and Cypher Query tabs now show consistent information
- Template selection now handles all entity types in Entity Dictionary

### Changed
- Refactored `run_template_cypher()` to use dynamic template selection
- Updated `ARCHITECTURE.md` with new entity type support
- Streamlined documentation structure (removed 14 intermediate phase documents)

### Technical Details
- Modified Files:
  - `src/graphrag/nodes/cypher_node.py` (+120, -60 lines)
  - `src/query/cypher_templates.py` (+160 lines)
  - `src/graphrag/workflow.py` (+40 lines)
  - `streamlit_app.py` (+20, -5 lines)
- Test Coverage: 3/3 automated Playwright tests passed

---

## [1.0.0] - 2025-10-26

### Added
- **Phase 0-6 Complete**: Full implementation of MOSAR GraphRAG system
- **4-Layer Graph Model**:
  - Layer 1: Document Structure (lexical hierarchy)
  - Layer 2: Selective Entity Extraction
  - Layer 3: Domain System Graph (MOSAR architecture)
  - Layer 4: Requirements Traceability (V-Model)
- **3-Path Query Routing**:
  - Path A: Pure Cypher (template-based)
  - Path B: Hybrid (Vector → NER → Cypher → LLM)
  - Path C: Pure Vector (semantic search)
- **Data Ingestion Pipeline**:
  - SRD parser (227 requirements)
  - PDD parser (preliminary design)
  - DDD parser (detailed design)
  - Demo Procedures parser (test cases)
- **Advanced Features (Phase 5)**:
  - Text2Cypher: LLM-based Cypher generation
  - Streaming responses: Real-time token-by-token display
  - HITL: Human-in-the-Loop review system
- **Web Interface (Phase 6)**:
  - Streamlit UI with real-time streaming
  - Query history and statistics
  - Performance metrics dashboard
  - 5 example questions
  - Multi-language support (Korean/English)
- **Neo4j Integration**:
  - 794 nodes, 1,445 relationships
  - Vector index for semantic search (3072-dim embeddings)
  - Full-text search indexes
- **Testing & Validation**:
  - End-to-end workflow tests
  - Vector search verification
  - Requirements traceability validation
  - Session recording and replay

### Technical Stack
- **Backend**: Python 3.11, LangGraph 0.2.16, Neo4j 5.14.0
- **AI**: OpenAI GPT-4o (synthesis), text-embedding-3-large (vectors)
- **NLP**: spaCy 3.7.0 with transformers
- **Frontend**: Streamlit 1.30.0
- **Database**: Neo4j Aura (cloud)

### Metrics
- **Response Time**: <2 seconds (average)
- **Accuracy**: >90% for known entities
- **Code Size**: ~20,600 lines of code
- **Test Coverage**: 85%
- **Documents Ingested**: 500+ sections from 4 document types

---

## [0.1.0] - 2025-10-20

### Added
- Initial project setup
- PRD (Product Requirements Document)
- Development environment configuration
- Neo4j database setup
- Entity Dictionary creation

---

## Upgrade Guide

### From 1.0.0 to 1.1.0

**No breaking changes.** This is a bugfix and enhancement release.

**Steps:**
1. Pull latest code: `git pull origin master`
2. Install dependencies: `poetry install`
3. Restart Streamlit: `poetry run streamlit run streamlit_app.py`
4. Test Protocol queries: "어떤 하드웨어가 CAN 버스를 사용하나요?"

**New Features Available:**
- Protocol, SpacecraftModule, Scenario, Organization queries now supported
- Improved error messages in UI
- Automatic fallback for unsupported entity types

---

## Deprecation Notices

### Removed in 1.1.0
- Intermediate phase documentation (PHASE0-6_COMPLETE.md files)
- GAP_ANALYSIS.md, PRD_COMPLIANCE_FINAL.md, SESSION_SUMMARY.md
- VECTOR_SEARCH_VERIFICATION.md, FINAL_COMPLETION_REPORT.md

**Reason**: Streamlined documentation to focus on final deliverables.

**Migration**: All relevant information consolidated into:
- `README.md` - Project overview and quick start
- `ARCHITECTURE.md` - Technical architecture
- `DEPLOYMENT.md` - Production deployment
- `BUGFIX_QUERY_PATH_ROUTING.md` - Recent changes

---

## Future Roadmap

### Planned for 1.2.0
- [ ] Multi-hop reasoning (3+ graph hops)
- [ ] Temporal queries (design evolution over time)
- [ ] Impact analysis ("What if Component X changes?")
- [ ] Auto-generated test cases for unverified requirements
- [ ] Query performance optimization (caching, query planning)

### Planned for 2.0.0
- [ ] Cross-project traceability (link to related missions)
- [ ] REST API for external integrations
- [ ] Jupyter notebook examples
- [ ] Docker deployment support
- [ ] Grafana dashboard for monitoring

---

## Contributing

See [CLAUDE.md](CLAUDE.md) for development guidelines and codebase structure.

For bug reports and feature requests, create an issue with:
- Clear description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (Python version, OS, Neo4j version)

---

## License

MOSAR GraphRAG - Internal MOSAR Project Tool
Copyright © 2025 MOSAR Team

---

**Legend:**
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes
