# Architecture Comparison: Microsoft Agent Framework vs Google ADK

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Runtime Architecture](#runtime-architecture)
3. [Agent Lifecycle](#agent-lifecycle)
4. [Tool Integration Architecture](#tool-integration-architecture)
5. [Memory & State Architecture](#memory--state-architecture)
6. [Multi-Agent Orchestration](#multi-agent-orchestration)
7. [Deployment Architecture](#deployment-architecture)
8. [Security Architecture](#security-architecture)
9. [Enterprise Integration Architecture](#enterprise-integration-architecture)
10. [Data Flow Comparison](#data-flow-comparison)

---

## High-Level Architecture

### Microsoft Agent Framework (MAF)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry Platform                     │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│  Agent       │  Model       │  Evaluation  │  Prompt            │
│  Hosting     │  Deployment  │  Framework   │  Optimizer         │
├──────────────┴──────────────┴──────────────┴────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Microsoft Agent Framework SDK                    │   │
│  │  ┌────────────┐ ┌──────────┐ ┌────────────┐             │   │
│  │  │   Agent    │ │  Tools   │ │  Memory    │             │   │
│  │  │  Runtime   │ │  Engine  │ │  Manager   │             │   │
│  │  └─────┬──────┘ └────┬─────┘ └─────┬──────┘             │   │
│  │        │              │             │                     │   │
│  │  ┌─────┴──────────────┴─────────────┴──────┐             │   │
│  │  │         Graph Orchestrator              │             │   │
│  │  │  (Fan-out/in, Loop, Human-in-the-Loop)  │             │   │
│  │  └─────────────────────────────────────────┘             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Hosting Adapter Layer                            │   │
│  │  ┌────────────┐ ┌──────────────┐ ┌─────────────┐        │   │
│  │  │ Agent Fwk  │ │  LangGraph   │ │   Custom    │        │   │
│  │  │  Adapter   │ │   Adapter    │ │   Adapter   │        │   │
│  │  └────────────┘ └──────────────┘ └─────────────┘        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure: Cosmos DB │ Azure Storage │ AI Search │ ACR   │
└─────────────────────────────────────────────────────────────────┘
```

### Google ADK

```
┌─────────────────────────────────────────────────────────────────┐
│                    Google Cloud Platform                         │
├──────────────┬──────────────┬───────────────────────────────────┤
│  Cloud Run   │  Vertex AI   │  (No built-in eval/optimization)  │
├──────────────┴──────────────┴───────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             Google ADK SDK (Python only)                 │   │
│  │  ┌────────────┐ ┌──────────┐ ┌────────────┐             │   │
│  │  │   Agent    │ │  Tools   │ │  Session   │             │   │
│  │  │  Class     │ │  List    │ │  Service   │             │   │
│  │  └─────┬──────┘ └────┬─────┘ └─────┬──────┘             │   │
│  │        │              │             │                     │   │
│  │  ┌─────┴──────────────┴─────────────┴──────┐             │   │
│  │  │    Fixed Pattern Orchestrators          │             │   │
│  │  │  (Sequential, Parallel, Loop)           │             │   │
│  │  └─────────────────────────────────────────┘             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Server Layer (manual setup)                      │   │
│  │  ┌────────────┐ ┌──────────────┐                         │   │
│  │  │ adk cli    │ │  Custom HTTP │                         │   │
│  │  │ api_server │ │   Server     │                         │   │
│  │  └────────────┘ └──────────────┘                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Infrastructure: (BYO) — manual DB, storage, search setup      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Runtime Architecture

### MAF: Managed Runtime

```
Client Request
    │
    ▼
┌──────────────────────┐
│  Hosting Adapter     │  ← Protocol translation (HTTP → SDK)
│  Port 8088           │
│  POST /responses     │
└──────────┬───────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Agent      │────►│  Model           │  Azure OpenAI / Foundry
    │  Runtime    │     │  Deployment      │  (intelligent routing)
    └──────┬──────┘     └──────────────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Tool       │────►│  External        │  MCP, Functions, AI Search
    │  Engine     │     │  Services        │
    └──────┬──────┘     └──────────────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Memory     │────►│  Cosmos DB       │  Threads, Messages, Memory
    │  Manager    │     │  (managed)       │
    └─────────────┘     └──────────────────┘
```

### ADK: Manual Runtime

```
Client Request
    │
    ▼
┌──────────────────────┐
│  Custom HTTP Server  │  ← Manual setup (no standard adapter)
│  or adk api_server   │
│  Port: configurable  │
└──────────┬───────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Runner     │────►│  Gemini / LiteLLM│  Model provider
    │  run_async()│     │  (manual config)  │
    └──────┬──────┘     └──────────────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Tool       │────►│  Custom          │  Manual function tools
    │  Execution  │     │  Connectors      │
    └──────┬──────┘     └──────────────────┘
           │
    ┌──────▼──────┐     ┌──────────────────┐
    │  Session    │────►│  In-Memory /     │  Default: volatile
    │  Service    │     │  SQLite (BYO)    │
    └─────────────┘     └──────────────────┘
```

---

## Agent Lifecycle

| Phase | MAF | ADK |
|-------|-----|-----|
| **Define** | SDK code + `agent.yaml` declarative config | Python code only |
| **Configure** | Model deployment, tools, memory — all in `agent.yaml` | Constructor kwargs in Python |
| **Test locally** | `agentdev` CLI + Agent Inspector UI | `adk web` dev server |
| **Containerize** | Standard Dockerfile + hosting adapter (port 8088) | Manual Dockerfile + custom server |
| **Deploy** | `az ai foundry agent create` → managed hosting | `gcloud run deploy` → manual config |
| **Monitor** | Application Insights (automatic) | Cloud Monitoring (manual setup) |
| **Evaluate** | Built-in evaluators (intent, task, groundedness, tool accuracy) | Manual test scripts |
| **Optimize** | Prompt optimizer from production traces | Manual prompt iteration |
| **Version** | `agent.yaml` version field + Foundry versioning | Git only (no agent versioning) |
| **Scale** | Foundry auto-scaling | Cloud Run auto-scaling (manual config) |

---

## Tool Integration Architecture

### MAF Tool Type Hierarchy

```
ToolSet (composable container)
├── FunctionTool                 — Custom Python functions
├── AzureAISearchToolDefinition  — Enterprise RAG (vector/semantic/hybrid)
├── WebSearchPreviewToolDefinition — Free web search (no setup)
├── CodeInterpreterToolDefinition  — Sandboxed Python execution
├── BingGroundingToolDefinition    — Enterprise Bing search
├── FileSearchToolDefinition       — Vector store file search
└── McpToolDefinition              — Any MCP server (remote tools)
    └── allowed_tools[]            — Fine-grained access control
```

### ADK Tool Type Hierarchy

```
tools=[] (simple list)
├── Python functions             — Custom function tools
├── google_search                — Google Search (only built-in)
├── MCPToolset.from_server()     — MCP server connection
│   └── (manual cleanup required)
└── (everything else: build manually)
    ├── No RAG tool
    ├── No code interpreter
    ├── No file search
    └── No enterprise search
```

### Tool Count Comparison

| Tool Type | MAF | ADK |
|-----------|-----|-----|
| Function tools | ✅ | ✅ |
| Web search | ✅ WebSearchPreview + Bing | ⚠️ Google Search only |
| RAG / Vector search | ✅ Azure AI Search | ❌ Manual build |
| Code interpreter | ✅ Sandboxed | ❌ Manual build |
| File search | ✅ Vector store | ❌ Manual build |
| MCP | ✅ Native with access control | ⚠️ MCPToolset (manual cleanup) |
| **Total built-in** | **6+** | **1** |

---

## Memory & State Architecture

### MAF Memory Stack

```
┌────────────────────────────────────────────┐
│ Layer 4: User Profile Memory               │
│ ├── Auto-learns preferences over time      │
│ ├── Embedding-based retrieval              │
│ └── Per-user isolation ({{$userId}})       │
├────────────────────────────────────────────┤
│ Layer 3: Chat Summary Memory               │
│ ├── Auto-summarizes on token overflow      │
│ └── Semantic search over past conversations│
├────────────────────────────────────────────┤
│ Layer 2: Thread Messages                   │
│ ├── Full message history (Cosmos DB)       │
│ └── Multi-turn conversation persistence    │
├────────────────────────────────────────────┤
│ Layer 1: Thread Container                  │
│ ├── Managed by Foundry                     │
│ └── Cosmos DB storage (production-ready)   │
└────────────────────────────────────────────┘
```

### ADK Memory Stack

```
┌────────────────────────────────────────────┐
│ Layer 2: Session State                     │
│ ├── Simple key-value dictionary            │
│ └── Manual management only                 │
├────────────────────────────────────────────┤
│ Layer 1: Session Storage                   │
│ ├── InMemorySessionService (default)       │
│ │   └── ❌ Lost on restart                 │
│ └── DatabaseSessionService (manual setup)  │
│     └── SQLite / PostgreSQL (BYO)          │
├────────────────────────────────────────────┤
│ (No higher layers — build from scratch)    │
│ ❌ No summary memory                       │
│ ❌ No user profile memory                  │
│ ❌ No embedding-based retrieval            │
└────────────────────────────────────────────┘
```

---

## Multi-Agent Orchestration

### MAF: Graph-Based

```
Capabilities:
├── AgentWorkflow (directed graph)
│   ├── Conditional edges (deterministic routing)
│   ├── Fan-out / Fan-in (parallel + aggregation)
│   ├── Loop with exit conditions
│   ├── Human-in-the-Loop checkpoints
│   └── Switch-case branching
├── All agents run in single process
├── Deterministic function nodes between agents
└── Type-safe transitions with context passing

Complexity: O(1) deployment — one container for entire workflow
```

### ADK: Fixed Patterns

```
Capabilities:
├── SequentialAgent (A → B → C)
├── ParallelAgent (A + B + C → results list)
├── LoopAgent (repeat N times)
└── A2A Protocol (for complex patterns)
    ├── Each agent = separate HTTP server
    ├── Manual message routing
    └── External orchestration required

Complexity: O(N) deployments for N agents in complex patterns
```

### Orchestration Pattern Support

| Pattern | MAF | ADK |
|---------|-----|-----|
| Sequential | ✅ Graph edge | ✅ SequentialAgent |
| Parallel | ✅ Fan-out | ✅ ParallelAgent |
| Parallel + Aggregate | ✅ Fan-in | ❌ Manual |
| Conditional routing | ✅ Conditional edges | ❌ Manual |
| Loop with exit | ✅ Loop node | ✅ LoopAgent |
| Human approval | ✅ Checkpoint | ❌ Manual |
| Switch-case | ✅ Built-in | ❌ Manual |
| Cross-process agents | ✅ Optional | ⚠️ Required (A2A) |

---

## Deployment Architecture

### MAF: Foundry Platform

```
Developer Machine                    Azure AI Foundry
┌────────────────┐                  ┌─────────────────────────────┐
│ agent code     │  docker build    │  Container Registry (ACR)   │
│ agent.yaml     │ ──────────────►  │  ┌─────────────────────┐    │
│ Dockerfile     │                  │  │ agent-image:1.2.0   │    │
└────────────────┘                  │  └─────────┬───────────┘    │
                                    │            │                │
                                    │  ┌─────────▼───────────┐    │
                                    │  │  Hosted Agent        │    │
                                    │  │  ├─ Managed Identity │    │
                                    │  │  ├─ RBAC             │    │
                                    │  │  ├─ Auto-scaling     │    │
                                    │  │  ├─ App Insights     │    │
                                    │  │  └─ /responses API   │    │
                                    │  └─────────────────────┘    │
                                    │                             │
                                    │  ┌─────────────────────┐    │
                                    │  │  Evaluation          │    │
                                    │  │  ├─ Batch eval       │    │
                                    │  │  ├─ Prompt optimizer │    │
                                    │  │  └─ Dataset harvest  │    │
                                    │  └─────────────────────┘    │
                                    └─────────────────────────────┘
```

### ADK: Manual Cloud Deployment

```
Developer Machine                    Google Cloud Platform
┌────────────────┐                  ┌─────────────────────────────┐
│ agent code     │  gcloud builds   │  Container Registry (GCR)   │
│ Dockerfile     │ ──────────────►  │  ┌─────────────────────┐    │
│ (no metadata)  │                  │  │ agent-image:latest   │    │
└────────────────┘                  │  └─────────┬───────────┘    │
                                    │            │                │
                                    │  ┌─────────▼───────────┐    │
                                    │  │  Cloud Run           │    │
                                    │  │  ├─ IAM (manual)     │    │
                                    │  │  ├─ Scaling (config) │    │
                                    │  │  ├─ Monitoring(sep)  │    │
                                    │  │  └─ Custom endpoint  │    │
                                    │  └─────────────────────┘    │
                                    │                             │
                                    │  (No built-in eval/optim)  │
                                    └─────────────────────────────┘
```

---

## Security Architecture

### MAF: Zero-Trust Enterprise Security

```
┌──────────────────────────────────────────────┐
│              Azure AD / Entra ID             │
│  ┌─────────────────────────────────────────┐ │
│  │         Managed Identity                │ │
│  │  ├─ Agent → OpenAI (model calls)        │ │
│  │  ├─ Agent → Cosmos DB (threads)         │ │
│  │  ├─ Agent → AI Search (RAG)             │ │
│  │  ├─ Agent → Key Vault (secrets)         │ │
│  │  ├─ Agent → Snowflake (SSO)             │ │
│  │  └─ Agent → Fabric (same identity)      │ │
│  └─────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │         RBAC                            │ │
│  │  ├─ Cognitive Services User             │ │
│  │  ├─ Search Index Data Reader            │ │
│  │  └─ Custom roles per agent              │ │
│  └─────────────────────────────────────────┘ │
│  No API keys in code. No secrets in env.     │
│  All auth via DefaultAzureCredential.        │
└──────────────────────────────────────────────┘
```

### ADK: Manual Credential Management

```
┌──────────────────────────────────────────────┐
│              GCP IAM (manual per service)     │
│  ┌─────────────────────────────────────────┐ │
│  │         Environment Variables           │ │
│  │  ├─ GOOGLE_API_KEY (Gemini)             │ │
│  │  ├─ SNOWFLAKE_USER + PASSWORD           │ │
│  │  ├─ BLUEYONDER_API_KEY                  │ │
│  │  ├─ AZURE_CLIENT_ID + SECRET (Fabric)   │ │
│  │  └─ DB_CONNECTION_STRING                │ │
│  └─────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │         Service Accounts               │ │
│  │  ├─ Manual IAM binding                  │ │
│  │  ├─ Per-service key rotation            │ │
│  │  └─ No unified identity plane           │ │
│  └─────────────────────────────────────────┘ │
│  API keys and secrets in env vars or files.  │
│  Manual rotation for each service.           │
└──────────────────────────────────────────────┘
```

---

## Enterprise Integration Architecture

### MAF: Unified Identity Plane

```
                    ┌──────────────┐
                    │  Azure AD    │
                    │  (one token) │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌─────▼──────┐
        │ Snowflake │ │ Fabric │ │ AI Search  │
        │ (AD SSO)  │ │(native)│ │ (built-in) │
        └───────────┘ └────────┘ └────────────┘
              │            │            │
              ▼            ▼            ▼
        ┌───────────────────────────────────┐
        │        MAF Agent                  │
        │  All services: one credential     │
        │  DefaultAzureCredential()         │
        └───────────────────────────────────┘
```

### ADK: Fragmented Identity

```
        ┌───────────┐ ┌────────┐ ┌───────────┐
        │ Snowflake │ │ Fabric │ │   GCP     │
        │ user/pass │ │client/ │ │  API key  │
        │           │ │secret  │ │           │
        └─────┬─────┘ └───┬────┘ └─────┬─────┘
              │            │            │
              ▼            ▼            ▼
        ┌───────────────────────────────────┐
        │        ADK Agent                  │
        │  3 separate credential sets       │
        │  3 different auth flows           │
        │  Manual rotation for each         │
        └───────────────────────────────────┘
```

---

## Data Flow Comparison

### MAF: Streaming Response Flow

```
User → POST /responses
          │
          ▼
   Hosting Adapter (protocol translation)
          │
          ▼
   Agent Runtime (tool selection, memory lookup)
          │
          ├──► Tool Call Event (SSE)     → client sees tool usage
          ├──► Text Delta Event (SSE)    → client sees partial text
          ├──► Citation Event (SSE)      → client sees sources
          └──► Response Complete (SSE)   → client gets full response

Events: response.output_text.delta
        response.tool_call
        response.output_item.done (annotations/citations)
```

### ADK: Event Iteration Flow

```
User → runner.run_async(new_message=content)
          │
          ▼
   Runner (tool selection, session lookup)
          │
          ├──► Event with content.parts[].text
          ├──► Event with tool_call
          └──► (no standard citation format)

Events: Custom event types
        Manual parsing required
        No standard SSE protocol
```

---

## Summary: Architecture Decision Factors

| Factor | MAF Winner? | Why |
|--------|-------------|-----|
| Platform integration | ✅ | Azure AI Foundry is a complete agent platform |
| Tool ecosystem | ✅ | 6+ built-in enterprise tools vs 1 |
| Memory sophistication | ✅ | 4-layer memory stack vs 2-layer |
| Orchestration flexibility | ✅ | Graph-based vs fixed patterns |
| Security model | ✅ | Managed Identity vs manual credentials |
| Multi-language | ✅ | Python + .NET vs Python only |
| Eval & optimization | ✅ | Built-in vs manual |
| API compatibility | ✅ | OpenAI Responses API vs proprietary |
| Rapid prototyping | ⚠️ | ADK has simpler setup for quick experiments |
| GCP-native workloads | ⚠️ | ADK is better for pure GCP shops |
| Gemini-first models | ⚠️ | ADK has native Gemini integration |
