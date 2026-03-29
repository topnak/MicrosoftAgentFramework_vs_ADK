"""Page 8: Microsoft Foundry vs Vertex AI — Platform Comparison."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css

st.set_page_config(page_title="8. Foundry vs Vertex AI", page_icon="☁️", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">☁️ Microsoft Foundry vs Google Vertex AI</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Both platforms are **unified AI development platforms** from their respective clouds. "
    "Here's what they are, how they differ, and when to choose one over the other."
)
st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# WHAT IS EACH
# ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="maf-col">
        <h3 style="color:#4A90D9;">Microsoft Foundry</h3>
        <p><em>Formerly: Azure AI Studio → Azure AI Foundry → Microsoft Foundry</em></p>
        <p>A unified <strong>Azure PaaS</strong> for enterprise AI operations,
        model deployment, agent building, and application development.</p>
        <ul>
        <li><strong>Portal:</strong> <a href="https://ai.azure.com" target="_blank">ai.azure.com</a></li>
        <li><strong>Cloud:</strong> Microsoft Azure</li>
        <li><strong>Agent API:</strong> OpenAI Responses protocol (Agents v2)</li>
        <li><strong>Resource Model:</strong> Foundry resource → Projects</li>
        <li><strong>SDKs:</strong> Python, C#, TypeScript (preview), Java (preview)</li>
        <li><strong>Agent Framework:</strong> Microsoft Agent Framework (MAF)</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="adk-col">
        <h3 style="color:#34A853;">Google Vertex AI</h3>
        <p><em>Also includes: Vertex AI Studio, Agent Builder, Agent Engine</em></p>
        <p>A unified, open <strong>Google Cloud platform</strong> for building,
        deploying, and scaling generative AI and machine learning models.</p>
        <ul>
        <li><strong>Portal:</strong> <a href="https://console.cloud.google.com/vertex-ai" target="_blank">console.cloud.google.com/vertex-ai</a></li>
        <li><strong>Cloud:</strong> Google Cloud Platform</li>
        <li><strong>Model Access:</strong> Model Garden (200+ models)</li>
        <li><strong>Resource Model:</strong> GCP project → resources</li>
        <li><strong>SDKs:</strong> Python, Node.js, Go, Java</li>
        <li><strong>Agent Framework:</strong> Agent Development Kit (ADK)</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# KEY CAPABILITIES COMPARISON
# ──────────────────────────────────────────────────────────────────
st.markdown("### 📊 Key Capabilities Comparison")

import pandas as pd

comparison = {
    "Capability": [
        "Platform Type",
        "Primary Models",
        "Model Catalog",
        "Third-Party Models",
        "Agent Building",
        "Agent Deployment",
        "Agent API",
        "Orchestration",
        "Tools / Integrations",
        "Memory / State",
        "Model Fine-Tuning",
        "Model Evaluation",
        "Responsible AI",
        "MLOps / Pipelines",
        "Notebooks",
        "Search / RAG",
        "Dev Portal / Studio",
        "CLI",
        "Observability",
        "Identity & Auth",
        "Enterprise Governance",
        "Pricing Model",
    ],
    "Microsoft Foundry": [
        "Unified Azure PaaS for AI",
        "GPT-4o, GPT-4.1, o3, o4-mini",
        "Foundry Model Garden (OpenAI, Anthropic, Mistral, Gemini, Llama, etc.)",
        "Claude, Gemini, Mistral, Llama, Cohere — via Foundry Models",
        "MAF SDK + Foundry Agents (server-side)",
        "Azure Functions, Container Apps, AKS, Foundry Agent Service",
        "OpenAI Responses protocol (conversations, items, responses)",
        "Graph-based workflows with checkpointing",
        "1,400+ tools via tool catalog + MCP + A2A",
        "Thread-based + Cosmos DB + Redis + Mem0",
        "SFT via Azure OpenAI + custom training",
        "Intent, Task Completion, Groundedness evals",
        "Content Safety, Prompt Shields, Groundedness Detection",
        "Azure ML Pipelines (separate but integrated)",
        "VS Code, Foundry extension",
        "Azure AI Search, Foundry IQ Knowledge Integration",
        "Foundry Portal (ai.azure.com)",
        "Azure CLI, az ai",
        "Application Insights, Azure Monitor, tracing/eval dashboard",
        "Azure AD / Entra ID, Managed Identity, RBAC",
        "Azure Policy, RBAC, network isolation, audit logs",
        "Pay-per-token/call, platform free to explore",
    ],
    "Google Vertex AI": [
        "Unified Google Cloud AI platform",
        "Gemini 3 Pro, Gemini 3 Flash, Gemini 2.5",
        "Model Garden (200+ models: Google, partners, open-source)",
        "Claude, Llama, Mistral — via Model Garden MaaS",
        "ADK + Agent Builder + Agent Engine (managed)",
        "Agent Engine (serverless), Cloud Run, GKE",
        "Gemini API (generateContent, streamGenerateContent)",
        "Sequential, Parallel, Loop + Graph (ADK 2.0)",
        "Google Search, Vertex AI Search, code execution + OpenAPI tools",
        "Session service + state + memory service + artifacts",
        "SFT, PEFT, RLHF via Vertex AI Training",
        "Gen AI Evaluation Service + ADK Eval Criteria + User Sim",
        "Model Armor, safety filters, responsible AI toolkit",
        "Vertex AI Pipelines (native, Kubeflow-based)",
        "Colab Enterprise, Vertex AI Workbench",
        "Vertex AI Search Grounding, Google Search Grounding",
        "Vertex AI Studio (console.cloud.google.com)",
        "gcloud CLI",
        "Cloud Logging, Cloud Monitoring, Cloud Trace",
        "GCP IAM, Workload Identity, service accounts",
        "Org policies, VPC-SC, audit logs, Model Armor",
        "Pay-per-token/call, varied by model",
    ],
}

df = pd.DataFrame(comparison)
st.dataframe(df, use_container_width=True, hide_index=True, height=820)

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# ARCHITECTURE COMPARISON
# ──────────────────────────────────────────────────────────────────
st.markdown("### 🏗️ Architecture Layers")

col_a1, col_a2 = st.columns(2)

with col_a1:
    st.markdown("**Microsoft Foundry Architecture**")
    st.code(
        """
┌─────────────────────────────────┐
│     Foundry Portal (ai.azure.com)│
├─────────────────────────────────┤
│  Agent Service (Responses API)  │
│  ┌────────────────────────────┐ │
│  │ Agents v2 (MAF-powered)   │ │
│  │ • Conversations & Items   │ │
│  │ • Tool Catalog (1400+)    │ │
│  │ • Foundry IQ Knowledge    │ │
│  │ • Memory & State          │ │
│  └────────────────────────────┘ │
├─────────────────────────────────┤
│  Foundry Models                 │
│  ┌────────────────────────────┐ │
│  │ OpenAI (GPT-4o, o3, o4)   │ │
│  │ Anthropic (Claude)        │ │
│  │ Google (Gemini)           │ │
│  │ Meta (Llama)              │ │
│  │ Mistral, Cohere, ...      │ │
│  └────────────────────────────┘ │
├─────────────────────────────────┤
│  Foundry Tools                  │
│  • AI Search  • Content Safety  │
│  • Speech     • Vision          │
│  • Document Intelligence       │
├─────────────────────────────────┤
│  Azure Infrastructure           │
│  • Entra ID  • Managed Identity │
│  • VNet      • Private Endpoints│
│  • Azure Policy • Monitor      │
└─────────────────────────────────┘
""",
        language="text",
    )

with col_a2:
    st.markdown("**Vertex AI Architecture**")
    st.code(
        """
┌─────────────────────────────────┐
│  Vertex AI Studio (Console)     │
├─────────────────────────────────┤
│  Agent Builder & Agent Engine   │
│  ┌────────────────────────────┐ │
│  │ ADK-powered Agents         │ │
│  │ • Tools & Grounding        │ │
│  │ • Sessions & Memory        │ │
│  │ • A2A Protocol             │ │
│  │ • Agent Identity (IAM)     │ │
│  └────────────────────────────┘ │
├─────────────────────────────────┤
│  Model Garden (200+ models)     │
│  ┌────────────────────────────┐ │
│  │ Google   (Gemini 3, Imagen)│ │
│  │ Anthropic (Claude)         │ │
│  │ Meta     (Llama)           │ │
│  │ Mistral, Open-source ...   │ │
│  └────────────────────────────┘ │
├─────────────────────────────────┤
│  Vertex AI Tools                │
│  • Search Grounding  • Eval    │
│  • Pipelines  • Feature Store  │
│  • Training   • Model Monitor │
│  • Notebooks  • Experiments   │
├─────────────────────────────────┤
│  GCP Infrastructure             │
│  • IAM      • Workload Identity│
│  • VPC-SC   • Private Google   │
│  • Org Policy • Cloud Audit   │
└─────────────────────────────────┘
""",
        language="text",
    )

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# EVOLUTION TIMELINE
# ──────────────────────────────────────────────────────────────────
st.markdown("### 📅 Platform Evolution")

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.markdown(
        """
        <div class="maf-col">
        <h4>Microsoft Foundry Evolution</h4>
        <ol>
        <li><strong>Azure AI Studio</strong> — Original portal for Azure AI services</li>
        <li><strong>Azure AI Foundry</strong> — Consolidated hub + Azure OpenAI + AI Services</li>
        <li><strong>Microsoft Foundry</strong> — Current: unified PaaS, single resource model,
            OpenAI Responses protocol, 1400+ tool catalog</li>
        </ol>
        <p><strong>Key shift:</strong> From multiple Azure AI packages and endpoints
        to a single <code>azure-ai-projects 2.x</code> client against one project endpoint.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_e2:
    st.markdown(
        """
        <div class="adk-col">
        <h4>Vertex AI Evolution</h4>
        <ol>
        <li><strong>Cloud AI Platform</strong> — Original ML training & prediction</li>
        <li><strong>Vertex AI</strong> — Unified ML + Gen AI platform with Model Garden</li>
        <li><strong>Vertex AI + Agent Builder</strong> — Current: ADK integration,
            Agent Engine (serverless), Gemini 3, 200+ models</li>
        </ol>
        <p><strong>Key shift:</strong> From ML-focused platform to full-stack
        generative AI and agentic development platform with ADK.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# WHEN TO CHOOSE
# ──────────────────────────────────────────────────────────────────
st.markdown("### 🎯 When to Choose Which")

col_w1, col_w2 = st.columns(2)

with col_w1:
    st.markdown(
        """
        <div class="maf-col">
        <h4>Choose Microsoft Foundry when:</h4>
        <ul>
        <li>Your organization is on <strong>Azure / M365</strong></li>
        <li>You need <strong>Managed Identity</strong> (Entra ID) across services</li>
        <li>You want <strong>GPT-4o / o3 / o4-mini</strong> as primary models</li>
        <li>You need <strong>Fabric / FabricIQ / WorkIQ</strong> integration</li>
        <li>You require <strong>Azure Policy</strong> governance and <strong>VNet</strong> isolation</li>
        <li>You want the <strong>OpenAI Responses protocol</strong> with server-side conversation management</li>
        <li>Your team uses <strong>.NET / C#</strong> primarily</li>
        <li>You need <strong>1,400+ enterprise tools</strong> from the tool catalog</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_w2:
    st.markdown(
        """
        <div class="adk-col">
        <h4>Choose Vertex AI when:</h4>
        <ul>
        <li>Your organization is on <strong>Google Cloud (GCP)</strong></li>
        <li>You want <strong>Gemini 3</strong> as the primary model</li>
        <li>You need <strong>BigQuery</strong> native integration for data + AI</li>
        <li>You want <strong>Agent Engine</strong> for serverless agent deployment</li>
        <li>You need <strong>200+ models</strong> from Model Garden MaaS</li>
        <li>You want <strong>ADK's multi-language support</strong> (Python, TS, Go, Java)</li>
        <li>You need <strong>Kubeflow-based pipelines</strong> for ML workflows</li>
        <li>You want <strong>Colab Enterprise</strong> for collaborative notebooks</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ──────────────────────────────────────────────────────────────────
# INTEROPERABILITY
# ──────────────────────────────────────────────────────────────────
st.markdown("### 🔗 Cross-Platform Interoperability")
st.markdown(
    "Both platforms are **not mutually exclusive**. Modern agent architectures "
    "can span both clouds using standard protocols."
)

st.markdown(
    """
    | Integration Point | How It Works |
    |-------------------|--------------|
    | **A2A Protocol** | Both MAF and ADK support A2A — agents on Azure can call agents on GCP and vice versa |
    | **MCP Servers** | Both frameworks consume MCP tool servers — host MCP on either cloud |
    | **Foundry models in ADK** | ADK uses LiteLLM to call Azure OpenAI / Foundry endpoints |
    | **Gemini in MAF** | MAF uses Foundry Model Garden or OpenAI-compatible Gemini endpoint |
    | **OpenAI compatibility** | Both Foundry and Vertex AI expose OpenAI-compatible APIs |
    """
)

st.info(
    "💡 **See Page 7 (Cross-Model Usage)** for implementation code showing "
    "how to use MAF with Gemini and ADK with Azure OpenAI.",
    icon="🔄",
)

st.markdown("---")
st.caption(
    "Microsoft Foundry (ai.azure.com) • Vertex AI (console.cloud.google.com/vertex-ai) • "
    "Both platforms are evolving rapidly — verify details against official docs."
)
