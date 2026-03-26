"""Page 3: Memory & State — Conversation persistence, long-term memory."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="3. Memory & State", page_icon="🧠", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🧠 Chapter 3: Memory & State Management</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "For enterprise conversational AI, **memory** is critical. "
    "Agents need to remember conversations, learn user preferences, "
    "and maintain context across sessions."
)
st.markdown("---")

# ── Section 1: Thread-based Conversations ───────────────────────────
render_comparison(
    section_title="3.1 — Conversation Persistence",
    maf_title="Thread-based (Cosmos DB Backed)",
    maf_description=(
        "MAF uses **Threads** — managed conversation containers backed by Cosmos DB. "
        "Full message history is preserved automatically. "
        "Multi-turn conversations just work — add messages and run the agent."
    ),
    maf_code=maf.MEMORY_THREAD,
    adk_title="Session-based (Manual DB Setup)",
    adk_description=(
        "ADK uses `SessionService` for conversation state. "
        "Default is **in-memory (lost on restart)**. "
        "For persistence, you must configure `DatabaseSessionService` with your own database."
    ),
    adk_code=adk.MEMORY_SESSION,
)

# ── Section 2: Long-term Memory ────────────────────────────────────
render_comparison(
    section_title="3.2 — Long-term Memory & User Profiles",
    maf_title="Multiple Persistence Backends",
    maf_description=(
        "MAF provides **built-in persistence** with multiple backends:\n\n"
        "- **Azure Cosmos DB** — Managed cloud persistence for threads\n"
        "- **Redis** — Fast key-value state storage\n"
        "- **Mem0** — Semantic long-term memory with embeddings\n"
        "- **Per-user isolation** — Scoped storage for multi-tenant apps"
    ),
    maf_code=maf.MEMORY_LONG_TERM,
    adk_title="State + Memory Services + Context Features",
    adk_description=(
        "ADK provides **state, memory, and context management**:\n\n"
        "- `output_key` — Auto-save agent outputs to state\n"
        "- Memory service — Cross-session recall\n"
        "- Context caching — Reduce token usage\n"
        "- Context compression — Auto-summarize long contexts\n"
        "- Session rewind — Time-travel to earlier states"
    ),
    adk_code=adk.MEMORY_STATE,
)

# ── Architecture Diagram ───────────────────────────────────────────
st.markdown("### 3.3 — Memory Architecture Comparison")
st.markdown("---")

col_maf, col_adk = st.columns(2)

with col_maf:
    st.markdown(
        '<span class="framework-label-maf">Microsoft Agent Framework</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        ```
        ┌─────────────────────────────────┐
        │        Agent Runtime            │
        ├─────────────────────────────────┤
        │  ChatSummaryMemory              │
        │  ├─ Auto-summarize on overflow  │
        │  └─ Embedding-based retrieval   │
        ├─────────────────────────────────┤
        │  UserProfileMemory              │
        │  ├─ Learn preferences over time │
        │  └─ Per-user isolation          │
        ├─────────────────────────────────┤
        │  Thread Storage (Cosmos DB)     │
        │  ├─ Full message history        │
        │  ├─ Multi-turn persistence      │
        │  └─ Managed by Foundry          │
        └─────────────────────────────────┘
        ```
        """
    )

with col_adk:
    st.markdown(
        '<span class="framework-label-adk">Google ADK</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        ```
        ┌─────────────────────────────────┐
        │        Agent Runtime            │
        ├─────────────────────────────────┤
        │  Session State (dict)           │
        │  ├─ Key-value store per session │
        │  └─ output_key auto-save        │
        ├─────────────────────────────────┤
        │  Context Management             │
        │  ├─ Context caching             │
        │  ├─ Context compression         │
        │  └─ Session rewind              │
        ├─────────────────────────────────┤
        │  Session Storage                │
        │  ├─ InMemory (default)          │
        │  └─ Database (SQLite/Postgres)  │
        ├─────────────────────────────────┤
        │  Memory Service                 │
        │  └─ Cross-session recall        │
        ├─────────────────────────────────┤
        │  Artifacts                      │
        │  └─ File/binary data management │
        └─────────────────────────────────┘
        ```
        """
    )

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Memory & State",
    [
        "<strong>Cosmos DB threads</strong> — Managed cloud persistence; ADK defaults to in-memory",
        "<strong>Redis + Mem0 integrations</strong> — Pre-built packages for fast state and semantic memory",
        "<strong>Per-user isolation</strong> — Built-in multi-tenant memory scoping",
        "<strong>Production-grade persistence</strong> — Azure Cosmos DB with automatic scaling",
    ],
)

st.markdown("---")

# ── ADK Unique Features: Memory & State ────────────────────────────
st.markdown("### 🌟 Features Unique to Google ADK — Memory & Context")

with st.expander("🔍 ADK-Only: Context Caching — Reduce token costs", expanded=False):
    st.markdown(
        """
        ADK supports **context caching** to reduce token usage and costs.
        Frequently used context (like system prompts or large documents)
        can be cached and reused across requests.

        This is especially valuable for agents processing large contexts repeatedly.

        **MAF equivalent:** No built-in context caching — relies on model-level
        caching if available from the provider.
        """
    )

with st.expander("🔍 ADK-Only: Context Compression — Auto-summarize long contexts", expanded=False):
    st.markdown(
        """
        When conversation history grows too long, ADK can **automatically compress
        the context** by summarizing older messages. This keeps the agent responsive
        without losing important conversation history.

        **MAF equivalent:** Thread management handles this at the persistence layer,
        but no built-in context compression at the agent runtime level.
        """
    )

with st.expander("🔍 ADK-Only: Session Rewind — Time-travel debugging", expanded=False):
    st.markdown(
        """
        ADK allows you to **rewind a session** to a previous state.
        This is powerful for:
        - **Debugging** — See what state looked like at any point
        - **Recovery** — Roll back to a known-good state
        - **Testing** — Replay scenarios from specific checkpoints

        ```python
        # Rewind session to a previous event
        # https://google.github.io/adk-docs/sessions/session/rewind/
        ```

        **MAF equivalent:** Graph workflows support checkpointing and time-travel
        at the orchestration level, but not at the session state level.
        """
    )

with st.expander("🔍 ADK-Only: Artifacts — File and binary data management", expanded=False):
    st.markdown(
        """
        ADK has a built-in **Artifact management system** for handling files
        and binary data (images, PDFs, documents) within agent sessions:

        - Save, load, and manage versioned artifacts
        - Associate artifacts with sessions or users
        - Handle images, documents, or generated reports

        ```python
        from google.adk.artifacts import InMemoryArtifactService

        artifact_service = InMemoryArtifactService()
        # Agents can save/load files during execution
        ```

        **MAF equivalent:** File handling via Azure Blob Storage or custom
        tool implementations — no built-in artifact system at the framework level.
        """
    )
