"""Build script — generates static HTML pages from Streamlit content."""

import os
import sys
import html as html_mod

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from content import snippets_maf as maf
from content import snippets_adk as adk

OUT = os.path.join(os.path.dirname(__file__), "static_site")

NAV_ITEMS = [
    ("index.html", "🤖 Home"),
    ("0-what-is.html", "📚 What Is MAF vs ADK"),
    ("1-agent-creation.html", "🏗️ Agent Creation"),
    ("2-tool-integration.html", "🔧 Tool Integration"),
    ("3-memory-state.html", "🧠 Memory & State"),
    ("4-multi-agent.html", "🔀 Multi-Agent"),
    ("5-deployment.html", "🚀 Deployment"),
    ("6-third-party.html", "🔗 3rd Party"),
    ("7-cross-model.html", "🔄 Cross-Model"),
    ("8-foundry-vs-vertex.html", "☁️ Foundry vs Vertex"),
]


def esc(text):
    return html_mod.escape(text)


def sidebar_html(active_file):
    items = ""
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if href == active_file else ""
        items += f'<li><a href="{href}"{cls}>{label}</a></li>\n'
    return f"""<nav class="sidebar">
    <h3>🗂️ MAF vs ADK</h3>
    <ul>{items}</ul>
    <div class="sidebar-meta">
        <p><strong>Baseline:</strong> MAF v2 Responses API</p>
        <p><strong>Compared with:</strong> Google ADK</p>
        <p style="margin-top:1rem;">March 2026</p>
    </div>
</nav>"""


def page(title, active_file, body):
    nav_options = ""
    for href, label in NAV_ITEMS:
        sel = " selected" if href == active_file else ""
        nav_options += f'<option value="{href}"{sel}>{label}</option>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} — MAF vs ADK</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{sidebar_html(active_file)}
<div class="mobile-nav">
    <select onchange="location.href=this.value">
        {nav_options}
    </select>
</div>
<main class="main-content">
{body}
<div class="footer">
    Built for Show &amp; Tell — Microsoft Agent Framework v2 Responses API — March 2026
</div>
</main>
</body>
</html>"""


def code_block(code, lang="python"):
    return f'<pre><code class="language-{lang}">{esc(code.strip())}</code></pre>'


def comparison(section_title, maf_title, maf_desc, maf_code, adk_title, adk_desc, adk_code,
               maf_lang="python", adk_lang="python"):
    return f"""<h3>{section_title}</h3><hr>
<div class="columns">
<div>
    <span class="framework-label-maf">Microsoft Agent Framework</span>
    <p><strong>{maf_title}</strong></p>
    <p>{maf_desc}</p>
    {code_block(maf_code, maf_lang)}
</div>
<div>
    <span class="framework-label-adk">Google ADK</span>
    <p><strong>{adk_title}</strong></p>
    <p>{adk_desc}</p>
    {code_block(adk_code, adk_lang)}
</div>
</div>"""


def advantage(title, points):
    bullets = "".join(f"<li>{p}</li>" for p in points)
    return f"""<div class="advantage-banner">
    <h4>✅ MAF Advantage — {title}</h4>
    <ul>{bullets}</ul>
</div>"""


def table_html(headers, rows):
    hdr = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>\n"
    return f"<table><thead><tr>{hdr}</tr></thead><tbody>{body}</tbody></table>"


def details(summary_text, content_html):
    return f"""<details>
<summary>{summary_text}</summary>
<div class="detail-content">{content_html}</div>
</details>"""


# ════════════════════════════════════════════
# INDEX PAGE
# ════════════════════════════════════════════
def build_index():
    matrix_rows = [
        ("Languages", "Python &amp; .NET ✅", "Python, TypeScript, Go, Java ✅"),
        ("Agent Definition", "SDK + agent.yaml ✅", "Python code + Agent Config ✅"),
        ("Invocation API", "OpenAI Responses protocol ✅", "Runner.run_async() ✅"),
        ("Streaming", "SSE streaming ✅", "Gemini Live API + Events ✅"),
        ("Built-in Web Search", "WebSearchPreview ✅", "Google Search Grounding ✅"),
        ("Built-in RAG / Vector Search", "Azure AI Search ✅", "Vertex AI Search Grounding ✅"),
        ("Code Execution (Sandbox)", "Built-in Code Interpreter ✅", "BuiltInCodeExecutor ✅"),
        ("MCP Tool Support", "Native MCP ✅", "MCP Tools ✅"),
        ("Long-term Memory", "Session + Cosmos DB + Redis + Mem0 ✅", "Memory Service + State ✅"),
        ("Multi-Agent Patterns", "Graph + Fan-out/in + Loop ✅", "Sequential + Parallel + Loop ✅"),
        ("Graph-based Orchestration", "Yes — with checkpointing ✅", "ADK 2.0 Graph Workflows ✅"),
        ("Human-in-the-Loop", "Built-in checkpoint ✅", "ADK 2.0 Human Input ✅"),
        ("Managed Identity", "Azure Managed Identity ✅", "GCP IAM + Workload Identity ✅"),
        ("Declarative Agent Config", "agent.yaml ✅", "Agent Config ✅"),
        ("Built-in Evaluation", "Intent, Task, Groundedness ✅", "Eval + User Sim + Optimization ✅"),
        ("Callbacks / Lifecycle Hooks", "Middleware pipeline ✅", "Rich callback system ✅"),
        ("Built-in Dev UI", "DevUI package ✅", "adk web UI ✅"),
        ("A2A Protocol", "agent-framework-a2a ✅", "Native A2A Protocol ✅"),
        ("Fabric / FabricIQ", "Native (same identity) ✅", "Custom connector ❌"),
        ("Snowflake Integration", "MCP + Function Tool ✅", "Custom connector ⚠️"),
        ("BlueYonder Integration", "Function Tool ✅", "Custom connector ⚠️"),
    ]

    cards = ""
    sections = [
        ("🏗️", "Agent Creation", "How agents are defined, configured, and invoked", "1-agent-creation.html"),
        ("🔧", "Tool Integration", "Built-in tools, custom functions, MCP servers", "2-tool-integration.html"),
        ("🧠", "Memory &amp; State", "Conversation persistence, long-term memory", "3-memory-state.html"),
        ("🔀", "Multi-Agent", "Orchestration patterns, graph workflows", "4-multi-agent.html"),
        ("🚀", "Deployment", "Containerisation, hosting, eval, prompt optimization", "5-deployment.html"),
        ("🔗", "3rd Party", "Snowflake, BlueYonder, Fabric FabricIQ", "6-third-party.html"),
        ("🔄", "Cross-Model", "MAF with Gemini, ADK with Azure OpenAI/Foundry", "7-cross-model.html"),
        ("☁️", "Foundry vs Vertex", "Platform comparison", "8-foundry-vs-vertex.html"),
    ]
    for icon, title, desc, href in sections:
        cards += f'<a href="{href}" style="text-decoration:none"><div class="metric-card"><h3>{icon} {title}</h3><p>{desc}</p></div></a>\n'

    body = f"""
<h1 style="text-align:center;">
    <span style="color:#4A90D9;">Microsoft Agent Framework</span>
    <span style="color:#888;"> vs </span>
    <span style="color:#34A853;">Google ADK</span>
</h1>
<p style="text-align:center; color:#8899aa; font-size:1.1rem;">
    A side-by-side comparison for enterprise conversational AI development<br>
    with Snowflake, BlueYonder &amp; Microsoft Fabric integration
</p>
<hr>

<div class="columns">
<div class="maf-col">
    <h3 style="color:#4A90D9;">Microsoft Agent Framework</h3>
    <ul>
    <li>Enterprise-grade SDK for Python &amp; .NET</li>
    <li>Native Azure AI Foundry integration</li>
    <li>OpenAI Responses protocol (streaming)</li>
    <li>Built-in tools: AI Search, Bing, Code Interpreter</li>
    <li>Graph-based multi-agent orchestration</li>
    <li>Long-term memory with auto-summarization</li>
    <li>Managed Identity — zero credential management</li>
    <li>Built-in eval, prompt optimization, CI/CD</li>
    </ul>
</div>
<div class="adk-col">
    <h3 style="color:#34A853;">Google Agent Development Kit</h3>
    <ul>
    <li>Multi-language: Python, TypeScript, Go, Java</li>
    <li>Vertex AI / Cloud Run / GKE deployment</li>
    <li>Runner-based invocation with event streaming</li>
    <li>Built-in: Google Search, code execution</li>
    <li>Sequential / Parallel / Loop + Graph (2.0)</li>
    <li>Session + state + memory services</li>
    <li>Callbacks, planners, artifacts, plugins</li>
    <li>Built-in eval with criteria &amp; user simulation</li>
    </ul>
</div>
</div>
<hr>

<h3>📊 Feature Comparison Matrix</h3>
{table_html(["Capability", "Microsoft Agent Framework", "Google ADK"], matrix_rows)}
<hr>

<h3>📖 Explore the Story</h3>
<div class="columns-3">{cards}</div>
"""
    return page("Home", "index.html", body)


# ════════════════════════════════════════════
# PAGE 0: WHAT IS
# ════════════════════════════════════════════
def build_page0():
    body = f"""
<h1 class="section-header">📚 What Is Microsoft Agent Framework vs Google ADK?</h1>
<p>Before comparing features, let's understand <strong>what each framework is</strong>,
how they're structured, and the architectural layers they provide.</p>
<hr>

<div class="columns">
<div class="maf-col">
    <h3 style="color:#4A90D9;">Microsoft Agent Framework (MAF)</h3>
    <p>A comprehensive <strong>multi-language framework</strong> for building,
    orchestrating, and deploying AI agents with support for both <strong>Python and .NET</strong>.</p>
    <p>Originally evolved from <strong>Semantic Kernel</strong> and <strong>AutoGen</strong>,
    MAF provides everything from simple chat agents to complex multi-agent workflows.</p>
    <ul>
    <li><strong>Package:</strong> <code>pip install agent-framework</code></li>
    <li><strong>Languages:</strong> Python &amp; .NET (C#)</li>
    <li><strong>API:</strong> OpenAI Responses protocol</li>
    <li><strong>Cloud:</strong> Azure AI Foundry</li>
    </ul>
</div>
<div class="adk-col">
    <h3 style="color:#34A853;">Google Agent Development Kit (ADK)</h3>
    <p>A flexible and modular framework for developing and deploying AI agents.
    While optimized for <strong>Gemini and the Google ecosystem</strong>,
    ADK is model-agnostic and deployment-agnostic.</p>
    <p>Designed to make agent development feel more like <strong>software development</strong>.</p>
    <ul>
    <li><strong>Package:</strong> <code>pip install google-adk</code></li>
    <li><strong>Languages:</strong> Python, TypeScript, Go, Java</li>
    <li><strong>API:</strong> Runner + Event pattern</li>
    <li><strong>Cloud:</strong> Vertex AI / Cloud Run / GKE</li>
    </ul>
</div>
</div>
<hr>

<h2>🏛️ Architecture Layers — Side by Side</h2>
<div class="columns">
<div>
    <div class="maf-col"><h4 style="color:#4A90D9;">MAF Architecture — 7 Layers</h4></div>
    {code_block('''
┌─────────────────────────────────────────┐
│  Layer 7: DEPLOYMENT & HOSTING          │
│  Azure AI Foundry · Containers · DevUI  │
├─────────────────────────────────────────┤
│  Layer 6: EVALUATION & OPTIMIZATION     │
│  Built-in Evaluators · Prompt Optimizer │
├─────────────────────────────────────────┤
│  Layer 5: ORCHESTRATION                 │
│  Graph Workflows · Checkpointing        │
│  Human-in-the-Loop · Time-travel        │
├─────────────────────────────────────────┤
│  Layer 4: MEMORY & STATE                │
│  Thread Persistence · Long-term Memory  │
│  Azure Cosmos DB · Redis · Mem0         │
├─────────────────────────────────────────┤
│  Layer 3: TOOLS & INTEGRATIONS          │
│  Function Tools · MCP · AI Search       │
│  Code Interpreter · Web Search          │
├─────────────────────────────────────────┤
│  Layer 2: AGENT CORE                    │
│  AzureOpenAIResponsesClient · .as_agent │
│  OpenAI Responses · Middleware          │
├─────────────────────────────────────────┤
│  Layer 1: PROVIDERS                     │
│  OpenAI · Azure OpenAI · Anthropic      │
│  Bedrock · Ollama · Foundry Local       │
└─────────────────────────────────────────┘''', "text")}
</div>
<div>
    <div class="adk-col"><h4 style="color:#34A853;">ADK Architecture — 7 Layers</h4></div>
    {code_block('''
┌─────────────────────────────────────────┐
│  Layer 7: DEPLOYMENT                    │
│  Vertex AI Agent Engine · Cloud Run     │
│  GKE · Docker · Agent Starter Pack      │
├─────────────────────────────────────────┤
│  Layer 6: EVALUATION & SAFETY           │
│  Built-in Eval Criteria · User Sim      │
│  Safety & Security Patterns             │
├─────────────────────────────────────────┤
│  Layer 5: ORCHESTRATION                 │
│  SequentialAgent · ParallelAgent        │
│  LoopAgent · ADK 2.0 Graph Workflows   │
├─────────────────────────────────────────┤
│  Layer 4: SESSIONS & MEMORY             │
│  Session Service · State · Artifacts    │
│  Context Caching · Compression          │
├─────────────────────────────────────────┤
│  Layer 3: TOOLS & INTEGRATIONS          │
│  Function Tools · MCP · OpenAPI Tools   │
│  Google Search · Code Execution         │
├─────────────────────────────────────────┤
│  Layer 2: AGENT CORE                    │
│  LlmAgent · Runner · Callbacks          │
│  Events · Gemini Live Streaming         │
├─────────────────────────────────────────┤
│  Layer 1: MODELS                        │
│  Gemini · Claude · Vertex AI-hosted     │
│  Ollama · vLLM · LiteLLM               │
└─────────────────────────────────────────┘''', "text")}
</div>
</div>
<hr>

<h2>📋 Layer-by-Layer Comparison</h2>
{table_html(
    ["Layer", "MAF Approach", "ADK Approach", "Key Difference"],
    [
        ("7 — Deployment", "Azure AI Foundry, agent.yaml, DevUI", "Vertex AI Agent Engine, Cloud Run, GKE, CLI", "MAF: Azure-native; ADK: GCP-native with flexible self-hosting"),
        ("6 — Evaluation", "Built-in evaluators, prompt optimizer", "Eval criteria, user simulation, safety patterns", "Both built-in eval; MAF adds prompt optimization from traces"),
        ("5 — Orchestration", "Graph workflows, checkpointing, HITL", "Sequential/Parallel/Loop + Graph (2.0)", "MAF: Graph-first; ADK: Workflow agents + graph in 2.0"),
        ("4 — Memory", "Thread persistence, Cosmos DB, Redis, Mem0", "SessionService, state, memory, artifacts, caching", "MAF: Managed persistence; ADK: Flexible manual sessions"),
        ("3 — Tools", "Function, MCP, AI Search, Code Interpreter", "Function, MCP, OpenAPI, Google Search, code exec", "MAF: Enterprise tools; ADK: Broader plugin ecosystem"),
        ("2 — Agent Core", "AzureOpenAIResponsesClient, middleware", "LlmAgent, Runner, callbacks, events", "MAF: OpenAI compatible; ADK: Custom runner + callbacks"),
        ("1 — Providers", "OpenAI, Azure, Anthropic, Bedrock, Ollama", "Gemini, Claude, Vertex, Ollama, vLLM, LiteLLM", "Similar breadth; each deeper in own ecosystem"),
    ]
)}
<hr>

<h2>📦 Package Ecosystem</h2>
<div class="columns">
<div>
    <div class="maf-col"><h4 style="color:#4A90D9;">MAF Python Packages</h4></div>
    {table_html(["Package", "Purpose"], [
        ("<code>agent-framework</code>", "Meta-package (installs all)"),
        ("<code>agent-framework-core</code>", "Base classes, interfaces"),
        ("<code>agent-framework-openai</code>", "OpenAI/Azure OpenAI provider"),
        ("<code>agent-framework-azure-ai</code>", "Azure AI Foundry integration"),
        ("<code>agent-framework-anthropic</code>", "Anthropic Claude provider"),
        ("<code>agent-framework-ollama</code>", "Ollama local models"),
        ("<code>agent-framework-orchestrations</code>", "Graph workflows"),
        ("<code>agent-framework-foundry</code>", "Foundry deployment"),
        ("<code>agent-framework-azure-cosmos</code>", "Cosmos DB persistence"),
        ("<code>agent-framework-redis</code>", "Redis state/memory"),
        ("<code>agent-framework-mem0</code>", "Mem0 memory integration"),
        ("<code>agent-framework-a2a</code>", "Agent-to-Agent protocol"),
    ])}
</div>
<div>
    <div class="adk-col"><h4 style="color:#34A853;">ADK SDKs</h4></div>
    {table_html(["Package/Repo", "Purpose"], [
        ("<code>google-adk</code> (Python)", "Main Python SDK"),
        ("<code>adk-js</code> (TypeScript)", "TypeScript SDK"),
        ("<code>adk-go</code> (Go)", "Go SDK"),
        ("<code>adk-java</code> (Java)", "Java SDK"),
    ])}
    <h4>Key Python Modules</h4>
    {table_html(["Module", "Purpose"], [
        ("<code>google.adk.agents</code>", "LlmAgent, workflow agents"),
        ("<code>google.adk.runners</code>", "Runner execution engine"),
        ("<code>google.adk.sessions</code>", "Session/state management"),
        ("<code>google.adk.tools</code>", "Tool definitions"),
        ("<code>google.adk.planners</code>", "BuiltInPlanner, PlanReAct"),
        ("<code>google.adk.callbacks</code>", "Lifecycle hooks"),
        ("<code>google.adk.artifacts</code>", "File/binary management"),
    ])}
</div>
</div>
<hr>

<h2>🎯 Design Philosophy</h2>
<div class="columns">
<div class="maf-col">
    <h4 style="color:#4A90D9;">MAF: Enterprise-First</h4>
    <ol>
    <li><strong>Managed resources</strong> — Agents are cloud resources with IDs, versioning</li>
    <li><strong>OpenAI API compatible</strong> — OpenAI Responses protocol</li>
    <li><strong>Azure-native security</strong> — Managed Identity, RBAC, Key Vault</li>
    <li><strong>Multi-language</strong> — Same patterns in Python and .NET</li>
    <li><strong>Declarative config</strong> — agent.yaml for GitOps</li>
    <li><strong>Production-grade</strong> — Eval, prompt optimization, observability built-in</li>
    </ol>
</div>
<div class="adk-col">
    <h4 style="color:#34A853;">ADK: Developer-First</h4>
    <ol>
    <li><strong>Code-native</strong> — Define agents as code objects</li>
    <li><strong>Multi-language SDKs</strong> — Python, TypeScript, Go, Java</li>
    <li><strong>Model-agnostic</strong> — Gemini, Claude, Ollama, vLLM, LiteLLM</li>
    <li><strong>Rich extensibility</strong> — Callbacks, plugins, skills, custom agents</li>
    <li><strong>Built-in dev tools</strong> — adk web UI, CLI, event inspection</li>
    <li><strong>Open protocols</strong> — MCP and A2A for cross-framework interop</li>
    </ol>
</div>
</div>
<hr>

<h2>⚡ Hello World — Side by Side</h2>
<div class="columns">
<div>
    <span class="framework-label-maf">Microsoft Agent Framework</span>
    {code_block(maf.AGENT_CREATION_BASIC)}
</div>
<div>
    <span class="framework-label-adk">Google ADK</span>
    {code_block(adk.AGENT_CREATION_BASIC)}
</div>
</div>
<div class="info-box">
    <strong>Key takeaway:</strong> MAF is more concise (managed resources, simpler API surface)
    while ADK requires explicit Runner and Session setup but gives you more control over the execution lifecycle.
</div>
"""
    return page("What Is MAF vs ADK", "0-what-is.html", body)


# ════════════════════════════════════════════
# PAGE 1: AGENT CREATION
# ════════════════════════════════════════════
def build_page1():
    body = f"""
<h1 class="section-header">🏗️ Chapter 1: Agent Creation</h1>
<p>How do you <strong>define, configure, and invoke</strong> an AI agent?
This is the foundation — and the two frameworks take very different approaches.</p>
<hr>

{comparison("1.1 — Basic Agent Definition",
    "SDK + Declarative Config",
    "Create agents via the <strong>AzureOpenAIResponsesClient</strong>. Use <code>.as_agent()</code> to wrap a model client into an agent.",
    maf.AGENT_CREATION_BASIC,
    "Python Code (LlmAgent)",
    "Define agents as Python <code>LlmAgent</code> objects. Uses Gemini by default or LiteLLM/Ollama/Claude for other providers.",
    adk.AGENT_CREATION_BASIC)}

{comparison("1.2 — Declarative Agent Metadata",
    "agent.yaml — Version-Controlled Config",
    "MAF provides <code>agent.yaml</code> — a declarative, version-controlled agent definition for CI/CD pipelines.",
    maf.AGENT_YAML, "Agent Config (Newer Feature)",
    "ADK has Agent Config for declarative definition. Less mature — no versioning, secret refs, or CI/CD patterns.",
    adk.AGENT_CONFIG, "yaml", "json")}

{comparison("1.3 — Agent Invocation & Streaming",
    "OpenAI Responses (Streaming)",
    "Invoke agents via the OpenAI Responses API — the industry-standard protocol with SSE streaming.",
    maf.AGENT_STREAMING,
    "Runner-based Event Iteration",
    "ADK uses a custom <code>Runner.run_async()</code> pattern. Not compatible with OpenAI API ecosystem.",
    adk.AGENT_INVOKE)}

<h3>1.4 — Agent Creation Feature Summary</h3><hr>
{table_html(
    ["Feature", "MAF", "ADK", "Why It Matters"],
    [
        ("Agent as managed resource", "✅ Server-side with unique ID", "✅ In-process Agent objects", "Lifecycle management, auditing"),
        ("Declarative config (agent.yaml)", "✅ Version-controlled YAML", "✅ Agent Config (JSON/YAML)", "CI/CD pipelines, GitOps"),
        ("Multi-language", "✅ Python &amp; .NET", "✅ Python, TS, Go, Java", "Enterprise team diversity"),
        ("OpenAI-compatible API", "✅ OpenAI Responses", "✅ Gemini API", "Ecosystem compatibility"),
        ("SSE streaming with typed events", "✅ text.delta, tool_call, citations", "✅ Gemini Live API streaming", "Real-time UX"),
        ("Managed Identity auth", "✅ DefaultAzureCredential", "✅ GCP IAM + Workload Identity", "Zero credentials in code"),
        ("Agent versioning", "✅ agent.yaml version field", "✅ Git + Agent Config", "Track changes, rollback"),
        ("Time to first agent", "~30 min (with Foundry setup)", "~5 min (API key + code)", "Setup investment vs readiness"),
    ]
)}

{advantage("Agent Creation", [
    "<strong>OpenAI Responses protocol</strong> — Industry-standard protocol",
    "<strong>agent.yaml</strong> — Mature declarative config with versioning, secrets, CI/CD",
    "<strong>Managed resource</strong> — Agents are Foundry resources with IDs and lifecycle management",
    "<strong>Azure-native security</strong> — Managed Identity, RBAC, Key Vault",
])}
"""
    return page("Agent Creation", "1-agent-creation.html", body)


# ════════════════════════════════════════════
# PAGE 2: TOOL INTEGRATION
# ════════════════════════════════════════════
def build_page2():
    body = f"""
<h1 class="section-header">🔧 Chapter 2: Tool Integration</h1>
<p>Tools extend what an agent can <strong>do</strong> — from querying databases to searching the web.</p>
<hr>

{comparison("2.1 — Custom Function Tools",
    "FunctionTool with Type Safety",
    "Wrap any Python function as a <code>FunctionTool</code>. Schema is auto-generated from type hints and docstrings.",
    maf.TOOLS_FUNCTION,
    "Functions as Tools",
    "ADK also supports function-based tools with automatic schema generation. Return type must be <code>dict</code>.",
    adk.TOOLS_FUNCTION)}

{comparison("2.2 — Built-in Enterprise Tools",
    "Azure AI Search, Bing, Code Interpreter, Web Search",
    "MAF provides 4+ built-in tools: WebSearchPreview, CodeInterpreter, Azure AI Search, Bing Grounding.",
    maf.TOOLS_BUILTIN,
    "Google Search + Code Execution",
    "ADK provides Google Search Grounding, BuiltInCodeExecutor, and OpenAPI tools. No Azure AI Search or Bing equivalent.",
    adk.TOOLS_CODE_EXEC)}

{comparison("2.3 — RAG / Vector Search",
    "Azure AI Search — Built-in RAG",
    "One-line RAG integration with <code>AzureAISearchToolDefinition</code>. Supports vector, semantic, hybrid search.",
    maf.TOOLS_AI_SEARCH,
    "Google Search + Vertex AI Search Grounding",
    "ADK provides Google Search Grounding built-in. Vertex AI Search for enterprise RAG requires separate setup.",
    adk.TOOLS_SEARCH)}

{comparison("2.4 — MCP (Model Context Protocol) Tools",
    "Native MCP with Allowed-Tools Control",
    "Connect to any MCP server with <code>McpToolDefinition</code>. Specify <code>allowed_tools</code> for access control.",
    maf.TOOLS_MCP,
    "MCPToolset (Cleanup Required)",
    "ADK supports MCP via <code>MCPToolset.from_server()</code>. Requires manual lifecycle management.",
    adk.TOOLS_MCP)}

{advantage("Tool Integration", [
    "<strong>Azure AI Search RAG</strong> — One-line vector/semantic/hybrid search",
    "<strong>Bing Grounding</strong> — Enterprise web search with citations",
    "<strong>Multi-tool ToolSet</strong> — Compose built-in + custom + MCP tools freely",
    "<strong>MCP with allowed_tools</strong> — Fine-grained remote tool access control",
])}
"""
    return page("Tool Integration", "2-tool-integration.html", body)


# ════════════════════════════════════════════
# PAGE 3: MEMORY & STATE
# ════════════════════════════════════════════
def build_page3():
    body = f"""
<h1 class="section-header">🧠 Chapter 3: Memory & State</h1>
<p>How agents <strong>remember</strong> conversations and maintain state across interactions is critical for enterprise applications.</p>
<hr>

{comparison("3.1 — Conversation Persistence",
    "Thread-based Persistence (Cosmos DB-backed)",
    "Conversations persist automatically via threads. Backed by Azure Cosmos DB with full message history.",
    maf.MEMORY_THREAD,
    "Session Service",
    "ADK uses SessionService for conversations. InMemorySessionService (lost on restart) or DatabaseSessionService for persistence.",
    adk.MEMORY_SESSION)}

{comparison("3.2 — Long-term Memory & State",
    "Built-in Long-term Memory",
    "MAF provides auto-summarized long-term memory across threads, backed by Cosmos DB, Redis, or Mem0.",
    maf.MEMORY_LONG_TERM,
    "State Dictionary + Memory Service",
    "ADK uses typed state dictionaries (app, user, session scope) plus a Memory Service for cross-session recall.",
    adk.MEMORY_STATE)}

<h3>Memory Architecture Comparison</h3><hr>
<div class="columns">
<div>
    <div class="maf-col"><h4 style="color:#4A90D9;">MAF Memory Architecture</h4></div>
    {code_block('''
┌─────────────────────────────┐
│   Agent Session             │
│   ┌─────────────────────┐   │
│   │ Thread (Messages)   │   │
│   │ • User messages     │   │
│   │ • Agent responses   │   │
│   │ • Tool calls        │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │ Long-term Memory    │   │
│   │ • Auto-summarized   │   │
│   │ • Cross-thread      │   │
│   │ • User profiles     │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │ Backend Store       │   │
│   │ • Azure Cosmos DB   │   │
│   │ • Redis             │   │
│   │ • Mem0              │   │
│   └─────────────────────┘   │
└─────────────────────────────┘''', "text")}
</div>
<div>
    <div class="adk-col"><h4 style="color:#34A853;">ADK Memory Architecture</h4></div>
    {code_block('''
┌─────────────────────────────┐
│   Runner Execution          │
│   ┌─────────────────────┐   │
│   │ Session             │   │
│   │ • Events history    │   │
│   │ • Turn tracking     │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │ State               │   │
│   │ • App-scope dict    │   │
│   │ • User-scope dict   │   │
│   │ • Session-scope     │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │ Memory Service      │   │
│   │ • Cross-session     │   │
│   │ • InMemory / DB     │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │ Artifacts           │   │
│   │ • Binary files      │   │
│   │ • Generated content │   │
│   └─────────────────────┘   │
└─────────────────────────────┘''', "text")}
</div>
</div>

{advantage("Memory & State", [
    "<strong>Azure Cosmos DB</strong> — Managed, globally-distributed persistence out of the box",
    "<strong>Auto-summarized memory</strong> — Long-term memory with automatic summarization",
    "<strong>Thread model</strong> — Server-side conversation management, not in-process",
    "<strong>Mem0 integration</strong> — Advanced memory retrieval with semantic search",
])}
"""
    return page("Memory & State", "3-memory-state.html", body)


# ════════════════════════════════════════════
# PAGE 4: MULTI-AGENT
# ════════════════════════════════════════════
def build_page4():
    body = f"""
<h1 class="section-header">🔀 Chapter 4: Multi-Agent Orchestration</h1>
<p>Complex tasks require <strong>multiple specialized agents</strong> working together. The orchestration model determines how agents collaborate.</p>
<hr>

{comparison("4.1 — Multi-Agent Patterns",
    "Graph-based Workflows with Checkpointing",
    "MAF uses graph-based workflows for explicit multi-agent coordination. Supports checkpointing, human-in-the-loop, and time-travel debugging.",
    maf.MULTI_AGENT_GRAPH,
    "Sequential + Parallel + Loop Agents",
    "ADK provides workflow agents (SequentialAgent, ParallelAgent, LoopAgent) plus LLM-driven agent transfer. ADK 2.0 adds graph-based workflows.",
    adk.MULTI_AGENT_BASIC)}

{comparison("4.2 — Advanced Orchestration Patterns",
    "Fan-out/Fan-in + Conditional Routing",
    "MAF graph workflows support fan-out/fan-in, conditional edges, checkpoints, and durable tasks for long-running operations.",
    maf.MULTI_AGENT_PATTERNS,
    "LLM-driven Transfer + Sub-Agents",
    "ADK supports transfer_to_agent for LLM-driven delegation, plus hierarchical sub-agent composition.",
    adk.MULTI_AGENT_PATTERNS)}

<h3>Orchestration Architecture</h3><hr>
<div class="columns">
<div>
    <div class="maf-col"><h4 style="color:#4A90D9;">MAF: Graph Workflow</h4></div>
    {code_block('''
┌─────────────────────────────┐
│   Graph Workflow Engine     │
│                             │
│   [Start] → [Agent A]      │
│              ↓              │
│         [Checkpoint]        │
│          ↙      ↘          │
│   [Agent B]   [Agent C]    │
│          ↘      ↙          │
│         [Merge/Join]        │
│              ↓              │
│        [Human Review]       │
│              ↓              │
│           [End]             │
│                             │
│   Features:                 │
│   • State checkpointing     │
│   • Time-travel debugging   │
│   • Human-in-the-loop       │
│   • Durable tasks           │
│   • Conditional edges       │
└─────────────────────────────┘''', "text")}
</div>
<div>
    <div class="adk-col"><h4 style="color:#34A853;">ADK: Workflow Agents</h4></div>
    {code_block('''
┌─────────────────────────────┐
│   Workflow Agent Types      │
│                             │
│   SequentialAgent:          │
│   [A] → [B] → [C]          │
│                             │
│   ParallelAgent:            │
│   [A] ─┐                   │
│   [B] ─┤→ [Merge]          │
│   [C] ─┘                   │
│                             │
│   LoopAgent:                │
│   [A] → [Check] → [A]...   │
│                             │
│   LLM Transfer:             │
│   [Router] ──→ [Specialist] │
│            └──→ [Specialist]│
│                             │
│   ADK 2.0 Graph:            │
│   [Node] → [Edge] → [Node] │
│   (Alpha — evolving)        │
└─────────────────────────────┘''', "text")}
</div>
</div>

{advantage("Multi-Agent Orchestration", [
    "<strong>Graph-first design</strong> — Native graph workflows from day one, not an add-on",
    "<strong>Checkpointing</strong> — Save and restore workflow state at any point",
    "<strong>Time-travel debugging</strong> — Replay and inspect any step in the workflow",
    "<strong>Durable tasks</strong> — Long-running operations survive process restarts",
    "<strong>Human-in-the-loop</strong> — Built-in checkpoint-based approval flows",
])}
"""
    return page("Multi-Agent", "4-multi-agent.html", body)


# ════════════════════════════════════════════
# PAGE 5: DEPLOYMENT
# ════════════════════════════════════════════
def build_page5():
    body = f"""
<h1 class="section-header">🚀 Chapter 5: Deployment & Production</h1>
<p>Getting agents into production requires <strong>containerization, hosting, evaluation, and optimization</strong>.</p>
<hr>

{comparison("5.1 — Containerization & Hosting",
    "Azure AI Foundry Managed Hosting",
    "Deploy agents to Azure AI Foundry with managed hosting. Supports Azure Functions, Container Apps, and AKS.",
    maf.DEPLOY_DOCKERFILE,
    "Vertex AI Agent Engine + Cloud Run/GKE",
    "Deploy to Vertex AI Agent Engine (serverless), Cloud Run, or GKE. Agent Starter Pack provides templates.",
    adk.DEPLOY_DOCKERFILE)}

{comparison("5.2 — Evaluation Framework",
    "Built-in Evaluators + Prompt Optimization",
    "MAF provides built-in evaluators for intent, task completion, and groundedness. Plus prompt optimization from production traces.",
    maf.DEPLOY_EVAL,
    "Built-in Eval Criteria + User Simulation",
    "ADK provides built-in eval criteria (tool_trajectory, response_match) and user simulation for automated testing.",
    adk.DEPLOY_NO_EVAL)}

{comparison("5.3 — CI/CD & DevOps",
    "GitOps with agent.yaml",
    "agent.yaml enables GitOps workflows. CI/CD pipelines read config, build containers, and deploy to Foundry.",
    maf.DEPLOY_AGENT_YAML,
    "Container-based Deployment",
    "ADK uses standard container-based deployment. No built-in CI/CD patterns — use standard Docker/K8s workflows.",
    adk.DEPLOY_CLOUD_RUN)}

<h3>Production Readiness Matrix</h3><hr>
{table_html(
    ["Capability", "MAF", "ADK"],
    [
        ("Managed hosting", "✅ Azure AI Foundry", "✅ Vertex AI Agent Engine"),
        ("Container support", "✅ Docker + AKS + Container Apps", "✅ Docker + Cloud Run + GKE"),
        ("Serverless option", "✅ Azure Functions adapter", "✅ Agent Engine (serverless)"),
        ("Built-in evaluation", "✅ Intent, Task, Groundedness", "✅ Eval Criteria + User Sim"),
        ("Prompt optimization", "✅ From production traces", "❌ Manual"),
        ("CI/CD integration", "✅ agent.yaml GitOps", "⚠️ Standard Docker/K8s"),
        ("Observability", "✅ Application Insights + OpenTelemetry", "✅ Cloud Logging + Trace"),
        ("A/B testing agents", "✅ Via agent versions", "⚠️ Manual traffic splitting"),
        ("Cost monitoring", "✅ Azure Cost Management", "✅ GCP Billing"),
        ("Compliance", "✅ Azure compliance certifications", "✅ GCP compliance certifications"),
    ]
)}

{advantage("Deployment & Production", [
    "<strong>Prompt optimization from traces</strong> — Automatically improve agent instructions from production data",
    "<strong>agent.yaml GitOps</strong> — Declarative deployment pipeline integration",
    "<strong>Agent versioning</strong> — A/B test agent versions with traffic routing",
    "<strong>Azure compliance</strong> — SOC2, HIPAA, FedRAMP certifications",
])}
"""
    return page("Deployment", "5-deployment.html", body)


# ════════════════════════════════════════════
# PAGE 6: THIRD PARTY
# ════════════════════════════════════════════
def build_page6():
    body = f"""
<h1 class="section-header">🔗 Chapter 6: 3rd Party Integration</h1>
<p>Enterprise agents need to connect to <strong>Snowflake, BlueYonder, and Microsoft Fabric</strong>. Here's how each framework handles these integrations.</p>
<hr>

<h3>Integration Architecture Overview</h3>
{code_block('''
┌───────────────────────────────────────────────────────┐
│                    AI Agent Layer                      │
│  ┌──────────────────┐    ┌──────────────────────┐    │
│  │  MAF Agent        │    │  ADK Agent            │    │
│  │  (Azure Foundry)  │    │  (Vertex AI)          │    │
│  └──────┬───────────┘    └──────┬───────────────┘    │
│         │                       │                     │
│  ┌──────▼───────────────────────▼───────────────┐    │
│  │          Integration Methods                  │    │
│  │  ┌─────────┐  ┌────────┐  ┌──────────────┐  │    │
│  │  │   MCP   │  │Function│  │ Direct SDK   │  │    │
│  │  │ Server  │  │  Tool  │  │ (Snowflake   │  │    │
│  │  │         │  │        │  │  connector)  │  │    │
│  │  └────┬────┘  └───┬────┘  └──────┬───────┘  │    │
│  └───────┼────────────┼──────────────┼──────────┘    │
│          │            │              │                │
├──────────▼────────────▼──────────────▼────────────────┤
│                 External Services                     │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │Snowflake │  │BlueYonder │  │Microsoft Fabric  │  │
│  │          │  │           │  │FabricIQ / WorkIQ │  │
│  └──────────┘  └───────────┘  └──────────────────┘  │
└───────────────────────────────────────────────────────┘''', "text")}
<hr>

{comparison("6.1 — Snowflake Integration",
    "MCP Server + Function Tool",
    "Connect via MCP server or FunctionTool. MAF supports Snowflake MCP with allowed_tools for access control.",
    maf.INTEGRATION_SNOWFLAKE,
    "Custom Function Tool",
    "ADK connects via custom function tools wrapping the Snowflake connector. No built-in Snowflake integration.",
    adk.INTEGRATION_SNOWFLAKE)}

{comparison("6.2 — BlueYonder Integration",
    "Function Tool with API Client",
    "Wrap BlueYonder REST APIs as FunctionTool with type-safe schema generation.",
    maf.INTEGRATION_BLUEYONDER,
    "Custom Function Tool",
    "Similar pattern — wrap BlueYonder APIs as custom functions.",
    adk.INTEGRATION_BLUEYONDER)}

{comparison("6.3 — Microsoft Fabric / FabricIQ / WorkIQ",
    "Native Azure Integration (Same Identity)",
    "MAF agents use the same Azure Managed Identity to access Fabric. FabricIQ provides AI-powered insights natively.",
    maf.INTEGRATION_FABRIC,
    "Custom REST API Connector",
    "ADK requires custom REST API connectors for Fabric. No Managed Identity — must manage API keys separately.",
    adk.INTEGRATION_FABRIC)}

<h3>Integration Summary</h3><hr>
{table_html(
    ["Service", "MAF Approach", "ADK Approach", "MAF Advantage"],
    [
        ("Snowflake", "MCP + FunctionTool ✅", "Custom function ⚠️", "Built-in MCP with access control"),
        ("BlueYonder", "FunctionTool ✅", "Custom function ⚠️", "Same pattern, better tooling"),
        ("Fabric / FabricIQ", "Native (same identity) ✅", "Custom connector ❌", "Same Azure identity, zero setup"),
        ("WorkIQ", "Azure Function adapter ✅", "Not supported ❌", "Native Azure integration"),
    ]
)}

{advantage("3rd Party Integration", [
    "<strong>Fabric / FabricIQ / WorkIQ</strong> — Same Azure Managed Identity; zero additional auth setup",
    "<strong>Snowflake MCP</strong> — Built-in MCP server with fine-grained tool access control",
    "<strong>Enterprise SSO</strong> — Azure AD/Entra ID flows for all integrations",
])}
"""
    return page("3rd Party Integration", "6-third-party.html", body)


# ════════════════════════════════════════════
# PAGE 7: CROSS-MODEL
# ════════════════════════════════════════════
def build_page7():
    body = f"""
<h1 class="section-header">🔄 Cross-Model Usage — Mixing Frameworks & LLMs</h1>
<p>Both frameworks support <strong>model-agnostic</strong> usage. You can use MAF with Gemini or ADK with Azure OpenAI / Foundry models.</p>
<hr>

<h2 style="color:#4A90D9;">1. Microsoft Agent Framework + Gemini LLM</h2>
<p>MAF does <strong>not</strong> have a dedicated Gemini provider package, but there are <strong>three practical approaches</strong>.</p>

<h3>Option A — Gemini via Azure AI Foundry (Recommended)</h3>
<p>Azure AI Foundry hosts Gemini models in its Model Garden. Deploy and use with the standard <code>FoundryChatClient</code>.</p>
<div class="columns">
<div>
    {code_block('''from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient, FoundryAgent

# Deploy "gemini-2.5-flash" in Foundry Model Garden
client = FoundryChatClient(
    project_endpoint="https://ai-foundry-<resource>.services.ai.azure.com/",
    credential=DefaultAzureCredential(),
)
agent = FoundryAgent(
    client=client,
    model="gemini-2.5-flash",
    instructions="You are a helpful assistant powered by Gemini on Azure.",
)
response = await agent.run("Explain quantum computing briefly.")''')}
</div>
<div>
    <p><strong>Why this approach?</strong></p>
    <ul>
    <li><strong>Enterprise compliance</strong> — Gemini runs inside your Azure tenant</li>
    <li><strong>Managed Identity</strong> — no API keys to manage</li>
    <li><strong>Unified billing</strong> — single Azure invoice</li>
    <li><strong>Same MAF code</strong> — just change the deployment name</li>
    </ul>
    <div class="success-box">✅ <strong>No code change required.</strong> Just deploy a Gemini model in Foundry and point at that deployment name.</div>
</div>
</div>

<h3>Option B — Gemini's OpenAI-Compatible Endpoint (Direct)</h3>
{code_block('''from openai import OpenAI
from agent_framework.openai import OpenAIChatCompletionClient

client = OpenAI(
    api_key="GOOGLE_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
agent = OpenAIChatCompletionClient(client=client).as_agent(
    model="gemini-2.5-flash",
    instructions="You are a helpful assistant powered by Gemini.",
)''')}
<div class="warning-box">⚠️ <strong>Data leaves Azure.</strong> API calls go to Google's servers. Ensure compliance with your data policies.</div>

<h3>Option C — Gemma (Open-Source Gemini) via Ollama (Local)</h3>
{code_block('''from agent_framework.ollama import OllamaChatClient

# Run locally: ollama pull gemma3
client = OllamaChatClient(model="gemma3")
agent = client.as_agent(
    instructions="You are a helpful assistant powered by Gemma 3.",
)''')}
<div class="success-box">🔒 <strong>Fully offline.</strong> No API calls, no data leaves your machine.</div>

<h3>MAF + Gemini — Approach Comparison</h3>
{table_html(["Approach", "Provider Package", "Data Location", "Best For"], [
    ("<strong>A. Foundry Model Garden</strong>", "<code>agent-framework-foundry</code>", "Azure tenant", "Enterprise production"),
    ("<strong>B. Gemini OpenAI endpoint</strong>", "<code>agent-framework-openai</code>", "Google servers", "Quick prototyping"),
    ("<strong>C. Gemma via Ollama</strong>", "<code>agent-framework-ollama</code>", "Local machine", "Offline / dev / testing"),
])}
<hr>

<h2 style="color:#34A853;">2. Google ADK + Azure OpenAI / Microsoft Foundry LLM</h2>
<p>ADK provides a <strong>LiteLLM model connector</strong> that supports 100+ providers, including Azure OpenAI.</p>

<h3>Option A — Azure OpenAI via LiteLLM (Recommended)</h3>
<div class="columns">
<div>
    <p><strong>Setup</strong></p>
    {code_block("pip install google-adk litellm", "bash")}
    {code_block('''# .env or export these
AZURE_API_KEY=your-azure-openai-key
AZURE_API_BASE=https://<resource>.openai.azure.com/
AZURE_API_VERSION=2024-12-01-preview''', "bash")}
</div>
<div>
    <p><strong>Implementation</strong></p>
    {code_block('''from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent = LlmAgent(
    model=LiteLlm(model="azure/gpt-4o"),
    name="azure_agent",
    instruction="You are a helpful assistant powered by Azure OpenAI.",
)''')}
</div>
</div>

<h3>Option B — Microsoft Foundry Models via LiteLLM</h3>
{code_block('''from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

agent = LlmAgent(
    model=LiteLlm(
        model="openai/gpt-4o",
        api_base="https://ai-foundry-<resource>.services.ai.azure.com/openai/v1/",
        api_key="your-foundry-api-key",
    ),
    name="foundry_agent",
    instruction="You are a helpful assistant using Foundry-hosted models.",
)''')}

<h3>ADK + Azure/Foundry — Approach Comparison</h3>
{table_html(["Approach", "LiteLLM Model String", "Env Vars", "Best For"], [
    ("<strong>A. Azure OpenAI</strong>", "<code>azure/&lt;deployment&gt;</code>", "AZURE_API_KEY, AZURE_API_BASE, AZURE_API_VERSION", "Existing Azure OpenAI users"),
    ("<strong>B. Foundry Models</strong>", "<code>openai/&lt;model&gt;</code> + custom base", "Foundry API key", "Foundry-hosted multi-vendor"),
    ("<strong>C. OpenAI Direct</strong>", "<code>openai/&lt;model&gt;</code>", "OPENAI_API_KEY", "Non-Azure OpenAI usage"),
])}
<hr>

<h2>🔑 Key Takeaways</h2>
<div class="columns">
<div class="maf-col">
    <h4 style="color:#4A90D9;">MAF Cross-Model Summary</h4>
    <ul>
    <li><strong>Multiple paths to Gemini:</strong> Foundry Model Garden, OpenAI-compatible endpoint, or Gemma via Ollama</li>
    <li><strong>Enterprise recommended:</strong> Deploy Gemini in Foundry for managed identity + compliance</li>
    <li><strong>Code change is minimal:</strong> Just swap the model deployment name</li>
    </ul>
</div>
<div class="adk-col">
    <h4 style="color:#34A853;">ADK Cross-Model Summary</h4>
    <ul>
    <li><strong>LiteLLM is the bridge:</strong> Single integration point for 100+ providers</li>
    <li><strong>Azure prefix <code>azure/</code>:</strong> Standard LiteLLM pattern for Azure OpenAI</li>
    <li><strong>Same ADK features:</strong> Tools, memory, multi-agent all work regardless of LLM provider</li>
    </ul>
</div>
</div>
"""
    return page("Cross-Model Usage", "7-cross-model.html", body)


# ════════════════════════════════════════════
# PAGE 8: FOUNDRY vs VERTEX
# ════════════════════════════════════════════
def build_page8():
    body = f"""
<h1 class="section-header">☁️ Microsoft Foundry vs Google Vertex AI</h1>
<p>Both platforms are <strong>unified AI development platforms</strong> from their respective clouds.</p>
<hr>

<div class="columns">
<div class="maf-col">
    <h3 style="color:#4A90D9;">Microsoft Foundry</h3>
    <p><em>Formerly: Azure AI Studio → Azure AI Foundry → Microsoft Foundry</em></p>
    <p>A unified <strong>Azure PaaS</strong> for enterprise AI operations, model deployment, agent building, and application development.</p>
    <ul>
    <li><strong>Portal:</strong> <a href="https://ai.azure.com" target="_blank">ai.azure.com</a></li>
    <li><strong>Cloud:</strong> Microsoft Azure</li>
    <li><strong>Agent API:</strong> OpenAI Responses protocol</li>
    <li><strong>SDKs:</strong> Python, C#, TypeScript (preview), Java (preview)</li>
    <li><strong>Agent Framework:</strong> Microsoft Agent Framework (MAF)</li>
    </ul>
</div>
<div class="adk-col">
    <h3 style="color:#34A853;">Google Vertex AI</h3>
    <p><em>Includes: Vertex AI Studio, Agent Builder, Agent Engine</em></p>
    <p>A unified, open <strong>Google Cloud platform</strong> for building, deploying, and scaling generative AI and ML models.</p>
    <ul>
    <li><strong>Portal:</strong> <a href="https://console.cloud.google.com/vertex-ai" target="_blank">console.cloud.google.com/vertex-ai</a></li>
    <li><strong>Cloud:</strong> Google Cloud Platform</li>
    <li><strong>Model Access:</strong> Model Garden (200+ models)</li>
    <li><strong>SDKs:</strong> Python, Node.js, Go, Java</li>
    <li><strong>Agent Framework:</strong> Agent Development Kit (ADK)</li>
    </ul>
</div>
</div>
<hr>

<h3>📊 Key Capabilities Comparison</h3>
{table_html(
    ["Capability", "Microsoft Foundry", "Google Vertex AI"],
    [
        ("Platform Type", "Unified Azure PaaS for AI", "Unified Google Cloud AI platform"),
        ("Primary Models", "GPT-4o, GPT-4.1, o3, o4-mini", "Gemini 3 Pro, Gemini 3 Flash, Gemini 2.5"),
        ("Model Catalog", "Foundry Model Garden (OpenAI, Anthropic, Gemini, Llama)", "Model Garden (200+ models)"),
        ("Agent Building", "MAF SDK + Foundry Agents (server-side)", "ADK + Agent Builder + Agent Engine"),
        ("Agent Deployment", "Azure Functions, Container Apps, AKS, Foundry Agent Service", "Agent Engine (serverless), Cloud Run, GKE"),
        ("Agent API", "OpenAI Responses protocol", "Gemini API (generateContent, streamGenerateContent)"),
        ("Tools / Integrations", "1,400+ tools via tool catalog + MCP + A2A", "Google Search, Vertex AI Search, code execution, OpenAPI tools"),
        ("Memory / State", "Thread-based + Cosmos DB + Redis + Mem0", "Session service + state + memory + artifacts"),
        ("Model Fine-Tuning", "SFT via Azure OpenAI + custom training", "SFT, PEFT, RLHF via Vertex AI Training"),
        ("Model Evaluation", "Intent, Task Completion, Groundedness evals", "Gen AI Evaluation Service + ADK Eval"),
        ("Responsible AI", "Content Safety, Prompt Shields, Groundedness", "Model Armor, safety filters"),
        ("MLOps / Pipelines", "Azure ML Pipelines (separate)", "Vertex AI Pipelines (native, Kubeflow-based)"),
        ("Notebooks", "VS Code, Foundry extension", "Colab Enterprise, Vertex AI Workbench"),
        ("Search / RAG", "Azure AI Search, Foundry IQ", "Vertex AI Search Grounding, Google Search"),
        ("Dev Portal", "Foundry Portal (ai.azure.com)", "Vertex AI Studio (console.cloud.google.com)"),
        ("Observability", "Application Insights, Azure Monitor", "Cloud Logging, Cloud Monitoring, Cloud Trace"),
        ("Identity &amp; Auth", "Azure AD / Entra ID, Managed Identity, RBAC", "GCP IAM, Workload Identity, service accounts"),
        ("Enterprise Governance", "Azure Policy, RBAC, network isolation", "Org policies, VPC-SC, audit logs"),
        ("Pricing Model", "Pay-per-token/call, platform free", "Pay-per-token/call, varied by model"),
    ]
)}
<hr>

<h3>🏗️ Architecture Layers</h3>
<div class="columns">
<div>
    <p><strong>Microsoft Foundry Architecture</strong></p>
    {code_block('''
┌─────────────────────────────────┐
│   Foundry Portal (ai.azure.com) │
├─────────────────────────────────┤
│  Agent Service (Responses API)  │
│  • Agents v2 (MAF-powered)     │
│  • Tool Catalog (1400+)        │
│  • Foundry IQ Knowledge        │
│  • Memory & State              │
├─────────────────────────────────┤
│  Foundry Models                 │
│  • OpenAI (GPT-4o, o3, o4)     │
│  • Anthropic (Claude)           │
│  • Google (Gemini)              │
│  • Meta (Llama), Mistral ...    │
├─────────────────────────────────┤
│  Foundry Tools                  │
│  • AI Search  • Content Safety  │
│  • Speech     • Vision          │
├─────────────────────────────────┤
│  Azure Infrastructure           │
│  • Entra ID  • Managed Identity │
│  • VNet      • Private Endpoints│
│  • Azure Policy • Monitor       │
└─────────────────────────────────┘''', "text")}
</div>
<div>
    <p><strong>Vertex AI Architecture</strong></p>
    {code_block('''
┌─────────────────────────────────┐
│   Vertex AI Studio (Console)    │
├─────────────────────────────────┤
│  Agent Builder & Agent Engine   │
│  • ADK-powered Agents           │
│  • Tools & Grounding            │
│  • Sessions & Memory            │
│  • A2A Protocol                 │
├─────────────────────────────────┤
│  Model Garden (200+ models)     │
│  • Google (Gemini 3, Imagen)    │
│  • Anthropic (Claude)           │
│  • Meta (Llama), Mistral ...    │
├─────────────────────────────────┤
│  Vertex AI Tools                │
│  • Search  • Eval  • Pipelines  │
│  • Training  • Feature Store    │
│  • Notebooks  • Experiments     │
├─────────────────────────────────┤
│  GCP Infrastructure             │
│  • IAM      • Workload Identity │
│  • VPC-SC   • Private Google    │
│  • Org Policy • Cloud Audit     │
└─────────────────────────────────┘''', "text")}
</div>
</div>
<hr>

<h3>📅 Platform Evolution</h3>
<div class="columns">
<div class="maf-col">
    <h4>Microsoft Foundry Evolution</h4>
    <ol>
    <li><strong>Azure AI Studio</strong> — Original portal for Azure AI services</li>
    <li><strong>Azure AI Foundry</strong> — Consolidated hub + Azure OpenAI + AI Services</li>
    <li><strong>Microsoft Foundry</strong> — Current: unified PaaS, single resource model, OpenAI Responses</li>
    </ol>
    <p><strong>Key shift:</strong> From multiple packages and endpoints to a single unified project client.</p>
</div>
<div class="adk-col">
    <h4>Vertex AI Evolution</h4>
    <ol>
    <li><strong>Cloud AI Platform</strong> — Original ML training &amp; prediction</li>
    <li><strong>Vertex AI</strong> — Unified ML + Gen AI platform with Model Garden</li>
    <li><strong>Vertex AI + Agent Builder</strong> — Current: ADK integration, Agent Engine, Gemini 3</li>
    </ol>
    <p><strong>Key shift:</strong> From ML-focused platform to full-stack generative AI and agentic development.</p>
</div>
</div>
<hr>

<h3>🎯 When to Choose Which</h3>
<div class="columns">
<div class="maf-col">
    <h4>Choose Microsoft Foundry when:</h4>
    <ul>
    <li>Your organization is on <strong>Azure / M365</strong></li>
    <li>You need <strong>Managed Identity</strong> (Entra ID)</li>
    <li>You want <strong>GPT-4o / o3 / o4-mini</strong> as primary models</li>
    <li>You need <strong>Fabric / FabricIQ / WorkIQ</strong></li>
    <li>You require <strong>Azure Policy</strong> governance</li>
    <li>You want the <strong>OpenAI Responses protocol</strong></li>
    <li>Your team uses <strong>.NET / C#</strong></li>
    <li>You need <strong>1,400+ enterprise tools</strong></li>
    </ul>
</div>
<div class="adk-col">
    <h4>Choose Vertex AI when:</h4>
    <ul>
    <li>Your organization is on <strong>Google Cloud (GCP)</strong></li>
    <li>You want <strong>Gemini 3</strong> as the primary model</li>
    <li>You need <strong>BigQuery</strong> native integration</li>
    <li>You want <strong>Agent Engine</strong> for serverless deployment</li>
    <li>You need <strong>200+ models</strong> from Model Garden</li>
    <li>You want <strong>multi-language SDKs</strong> (Python, TS, Go, Java)</li>
    <li>You need <strong>Kubeflow-based pipelines</strong></li>
    <li>You want <strong>Colab Enterprise</strong></li>
    </ul>
</div>
</div>
<hr>

<h3>🔗 Cross-Platform Interoperability</h3>
<p>Both platforms are <strong>not mutually exclusive</strong>. Modern agent architectures can span both clouds.</p>
{table_html(["Integration Point", "How It Works"], [
    ("<strong>A2A Protocol</strong>", "Both MAF and ADK support A2A — agents on Azure can call agents on GCP"),
    ("<strong>MCP Servers</strong>", "Both frameworks consume MCP tool servers — host on either cloud"),
    ("<strong>Foundry models in ADK</strong>", "ADK uses LiteLLM to call Azure OpenAI / Foundry endpoints"),
    ("<strong>Gemini in MAF</strong>", "MAF uses Foundry Model Garden or OpenAI-compatible Gemini endpoint"),
    ("<strong>OpenAI compatibility</strong>", "Both Foundry and Vertex AI expose OpenAI-compatible APIs"),
])}
<div class="info-box">💡 <strong>See page 7 (Cross-Model Usage)</strong> for implementation code showing how to use MAF with Gemini and ADK with Azure OpenAI.</div>
"""
    return page("Foundry vs Vertex AI", "8-foundry-vs-vertex.html", body)


# ════════════════════════════════════════════
# BUILD ALL
# ════════════════════════════════════════════
def write(filename, content):
    path = os.path.join(OUT, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {filename}")


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "css"), exist_ok=True)
    print("Building static site...")
    write("index.html", build_index())
    write("0-what-is.html", build_page0())
    write("1-agent-creation.html", build_page1())
    write("2-tool-integration.html", build_page2())
    write("3-memory-state.html", build_page3())
    write("4-multi-agent.html", build_page4())
    write("5-deployment.html", build_page5())
    write("6-third-party.html", build_page6())
    write("7-cross-model.html", build_page7())
    write("8-foundry-vs-vertex.html", build_page8())
    print(f"\nDone! {len(NAV_ITEMS)} pages generated in {OUT}/")
