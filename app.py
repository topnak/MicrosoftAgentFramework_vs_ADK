"""MAF vs ADK — Side-by-Side Comparison Demo.

Landing page with executive summary, comparison matrix, and live demo.
"""

import pathlib
import streamlit as st

# ── Page config (must be first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="MAF vs ADK Comparison",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ──────────────────────────────────────────────────────
css_path = pathlib.Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.markdown("### 🗂️ Story Sections")
    st.markdown("""
    1. 🏗️ Agent Creation
    2. 🔧 Tool Integration
    3. 🧠 Memory & State
    4. 🔀 Multi-Agent Orchestration
    5. 🚀 Deployment & Production
    6. 🔗 3rd Party Integration
    """)
    st.markdown("---")
    st.markdown("**Baseline**: MAF v2 Responses API")
    st.markdown("**Compared with**: Google ADK")
    st.markdown("---")
    st.caption("Navigate sections using the sidebar pages ↑")

# ── Hero Section ────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style="text-align:center;">
        <span style="color:#4A90D9;">Microsoft Agent Framework</span>
        <span style="color:#888;"> vs </span>
        <span style="color:#34A853;">Google ADK</span>
    </h1>
    <p style="text-align:center; color:#8899aa; font-size:1.2rem;">
        A side-by-side comparison for enterprise conversational AI development<br/>
        with Snowflake, BlueYonder & Microsoft Fabric integration
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Executive Summary ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h3 style="color:#4A90D9;">Microsoft Agent Framework</h3>
        <ul>
        <li>Enterprise-grade SDK for Python & .NET</li>
        <li>Native Azure AI Foundry integration</li>
        <li>OpenAI Responses API v2 (streaming)</li>
        <li>Built-in tools: AI Search, Bing, Code Interpreter</li>
        <li>Graph-based multi-agent orchestration</li>
        <li>Long-term memory with auto-summarization</li>
        <li>Managed Identity — zero credential management</li>
        <li>Built-in eval, prompt optimization, CI/CD</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h3 style="color:#34A853;">Google Agent Development Kit</h3>
        <ul>
        <li>Python-first SDK (no .NET support)</li>
        <li>Vertex AI / Cloud Run deployment</li>
        <li>Runner-based invocation pattern</li>
        <li>Built-in: Google Search only</li>
        <li>Sequential / Parallel / Loop patterns</li>
        <li>Session-based state (manual memory)</li>
        <li>Manual credential management</li>
        <li>No built-in eval or prompt optimization</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Comparison Matrix ──────────────────────────────────────────────
st.markdown("### 📊 Feature Comparison Matrix")

matrix_data = {
    "Capability": [
        "Languages",
        "Agent Definition",
        "Invocation API",
        "Streaming",
        "Built-in Web Search",
        "Built-in RAG / Vector Search",
        "Code Interpreter (Sandbox)",
        "MCP Tool Support",
        "Long-term Memory",
        "User Profile Memory",
        "Multi-Agent Patterns",
        "Graph-based Orchestration",
        "Human-in-the-Loop",
        "Managed Identity",
        "Declarative Agent Config",
        "Built-in Evaluation",
        "Prompt Optimization",
        "Dataset from Traces",
        "Fabric / FabricIQ",
        "Snowflake Integration",
        "BlueYonder Integration",
    ],
    "Microsoft Agent Framework": [
        "Python & .NET ✅",
        "SDK + agent.yaml ✅",
        "OpenAI Responses API v2 ✅",
        "SSE streaming ✅",
        "WebSearchPreview ✅",
        "Azure AI Search ✅",
        "Built-in sandbox ✅",
        "Native MCP ✅",
        "ChatSummary + UserProfile ✅",
        "Auto-learning ✅",
        "Graph + Fan-out/in + Loop ✅",
        "Yes ✅",
        "Built-in checkpoint ✅",
        "Azure Managed Identity ✅",
        "agent.yaml ✅",
        "Intent, Task, Groundedness ✅",
        "Auto from traces ✅",
        "Production harvesting ✅",
        "Native (same identity) ✅",
        "MCP + Function Tool ✅",
        "Function Tool ✅",
    ],
    "Google ADK": [
        "Python only ⚠️",
        "Python code only ⚠️",
        "Runner.run_async() ⚠️",
        "Event iteration ✅",
        "Google Search only ⚠️",
        "Manual build ❌",
        "Manual build ❌",
        "MCPToolset ✅",
        "Manual build ❌",
        "Manual build ❌",
        "Sequential + Parallel + Loop ⚠️",
        "No ❌",
        "Manual build ❌",
        "Manual (GCP IAM) ⚠️",
        "None ❌",
        "Manual build ❌",
        "Manual build ❌",
        "Manual build ❌",
        "Custom connector ❌",
        "Custom connector ⚠️",
        "Custom connector ⚠️",
    ],
}

import pandas as pd

df = pd.DataFrame(matrix_data)
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=780,
)

st.markdown("---")

# ── Story Navigation ──────────────────────────────────────────────
st.markdown("### 📖 Explore the Story")
st.markdown("Navigate through each section using the sidebar to see **side-by-side code comparisons** for every part of the agent framework.")

story_cols = st.columns(3)
sections = [
    ("🏗️", "Agent Creation", "How agents are defined, configured, and invoked"),
    ("🔧", "Tool Integration", "Built-in tools, custom functions, MCP servers"),
    ("🧠", "Memory & State", "Conversation persistence, long-term memory, user profiles"),
    ("🔀", "Multi-Agent", "Orchestration patterns, graph workflows, human-in-the-loop"),
    ("🚀", "Deployment", "Containerisation, hosting, eval, prompt optimization"),
    ("🔗", "3rd Party", "Snowflake, BlueYonder, Fabric FabricIQ & WorkIQ"),
]

for i, (icon, title, desc) in enumerate(sections):
    with story_cols[i % 3]:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown("---")

# ── Live Demo Teaser ──────────────────────────────────────────────
st.markdown("### 🎯 Live Demo — MAF Conversational Agent")
st.info(
    "A live MAF chat agent is embedded in **Page 1: Agent Creation** — "
    "scroll down to try the Responses API v2 streaming experience. "
    "Configure your `.env` file with `FOUNDRY_PROJECT_ENDPOINT` and "
    "`FOUNDRY_MODEL_DEPLOYMENT_NAME` to connect to your Foundry project.",
    icon="💡",
)

st.markdown("---")
st.caption("Built with Streamlit • Microsoft Agent Framework v2 Responses API • March 2026")
