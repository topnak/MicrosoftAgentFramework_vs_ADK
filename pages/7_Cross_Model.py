"""Page 7: Cross-Model Usage — MAF with Gemini & ADK with Azure OpenAI/Foundry."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css

st.set_page_config(page_title="7. Cross-Model Usage", page_icon="🔄", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🔄 Cross-Model Usage — Mixing Frameworks & LLMs</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Both frameworks support **model-agnostic** usage. "
    "You can use MAF with Gemini or ADK with Azure OpenAI / Foundry models. "
    "This page shows the exact implementation patterns."
)
st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# SECTION 1: MAF with Gemini
# ──────────────────────────────────────────────────────────────────
st.markdown(
    '<h2 style="color:#4A90D9;">1. Microsoft Agent Framework + Gemini LLM</h2>',
    unsafe_allow_html=True,
)
st.markdown(
    "MAF does **not** have a dedicated Gemini provider package, but there are "
    "**three practical approaches** to use Gemini models with MAF — all code-only, "
    "no special configuration files needed beyond environment variables."
)

# ── Approach A ──
st.markdown("### Option A — Gemini via Azure AI Foundry (Recommended for Enterprise)")
st.markdown(
    "Azure AI Foundry **hosts Gemini models** in its Model Garden. "
    "Deploy a Gemini model in your Foundry project, then use the standard "
    "`FoundryChatClient` or `OpenAIChatCompletionClient` — zero code changes needed."
)

col_a1, col_a2 = st.columns(2)

with col_a1:
    st.markdown("**Python**")
    st.code(
        '''from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient, FoundryAgent

# Deploy "gemini-2.5-flash" in Foundry Model Garden first
client = FoundryChatClient(
    project_endpoint="https://ai-foundry-<resource>.services.ai.azure.com/",
    credential=DefaultAzureCredential(),
)

agent = FoundryAgent(
    client=client,
    model="gemini-2.5-flash",  # Foundry deployment name
    instructions="You are a helpful assistant powered by Gemini on Azure.",
)

response = await agent.run("Explain quantum computing briefly.")
print(response)''',
        language="python",
    )

with col_a2:
    st.markdown("**Why this approach?**")
    st.markdown(
        """
        - **Enterprise compliance** — Gemini runs inside your Azure tenant
        - **Managed Identity** — no API keys to manage
        - **Unified billing** — single Azure invoice
        - **Same MAF code** — just change the deployment name
        - **Data residency** — pick your Azure region
        """
    )
    st.info(
        "💡 **No code change required.** If you're already using MAF with Azure OpenAI, "
        "simply deploy a Gemini model in Foundry and point your agent at that deployment name.",
        icon="✅",
    )

# ── Approach B ──
st.markdown("### Option B — Gemini's OpenAI-Compatible Endpoint (Direct)")
st.markdown(
    "Google provides an **OpenAI-compatible endpoint** for Gemini. "
    "Since MAF's `OpenAIChatCompletionClient` accepts a custom base URL, "
    "you can point it directly at Google's Gemini API."
)

st.code(
    '''from openai import OpenAI
from agent_framework.openai import OpenAIChatCompletionClient

# Gemini exposes an OpenAI-compatible endpoint
client = OpenAI(
    api_key="GOOGLE_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

agent = OpenAIChatCompletionClient(client=client).as_agent(
    model="gemini-2.5-flash",
    instructions="You are a helpful assistant powered by Gemini.",
)

response = await agent.run("What are the benefits of multi-agent systems?")
print(response)''',
    language="python",
)

st.warning(
    "⚠️ **Data leaves Azure.** API calls go to Google's servers. "
    "Ensure compliance with your organization's data policies.",
    icon="⚠️",
)

# ── Approach C ──
st.markdown("### Option C — Gemma (Open-Source Gemini) via Ollama (Local)")
st.markdown(
    "Run **Gemma** (Google's open-source model from the Gemini family) "
    "locally with Ollama. MAF has a first-class `OllamaChatClient` provider."
)

st.code(
    '''from agent_framework.ollama import OllamaChatClient

# Run locally: ollama pull gemma3
client = OllamaChatClient(model="gemma3")

agent = client.as_agent(
    instructions="You are a helpful assistant powered by Gemma 3.",
)

response = await agent.run("Summarize the key features of Gemma.")
print(response)''',
    language="python",
)

st.success(
    "✅ **Fully offline.** No API calls, no data leaves your machine. "
    "Great for development, testing, and air-gapped environments.",
    icon="🔒",
)

# ── Summary Table ──
st.markdown("### MAF + Gemini — Approach Comparison")
st.markdown(
    """
    | Approach | Provider Package | Data Location | Auth | Best For |
    |----------|-----------------|---------------|------|----------|
    | **A. Foundry Model Garden** | `agent-framework-foundry` | Azure tenant | Managed Identity | Enterprise production |
    | **B. Gemini OpenAI endpoint** | `agent-framework-openai` | Google servers | API key | Quick prototyping |
    | **C. Gemma via Ollama** | `agent-framework-ollama` | Local machine | None | Offline / dev / testing |
    """
)

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# SECTION 2: ADK with Azure OpenAI / Foundry
# ──────────────────────────────────────────────────────────────────
st.markdown(
    '<h2 style="color:#34A853;">2. Google ADK + Azure OpenAI / Microsoft Foundry LLM</h2>',
    unsafe_allow_html=True,
)
st.markdown(
    "ADK provides a **LiteLLM model connector** that supports 100+ LLM providers, "
    "including Azure OpenAI and any OpenAI-compatible endpoint. "
    "This is the officially documented approach for using non-Google models with ADK."
)

# ── Approach A ──
st.markdown("### Option A — Azure OpenAI via LiteLLM (Recommended)")
st.markdown(
    "Use ADK's built-in `LiteLlm` wrapper with the `azure/` prefix. "
    "This is the most straightforward approach for Azure OpenAI deployments."
)

col_b1, col_b2 = st.columns(2)

with col_b1:
    st.markdown("**Setup**")
    st.code(
        '''pip install google-adk litellm''',
        language="bash",
    )
    st.code(
        '''# .env or export these
AZURE_API_KEY=your-azure-openai-key
AZURE_API_BASE=https://<resource>.openai.azure.com/
AZURE_API_VERSION=2024-12-01-preview''',
        language="bash",
    )

with col_b2:
    st.markdown("**Implementation**")
    st.code(
        '''from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Use azure/ prefix for Azure OpenAI deployments
agent = LlmAgent(
    model=LiteLlm(model="azure/gpt-4o"),  # deployment name
    name="azure_agent",
    instruction="You are a helpful assistant powered by Azure OpenAI.",
)''',
        language="python",
    )

# ── Approach B ──
st.markdown("### Option B — Microsoft Foundry Models via LiteLLM")
st.markdown(
    "Microsoft Foundry exposes models through an OpenAI-compatible endpoint. "
    "You can use ADK's LiteLLM connector with the `openai/` prefix pointing "
    "at your Foundry resource URL."
)

st.code(
    '''from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Foundry models expose an OpenAI-compatible API
agent = LlmAgent(
    model=LiteLlm(
        model="openai/gpt-4o",  # model deployed in Foundry
        api_base="https://ai-foundry-<resource>.services.ai.azure.com/openai/v1/",
        api_key="your-foundry-api-key",
    ),
    name="foundry_agent",
    instruction="You are a helpful assistant using Foundry-hosted models.",
)''',
    language="python",
)

# ── Approach C ──
st.markdown("### Option C — OpenAI Direct via LiteLLM")
st.markdown(
    "For comparison, here's the simpler OpenAI direct pattern — "
    "same `LiteLlm` wrapper, different prefix."
)

st.code(
    '''from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Requires OPENAI_API_KEY env var
agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="openai_agent",
    instruction="You are a helpful assistant powered by GPT-4o.",
)''',
    language="python",
)

# ── Runner Invocation ──
st.markdown("### Running the ADK Agent (same for all approaches)")
st.code(
    '''from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

runner = Runner(
    agent=agent,  # any of the agents defined above
    app_name="cross_model_app",
    session_service=InMemorySessionService(),
)

session = await runner.session_service.create_session(
    app_name="cross_model_app", user_id="user-1"
)

from google.genai import types
response = runner.run(
    user_id="user-1",
    session_id=session.id,
    new_message=types.Content(
        role="user",
        parts=[types.Part(text="Hello from ADK with Azure!")],
    ),
)

async for event in response:
    if event.content and event.content.parts:
        print(event.content.parts[0].text, end="")''',
    language="python",
)

# ── Summary Table ──
st.markdown("### ADK + Azure/Foundry — Approach Comparison")
st.markdown(
    """
    | Approach | LiteLLM Model String | Env Vars Needed | Best For |
    |----------|---------------------|-----------------|----------|
    | **A. Azure OpenAI** | `azure/<deployment>` | `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION` | Existing Azure OpenAI users |
    | **B. Foundry Models** | `openai/<model>` + custom base | Foundry API key | Foundry-hosted multi-vendor models |
    | **C. OpenAI Direct** | `openai/<model>` | `OPENAI_API_KEY` | Non-Azure OpenAI usage |
    """
)

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# SECTION 3: Key Takeaways
# ──────────────────────────────────────────────────────────────────
st.markdown("### 🔑 Key Takeaways")

col_k1, col_k2 = st.columns(2)

with col_k1:
    st.markdown(
        """
        <div class="maf-col">
        <h4 style="color:#4A90D9;">MAF Cross-Model Summary</h4>
        <ul>
        <li><strong>Multiple paths to Gemini:</strong> Foundry Model Garden, 
            OpenAI-compatible endpoint, or Gemma via Ollama</li>
        <li><strong>Enterprise recommended:</strong> Deploy Gemini in Foundry 
            for managed identity + compliance</li>
        <li><strong>Code change is minimal:</strong> Just swap the model 
            deployment name or client base URL</li>
        <li><strong>Provider extensibility:</strong> Custom <code>IChatClient</code> 
            or <code>BaseChatClient</code> for any model API</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_k2:
    st.markdown(
        """
        <div class="adk-col">
        <h4 style="color:#34A853;">ADK Cross-Model Summary</h4>
        <ul>
        <li><strong>LiteLLM is the bridge:</strong> Single integration point 
            for 100+ providers including Azure</li>
        <li><strong>Azure prefix <code>azure/</code>:</strong> Standard LiteLLM 
            pattern for Azure OpenAI deployments</li>
        <li><strong>Foundry access:</strong> Use OpenAI-compatible endpoint with 
            custom <code>api_base</code></li>
        <li><strong>Same ADK features:</strong> Tools, memory, multi-agent — all 
            work regardless of which LLM provider is used</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Architecture Diagram ──
st.markdown("### 🏗️ Cross-Framework Architecture")
st.code(
    """
┌──────────────────────────────────────────────────────────────────┐
│                       Your Application                           │
├──────────────────────────────┬───────────────────────────────────┤
│     MAF Agent Framework      │        Google ADK                 │
│                              │                                   │
│  ┌─────────────────────┐     │  ┌─────────────────────────┐     │
│  │  OpenAI Provider    │──┐  │  │  LiteLlm("azure/...")   │──┐  │
│  │  Foundry Provider   │  │  │  │  LiteLlm("openai/...")  │  │  │
│  │  Ollama Provider    │  │  │  │  Gemini (native)        │  │  │
│  │  Anthropic Provider │  │  │  │  Claude (native)        │  │  │
│  │  Custom IChatClient │  │  │  │  Ollama / vLLM          │  │  │
│  └─────────────────────┘  │  │  └─────────────────────────┘  │  │
│                           ▼  │                                ▼  │
├──────────────────────────────┴───────────────────────────────────┤
│                        LLM Providers                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │
│  │Azure AOAI│  │  Gemini  │  │  OpenAI  │  │Foundry Models│    │
│  │ / Foundry│  │  API     │  │  API     │  │ (multi-vendor)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │
└──────────────────────────────────────────────────────────────────┘
""",
    language="text",
)

st.markdown("---")
st.caption(
    "Both frameworks are model-agnostic at the core. "
    "The choice of LLM provider is an infrastructure decision, not a framework lock-in."
)
