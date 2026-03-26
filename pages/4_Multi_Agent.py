"""Page 4: Multi-Agent Orchestration — Graph workflows, patterns."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="4. Multi-Agent", page_icon="🔀", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🔀 Chapter 4: Multi-Agent Orchestration</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Complex enterprise workflows require **multiple specialized agents** working together. "
    "The orchestration model determines how flexible and production-ready your system can be."
)
st.markdown("---")

# ── Section 1: Basic Multi-Agent ────────────────────────────────────
render_comparison(
    section_title="4.1 — Multi-Agent Setup",
    maf_title="Graph-based Workflow with Deterministic Routing",
    maf_description=(
        "MAF uses a **graph-based orchestration model**. "
        "Define agent nodes, connect them with conditional edges, "
        "and let deterministic functions route between agents. "
        "Full control over task flow with type-safe transitions."
    ),
    maf_code=maf.MULTI_AGENT_GRAPH,
    adk_title="Fixed Patterns (Sequential / Parallel)",
    adk_description=(
        "ADK provides **pre-built orchestration classes**: "
        "`SequentialAgent`, `ParallelAgent`, `LoopAgent`. "
        "These cover basic patterns but lack the flexibility of graph-based routing."
    ),
    adk_code=adk.MULTI_AGENT_BASIC,
)

# ── Section 2: Advanced Patterns ────────────────────────────────────
render_comparison(
    section_title="4.2 — Advanced Orchestration Patterns",
    maf_title="Fan-out/Fan-in, Human-in-the-Loop, Loops",
    maf_description=(
        "MAF supports sophisticated patterns:\n\n"
        "- **Fan-out / Fan-in** — Parallel agent execution with result aggregation\n"
        "- **Human-in-the-Loop** — Pause workflow for human approval\n"
        "- **Conditional loops** — Retry with feedback until quality checks pass\n"
        "- **Switch-case routing** — Deterministic branching based on context"
    ),
    maf_code=maf.MULTI_AGENT_PATTERNS,
    adk_title="Limited Patterns (A2A for Complex)",
    adk_description=(
        "ADK's built-in patterns are limited to basic Sequential/Parallel/Loop.\n\n"
        "❌ No graph-based orchestration\n"
        "❌ No deterministic conditional routing\n"
        "❌ No built-in human-in-the-loop\n"
        "❌ No fan-out/fan-in with aggregation\n\n"
        "For complex patterns, ADK requires **A2A protocol** — each agent as a separate HTTP service."
    ),
    adk_code=adk.MULTI_AGENT_PATTERNS,
)

# ── Architecture Diagram ───────────────────────────────────────────
st.markdown("### 4.3 — Orchestration Architecture")
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
        ┌──────────────────────────────────────┐
        │         Graph-based Workflow         │
        │                                      │
        │    ┌────────────┐                    │
        │    │ Supervisor │◄──── User Input     │
        │    └─────┬──────┘                    │
        │          │                           │
        │    ┌─────┴──────┐                    │
        │    ▼            ▼                    │
        │ ┌──────┐   ┌──────────┐              │
        │ │ Data │   │Fulfillment│             │
        │ │Agent │   │  Agent    │             │
        │ └──┬───┘   └────┬─────┘             │
        │    │             │                   │
        │    ▼             ▼                   │
        │ ┌──────────────────┐                 │
        │ │   Fan-in Node    │                 │
        │ │ (Aggregate)      │                 │
        │ └──────┬───────────┘                 │
        │        ▼                             │
        │ ┌──────────────────┐                 │
        │ │ Human Checkpoint │                 │
        │ │ (Approve/Reject) │                 │
        │ └──────────────────┘                 │
        └──────────────────────────────────────┘
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
        ┌──────────────────────────────────────┐
        │       Fixed Pattern Agents           │
        │                                      │
        │   SequentialAgent:                   │
        │   Agent A ──► Agent B ──► Agent C    │
        │                                      │
        │   ParallelAgent:                     │
        │   Agent A ──┐                        │
        │   Agent B ──┼──► [Results list]      │
        │   Agent C ──┘                        │
        │                                      │
        │   LoopAgent:                         │
        │   Agent A ──► repeat (max N)         │
        │                                      │
        │   Complex? Use A2A:                  │
        │   ┌───────┐    ┌───────┐             │
        │   │HTTP   │◄──►│HTTP   │             │
        │   │Server │    │Server │             │
        │   │Agent A│    │Agent B│             │
        │   └───────┘    └───────┘             │
        │   ⚠️ Separate services required      │
        └──────────────────────────────────────┘
        ```
        """
    )

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Multi-Agent Orchestration",
    [
        "<strong>Graph-based orchestration</strong> — Flexible workflow graphs with conditional routing; ADK has only fixed Sequential/Parallel/Loop",
        "<strong>Fan-out / Fan-in</strong> — Parallel agent execution with result aggregation built-in",
        "<strong>Human-in-the-Loop</strong> — Checkpoint-based approval workflow; ADK has no equivalent",
        "<strong>Deterministic routing</strong> — Type-safe conditional edges between agents; ADK requires A2A (separate HTTP services)",
        "<strong>Single process</strong> — All agents run in one workflow; ADK A2A requires separate deployments for each agent",
    ],
)
