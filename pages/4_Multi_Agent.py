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
    adk_title="Workflow Agents + LLM Transfer + ADK 2.0 Graph",
    adk_description=(
        "ADK offers multiple orchestration approaches:\n\n"
        "- **Workflow agents** — SequentialAgent, ParallelAgent, LoopAgent\n"
        "- **LLM-driven transfer** — Dynamic routing via sub_agents\n"
        "- **Custom agents** — Extend BaseAgent for custom logic\n"
        "- **ADK 2.0 Alpha** — Graph-based workflows with routes, data handling, human input\n"
        "- **A2A protocol** — Cross-framework agent communication"
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
        │     ADK Orchestration Options        │
        │                                      │
        │   Workflow Agents:                   │
        │   Sequential: A ──► B ──► C          │
        │   Parallel:   A ──┐                  │
        │               B ──┼──► [Results]     │
        │               C ──┘                  │
        │   Loop: A ──► repeat (max N)         │
        │                                      │
        │   LLM-driven Transfer:               │
        │   Router → sub_agents=[A, B, C]      │
        │   (LLM decides which agent to call)  │
        │                                      │
        │   ADK 2.0: Graph Workflows (Alpha)   │
        │   Routes, data handling, human input │
        │                                      │
        │   A2A Protocol:                      │
        │   Cross-framework interoperability   │
        └──────────────────────────────────────┘
        ```
        """
    )

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Multi-Agent Orchestration",
    [
        "<strong>Mature graph orchestration</strong> — Production-ready graph workflows with checkpointing; ADK 2.0 graph is in Alpha",
        "<strong>Fan-out / Fan-in</strong> — Parallel agent execution with result aggregation built-in",
        "<strong>Human-in-the-Loop</strong> — Checkpoint-based approval workflow built into graph",
        "<strong>Durable Tasks</strong> — Long-running workflow orchestration via durable task framework",
        "<strong>Time-travel debugging</strong> — Replay and inspect workflow execution at any checkpoint",
    ],
)

st.markdown("---")

# ── ADK Unique Features: Orchestration ─────────────────────────────
st.markdown("### 🌟 Features Unique to Google ADK — Orchestration")

with st.expander("🔍 ADK-Only: Callbacks — Deep lifecycle hooks", expanded=False):
    st.markdown(
        """
        ADK provides a **rich callback system** with hooks at every stage of agent execution:

        - `before_model_callback` — Run code before the LLM is called
        - `after_model_callback` — Intercept/modify LLM responses
        - `before_tool_callback` — Validate or modify tool inputs
        - `after_tool_callback` — Process tool outputs before returning

        ```python
        def log_model_call(callback_context, llm_request):
            print(f"Calling model with {len(llm_request.contents)} messages")
            return None  # Continue normally

        agent = LlmAgent(
            name="monitored_agent",
            model="gemini-2.5-flash",
            before_model_callback=log_model_call,
        )
        ```

        **Use cases:** Logging, security filtering, input validation,
        cost tracking, response modification.

        **MAF equivalent:** Middleware pipeline provides similar request/response
        interception but at a different abstraction level.
        """
    )

with st.expander("🔍 ADK-Only: Planners — Built-in reasoning strategies", expanded=False):
    st.markdown(
        """
        ADK includes built-in **planner** support for multi-step reasoning:

        **BuiltInPlanner** — Uses Gemini's native thinking feature:
        ```python
        from google.adk.planners import BuiltInPlanner
        from google.genai.types import ThinkingConfig

        agent = LlmAgent(
            model="gemini-2.5-flash",
            planner=BuiltInPlanner(
                thinking_config=ThinkingConfig(
                    include_thoughts=True,
                    thinking_budget=1024,
                )
            ),
        )
        ```

        **PlanReActPlanner** — Structured plan/action/reasoning format:
        ```python
        from google.adk.planners import PlanReActPlanner

        agent = LlmAgent(
            model="gemini-2.5-flash",
            planner=PlanReActPlanner(),
        )
        ```

        **MAF equivalent:** No built-in planner abstraction — similar behavior
        can be achieved through prompt engineering or custom middleware.
        """
    )

with st.expander("🔍 ADK-Only: A2A Protocol — Cross-framework agent interoperability", expanded=False):
    st.markdown(
        """
        The **Agent-to-Agent (A2A) Protocol** is an open standard for agent
        communication across different frameworks:

        - **Expose ADK agents** as A2A-compatible services
        - **Consume external agents** from any A2A-compatible framework
        - **Cross-framework interop** — ADK agents can talk to MAF agents and vice versa

        ```python
        # Expose an ADK agent as A2A service
        # https://google.github.io/adk-docs/a2a/quickstart-exposing/

        # Consume an A2A agent from ADK
        # https://google.github.io/adk-docs/a2a/quickstart-consuming/
        ```

        **Note:** MAF also has `agent-framework-a2a` package for A2A support.
        A2A is an open standard that both frameworks support.
        """
    )

with st.expander("🔍 ADK-Only: Gemini Live API Toolkit — Real-time multimodal streaming", expanded=False):
    st.markdown(
        """
        ADK provides native support for **bidirectional streaming** with
        the Gemini Live API Toolkit:

        - **Audio streaming** — Real-time voice interaction
        - **Video streams** — Process video input
        - **Image handling** — Multimodal conversations
        - **Low latency** — Designed for real-time experiences

        This enables building voice assistants, video analysis agents,
        and interactive multimodal applications.

        **MAF equivalent:** SSE streaming for text is built-in,
        but real-time audio/video streaming requires custom implementation.
        """
    )
