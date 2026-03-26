"""Page 2: Tool Integration — Built-in tools, custom functions, MCP."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="2. Tool Integration", page_icon="🔧", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🔧 Chapter 2: Tool Integration</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Tools extend what an agent can **do** — from querying databases to searching the web. "
    "The breadth of built-in tools is a major differentiator."
)
st.markdown("---")

# ── Section 1: Function Tools ───────────────────────────────────────
render_comparison(
    section_title="2.1 — Custom Function Tools",
    maf_title="FunctionTool with Type Safety",
    maf_description=(
        "Wrap any Python function as a `FunctionTool`. Schema is auto-generated from "
        "type hints and docstrings. Supports `strict=True` for input validation."
    ),
    maf_code=maf.TOOLS_FUNCTION,
    adk_title="Functions as Tools",
    adk_description=(
        "ADK also supports function-based tools with automatic schema generation. "
        "Similar pattern, but return type must be `dict`."
    ),
    adk_code=adk.TOOLS_FUNCTION,
)

# ── Section 2: Built-in Enterprise Tools ────────────────────────────
render_comparison(
    section_title="2.2 — Built-in Enterprise Tools",
    maf_title="Azure AI Search, Bing, Code Interpreter, Web Search",
    maf_description=(
        "MAF provides **4+ built-in tools** out-of-the-box:\n"
        "- **WebSearchPreview** — Free web search, no setup\n"
        "- **CodeInterpreter** — Sandboxed Python execution\n"
        "- **Azure AI Search** — Enterprise RAG with vector search\n"
        "- **Bing Grounding** — Enterprise web search\n\n"
        "Compose them freely with `ToolSet`."
    ),
    maf_code=maf.TOOLS_BUILTIN,
    adk_title="Google Search Only",
    adk_description=(
        "ADK provides only **Google Search** as a built-in tool.\n\n"
        "❌ No built-in RAG/vector search\n"
        "❌ No built-in code interpreter\n"
        "❌ No built-in file search\n\n"
        "All enterprise tools must be **built manually**."
    ),
    adk_code=adk.TOOLS_NO_BUILTIN,
)

# ── Section 3: Azure AI Search (RAG) ───────────────────────────────
render_comparison(
    section_title="2.3 — RAG / Vector Search",
    maf_title="Azure AI Search — Built-in RAG",
    maf_description=(
        "One-line RAG integration with `AzureAISearchToolDefinition`. "
        "Supports vector, semantic, and hybrid search modes. "
        "Agent automatically generates search queries and cites sources."
    ),
    maf_code=maf.TOOLS_AI_SEARCH,
    adk_title="Manual RAG Implementation",
    adk_description=(
        "ADK has **no built-in RAG tool**. You must:\n"
        "1. Generate embeddings manually\n"
        "2. Set up and query a vector database\n"
        "3. Build retrieval logic\n"
        "4. Handle citation formatting"
    ),
    adk_code=adk.TOOLS_SEARCH,
)

# ── Section 4: MCP Integration ─────────────────────────────────────
render_comparison(
    section_title="2.4 — MCP (Model Context Protocol) Tools",
    maf_title="Native MCP with Allowed-Tools Control",
    maf_description=(
        "Connect to **any MCP server** with `McpToolDefinition`. "
        "Specify `allowed_tools` to control which remote tools the agent can access. "
        "Ideal for Snowflake, BlueYonder, or any custom API."
    ),
    maf_code=maf.TOOLS_MCP,
    adk_title="MCPToolset (Cleanup Required)",
    adk_description=(
        "ADK supports MCP via `MCPToolset.from_server()`. "
        "Requires manual lifecycle management — you must call `await cleanup()` yourself."
    ),
    adk_code=adk.TOOLS_MCP,
)

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Tool Integration",
    [
        "<strong>4+ built-in enterprise tools</strong> — AI Search, Bing, Code Interpreter, Web Search; ADK has only Google Search",
        "<strong>Azure AI Search RAG</strong> — One-line vector/semantic/hybrid search; ADK requires manual RAG pipeline",
        "<strong>Multi-tool ToolSet</strong> — Compose built-in + custom + MCP tools freely",
        "<strong>MCP with allowed_tools</strong> — Fine-grained remote tool access control",
        "<strong>Code Interpreter sandbox</strong> — Secure Python execution for data analysis; ADK has none",
    ],
)
