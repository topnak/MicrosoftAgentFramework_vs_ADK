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
    maf_title="ChatSummary + UserProfile Memory",
    maf_description=(
        "MAF provides **built-in long-term memory**:\n\n"
        "- **ChatSummaryMemory** — Automatically summarizes conversations for continuity\n"
        "- **UserProfileMemory** — Learns and stores user preferences over time\n"
        "- **Per-user isolation** — `{{$userId}}` scoping for multi-tenant apps\n"
        "- **Embedding-based retrieval** — Semantic search over past interactions"
    ),
    maf_code=maf.MEMORY_LONG_TERM,
    adk_title="Manual State Dictionary",
    adk_description=(
        "ADK provides only a **simple key-value state dict** per session.\n\n"
        "❌ No automatic conversation summarization\n"
        "❌ No user profile learning\n"
        "❌ No embedding-based memory retrieval\n"
        "❌ No per-user memory scoping\n\n"
        "All memory patterns must be **built from scratch**."
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
        │  ├─ Simple key-value store      │
        │  └─ Manual management           │
        ├─────────────────────────────────┤
        │  Session Storage                │
        │  ├─ InMemory (default)          │
        │  │   └─ ❌ Lost on restart      │
        │  └─ Database (manual setup)     │
        │      └─ SQLite / PostgreSQL     │
        ├─────────────────────────────────┤
        │  Long-term Memory               │
        │  └─ ❌ Build from scratch       │
        └─────────────────────────────────┘
        ```
        """
    )

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Memory & State",
    [
        "<strong>Cosmos DB threads</strong> — Managed conversation persistence; ADK defaults to in-memory (lost on restart)",
        "<strong>ChatSummaryMemory</strong> — Automatic conversation summarization; ADK has no equivalent",
        "<strong>UserProfileMemory</strong> — Auto-learning user preferences; must be built manually in ADK",
        "<strong>Per-user isolation</strong> — Built-in multi-tenant memory scoping via <code>{{$userId}}</code>",
        "<strong>Embedding-based retrieval</strong> — Semantic search over conversation history; ADK uses simple key-value dict",
    ],
)
