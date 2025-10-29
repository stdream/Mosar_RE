"""
MOSAR GraphRAG Web Interface - Streamlit Application

Full-stack features:
- Real-time streaming responses
- Query history tracking
- Query path visualization
- Performance metrics
- Citation display
- Multi-language support (Korean/English)
- HITL (Human-in-the-Loop) mode

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import time
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.graphrag.workflow import GraphRAGWorkflow
from src.graphrag.hitl import HITLManager

# Page config
st.set_page_config(
    page_title="MOSAR GraphRAG",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1f77b4;
    margin-bottom: 0.5rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
}
.metric-box {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.status-message {
    padding: 0.5rem;
    border-left: 4px solid #1f77b4;
    background-color: #e8f4f8;
    margin: 0.5rem 0;
}
.citation-box {
    background-color: #fff9e6;
    padding: 0.8rem;
    border-radius: 0.3rem;
    border-left: 4px solid #ff9800;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = GraphRAGWorkflow()

    if 'hitl_manager' not in st.session_state:
        hitl_enabled = os.getenv("HITL_ENABLED", "false").lower() == "true"
        st.session_state.hitl_manager = HITLManager(enabled=hitl_enabled)

    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'current_answer' not in st.session_state:
        st.session_state.current_answer = ""

    if 'current_metadata' not in st.session_state:
        st.session_state.current_metadata = {}

    if 'streaming_enabled' not in st.session_state:
        st.session_state.streaming_enabled = os.getenv("STREAMING_ENABLED", "true").lower() == "true"

    if 'text2cypher_enabled' not in st.session_state:
        st.session_state.text2cypher_enabled = os.getenv("USE_TEXT2CYPHER", "true").lower() == "true"


def render_header():
    """Render page header."""
    st.markdown('<div class="main-header">🚀 MOSAR GraphRAG System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Intelligent Requirements Engineering with Knowledge Graphs</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")


def render_sidebar():
    """Render sidebar with settings and stats."""
    with st.sidebar:
        st.header("⚙️ Settings")

        # Streaming toggle
        st.session_state.streaming_enabled = st.toggle(
            "Enable Streaming Responses",
            value=st.session_state.streaming_enabled,
            help="Stream answers token-by-token for real-time feedback"
        )

        # Text2Cypher toggle
        st.session_state.text2cypher_enabled = st.toggle(
            "Enable Text2Cypher (LLM)",
            value=st.session_state.text2cypher_enabled,
            help="Use LLM to generate Cypher queries from natural language"
        )

        st.markdown("---")

        # Statistics
        st.header("📊 Session Statistics")

        if st.session_state.history:
            total_queries = len(st.session_state.history)
            avg_time = sum(h.get('processing_time_ms', 0) for h in st.session_state.history) / total_queries

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Queries", total_queries)
            with col2:
                st.metric("Avg Response Time", f"{avg_time:.0f}ms")

            # Query path distribution
            path_counts = {}
            for h in st.session_state.history:
                path = h.get('query_path', 'unknown')
                path_counts[path] = path_counts.get(path, 0) + 1

            st.markdown("**Query Paths:**")
            for path, count in path_counts.items():
                st.write(f"- {path}: {count}")

        else:
            st.info("No queries yet")

        st.markdown("---")

        # Query history
        st.header("📜 Query History")

        if st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history[-10:])):  # Last 10
                with st.expander(f"Q{len(st.session_state.history) - i}: {item['question'][:50]}..."):
                    st.write(f"**Path:** {item.get('query_path', 'unknown')}")
                    st.write(f"**Time:** {item.get('processing_time_ms', 0):.0f}ms")
                    st.write(f"**Timestamp:** {item.get('timestamp', 'N/A')}")
        else:
            st.info("No history yet")

        # Clear history button
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()


def render_example_questions():
    """Render example questions as quick-start buttons."""
    st.subheader("💡 Example Questions")

    examples = [
        {
            "text": "R-ICU를 변경하면 어떤 요구사항이 영향받나요?",
            "emoji": "🔧",
            "type": "Component Impact"
        },
        {
            "text": "FuncR_S110의 전체 추적성을 보여주세요",
            "emoji": "🔗",
            "type": "Traceability"
        },
        {
            "text": "테스트 케이스가 없는 요구사항은 무엇인가요?",
            "emoji": "⚠️",
            "type": "Testing Gap"
        },
        {
            "text": "What hardware handles network communication?",
            "emoji": "🌐",
            "type": "Architecture"
        },
        {
            "text": "Show me components that use the CAN protocol",
            "emoji": "🚌",
            "type": "Protocol Query"
        }
    ]

    cols = st.columns(len(examples))
    for col, ex in zip(cols, examples):
        with col:
            if st.button(f"{ex['emoji']} {ex['type']}", use_container_width=True, key=f"ex_{examples.index(ex)}"):
                st.session_state.example_question = ex['text']
                st.rerun()


def render_query_path_badge(query_path: str, confidence: float):
    """Render query path badge with color coding."""
    color_map = {
        "PURE_CYPHER": "#28a745",  # Green
        "HYBRID": "#ffc107",        # Yellow
        "PURE_VECTOR": "#17a2b8"    # Blue
    }

    color = color_map.get(query_path, "#6c757d")

    st.markdown(f"""
    <div style="display: inline-block; background-color: {color}; color: white; padding: 0.3rem 0.8rem;
                border-radius: 1rem; font-size: 0.9rem; font-weight: 600; margin-right: 0.5rem;">
        {query_path} • {confidence:.0%}
    </div>
    """, unsafe_allow_html=True)


def process_query_non_streaming(question: str):
    """Process query without streaming."""
    with st.spinner("Processing query..."):
        start_time = time.time()

        result = st.session_state.workflow.query(question)

        processing_time = (time.time() - start_time) * 1000

        return result


def process_query_streaming(question: str):
    """Process query with streaming."""
    answer_placeholder = st.empty()
    status_placeholder = st.empty()
    full_answer = ""
    metadata = {}

    for chunk in st.session_state.workflow.query_stream(question):
        chunk_type = chunk.get("type")

        if chunk_type == "status":
            # Show status message
            status_placeholder.markdown(
                f'<div class="status-message">🔄 {chunk["message"]}</div>',
                unsafe_allow_html=True
            )

        elif chunk_type == "chunk":
            # Append answer chunk
            full_answer += chunk["content"]
            answer_placeholder.markdown(full_answer)

        elif chunk_type == "metadata":
            # Store metadata
            metadata = chunk["data"]
            status_placeholder.empty()  # Clear status

        elif chunk_type == "error":
            st.error(chunk["message"])
            return None

    return {
        "answer": full_answer,
        "citations": metadata.get("citations", []),
        "metadata": metadata
    }


def display_result(result: Dict[str, Any]):
    """Display query result with all metadata."""
    if not result:
        return

    # Answer
    st.markdown("### 📝 Answer")
    st.markdown(result["answer"])

    st.markdown("---")

    # Metadata tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Query Details", "📚 Citations", "🔍 Cypher Query", "⚡ Performance"])

    metadata = result["metadata"]

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Query Path:**")
            render_query_path_badge(
                metadata.get("query_path", "unknown"),
                metadata.get("routing_confidence", 0)
            )

            st.markdown("<br>**Language:**", unsafe_allow_html=True)
            st.write(metadata.get("language", "unknown").upper())

            if metadata.get("extracted_entities"):
                st.markdown("**Extracted Entities:**")
                for entity_type, entity_list in metadata["extracted_entities"].items():
                    st.write(f"- {entity_type}: {', '.join(entity_list)}")

        with col2:
            if metadata.get("matched_entities"):
                st.markdown("**Matched Entities:**")
                for entity_type, entity_list in metadata["matched_entities"].items():
                    st.write(f"- {entity_type}: {', '.join(str(e) for e in entity_list)}")

            if metadata.get("query_generation_method"):
                st.markdown("**Query Generation:**")
                st.write(metadata["query_generation_method"])

    with tab2:
        citations = result.get("citations", [])
        if citations:
            st.markdown(f"**{len(citations)} sources cited:**")
            for i, citation in enumerate(citations, 1):
                st.markdown(
                    f'<div class="citation-box">[{i}] {citation}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No citations available")

    with tab3:
        if metadata.get("cypher_query"):
            st.code(metadata["cypher_query"], language="cypher")
        else:
            st.info("No Cypher query generated (Pure Vector path)")

    with tab4:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Processing Time",
                f"{metadata.get('processing_time_ms', 0):.0f} ms"
            )

        with col2:
            st.metric(
                "Routing Confidence",
                f"{metadata.get('routing_confidence', 0):.0%}"
            )

        with col3:
            graph_results_count = len(metadata.get("graph_results", []))  if "graph_results" in metadata else 0
            st.metric(
                "Graph Results",
                graph_results_count
            )


def main():
    """Main application."""
    init_session_state()

    render_header()
    render_sidebar()

    # Main content area
    render_example_questions()

    st.markdown("### 💬 Ask a Question")

    # Check for example question
    default_question = st.session_state.get("example_question", "")
    if default_question:
        del st.session_state.example_question  # Clear after use

    # Question input
    user_question = st.text_area(
        "Enter your question:",
        value=default_question,
        height=100,
        placeholder="예: R-ICU를 변경하면 어떤 요구사항이 영향받나요?\nOr: What requirements are related to R-ICU?"
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        submit_button = st.button("🚀 Ask", type="primary", use_container_width=True)

    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)

    if clear_button:
        st.rerun()

    # Process query
    if submit_button and user_question.strip():
        st.markdown("---")

        # Process based on streaming setting
        if st.session_state.streaming_enabled:
            result = process_query_streaming(user_question)
        else:
            result = process_query_non_streaming(user_question)

        if result:
            # Display result
            display_result(result)

            # Add to history
            history_entry = {
                "question": user_question,
                "answer": result["answer"][:200],  # Truncate
                "query_path": result["metadata"].get("query_path", "unknown"),
                "processing_time_ms": result["metadata"].get("processing_time_ms", 0),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.history.append(history_entry)

    elif submit_button:
        st.warning("Please enter a question!")


if __name__ == "__main__":
    main()
