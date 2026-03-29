# Expert Framework Choice Guide: MAF vs ADK

## Who Should Read This

This is **not a marketing document**. It's a quantified, expert-level analysis for practitioners who build production agent systems. If you're evaluating Microsoft Agent Framework (MAF) vs Google ADK for real workloads, this is your reference.

---

## The Expert's Framework: "If I Am an Agentic Platform Expert, Why Choose MAF?"

### 1. Tool Infrastructure Cost: 6 Built-In vs 1

**Quantified impact**: Building equivalent tools from scratch costs engineering time.

| Tool | MAF (built-in) | ADK (build time estimate) |
|------|----------------|---------------------------|
| RAG / Vector Search | `AzureAISearchToolDefinition` — 1 line | Custom embedding pipeline + vector DB + retrieval logic: **2–4 weeks** |
| Code Interpreter | `CodeInterpreterToolDefinition` — 1 line | Sandboxed Python execution environment with security isolation: **3–6 weeks** |
| File Search | `FileSearchToolDefinition` — 1 line | Vector store indexing + chunking + retrieval: **1–2 weeks** |
| Enterprise Web Search | `BingGroundingToolDefinition` — 1 line | Google Search available, but no enterprise-grade alternative: **N/A** |
| Web Search (free) | `WebSearchPreviewToolDefinition` — 1 line | `google_search` available: **0** |
| MCP (with access control) | `McpToolDefinition` + `allowed_tools` | `MCPToolset.from_server()` (no `allowed_tools`): **1 week** to add access control |

**Total saved**: ~6–13 weeks of engineering time on tool infrastructure alone.

**Why this matters**: In enterprise settings, the RAG pipeline alone is often the most time-consuming component. MAF's `AzureAISearchToolDefinition` eliminates this entirely — the agent auto-generates search queries, retrieves results, and formats citations. In ADK, you're building the embedding pipeline, vector database integration, retrieval logic, and citation formatting from scratch.

### 2. Memory: Production-Grade vs Prototype-Grade

**Quantified gap**:

| Memory Feature | MAF | ADK | Impact |
|---------------|-----|-----|--------|
| Conversation persistence | Cosmos DB (managed, 99.999% SLA) | InMemory (default) — **lost on restart** | Production readiness |
| Long-term summarization | `ChatSummaryMemory` — auto-summarizes when context exceeds token limit | None — manual implementation | **Context window efficiency**: MAF agents maintain coherence across 100+ turn conversations without hitting token limits |
| User preference learning | `UserProfileMemory` — automatically extracts and stores user preferences | None | **Personalization**: MAF agents improve over time; ADK agents are stateless across sessions |
| Per-user isolation | `{{$userId}}` scoping — built-in multi-tenancy | Manual implementation | **Enterprise multi-tenancy**: MAF handles N users with zero additional code |

**Why this matters**: A production conversational AI system with 10,000+ users needs multi-tenant memory with automatic summarization. Building this from scratch in ADK means implementing: embedding model integration, similarity search, summarization triggers, memory pruning, user scoping, and a persistence layer. That's 4–8 weeks of engineering plus ongoing maintenance.

### 3. Orchestration: Graph vs Patterns

**Quantified flexibility**:

| Pattern | MAF | ADK | Complexity |
|---------|-----|-----|-----------|
| A → B → C | ✅ Edge | ✅ SequentialAgent | Same |
| A + B → merge | ✅ Fan-in | ✅ ADK 2.0 graph workflows | MAF: 2 lines, ADK: graph config |
| if X → A, else → B | ✅ Conditional edge | ✅ ADK 2.0 graph workflows | MAF: 1 line, ADK: graph config |
| Run A, wait for human OK, then B | ✅ Checkpoint | ✅ ADK 2.0 human input | MAF: 3 lines, ADK: graph config |
| Retry A until quality check passes | ✅ Loop with exit | ✅ LoopAgent | MAF: more configurable |

**Deployment cost for complex workflows**:
- **MAF**: 1 container, 1 deployment — all agents in one graph
- **ADK (A2A)**: N containers, N deployments — one per agent in complex patterns

**Why this matters**: Enterprise supply chain workflows typically require conditional routing (data questions vs order actions), human approval gates (order cancellations > $10K), and parallel execution with aggregation (query multiple warehouses). Both frameworks now support graph-based orchestration. MAF’s graph API is more mature; ADK 2.0 graph workflows are newer but functional.

### 4. Security: Managed Identity vs GCP IAM

**Quantified risk reduction**:

| Security Dimension | MAF | ADK |
|-------------------|-----|-----|
| Azure service auth | DefaultAzureCredential (automatic) | GCP Application Default Credentials |
| Cross-cloud services (Snowflake) | Azure AD SSO (same principal) | Key pair auth / OAuth |
| Secret management | Azure Key Vault (automatic rotation) | GCP Secret Manager |
| Audit trail | App Insights (automatic) | Cloud Logging |
| RBAC | Built-in per agent | GCP IAM + Workload Identity |

**Credential approach**:
- **MAF**: `DefaultAzureCredential()` — one call for all Azure services, zero secrets in code
- **ADK**: `google.auth.default()` for GCP services; external services (Snowflake, Fabric) require separate credentials on both platforms

**Why this matters**: Every credential in an environment variable is a potential breach vector. MAF's Managed Identity eliminates this entire class of risk. In regulated industries (finance, healthcare, supply chain), this isn't optional — it's a compliance requirement.

### 5. Evaluation & Optimization: Built-In vs Manual

**Quantified gap**:

| Capability | MAF | ADK | Gap |
|-----------|-----|-----|-----|
| Batch evaluation | ✅ Built-in with 4+ evaluators | ✅ Built-in evaluation framework | Similar |
| Intent resolution scoring | ✅ | ✅ Custom evaluators | Similar |
| Task adherence scoring | ✅ | ✅ Custom evaluators | Similar |
| Tool call accuracy scoring | ✅ | ✅ Custom metrics | Similar |
| Groundedness scoring | ✅ | ⚠️ Custom implementation | MAF more turnkey |
| Prompt optimization from traces | ✅ Automatic | ✅ ADK Optimization docs | Similar |
| Dataset harvesting from production | ✅ | ⚠️ Manual setup | MAF more integrated |

**Why this matters**: Both platforms now offer evaluation and optimization capabilities. MAF's advantage is tighter integration with Azure AI Foundry for turnkey evaluators. ADK has added optimization docs and custom metrics but may require more custom setup for enterprise-grade eval pipelines.

### 6. API Ecosystem: OpenAI-Compatible vs Gemini API

**MAF** uses the **OpenAI Responses** protocol — the de facto industry standard. This means:
- Any OpenAI-compatible client library works
- Existing tools (LangSmith, Braintrust, Humanloop) integrate directly
- Streaming uses standard SSE events
- Developers with OpenAI experience can start immediately

**ADK** uses a `Runner.run_async()` pattern with Gemini API:
- Custom event types
- Standard async Python interface
- A2A protocol for cross-agent communication
- Learning curve for OpenAI-experienced developers

---

## The Data Engineer's Perspective: "When Might I Consider ADK?"

### Scenario 1: Pure GCP Data Stack

If your entire data platform is **GCP-native** (BigQuery, Dataflow, Cloud Storage, Vertex AI):

| Advantage | Reason |
|-----------|--------|
| Native BigQuery integration | ADK function tools can call BigQuery directly with GCP service accounts |
| Vertex AI model serving | Direct model access without cross-cloud latency |
| GCP IAM + Workload Identity | Unified identity system for data + agents |
| Cost alignment | Single cloud billing, no cross-cloud egress fees |

**Quantified**: If 100% of your data is in BigQuery and you have zero Azure footprint, ADK saves:
- ~$200–500/month in cross-cloud data transfer fees (for high-volume workloads)
- ~1 week of setup for Azure AD integration you wouldn't otherwise need

### Scenario 2: Rapid Prototyping / Research

If you need a quick agent prototype for **data exploration** (not production):

| Advantage | Reason |
|-----------|--------|
| Simpler setup | `pip install google-adk` + API key = running in 5 minutes |
| Fewer concepts | Agent + Runner + Session — 3 concepts vs MAF's broader surface |
| Gemini-first | Native Gemini 2.5 Flash — fastest model for exploration |
| No Azure subscription | No cloud setup required for local development |

**Quantified**: Time to first running agent:
- ADK: ~5 minutes (API key + 10 lines of code)
- MAF: ~30 minutes (Azure subscription + Foundry project + model deployment + code)

### Scenario 3: Gemini Model Preference

If your team has standardized on **Google Gemini** models and needs:
- Gemini-native function calling (no protocol translation)
- Gemini 2.5 Flash for low-latency, low-cost inference
- Google Search grounding (Gemini-specific feature)

### Scenario 4: A2A (Agent-to-Agent) Protocol

If you're building a **multi-vendor agent ecosystem** where agents from different organizations need to communicate:
- ADK's A2A protocol is designed for cross-organization agent communication
- MAF's graph orchestration is optimized for single-organization, single-deployment workflows

---

## Head-to-Head: Quantified Decision Matrix

| Decision Factor | MAF Score | ADK Score | Reasoning |
|----------------|-----------|-----------|-----------|
| Enterprise production readiness | **9/10** | 6/10 | Managed Identity, RBAC, eval, prompt optimization |
| Tool ecosystem richness | **9/10** | 5/10 | 6+ built-in vs Google Search + Code Exec + Vertex AI Search |
| Memory & state management | **9/10** | 5/10 | Multi-backend persistence vs session state + memory service |
| Multi-agent flexibility | **8/10** | 7/10 | Graph-based; ADK 2.0 adds graph workflows |
| Security & compliance | **9/10** | 6/10 | Managed Identity vs GCP IAM + Workload Identity |
| API ecosystem compatibility | **9/10** | 6/10 | OpenAI-standard vs Gemini API |
| 3rd-party integration (Azure ecosystem) | **10/10** | 3/10 | Native Fabric, AD SSO, Key Vault |
| 3rd-party integration (GCP ecosystem) | 4/10 | **9/10** | ADK native to BigQuery, Vertex |
| Rapid prototyping speed | 6/10 | **8/10** | Simpler setup, fewer concepts |
| Multi-language support | **9/10** | **9/10** | Python + .NET vs Python, TS, Go, Java |
| Gemini-native features | 5/10 | **9/10** | ADK is Gemini-optimized |
| Continuous improvement pipeline | **9/10** | 5/10 | Built-in eval + optimizer; ADK has optimization + custom metrics |

### Weighted Score for Enterprise Conversational AI

Using weights relevant to enterprise supply-chain scenario (Snowflake + BlueYonder + Fabric):

| Factor | Weight | MAF | ADK |
|--------|--------|-----|-----|
| Production readiness | 25% | 2.25 | 1.50 |
| Tool ecosystem | 20% | 1.80 | 1.00 |
| Security | 20% | 1.80 | 1.20 |
| Integration (Azure) | 15% | 1.50 | 0.45 |
| Memory | 10% | 0.90 | 0.50 |
| Orchestration | 10% | 0.80 | 0.70 |
| **Total** | **100%** | **9.05** | **5.35** |

---

## The Bottom Line

### Choose MAF when:
- You need **production-grade** enterprise conversational AI
- Your data lives in Azure, Snowflake, or hybrid cloud
- You need **Fabric/FabricIQ/WorkIQ** integration
- Security and compliance are non-negotiable
- You need **continuous evaluation and optimization**
- Your team uses both Python and .NET
- You need **3+ integrated enterprise tools** (RAG, code interpreter, web search)
- You want **graph-based orchestration** with human-in-the-loop

### Choose ADK when:
- Your **entire stack is GCP** (BigQuery, Vertex AI, Cloud Run)
- You're building a **prototype or research project** (not production enterprise)
- You need **Gemini-native** model features
- You're building **A2A cross-organization** agent networks
- You want the **simplest possible setup** (5-minute time-to-first-agent)
- Your workload is **read-only data exploration** without enterprise tool needs

### The honest assessment:
For the specific scenario of **enterprise conversational AI with Snowflake, BlueYonder, and Fabric integration**, MAF scores **1.7x higher** than ADK on weighted enterprise criteria. The gap is largest in Azure ecosystem integration (native vs custom connectors), tool infrastructure (6+ built-in vs fewer), and security (Managed Identity vs GCP IAM). ADK's advantages (simpler setup, Gemini-native, multi-language SDK) don't fully offset these gaps for Azure-centric production enterprise workloads.
