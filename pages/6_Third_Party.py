"""Page 6: 3rd Party Integration — Snowflake, BlueYonder, Fabric."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="6. 3rd Party Integration", page_icon="🔗", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🔗 Chapter 6: 3rd Party Integration</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Enterprise AI agents must connect to **real business systems** — "
    "Snowflake for data warehousing, BlueYonder for supply chain fulfillment, "
    "and Microsoft Fabric for analytics intelligence. "
    "The integration model makes a massive difference."
)
st.markdown("---")

# ── Architecture Overview ──────────────────────────────────────────
st.markdown("### Integration Architecture Overview")

col_maf, col_adk = st.columns(2)

with col_maf:
    st.markdown(
        '<span class="framework-label-maf">Microsoft Agent Framework</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        ```
        ┌─────────────────────────────────────┐
        │     MAF Agent (Azure AI Foundry)    │
        │     🔐 Managed Identity             │
        ├─────────────────────────────────────┤
        │                                     │
        │  ┌─────────┐  ┌─────────────────┐   │
        │  │   MCP   │  │  Function Tools │   │
        │  │ Server  │  │  (SDK-native)   │   │
        │  └────┬────┘  └───────┬─────────┘   │
        │       │               │             │
        └───────┼───────────────┼─────────────┘
                │               │
        ┌───────┴───┐   ┌──────┴──────┐
        │ Snowflake │   │ BlueYonder  │
        │ (SSO/AD)  │   │ (Token)     │
        └───────────┘   └─────────────┘
                │
        ┌───────┴───────────────────────┐
        │ Microsoft Fabric              │
        │ ├─ FabricIQ (AI Search index) │
        │ └─ WorkIQ (REST API)          │
        │ 🔐 Same Azure AD identity     │
        └───────────────────────────────┘
        ```

        **Key**: Single identity plane — Azure AD flows through
        all services. No separate credentials for each system.
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
        ┌─────────────────────────────────────┐
        │     ADK Agent (Cloud Run)           │
        │     ⚠️ Manual credentials            │
        ├─────────────────────────────────────┤
        │                                     │
        │  ┌─────────────────────────────┐    │
        │  │   Custom Function Tools     │    │
        │  │   (manual REST clients)     │    │
        │  └────────────┬────────────────┘    │
        │               │                     │
        └───────────────┼─────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ┌───────┴───┐ ┌─┴───────┐ ┌────┴──────┐
        │ Snowflake │ │BlueYonder│ │  Fabric   │
        │ ⚠️ User/  │ │⚠️ API    │ │⚠️ Client  │
        │  Password │ │  Key    │ │  Secret   │
        └───────────┘ └─────────┘ └───────────┘

        Each service requires separate credential
        management. No unified identity plane.
        ```
        """
    )

st.markdown("---")

# ── Section 1: Snowflake ────────────────────────────────────────────
render_comparison(
    section_title="6.1 — Snowflake Integration",
    maf_title="MCP + Function Tool + Azure AD SSO",
    maf_description=(
        "MAF offers **two integration paths** for Snowflake:\n\n"
        "1. **MCP Server** — Connect to a Snowflake MCP server for query execution, table listing, and schema inspection\n"
        "2. **Function Tool** — Direct Snowflake connector with **Azure AD SSO** (no passwords)\n\n"
        "Both use **Managed Identity** — zero credential management."
    ),
    maf_code=maf.INTEGRATION_SNOWFLAKE,
    adk_title="Custom Connector (Manual Credentials)",
    adk_description=(
        "ADK requires a **manual Snowflake connector** with traditional username/password authentication.\n\n"
        "⚠️ No managed identity\n"
        "⚠️ Credentials in environment variables\n"
        "⚠️ Manual credential rotation"
    ),
    adk_code=adk.INTEGRATION_SNOWFLAKE,
)

# ── Section 2: BlueYonder ──────────────────────────────────────────
render_comparison(
    section_title="6.2 — BlueYonder Integration",
    maf_title="Function Tool + Azure Key Vault",
    maf_description=(
        "Wrap BlueYonder REST APIs as `FunctionTool`s. "
        "API tokens can be stored in **Azure Key Vault** and rotated automatically. "
        "The agent can query order status, reschedule deliveries, and manage fulfillment."
    ),
    maf_code=maf.INTEGRATION_BLUEYONDER,
    adk_title="Custom REST Client (Static API Key)",
    adk_description=(
        "Similar REST integration pattern, but with **static API keys** in environment variables. "
        "No native Key Vault integration — manual credential rotation required."
    ),
    adk_code=adk.INTEGRATION_BLUEYONDER,
)

# ── Section 3: Microsoft Fabric ─────────────────────────────────────
render_comparison(
    section_title="6.3 — Microsoft Fabric (FabricIQ & WorkIQ)",
    maf_title="Native Azure Integration — Same Identity Plane",
    maf_description=(
        "MAF has a **native advantage** with Fabric:\n\n"
        "- **FabricIQ**: Index Fabric lakehouse data into Azure AI Search → agent queries it via built-in RAG tool\n"
        "- **WorkIQ**: Access workforce intelligence metrics via Fabric REST API with `DefaultAzureCredential`\n"
        "- **Same identity plane**: Azure AD → Fabric → AI Search → Agent — **one credential, all services**"
    ),
    maf_code=maf.INTEGRATION_FABRIC,
    adk_title="Custom Connectors (No Native Support)",
    adk_description=(
        "ADK has **no native Fabric integration**.\n\n"
        "❌ Must register Azure AD app manually\n"
        "❌ Client secrets in env vars (not managed identity)\n"
        "❌ No Azure AI Search for Fabric data\n"
        "❌ No FabricIQ native query support\n"
        "❌ No WorkIQ API integration\n"
        "❌ Separate auth flow for each Azure service"
    ),
    adk_code=adk.INTEGRATION_FABRIC,
)

# ── Integration Summary Table ──────────────────────────────────────
st.markdown("### 6.4 — Integration Summary")
st.markdown("---")

import pandas as pd

integration_data = {
    "Integration": [
        "Snowflake — Authentication",
        "Snowflake — Query Execution",
        "Snowflake — Schema Discovery",
        "BlueYonder — Order Status",
        "BlueYonder — Fulfillment Actions",
        "BlueYonder — Credential Mgmt",
        "Fabric FabricIQ — Lakehouse Query",
        "Fabric WorkIQ — Workforce Metrics",
        "Fabric — Authentication",
        "Cross-service Identity",
    ],
    "MAF Approach": [
        "Azure AD SSO / Managed Identity ✅",
        "MCP Server + Function Tool ✅",
        "MCP allowed_tools ✅",
        "Function Tool ✅",
        "Function Tool ✅",
        "Azure Key Vault ✅",
        "Azure AI Search (built-in RAG) ✅",
        "Fabric REST API + DefaultAzureCredential ✅",
        "DefaultAzureCredential (auto) ✅",
        "Single Azure AD identity ✅",
    ],
    "ADK Approach": [
        "Username/Password ⚠️",
        "Custom function tool ⚠️",
        "Manual SQL queries ⚠️",
        "Custom function tool ⚠️",
        "Custom function tool ⚠️",
        "Env vars (static) ⚠️",
        "Custom connector (no RAG) ❌",
        "Custom OAuth flow ❌",
        "Client secrets (manual) ⚠️",
        "Separate creds per service ❌",
    ],
}

df = pd.DataFrame(integration_data)
st.dataframe(df, use_container_width=True, hide_index=True, height=400)

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "3rd Party Integration",
    [
        "<strong>Azure AD SSO for Snowflake</strong> — No passwords; ADK uses traditional username/password",
        "<strong>MCP for Snowflake</strong> — Managed server connection with allowed_tools; ADK needs custom connector",
        "<strong>Azure Key Vault for BlueYonder</strong> — Auto-rotating API tokens; ADK uses static env vars",
        "<strong>Native Fabric integration</strong> — FabricIQ via Azure AI Search + WorkIQ via REST API; ADK has no Fabric support",
        "<strong>Single identity plane</strong> — One Azure AD credential for Snowflake, BlueYonder, Fabric, AI Search; ADK needs separate creds for every service",
    ],
)

st.markdown("---")

# ── Final Summary ──────────────────────────────────────────────────
st.markdown("### 🏁 The Bottom Line")
st.markdown(
    """
    <div class="advantage-banner">
        <h4>Why Microsoft Agent Framework for Enterprise Conversational AI?</h4>
        <ul>
            <li><strong>Unified Identity</strong> — Azure AD Managed Identity flows through every service (Snowflake, BlueYonder, Fabric, AI Search) with zero credential management</li>
            <li><strong>Native Fabric</strong> — FabricIQ and WorkIQ are first-class citizens in the Azure ecosystem; Google ADK has no Fabric story</li>
            <li><strong>Enterprise Tools</strong> — Built-in RAG, Code Interpreter, Bing, and MCP eliminate weeks of custom tool development</li>
            <li><strong>Production Platform</strong> — Evaluation, prompt optimization, dataset harvesting, and observability come built-in with Foundry</li>
            <li><strong>Graph Orchestration</strong> — Flexible, deterministic multi-agent workflows with human-in-the-loop; ADK limited to Sequential/Parallel</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)
