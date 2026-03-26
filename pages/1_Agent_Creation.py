"""Page 1: Agent Creation — How agents are defined, configured, and invoked."""

import sys
import pathlib

# Allow imports from project root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="1. Agent Creation", page_icon="🏗️", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🏗️ Chapter 1: Agent Creation</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "How do you **define, configure, and invoke** an AI agent? "
    "This is the foundation — and the two frameworks take very different approaches."
)
st.markdown("---")

# ── Section 1: Basic Agent Definition ───────────────────────────────
render_comparison(
    section_title="1.1 — Basic Agent Definition",
    maf_title="SDK + Declarative Config",
    maf_description=(
        "Create agents via the **AIProjectClient SDK** connected to Azure AI Foundry. "
        "The agent is a managed resource with a unique ID, linked to a model deployment."
    ),
    maf_code=maf.AGENT_CREATION_BASIC,
    adk_title="Python Code Only",
    adk_description=(
        "Define agents as Python objects with `Agent()` constructor. "
        "Uses Google's Gemini models by default, or LiteLLM for other providers."
    ),
    adk_code=adk.AGENT_CREATION_BASIC,
)

# ── Feature deep-dive: Agent Definition ─────────────────────────────
with st.expander("🔍 Deep Dive: Agent Definition — Feature Comparison", expanded=False):
    st.markdown("#### What makes agent definition matter?")
    st.markdown(
        "The agent definition determines **how your agent is created, versioned, and managed** "
        "throughout its lifecycle. The approach each framework takes has significant implications "
        "for enterprise teams."
    )

    feat_col1, feat_col2 = st.columns(2)
    with feat_col1:
        st.markdown(
            """
            <div class="maf-col">
            <h4 style="color:#4A90D9;">MAF: Managed Resource Model</h4>
            <p><strong>How it works:</strong> <code>create_agent()</code> registers the agent as a managed resource
            in Azure AI Foundry. The agent gets a unique ID, is associated with a model deployment,
            and its configuration is stored server-side.</p>

            <p><strong>Benefits:</strong></p>
            <ul>
            <li><strong>Lifecycle management</strong> — Create, update, delete agents via API. Track versions.</li>
            <li><strong>Model abstraction</strong> — Reference model deployments by name. Foundry handles routing,
            failover, and quota management across regions.</li>
            <li><strong>Credential isolation</strong> — <code>DefaultAzureCredential</code> means zero API keys
            in your code. Works locally (Azure CLI) and in production (Managed Identity).</li>
            <li><strong>Multi-language</strong> — Same pattern works in Python and .NET with identical behavior.</li>
            </ul>

            <p><strong>When to use:</strong> Enterprise production systems where agent versioning, auditing,
            and managed infrastructure matter.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with feat_col2:
        st.markdown(
            """
            <div class="adk-col">
            <h4 style="color:#34A853;">ADK: In-Process Object Model</h4>
            <p><strong>How it works:</strong> <code>Agent()</code> creates a Python object in your process.
            No server-side registration. The agent exists only while your code runs.</p>

            <p><strong>Benefits:</strong></p>
            <ul>
            <li><strong>Simplicity</strong> — No cloud setup needed. Agent runs in 10 lines of code.</li>
            <li><strong>Fast iteration</strong> — Change instructions, restart, test immediately.</li>
            <li><strong>LiteLLM routing</strong> — Use any model provider via LiteLLM prefix
            (e.g., <code>"litellm/gpt-4o"</code>).</li>
            </ul>

            <p><strong>Limitations:</strong></p>
            <ul>
            <li>No server-side agent management or versioning</li>
            <li>Python only — no .NET</li>
            <li>API keys required (no managed identity)</li>
            <li>No built-in model failover or region routing</li>
            </ul>

            <p><strong>When to use:</strong> Prototypes, research, or GCP-native environments where
            simplicity and speed of iteration are the priority.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("")

# ── Section 2: Declarative Agent Metadata ───────────────────────────
render_comparison(
    section_title="1.2 — Declarative Agent Metadata",
    maf_title="agent.yaml — Version-Controlled Config",
    maf_description=(
        "MAF provides `agent.yaml` — a **declarative, version-controlled** agent definition. "
        "Tools, model config, and instructions are all codified for CI/CD pipelines."
    ),
    maf_code=maf.AGENT_YAML,
    maf_lang="yaml",
    adk_title="No Declarative Format",
    adk_description=(
        "ADK has **no equivalent** to `agent.yaml`. Agent configuration lives entirely in Python code. "
        "No standardized metadata format for CI/CD or agent management."
    ),
    adk_code=adk.AGENT_NO_YAML,
)

# ── Feature deep-dive: agent.yaml ───────────────────────────────────
with st.expander("🔍 Deep Dive: Declarative Config — Why agent.yaml Matters", expanded=False):
    st.markdown(
        """
        #### The Problem `agent.yaml` Solves

        In enterprise environments, agent configurations need to be:
        - **Version-controlled** — Track changes in Git, review in PRs
        - **Environment-agnostic** — Same definition works in dev, staging, production
        - **CI/CD-friendly** — Automated deployment pipelines can read and deploy from config
        - **Auditable** — Who changed what, when, and why

        #### How `agent.yaml` Works

        | Field | Purpose | Example |
        |-------|---------|---------|
        | `name` | Unique agent identifier | `supply-chain-assistant` |
        | `version` | Semantic version for tracking | `1.2.0` |
        | `description` | Human-readable purpose | `Enterprise supply chain AI agent` |
        | `model.deployment` | Model to use | `gpt-4o` |
        | `model.parameters` | Temperature, top_p, etc. | `temperature: 0.1` |
        | `tools` | List of enabled tools | `query_snowflake`, `azure_ai_search:catalog` |
        | `environment` | Env vars (can reference secrets) | `{{secrets.SNOWFLAKE_ACCOUNT}}` |

        #### Benefits for Enterprise Teams

        1. **GitOps workflow** — Agent config lives in the same repo as code. PRs review both code and config changes.
        2. **No code changes for config updates** — Change model temperature, add a tool, or update instructions without touching Python/C# code.
        3. **Secret management** — `{{secrets.KEY}}` syntax integrates with Azure Key Vault. No plaintext secrets.
        4. **Deployment automation** — CI/CD pipelines can read `agent.yaml`, build the container, and deploy to Foundry automatically.

        #### ADK Equivalent: None

        In ADK, all configuration is embedded in Python code. To change a model parameter, you modify source code.
        To track agent versions, you rely on Git commit history alone. There's no standardized metadata format
        that CI/CD tools can parse.
        """
    )

st.markdown("")

# ── Section 3: Agent Invocation ─────────────────────────────────────
render_comparison(
    section_title="1.3 — Agent Invocation & Streaming",
    maf_title="OpenAI Responses API v2 (Streaming)",
    maf_description=(
        "Invoke agents via the **OpenAI Responses API** — the industry-standard protocol. "
        "Built-in SSE streaming with typed events for text deltas, tool calls, and citations."
    ),
    maf_code=maf.AGENT_STREAMING,
    adk_title="Runner-based Event Iteration",
    adk_description=(
        "ADK uses a custom `Runner.run_async()` pattern with async event iteration. "
        "Not compatible with OpenAI API ecosystem or third-party client libraries."
    ),
    adk_code=adk.AGENT_INVOKE,
)

# ── Feature deep-dive: Responses API v2 ─────────────────────────────
with st.expander("🔍 Deep Dive: Responses API v2 — The Industry Standard", expanded=False):
    st.markdown(
        """
        #### Why the Invocation Protocol Matters

        The invocation API determines **how your application talks to the agent**. It affects:
        - Which client libraries you can use
        - How streaming works in your UI
        - Whether third-party observability tools can intercept and analyze calls
        - How easy it is for developers to adopt

        #### MAF: OpenAI Responses API v2

        | Feature | Detail |
        |---------|--------|
        | **Protocol** | HTTP POST with SSE (Server-Sent Events) streaming |
        | **Endpoint** | `POST /responses` — same as OpenAI's API |
        | **Client** | Any OpenAI-compatible SDK (`openai` Python, TypeScript, etc.) |
        | **Events** | `response.output_text.delta` (text), `response.tool_call` (tools), `response.output_item.done` (citations) |
        | **Compatibility** | Works with LangSmith, Braintrust, Humanloop, and any OpenAI-compatible tool |

        **How to use:**
        ```python
        # Same client you'd use for OpenAI directly
        openai_client = project.get_openai_client()

        # Stream with standard SSE events
        stream = openai_client.responses.create(
            model="gpt-4o",
            input="Your question",
            stream=True,
            extra_body={"agent": {"name": "my-agent", "type": "agent_reference"}}
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                # Real-time text streaming
                print(event.delta, end="")
        ```

        #### ADK: Runner.run_async()

        | Feature | Detail |
        |---------|--------|
        | **Protocol** | Python async generator (in-process) |
        | **No HTTP standard** | Must build your own HTTP server for remote access |
        | **Client** | ADK-specific — no third-party compatibility |
        | **Events** | Custom event objects with `content.parts` |
        | **Compatibility** | ADK-only — no external tool integration |

        #### Practical Impact

        - **Frontend integration**: MAF streaming works with any SSE client (React, Vue, plain JS).
          ADK requires a custom WebSocket/HTTP bridge.
        - **Observability**: OpenAI-compatible tools (LangSmith, etc.) can trace MAF calls natively.
          ADK calls need custom instrumentation.
        - **Developer onboarding**: Developers who know OpenAI API can use MAF immediately.
          ADK requires learning a new API.
        """
    )

st.markdown("")

# ── Feature Comparison Table ────────────────────────────────────────
st.markdown("### 1.4 — Agent Creation Feature Summary")
st.markdown("---")

import pandas as pd

features = {
    "Feature": [
        "Agent as managed resource",
        "Declarative config (agent.yaml)",
        "Multi-language (Python + .NET)",
        "OpenAI-compatible API",
        "SSE streaming with typed events",
        "Model failover / region routing",
        "Managed Identity auth",
        "Agent versioning",
        "Hosting adapter pattern",
        "Time to first agent",
    ],
    "MAF": [
        "✅ Server-side with unique ID",
        "✅ Version-controlled YAML",
        "✅ Python & .NET first-class",
        "✅ Responses API v2",
        "✅ text.delta, tool_call, citations",
        "✅ Foundry intelligent routing",
        "✅ DefaultAzureCredential",
        "✅ agent.yaml version field",
        "✅ Framework-agnostic adapter",
        "~30 min (with Foundry setup)",
    ],
    "ADK": [
        "❌ In-process Python object",
        "❌ None",
        "❌ Python only",
        "❌ Proprietary runner",
        "⚠️ Custom event iteration",
        "❌ Manual",
        "❌ API keys required",
        "❌ Git only",
        "❌ Manual server setup",
        "~5 min (API key + code)",
    ],
    "Why It Matters": [
        "Lifecycle management, auditing, team collaboration",
        "CI/CD pipelines, GitOps, environment-agnostic deploys",
        "Enterprise teams often use both Python and .NET",
        "Ecosystem compatibility, frontend integration ease",
        "Real-time UX, tool call visibility, source citations",
        "High availability, cost optimization across regions",
        "Zero credentials in code — compliance requirement",
        "Track changes, rollback, A/B test agent versions",
        "Same code runs locally and in Foundry containers",
        "Tradeoff: setup investment vs production readiness",
    ],
}

df = pd.DataFrame(features)
st.dataframe(df, use_container_width=True, hide_index=True, height=420)

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Agent Creation",
    [
        "<strong>Python & .NET</strong> — First-class support for both languages; ADK is Python-only",
        "<strong>agent.yaml</strong> — Declarative, version-controlled agent metadata for CI/CD",
        "<strong>OpenAI Responses API v2</strong> — Industry-standard protocol; ADK uses proprietary runner",
        "<strong>Managed resource</strong> — Agents are Foundry resources with IDs, versioning, and lifecycle management",
        "<strong>Hosting adapter</strong> — One codebase works locally and in Foundry containers",
    ],
)

st.markdown("---")

# ── Live Demo ───────────────────────────────────────────────────────
st.markdown("## 🎯 Try It — Live MAF Agent Demo")
st.markdown(
    "See the **Responses API v2 streaming** in action. "
    "This demo connects to a MAF agent in Azure AI Foundry."
)

from live_demo.maf_chat import render_live_demo

render_live_demo()
