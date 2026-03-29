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
│  Cloud Run   │  Vertex AI   │  ADK Eval + Optimization          │
├──────────────┴──────────────┴───────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             Google ADK SDK (Python, TS, Go, Java)          │   │
│  │  ┌────────────┐ ┌──────────┐ ┌────────────┐             │   │
│  │  │   Agent    │ │  Tools   │ │  Session   │             │   │
│  │  │  Class     │ │  List    │ │  Service   │             │   │
│  │  └─────┬──────┘ └────┬─────┘ └─────┬──────┘             │   │
│  │        │              │             │                     │   │
│  │  ┌─────┴──────────────┴─────────────┴──────┐             │   │
│  │  │    Built-in + ADK 2.0 Graph Orchestrators   │             │   │
│  │  │  (Sequential, Parallel, Loop, Graph)      │             │   │
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
| **Deploy** | `az ai foundry agent create` → managed hosting | `gcloud run deploy` → Cloud Run |
| **Monitor** | Application Insights (automatic) | Cloud Monitoring + Cloud Logging |
| **Evaluate** | Built-in evaluators (intent, task, groundedness, tool accuracy) | Built-in evaluation framework + custom metrics |
| **Optimize** | Prompt optimizer from production traces | ADK Optimization (prompt optimization docs) |
| **Version** | `agent.yaml` version field + Foundry versioning | Agent Config (JSON/YAML) + Git |
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
├── google_search                — Google Search Grounding
├── built_in_code_execution      — Code execution via Gemini
├── vertex_ai_search_tool        — Vertex AI Search Grounding
├── MCPToolset.from_server()     — MCP server connection
└── OpenAPI tools                — REST API integration
```

### Tool Count Comparison

| Tool Type | MAF | ADK |
|-----------|-----|-----|
| Function tools | ✅ | ✅ |
| Web search | ✅ WebSearchPreview + Bing | ✅ Google Search Grounding |
| RAG / Vector search | ✅ Azure AI Search | ✅ Vertex AI Search Grounding |
| Code interpreter | ✅ Sandboxed | ✅ BuiltInCodeExecutor |
| File search | ✅ Vector store | ⚠️ Manual build |
| MCP | ✅ Native with access control | ✅ MCPToolset |
| **Total built-in** | **6+** | **4+** |

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
│ Layer 3: Memory Service                    │
│ ├── Cross-session recall                   │
│ └── Memory-based context enrichment        │
├────────────────────────────────────────────┤
│ Layer 2: Session State + Context Mgmt      │
│ ├── Key-value dictionary per session       │
│ ├── output_key auto-save                   │
│ ├── Context caching (reduce token costs)   │
│ ├── Context compression (auto-summarize)   │
│ └── Session rewind (time-travel)           │
├────────────────────────────────────────────┤
│ Layer 1: Session Storage                   │
│ ├── InMemorySessionService (default)       │
│ └── DatabaseSessionService (SQLite/PG)     │
├────────────────────────────────────────────┤
│ Artifacts                                  │
│ └── File/binary data management            │
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

### ADK: Built-in Patterns + ADK 2.0 Graph Workflows

```
Capabilities:
├── SequentialAgent (A → B → C)
├── ParallelAgent (A + B + C → results list)
├── LoopAgent (repeat N times)
├── ADK 2.0 Graph Workflows
│   ├── Conditional routing
│   ├── Dynamic workflows
│   ├── Human input integration
│   └── Collaborative agents
└── A2A Protocol (for cross-organization agents)
    ├── Each agent = separate HTTP server
    └── Cross-organization communication

Complexity: O(1) for graph workflows, O(N) for A2A patterns
```

### Orchestration Pattern Support

| Pattern | MAF | ADK |
|---------|-----|-----|
| Sequential | ✅ Graph edge | ✅ SequentialAgent |
| Parallel | ✅ Fan-out | ✅ ParallelAgent |
| Parallel + Aggregate | ✅ Fan-in | ✅ ADK 2.0 graph |
| Conditional routing | ✅ Conditional edges | ✅ ADK 2.0 graph |
| Loop with exit | ✅ Loop node | ✅ LoopAgent |
| Human approval | ✅ Checkpoint | ✅ ADK 2.0 human input |
| Switch-case | ✅ Built-in | ⚠️ Custom routing |
| Cross-process agents | ✅ Optional | ✅ A2A protocol |

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
                                    │  │  ├─ IAM (config)     │    │
                                    │  │  ├─ Scaling (config) │    │
                                    │  │  ├─ Monitoring       │    │
                                    │  │  └─ Custom endpoint  │    │
                                    │  └─────────────────────┘    │
                                    │                             │
                                    │  ADK Eval + Optimization    │
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

### ADK: GCP IAM + Workload Identity

```
┌──────────────────────────────────────────────┐
│              GCP IAM + Workload Identity      │
│  ┌─────────────────────────────────────────┐ │
│  │         Application Default Credentials │ │
│  │  ├─ Agent → Gemini API (model calls)    │ │
│  │  ├─ Agent → BigQuery (data)             │ │
│  │  ├─ Agent → Vertex AI (ML)              │ │
│  │  ├─ Agent → Secret Manager (secrets)    │ │
│  │  └─ Agent → Cloud Storage (artifacts)   │ │
│  └─────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────┐ │
│  │         Service Accounts               │ │
│  │  ├─ Workload Identity Federation        │ │
│  │  ├─ IAM role binding per service        │ │
│  │  └─ Cross-cloud via federation          │ │
│  └─────────────────────────────────────────┘ │
│  GCP services: google.auth.default().        │
│  Cross-cloud services: separate credentials. │
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
          └──► Gemini Live API streaming

Events: Gemini API event types
        Standard async iteration
```

---

## Summary: Architecture Decision Factors

| Factor | MAF Winner? | Why |
|--------|-------------|-----|
| Platform integration | ✅ | Azure AI Foundry is a complete agent platform |
| Tool ecosystem | ✅ | 6+ built-in enterprise tools vs 4+ |
| Memory sophistication | ✅ | More persistence backends; ADK has unique context features |
| Orchestration flexibility | ✅ | More mature graph API; ADK 2.0 adds graph workflows |
| Security model | ✅ | Managed Identity vs GCP IAM + Workload Identity |
| Multi-language | ≈ | Python + .NET vs Python, TS, Go, Java |
| Eval & optimization | ✅ | More turnkey evaluators; ADK has optimization + custom metrics |
| API compatibility | ✅ | OpenAI Responses protocol vs Gemini API |
| Rapid prototyping | ⚠️ | ADK has simpler setup for quick experiments |
| GCP-native workloads | ⚠️ | ADK is better for pure GCP shops |
| Gemini-first models | ⚠️ | ADK has native Gemini integration |
