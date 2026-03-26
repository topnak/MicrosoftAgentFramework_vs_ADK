"""Page 0: What Is MAF vs ADK — Architecture layers and framework overview."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css

st.set_page_config(page_title="0. What Is MAF vs ADK", page_icon="📚", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">📚 What Is Microsoft Agent Framework vs Google ADK?</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Before comparing features, let's understand **what each framework is**, "
    "how they're structured, and the architectural layers they provide."
)
st.markdown("---")

# ── Overview ────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h3 style="color:#4A90D9;">Microsoft Agent Framework (MAF)</h3>
        <p>A comprehensive <strong>multi-language framework</strong> for building,
        orchestrating, and deploying AI agents with support for both
        <strong>Python and .NET</strong>.</p>
        <p>Originally evolved from <strong>Semantic Kernel</strong> and <strong>AutoGen</strong>,
        MAF provides everything from simple chat agents to complex
        multi-agent workflows with graph-based orchestration.</p>
        <ul>
        <li><strong>Package:</strong> <code>pip install agent-framework</code></li>
        <li><strong>Languages:</strong> Python & .NET (C#)</li>
        <li><strong>API Baseline:</strong> OpenAI Responses API v2</li>
        <li><strong>Cloud:</strong> Azure AI Foundry</li>
        <li><strong>Stars:</strong> 8.2k+ GitHub</li>
        <li><strong>Latest:</strong> python-1.0.0rc5</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h3 style="color:#34A853;">Google Agent Development Kit (ADK)</h3>
        <p>A flexible and modular framework for developing and deploying AI agents.
        While optimized for <strong>Gemini and the Google ecosystem</strong>,
        ADK is model-agnostic and deployment-agnostic.</p>
        <p>Designed to make agent development feel more like
        <strong>software development</strong>, ADK supports agents ranging from
        simple tasks to complex workflows.</p>
        <ul>
        <li><strong>Package:</strong> <code>pip install google-adk</code></li>
        <li><strong>Languages:</strong> Python, TypeScript, Go, Java</li>
        <li><strong>API Baseline:</strong> Runner + Event pattern</li>
        <li><strong>Cloud:</strong> Vertex AI / Cloud Run / GKE</li>
        <li><strong>SDK repos:</strong> adk-python, adk-js, adk-go, adk-java</li>
        <li><strong>Latest:</strong> ADK 2.0 Alpha (graph workflows)</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Architecture Layers ────────────────────────────────────────────
st.markdown("## 🏛️ Architecture Layers — Side by Side")
st.markdown(
    "Each framework is organized into distinct architectural layers. "
    "Understanding these layers helps you see where each framework invests its capabilities."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h4 style="color:#4A90D9;">MAF Architecture — 7 Layers</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(
        """
┌─────────────────────────────────────────┐
│  Layer 7: DEPLOYMENT & HOSTING          │
│  Azure AI Foundry · Containers · DevUI  │
│  CI/CD · agent.yaml · Hosting Adapter   │
├─────────────────────────────────────────┤
│  Layer 6: EVALUATION & OPTIMIZATION     │
│  Built-in Evaluators · Prompt Optimizer │
│  Dataset Harvesting · A/B Testing       │
├─────────────────────────────────────────┤
│  Layer 5: ORCHESTRATION                 │
│  Graph Workflows · Checkpointing        │
│  Human-in-the-Loop · Time-travel        │
│  Fan-out/Fan-in · Durable Tasks         │
├─────────────────────────────────────────┤
│  Layer 4: MEMORY & STATE                │
│  Thread Persistence · Long-term Memory  │
│  User Profiles · Azure Cosmos DB        │
│  Redis · Mem0 Integration               │
├─────────────────────────────────────────┤
│  Layer 3: TOOLS & INTEGRATIONS          │
│  Function Tools · MCP · AI Search       │
│  Code Interpreter · Web Search          │
│  Bing Grounding · File Search           │
├─────────────────────────────────────────┤
│  Layer 2: AGENT CORE                    │
│  AzureOpenAIResponsesClient · .as_agent │
│  Responses API v2 · Streaming           │
│  Middleware · OpenTelemetry              │
├─────────────────────────────────────────┤
│  Layer 1: PROVIDERS                     │
│  OpenAI · Azure OpenAI · Anthropic      │
│  Bedrock · Ollama · Foundry Local       │
│  Claude · Copilot Studio · GitHub       │
└─────────────────────────────────────────┘
        """,
        language="text",
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h4 style="color:#34A853;">ADK Architecture — 7 Layers</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(
        """
┌─────────────────────────────────────────┐
│  Layer 7: DEPLOYMENT                    │
│  Vertex AI Agent Engine · Cloud Run     │
│  GKE · Docker · Agent Starter Pack      │
│  CLI (adk web / adk api_server)         │
├─────────────────────────────────────────┤
│  Layer 6: EVALUATION & SAFETY           │
│  Built-in Eval Criteria · User Sim      │
│  Safety & Security Patterns             │
│  Observability & Logging                │
├─────────────────────────────────────────┤
│  Layer 5: ORCHESTRATION                 │
│  SequentialAgent · ParallelAgent        │
│  LoopAgent · LLM-driven Transfer       │
│  ADK 2.0: Graph-based Workflows        │
├─────────────────────────────────────────┤
│  Layer 4: SESSIONS & MEMORY             │
│  Session Service · State Management     │
│  Memory Service · Artifacts             │
│  Context Caching · Context Compression  │
│  Session Rewind · Session Migration     │
├─────────────────────────────────────────┤
│  Layer 3: TOOLS & INTEGRATIONS          │
│  Function Tools · MCP · OpenAPI Tools   │
│  Google Search · Code Execution         │
│  Agent Skills · Plugins · A2A Protocol  │
│  Grounding (Search · Vertex AI Search)  │
├─────────────────────────────────────────┤
│  Layer 2: AGENT CORE                    │
│  LlmAgent (Agent) · BaseAgent          │
│  Runner · Callbacks · Planners          │
│  Events · Gemini Live API Streaming     │
├─────────────────────────────────────────┤
│  Layer 1: MODELS                        │
│  Gemini · Claude · Vertex AI-hosted     │
│  Ollama · vLLM · LiteLLM · LiteRT-LM   │
│  Apigee AI Gateway                     │
└─────────────────────────────────────────┘
        """,
        language="text",
    )

st.markdown("---")

# ── Layer-by-layer comparison ──────────────────────────────────────
st.markdown("## 📋 Layer-by-Layer Comparison")

import pandas as pd

layer_comparison = {
    "Layer": [
        "7 — Deployment",
        "6 — Evaluation",
        "5 — Orchestration",
        "4 — Memory & State",
        "3 — Tools",
        "2 — Agent Core",
        "1 — Model Providers",
    ],
    "MAF Approach": [
        "Azure AI Foundry managed hosting, agent.yaml declarative config, DevUI for debugging",
        "Built-in evaluators (intent, task, groundedness), prompt optimizer from traces",
        "Graph workflows with checkpointing, human-in-the-loop, time-travel, durable tasks",
        "Thread persistence, long-term memory, user profiles, Azure Cosmos DB, Redis, Mem0",
        "Function tools, MCP, AI Search, Code Interpreter, Web Search, Bing Grounding",
        "AzureOpenAIResponsesClient.as_agent(), Responses API v2, middleware, OpenTelemetry",
        "OpenAI, Azure OpenAI, Anthropic, Bedrock, Ollama, Claude, Foundry Local, Copilot Studio",
    ],
    "ADK Approach": [
        "Vertex AI Agent Engine, Cloud Run, GKE, Docker, CLI tools (adk web/api_server)",
        "Built-in eval criteria, user simulation, safety patterns, observability/logging",
        "SequentialAgent, ParallelAgent, LoopAgent, LLM transfer, ADK 2.0 graph workflows",
        "SessionService, state dict, memory service, artifacts, context caching/compression, session rewind",
        "Function tools, MCP, OpenAPI tools, Google Search, code execution, skills, plugins, A2A",
        "LlmAgent/Agent, BaseAgent, Runner, callbacks, planners, events, Gemini Live streaming",
        "Gemini, Claude, Vertex AI, Ollama, vLLM, LiteLLM, LiteRT-LM, Apigee AI Gateway",
    ],
    "Key Difference": [
        "MAF: Azure-native managed hosting; ADK: GCP-native with more flexible self-hosting",
        "Both have built-in eval; MAF adds prompt optimization from production traces",
        "MAF: Graph-first from day one; ADK: Workflow agents + graph in 2.0",
        "MAF: Managed persistence via Cosmos DB; ADK: Flexible with manual session services",
        "MAF: Enterprise-ready built-in tools; ADK: Broader plugin/skills ecosystem",
        "MAF: OpenAI API compatibility; ADK: Custom runner with rich callback system",
        "Similar breadth; MAF deeper on Azure ecosystem, ADK deeper on Google ecosystem",
    ],
}

df_layers = pd.DataFrame(layer_comparison)
st.dataframe(df_layers, use_container_width=True, hide_index=True, height=320)

st.markdown("---")

# ── Python Packages ────────────────────────────────────────────────
st.markdown("## 📦 Package Ecosystem")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h4 style="color:#4A90D9;">MAF Python Packages</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        | Package | Purpose |
        |---------|---------|
        | `agent-framework` | Meta-package (installs all) |
        | `agent-framework-core` | Base classes, interfaces |
        | `agent-framework-openai` | OpenAI/Azure OpenAI provider |
        | `agent-framework-azure-ai` | Azure AI Foundry integration |
        | `agent-framework-anthropic` | Anthropic Claude provider |
        | `agent-framework-bedrock` | AWS Bedrock provider |
        | `agent-framework-ollama` | Ollama local models |
        | `agent-framework-orchestrations` | Graph-based workflows |
        | `agent-framework-durabletask` | Durable task orchestration |
        | `agent-framework-declarative` | agent.yaml parsing |
        | `agent-framework-devui` | Interactive dev UI |
        | `agent-framework-azure-ai-search` | AI Search integration |
        | `agent-framework-azure-cosmos` | Cosmos DB persistence |
        | `agent-framework-redis` | Redis state/memory |
        | `agent-framework-mem0` | Mem0 memory integration |
        | `agent-framework-a2a` | Agent-to-Agent protocol |
        | `agent-framework-foundry` | Foundry deployment |
        | `agent-framework-lab` | Experimental features |
        """
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h4 style="color:#34A853;">ADK SDKs</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        | Package/Repo | Purpose |
        |---------|---------|
        | `google-adk` (Python) | Main Python SDK |
        | `adk-js` (TypeScript) | TypeScript SDK |
        | `adk-go` (Go) | Go SDK |
        | `adk-java` (Java) | Java SDK |

        **Python modules include:**
        | Module | Purpose |
        |--------|---------|
        | `google.adk.agents` | LlmAgent, workflow agents |
        | `google.adk.runners` | Runner execution engine |
        | `google.adk.sessions` | Session/state management |
        | `google.adk.tools` | Tool definitions |
        | `google.adk.planners` | BuiltInPlanner, PlanReAct |
        | `google.adk.callbacks` | Lifecycle hooks |
        | `google.adk.artifacts` | File/binary management |
        | `google.adk.code_executors` | Code execution |
        | `google.adk.flows` | Internal flow control |
        """
    )

st.markdown("---")

# ── Core Philosophy ────────────────────────────────────────────────
st.markdown("## 🎯 Design Philosophy")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h4 style="color:#4A90D9;">MAF: Enterprise-First</h4>
        <ol>
        <li><strong>Managed resources</strong> — Agents are cloud resources with IDs, versioning, lifecycle management</li>
        <li><strong>OpenAI API compatible</strong> — Uses Responses API v2, works with any OpenAI-compatible client</li>
        <li><strong>Azure-native security</strong> — Managed Identity, RBAC, Key Vault, private networking</li>
        <li><strong>Multi-language</strong> — Same patterns in Python and .NET</li>
        <li><strong>Declarative config</strong> — agent.yaml for GitOps workflows</li>
        <li><strong>Production-grade</strong> — Eval, prompt optimization, observability built-in</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h4 style="color:#34A853;">ADK: Developer-First</h4>
        <ol>
        <li><strong>Code-native</strong> — Define agents as code objects, feel like software development</li>
        <li><strong>Multi-language SDKs</strong> — Python, TypeScript, Go, Java (4 languages)</li>
        <li><strong>Model-agnostic</strong> — Optimized for Gemini but works with Claude, Ollama, vLLM, etc.</li>
        <li><strong>Rich extensibility</strong> — Callbacks, plugins, skills, custom agents via BaseAgent</li>
        <li><strong>Built-in dev tools</strong> — adk web UI, CLI, event inspection</li>
        <li><strong>Open protocols</strong> — MCP and A2A for cross-framework interoperability</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Quickstart Code ────────────────────────────────────────────────
st.markdown("## ⚡ Hello World — Side by Side")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        '<span class="framework-label-maf">Microsoft Agent Framework</span>',
        unsafe_allow_html=True,
    )
    st.code(
        """\
# pip install agent-framework --pre
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
import asyncio

async def main():
    agent = AzureOpenAIResponsesClient(
        credential=AzureCliCredential(),
    ).as_agent(
        name="HaikuBot",
        instructions="You write beautiful haikus.",
    )
    print(await agent.run("Write a haiku about AI agents."))

asyncio.run(main())
""",
        language="python",
    )

with col2:
    st.markdown(
        '<span class="framework-label-adk">Google ADK</span>',
        unsafe_allow_html=True,
    )
    st.code(
        """\
# pip install google-adk
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

async def main():
    agent = LlmAgent(
        name="haiku_bot",
        model="gemini-2.5-flash",
        instruction="You write beautiful haikus.",
    )
    runner = Runner(
        agent=agent, app_name="haiku_app",
        session_service=InMemorySessionService(),
    )
    content = types.Content(
        role="user",
        parts=[types.Part(text="Write a haiku about AI agents.")],
    )
    async for event in runner.run_async(
        user_id="u1", session_id="s1", new_message=content
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)

asyncio.run(main())
""",
        language="python",
    )

st.info(
    "**Key takeaway:** MAF is more concise (managed resources, simpler API surface) "
    "while ADK requires explicit Runner and Session setup but gives you more control "
    "over the execution lifecycle."
)

st.markdown("---")
st.markdown(
    "**Next:** Navigate to **Chapter 1: Agent Creation** to see detailed "
    "side-by-side comparisons of how agents are defined, configured, and invoked →"
)
