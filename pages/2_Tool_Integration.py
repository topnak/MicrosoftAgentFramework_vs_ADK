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
    adk_title="Google Search + Code Execution",
    adk_description=(
        "ADK provides **Google Search Grounding** and **BuiltInCodeExecutor**.\n\n"
        "Also supports **OpenAPI tools** for REST API integration and\n"
        "**Vertex AI Search Grounding** for enterprise data.\n\n"
        "⚠️ No built-in Azure AI Search equivalent\n"
        "⚠️ No built-in Bing Grounding"
    ),
    adk_code=adk.TOOLS_CODE_EXEC,
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
    adk_title="Google Search + Vertex AI Search Grounding",
    adk_description=(
        "ADK provides **Google Search Grounding** built-in.\n"
        "For enterprise RAG, **Vertex AI Search Grounding** is available\n"
        "but requires Vertex AI setup (not a standalone tool like Azure AI Search)."
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
        "<strong>Azure AI Search RAG</strong> — One-line vector/semantic/hybrid search; ADK uses Vertex AI Search (more setup)",
        "<strong>Bing Grounding</strong> — Enterprise web search with citations; ADK has Google Search Grounding",
        "<strong>Multi-tool ToolSet</strong> — Compose built-in + custom + MCP tools freely",
        "<strong>MCP with allowed_tools</strong> — Fine-grained remote tool access control",
        "<strong>Code Interpreter sandbox</strong> — Managed sandbox; ADK has BuiltInCodeExecutor via Gemini API",
    ],
)

st.markdown("---")

# ── ADK Unique Features: Tools ─────────────────────────────────────
st.markdown("### 🌟 Features Unique to Google ADK — Tools & Integrations")

with st.expander("🔍 ADK-Only: OpenAPI Tools — Auto-generate tools from OpenAPI specs", expanded=False):
    st.markdown(
        """
        ADK can **automatically generate tools from OpenAPI/Swagger specifications**.
        Point it at any REST API spec and get callable tools instantly:

        ```python
        from google.adk.tools.openapi_tool import OpenAPIToolset

        # Auto-generate tools from an OpenAPI spec URL
        tools = OpenAPIToolset.from_url(
            "https://api.example.com/openapi.json"
        )

        agent = LlmAgent(
            name="api_agent",
            model="gemini-2.5-flash",
            tools=tools,
        )
        ```

        **Why this matters:** Any REST API with an OpenAPI spec becomes instantly usable
        as agent tools — no manual function wrapping needed.

        **MAF equivalent:** You'd use `FunctionTool` to wrap individual API calls manually,
        or use MCP for external service integration.
        """
    )

with st.expander("🔍 ADK-Only: Agent Skills — Reusable, context-window-efficient capabilities", expanded=False):
    st.markdown(
        """
        **Agent Skills** are pre-built or custom capabilities that work efficiently
        inside AI context window limits. Available at [agentskills.io](https://agentskills.io/).

        Skills differ from regular tools:
        - **Context-efficient** — Designed to minimize token usage
        - **Pre-packaged** — Ready-to-use capabilities for common tasks
        - **Composable** — Mix and match skills across agents

        ```python
        from google.adk.agents import LlmAgent

        agent = LlmAgent(
            name="skilled_agent",
            model="gemini-2.5-flash",
            skills=["web_browsing", "code_analysis"],
        )
        ```

        **MAF equivalent:** No direct equivalent — closest is using built-in tools
        or composing with MCP servers.
        """
    )

with st.expander("🔍 ADK-Only: Plugins — Pre-packaged third-party integrations", expanded=False):
    st.markdown(
        """
        ADK **Plugins** allow integrating complex, pre-packaged behaviors and
        third-party services directly into agent workflows:

        - Pre-built plugin marketplace
        - Third-party service integrations
        - Complex behavior packages

        **MAF equivalent:** Similar functionality via MCP servers and built-in tool
        definitions, but no formalized plugin system.
        """
    )

with st.expander("🔍 ADK-Only: Action Confirmations — Built-in tool execution approval", expanded=False):
    st.markdown(
        """
        ADK has built-in support for **action confirmations** before tool execution.
        This allows agents to ask for user approval before performing actions:

        ```python
        # Tools can require confirmation before execution
        # https://google.github.io/adk-docs/tools-custom/confirmation/
        ```

        This provides a safety net for destructive or irreversible operations.

        **MAF equivalent:** Human-in-the-loop checkpoints in graph workflows serve
        a similar purpose but at the orchestration level rather than tool level.
        """
    )
