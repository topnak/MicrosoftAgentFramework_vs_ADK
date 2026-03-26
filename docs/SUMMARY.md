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

### 3. Orchestration: Graph vs Fixed Patterns

**Quantified flexibility**:

| Pattern | MAF | ADK | Complexity |
|---------|-----|-----|-----------|
| A → B → C | ✅ Edge | ✅ SequentialAgent | Same |
| A + B → merge | ✅ Fan-in | ❌ Manual aggregation | MAF: 2 lines, ADK: ~100 lines custom |
| if X → A, else → B | ✅ Conditional edge | ❌ Manual routing | MAF: 1 line, ADK: custom orchestrator |
| Run A, wait for human OK, then B | ✅ Checkpoint | ❌ Custom webhook + state machine | MAF: 3 lines, ADK: ~200 lines + external state |
| Retry A until quality check passes | ✅ Loop with exit | ⚠️ LoopAgent (no custom exit) | MAF: more flexible |

**Deployment cost for complex workflows**:
- **MAF**: 1 container, 1 deployment — all agents in one graph
- **ADK (A2A)**: N containers, N deployments — one per agent in complex patterns

**Why this matters**: Enterprise supply chain workflows typically require conditional routing (data questions vs order actions), human approval gates (order cancellations > $10K), and parallel execution with aggregation (query multiple warehouses). MAF handles this in a single graph definition. ADK requires A2A protocol with separate HTTP services for each agent — multiplying infrastructure cost, networking complexity, and failure modes.

### 4. Security: Zero-Credential vs N-Credential

**Quantified risk reduction**:

| Security Dimension | MAF | ADK |
|-------------------|-----|-----|
| Credentials in code | 0 | N (one per external service) |
| Azure AD SSO for Snowflake | ✅ (same principal) | ❌ (username/password) |
| Secret rotation | Automatic (Managed Identity) | Manual per credential |
| Audit trail | App Insights (automatic) | Manual logging |
| RBAC | Built-in per agent | Manual IAM per service |

**Credential exposure surface**:
- **MAF**: `DefaultAzureCredential()` — one call, zero secrets in code or env
- **ADK**: `SNOWFLAKE_PASSWORD`, `BY_API_KEY`, `AZURE_CLIENT_SECRET`, `GOOGLE_API_KEY` — 4+ secrets to manage, rotate, and audit

**Why this matters**: Every credential in an environment variable is a potential breach vector. MAF's Managed Identity eliminates this entire class of risk. In regulated industries (finance, healthcare, supply chain), this isn't optional — it's a compliance requirement.

### 5. Evaluation & Optimization: Built-In vs Manual

**Quantified gap**:

| Capability | MAF | ADK | Build cost for ADK |
|-----------|-----|-----|--------------------|
| Batch evaluation | ✅ Built-in with 4+ evaluators | ❌ | 2–3 weeks |
| Intent resolution scoring | ✅ | ❌ | 1 week |
| Task adherence scoring | ✅ | ❌ | 1 week |
| Tool call accuracy scoring | ✅ | ❌ | 1 week |
| Groundedness scoring | ✅ | ❌ | 1–2 weeks |
| Prompt optimization from traces | ✅ Automatic | ❌ | 3–4 weeks |
| Dataset harvesting from production | ✅ | ❌ | 2–3 weeks |

**Total to build equivalent in ADK**: ~12–16 weeks of engineering

**Why this matters**: Production agents drift. User patterns change. Model versions update. Without automated evaluation, you're flying blind. MAF's prompt optimizer automatically improves instructions by analyzing production traces — this creates a continuous improvement loop that's extremely expensive to replicate.

### 6. API Ecosystem: OpenAI-Compatible vs Proprietary

**MAF** uses the **OpenAI Responses API v2** — the de facto industry standard. This means:
- Any OpenAI-compatible client library works
- Existing tools (LangSmith, Braintrust, Humanloop) integrate directly
- Streaming uses standard SSE events
- Developers with OpenAI experience can start immediately

**ADK** uses a proprietary `Runner.run_async()` pattern:
- Custom event types
- Custom client required
- No third-party tool compatibility
- Learning curve for OpenAI-experienced developers

---

## The Data Engineer's Perspective: "When Might I Consider ADK?"

### Scenario 1: Pure GCP Data Stack

If your entire data platform is **GCP-native** (BigQuery, Dataflow, Cloud Storage, Vertex AI):

| Advantage | Reason |
|-----------|--------|
| Native BigQuery integration | ADK function tools can call BigQuery directly with GCP service accounts |
| Vertex AI model serving | Direct model access without cross-cloud latency |
| Cloud IAM consistency | One IAM system for data + agents |
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
| Gemini-first | Native Gemini 2.0 Flash — fastest model for exploration |
| No Azure subscription | No cloud setup required for local development |

**Quantified**: Time to first running agent:
- ADK: ~5 minutes (API key + 10 lines of code)
- MAF: ~30 minutes (Azure subscription + Foundry project + model deployment + code)

### Scenario 3: Gemini Model Preference

If your team has standardized on **Google Gemini** models and needs:
- Gemini-native function calling (no protocol translation)
- Gemini 2.0 Flash for low-latency, low-cost inference
- Google Search grounding (Gemini-specific feature)

### Scenario 4: A2A (Agent-to-Agent) Protocol

If you're building a **multi-vendor agent ecosystem** where agents from different organizations need to communicate:
- ADK's A2A protocol is designed for cross-organization agent communication
- MAF's graph orchestration is optimized for single-organization, single-deployment workflows

---

## Head-to-Head: Quantified Decision Matrix

| Decision Factor | MAF Score | ADK Score | Reasoning |
|----------------|-----------|-----------|-----------|
| Enterprise production readiness | **9/10** | 5/10 | Managed Identity, RBAC, eval, prompt optimization |
| Tool ecosystem richness | **9/10** | 4/10 | 6+ built-in vs 1 |
| Memory & state management | **9/10** | 3/10 | 4-layer memory stack vs basic sessions |
| Multi-agent flexibility | **8/10** | 5/10 | Graph-based vs fixed patterns |
| Security & compliance | **9/10** | 4/10 | Zero-credential vs N-credential |
| API ecosystem compatibility | **9/10** | 4/10 | OpenAI-standard vs proprietary |
| 3rd-party integration (Azure ecosystem) | **10/10** | 3/10 | Native Fabric, AD SSO, Key Vault |
| 3rd-party integration (GCP ecosystem) | 4/10 | **9/10** | ADK native to BigQuery, Vertex |
| Rapid prototyping speed | 6/10 | **8/10** | Simpler setup, fewer concepts |
| .NET support | **10/10** | 0/10 | First-class .NET vs Python-only |
| Gemini-native features | 5/10 | **9/10** | ADK is Gemini-optimized |
| Continuous improvement pipeline | **9/10** | 2/10 | Eval + prompt optimizer + dataset harvesting |

### Weighted Score for Enterprise Conversational AI

Using weights relevant to enterprise supply-chain scenario (Snowflake + BlueYonder + Fabric):

| Factor | Weight | MAF | ADK |
|--------|--------|-----|-----|
| Production readiness | 25% | 2.25 | 1.25 |
| Tool ecosystem | 20% | 1.80 | 0.80 |
| Security | 20% | 1.80 | 0.80 |
| Integration (Azure) | 15% | 1.50 | 0.45 |
| Memory | 10% | 0.90 | 0.30 |
| Orchestration | 10% | 0.80 | 0.50 |
| **Total** | **100%** | **9.05** | **4.10** |

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
For the specific scenario of **enterprise conversational AI with Snowflake, BlueYonder, and Fabric integration**, MAF scores **2.2x higher** than ADK on weighted enterprise criteria. The gap is largest in security (Managed Identity vs manual credentials), tool infrastructure (6+ built-in vs 1), and Azure ecosystem integration (native vs custom connectors). ADK's advantages (simpler setup, Gemini-native) don't offset these gaps for production enterprise workloads.
