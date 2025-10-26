# MOSAR GraphRAG - Quick Start Guide

## 현재 상태 (Current Status)

### ✅ 완료된 것 (Completed)
- **아키텍처 설계**: 4-Layer GraphRAG 모델 완성
  - Layer 1: Document Structure (문서 구조 그래프)
  - Layer 2: Selective Entities (선택적 엔티티 추출)
  - Layer 3: Domain System Graph (MOSAR 시스템 아키텍처)
  - Layer 4: Requirements Traceability (요구사항 추적성)
- **PRD 작성**: 4주 구현 계획 (Phase 0-4) 상세 문서화
- **CLAUDE.md**: 향후 Claude 인스턴스를 위한 아키텍처 가이드
- **문서 준비**: SRD (227 requirements), PDD, DDD, Demo Procedures

### ⏳ 다음 단계 (Next Steps)
**Phase 0: Environment Setup (Days 1-2)** 부터 시작

### 📊 예상 데이터 규모
- Requirements: 227개
- Document Sections: 500+ 개
- Total Nodes: ~3,000개
- Total Relationships: ~4,300개

---

## 🚀 다음 세션 즉시 시작 명령어

### 방법 1: 전체 Phase 0 자동 실행
```
QUICKSTART.md를 읽었어. PRD.md의 Phase 0 섹션을 보고 구현 시작해줘.
```

### 방법 2: 단계별 실행
```
1단계: Neo4j 설치 및 설정부터 시작해줘
```

---

## 📋 Phase 0 체크리스트 (Days 1-2)

### Day 1: 환경 구축

#### 1. Neo4j 설치 및 설정
- [ ] Neo4j Desktop 또는 Docker로 설치
- [ ] 데이터베이스 생성: `mosar-graphrag`
- [ ] APOC 플러그인 활성화
- [ ] 연결 확인: `bolt://localhost:7687`

**Docker 사용 시**:
```bash
docker run -d \
  --name neo4j-mosar \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5.14.0
```

#### 2. Python 환境 설정
- [ ] Python 3.11+ 설치 확인
- [ ] Poetry 설치: `pip install poetry`
- [ ] `pyproject.toml` 생성 (PRD.md 참조)
- [ ] 의존성 설치: `poetry install`
- [ ] spaCy 모델 다운로드: `python -m spacy download en_core_web_trf`

**주요 의존성**:
```toml
langgraph = "^0.2.0"
neo4j = "^5.14.0"
openai = "^1.3.0"
spacy = "^3.7.0"
spacy-transformers = "^1.3.0"
```

#### 3. 환경 변수 설정
- [ ] `.env` 파일 생성

```env
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# OpenAI
OPENAI_API_KEY=sk-...

# Embeddings
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSION=3072
```

### Day 2: 그래프 스키마 초기화

#### 4. 제약조건 생성
- [ ] `scripts/setup_constraints.cypher` 실행
  - Unique constraints: `Requirement.id`, `Component.id`, `Section.id`
  - Existence constraints: 필수 속성 정의

**Cypher 스크립트** (PRD.md Phase 0-4 참조):
```cypher
CREATE CONSTRAINT unique_requirement_id IF NOT EXISTS
FOR (r:Requirement) REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT unique_component_id IF NOT EXISTS
FOR (c:Component) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT unique_section_id IF NOT EXISTS
FOR (s:Section) REQUIRE s.id IS UNIQUE;
```

#### 5. 벡터 인덱스 생성
- [ ] TextChunk, Requirement 노드에 벡터 인덱스 생성
- [ ] 3072 차원, cosine similarity

```cypher
CREATE VECTOR INDEX chunk_embeddings IF NOT EXISTS
FOR (n:TextChunk) ON (n.embedding)
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 3072,
    `vector.similarity_function`: 'cosine'
  }
};
```

#### 6. Entity Dictionary 초안 작성
- [ ] `data/entities/mosar_entities.json` 생성
- [ ] 주요 컴포넌트 30개 등록 (R-ICU, WM, SM, OBC, cPDU, HOTDOCK 등)
- [ ] 요구사항 카테고리 4개 등록 (FuncR, SafR, PerfR, IntR)

**초안 구조**:
```json
{
  "components": {
    "R-ICU": {"id": "R-ICU", "type": "Component"},
    "Walking Manipulator": {"id": "WM", "type": "Component"},
    "Service Module": {"id": "SM", "type": "SpacecraftModule"}
  },
  "requirements": {
    "기능 요구사항": {"type": "Requirement", "filter": {"type": "FuncR"}},
    "안전 요구사항": {"type": "Requirement", "filter": {"type": "SafR"}}
  }
}
```

---

## 📁 프로젝트 구조 (Phase 0 완료 후)

```
ReqEng/
├── .env                          # API keys, Neo4j credentials
├── .gitignore
├── README.md
├── QUICKSTART.md                 # ← 현재 파일
├── CLAUDE.md                     # Architecture guide
├── PRD.md                        # Complete implementation plan
├── pyproject.toml                # Python dependencies
├── Documents/                    # 원본 문서들
│   ├── SRD/
│   ├── PDD/
│   ├── DDD/
│   └── Demo_Procedures/
├── scripts/
│   └── setup_constraints.cypher  # DB 초기화 스크립트
├── data/
│   └── entities/
│       └── mosar_entities.json   # Entity Dictionary
└── src/                          # Phase 1부터 생성
    ├── ingestion/
    ├── query/
    └── utils/
```

---

## 🔍 참고 문서

### 주요 문서 위치
- **[PRD.md](PRD.md)**: 전체 구현 계획 및 상세 코드 (111K+ tokens)
  - Phase 0: Lines ~200-400 (환경 설정)
  - Phase 1: Lines ~400-1200 (데이터 적재)
  - Phase 3: Lines ~1400-2000 (Hybrid Workflow)

- **[CLAUDE.md](CLAUDE.md)**: 아키텍처 개요 및 개발 가이드 (28K tokens)
  - 4-Layer Graph Model
  - Hybrid Query Architecture
  - MOSAR Domain Knowledge

- **[Documents/SRD/System Requirements Document_MOSAR.md](Documents/SRD/System Requirements Document_MOSAR.md)**: 227개 요구사항

### 외부 참고자료
- GraphRAG Concepts: https://graphrag.com/concepts/intro-to-graphrag/
- LangGraph Docs: https://langchain-ai.github.io/langgraph/
- Neo4j Vector Search: https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/

---

## ⚡ 자주 사용할 명령어

### Neo4j 확인
```bash
# Docker 사용 시
docker ps | grep neo4j
docker logs neo4j-mosar

# Neo4j Browser 접속
# http://localhost:7474
```

### Python 환경
```bash
# 가상환경 활성화
poetry shell

# 의존성 추가
poetry add <package>

# spaCy 모델 확인
python -m spacy validate
```

### Git
```bash
# 현재 상태 확인
git status

# 변경사항 커밋
git add .
git commit -m "Phase 0 complete: Environment setup"
```

---

## 🎯 성공 기준 (Acceptance Criteria)

### Phase 0 완료 조건
- ✅ Neo4j 데이터베이스 연결 성공
- ✅ Python 환경 및 모든 의존성 설치 완료
- ✅ 제약조건 6개 생성 완료
- ✅ 벡터 인덱스 2개 생성 완료
- ✅ Entity Dictionary 초안 (30+ entities)
- ✅ 환경 변수 설정 완료

### Phase 0 검증 방법
```python
# test_environment.py 실행 (PRD.md 참조)
from neo4j import GraphDatabase
import openai
import spacy

# 1. Neo4j 연결 테스트
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
with driver.session() as session:
    result = session.run("SHOW CONSTRAINTS")
    print(f"Constraints: {len(result.data())}")  # Should be 6+

# 2. OpenAI API 테스트
embedding = openai.embeddings.create(
    model="text-embedding-3-large",
    input="test"
)
print(f"Embedding dim: {len(embedding.data[0].embedding)}")  # Should be 3072

# 3. spaCy 모델 테스트
nlp = spacy.load("en_core_web_trf")
doc = nlp("R-ICU communicates via CAN bus")
print(f"Entities: {[(ent.text, ent.label_) for ent in doc.ents]}")
```

---

## 💡 Tips

### 다음 세션 시작 시
1. **QUICKSTART.md를 먼저 열기** (현재 파일)
2. "Phase 0 시작해줘" 또는 "QUICKSTART.md 보고 Phase 0 실행해줘"
3. 필요 시 **PRD.md의 Phase 0 섹션** 참조 (상세 코드 포함)

### 문제 발생 시
- Neo4j 연결 실패: `.env` 파일의 credentials 확인
- spaCy 모델 에러: `python -m spacy download en_core_web_trf` 재실행
- OpenAI API 에러: API key 및 quota 확인

### 시간 절약
- Docker로 Neo4j 사용 (수동 설치보다 빠름)
- Entity Dictionary는 최소한으로 시작 (Phase 1에서 확장 가능)
- 제약조건 스크립트를 Neo4j Browser에서 직접 실행

---

**Last Updated**: 2025-10-26
**Status**: Ready to start Phase 0
**Next Session**: "QUICKSTART.md 읽고 Phase 0 시작해줘"
