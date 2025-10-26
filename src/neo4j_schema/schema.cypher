// ==========================================
// CONSTRAINTS (Uniqueness & Data Integrity)
// ==========================================

// Documents
CREATE CONSTRAINT unique_document_id IF NOT EXISTS
FOR (d:Document) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT unique_section_id IF NOT EXISTS
FOR (s:Section) REQUIRE s.id IS UNIQUE;

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
FOR (tc:TestCase) ON (tc.status, tc.type);

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
