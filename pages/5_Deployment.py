"""Page 5: Deployment & Production — Containers, eval, prompt optimization."""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st
from components.page_setup import inject_css
from components.side_by_side import render_comparison
from components.advantage_banner import render_advantage
from content import snippets_maf as maf
from content import snippets_adk as adk

st.set_page_config(page_title="5. Deployment", page_icon="🚀", layout="wide")
inject_css()

# ── Header ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 class="section-header">🚀 Chapter 5: Deployment & Production</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "Getting from prototype to production requires **containerization, hosting, monitoring, "
    "evaluation, and continuous improvement**. This is where enterprise frameworks prove their value."
)
st.markdown("---")

# ── Section 1: Containerization ─────────────────────────────────────
render_comparison(
    section_title="5.1 — Containerization & Hosting",
    maf_title="Foundry Hosting Adapter (Port 8088)",
    maf_description=(
        "MAF provides a **hosting adapter** that wraps your agent into a Foundry-compatible container. "
        "Standard Dockerfile pattern, standard port (8088), standard `/responses` endpoint. "
        "The adapter handles protocol translation automatically."
    ),
    maf_code=maf.DEPLOY_DOCKERFILE,
    maf_lang="dockerfile",
    adk_title="Manual Server Setup",
    adk_description=(
        "ADK requires you to set up your own HTTP server or use the `adk api_server` CLI. "
        "No standard hosting adapter — you manage the server lifecycle."
    ),
    adk_code=adk.DEPLOY_DOCKERFILE,
    adk_lang="dockerfile",
)

# ── Section 2: Agent Metadata & Deployment ──────────────────────────
render_comparison(
    section_title="5.2 — Agent Metadata & Cloud Deployment",
    maf_title="agent.yaml + Foundry CLI Deployment",
    maf_description=(
        "Deploy with a single `az ai foundry agent create` command. "
        "The `agent.yaml` captures all metadata for version control. "
        "**Production features come automatically**: Managed Identity, RBAC, App Insights, auto-scaling."
    ),
    maf_code=maf.DEPLOY_FOUNDRY,
    maf_lang="bash",
    adk_title="ADK CLI + Cloud Run/Vertex AI",
    adk_description=(
        "ADK provides built-in CLI tools and multiple deployment options:\n"
        "- **Vertex AI Agent Engine** (managed hosting)\n"
        "- **Cloud Run** (serverless containers)\n"
        "- **GKE** (Kubernetes)\n"
        "- **Agent Starter Pack** (templates)"
    ),
    adk_code=adk.DEPLOY_CLOUD_RUN,
    adk_lang="bash",
)

# ── Section 3: Evaluation & Optimization ────────────────────────────
render_comparison(
    section_title="5.3 — Evaluation & Prompt Optimization",
    maf_title="Built-in Eval + Prompt Optimizer",
    maf_description=(
        "MAF includes a **complete evaluation framework**:\n\n"
        "- **Built-in evaluators**: Intent resolution, task adherence, tool accuracy, groundedness\n"
        "- **Prompt optimization**: Automatically improve instructions from production traces\n"
        "- **Dataset harvesting**: Curate test datasets from real user interactions\n"
        "- **A/B testing**: Compare agent versions with quality metrics"
    ),
    maf_code=maf.DEPLOY_EVAL,
    adk_title="Built-in Eval Criteria + User Sim",
    adk_description=(
        "ADK has **built-in evaluation** with:\n\n"
        "- **Eval criteria** for response quality and tool trajectories\n"
        "- **User simulation** for multi-turn testing\n"
        "- **CLI support**: `adk eval` and Dev UI evaluation tab\n"
        "- **Optimization**: Prompt optimization via ADK Optimization docs\n"
        "- **Custom metrics**: Define your own eval metrics"
    ),
    adk_code=adk.DEPLOY_NO_EVAL,
)

# ── Production Readiness Matrix ─────────────────────────────────────
st.markdown("### 5.4 — Production Readiness Comparison")
st.markdown("---")

prod_features = {
    "Production Feature": [
        "Managed Identity (no API keys)",
        "RBAC Access Control",
        "Application Insights / Tracing",
        "Auto-scaling",
        "Private Networking",
        "Built-in Evaluators",
        "Prompt Optimization",
        "Dataset from Traces",
        "CI/CD Agent Metadata",
        "Blue/Green Deployments",
    ],
    "MAF + Foundry": [
        "✅ Automatic",
        "✅ Built-in RBAC",
        "✅ Automatic App Insights",
        "✅ Foundry-managed",
        "✅ VNet support",
        "✅ 4+ evaluators",
        "✅ Auto from traces",
        "✅ Production harvesting",
        "✅ agent.yaml",
        "✅ Version-based",
    ],
    "ADK + GCP": [
        "✅ GCP IAM / Workload Identity",
        "✅ GCP IAM policies",
        "✅ Cloud Logging / Monitoring",
        "✅ Vertex AI / Cloud Run",
        "✅ VPC-SC support",
        "✅ Eval criteria + user sim",
        "✅ ADK Optimization docs",
        "⚠️ Manual setup",
        "✅ Agent Config",
        "✅ Cloud Run revisions",
    ],
}

import pandas as pd

df = pd.DataFrame(prod_features)
st.dataframe(df, use_container_width=True, hide_index=True, height=400)

# ── Advantage Banner ────────────────────────────────────────────────
render_advantage(
    "Deployment & Production",
    [
        "<strong>Hosting adapter</strong> — Standard container pattern with protocol translation; ADK uses CLI-based server",
        "<strong>Managed Identity + RBAC</strong> — Zero credential management; ADK requires manual IAM setup",
        "<strong>Prompt optimization from traces</strong> — Automatically improve instructions from production data; unique to MAF",
        "<strong>agent.yaml for CI/CD</strong> — Mature declarative config; ADK Agent Config is newer and less featured",
        "<strong>Production observability</strong> — Automatic App Insights tracing; ADK uses Cloud Monitoring (manual setup)",
    ],
)
