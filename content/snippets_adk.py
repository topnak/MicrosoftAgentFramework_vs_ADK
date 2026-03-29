"""Google Agent Development Kit (ADK) code snippets — based on official docs (google.github.io/adk-docs/)."""

# ─────────────────────────────────────────────
# Section 1: Agent Creation
# ─────────────────────────────────────────────

AGENT_CREATION_BASIC = '''\
from google.adk.agents import Agent  # LlmAgent aliased as Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Agent (alias for LlmAgent) is the core component
agent = Agent(
    name="supply_chain_assistant",
    model="gemini-2.5-flash",
    description="Handles supply chain queries.",
    instruction="""You are a supply chain assistant.
    Help users query inventory and track orders.""",
)

# Create runner and session service
session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="supply_chain_app",
    session_service=session_service,
)

# Run the agent
content = types.Content(
    role="user",
    parts=[types.Part(text="What is inventory for SKU-4521?")]
)

async for event in runner.run_async(
    user_id="user-1",
    session_id="session-1",
    new_message=content,
):
    if event.is_final_response() and event.content:
        print(event.content.parts[0].text)
'''

AGENT_CONFIG = '''\
# ADK: Agent Config — declarative agent definition
# Supported via adk CLI and documented at:
# https://google.github.io/adk-docs/agents/config/

# agent.json or agent config file
{
    "name": "supply_chain_assistant",
    "model": "gemini-2.5-flash",
    "instruction": "You are a supply chain assistant.",
    "tools": ["query_inventory", "check_orders"],
    "description": "Handles supply chain queries"
}

# Deploy with adk CLI:
# $ adk api_server --agent supply_chain_app.agent
# $ adk web  (launches built-in dev UI)

# Note: Agent Config is less mature than MAF agent.yaml
# — no version field, no secret references,
# — no environment variable templating
# — no CI/CD pipeline integration patterns
'''

AGENT_INVOKE = '''\
# ADK uses runner-based invocation
# No built-in streaming protocol like Responses API

from google.adk.runners import Runner

runner = Runner(
    agent=agent,
    app_name="supply_chain_app",
    session_service=InMemorySessionService(),
)

# Async iteration over events
async for event in runner.run_async(
    user_id="user-1",
    session_id="session-1",
    new_message=content,
):
    if event.content:
        for part in event.content.parts:
            if part.text:
                print(part.text, end="", flush=True)
'''

# ─────────────────────────────────────────────
# Section 2: Tool Integration
# ─────────────────────────────────────────────

TOOLS_FUNCTION = '''\
from google.adk.agents import Agent

def query_snowflake(query: str, warehouse: str = "COMPUTE_WH") -> dict:
    """Execute a query against Snowflake data warehouse."""
    # Manual Snowflake connector setup required
    return {"results": f"Results for: {query}"}

def check_order_status(order_id: str) -> dict:
    """Check order fulfillment status."""
    return {"status": "In Transit", "eta": "2 days"}

# ADK auto-wraps plain functions as FunctionTool
agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.5-flash",
    instruction="Use tools to answer supply chain questions.",
    tools=[query_snowflake, check_order_status],
)
# Docstrings and type hints are used for tool schemas
'''

TOOLS_SEARCH = '''\
from google.adk.agents import Agent
from google.adk.tools import google_search

# Built-in: Google Search Grounding
agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    instruction="Search the web for information.",
    tools=[google_search],
)

# Also available: Vertex AI Search Grounding
# for enterprise search over custom data sources.
# Configured via Vertex AI, not a standalone tool.

# ⚠️ No built-in Azure AI Search equivalent
# ⚠️ No built-in Bing Grounding
# ⚠️ No built-in File Search with vector store
# → Use OpenAPI tools or custom functions for RAG
'''

TOOLS_CODE_EXEC = '''\
from google.adk.agents import Agent
from google.adk.code_executors import BuiltInCodeExecutor

# ADK: Built-in code execution via Gemini API
code_agent = Agent(
    name="calculator_agent",
    model="gemini-2.5-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    Write and execute Python code to calculate results.""",
    description="Executes Python code for calculations.",
)

# The BuiltInCodeExecutor uses Gemini's native
# code execution capability — runs in Google's sandbox

# Also supports OpenAPI tools for REST API integration:
# from google.adk.tools.openapi_tool import OpenAPIToolset
# tools = OpenAPIToolset.from_url("https://api.example.com/openapi.json")
'''

TOOLS_MCP = '''\
# ADK: MCP tool support
from google.adk.tools.mcp_tool import MCPToolset, SseServerParams

# Connect to MCP server
tools, cleanup = await MCPToolset.from_server(
    connection_params=SseServerParams(
        url="https://snowflake-mcp-server.example.com/sse",
    ),
)

agent = Agent(
    name="mcp_agent",
    model="gemini-2.5-flash",
    instruction="Query Snowflake via MCP.",
    tools=tools,
)

# Note: Must manage cleanup lifecycle manually
# await cleanup()
'''

# ─────────────────────────────────────────────
# Section 3: Memory & State
# ─────────────────────────────────────────────

MEMORY_SESSION = '''\
from google.adk.sessions import InMemorySessionService

# In-memory sessions — lost on restart
session_service = InMemorySessionService()

# For persistence, use database-backed sessions
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///sessions.db",
    # or PostgreSQL for production
)

# ADK also supports session rewind (time-travel)
# and session migration between services

runner = Runner(
    agent=agent,
    app_name="supply_chain_app",
    session_service=session_service,
)
'''

MEMORY_STATE = '''\
# ADK: State and Memory services
# State = per-session key-value store
# Memory = cross-session recall

# State is accessed via session
session = await session_service.get_session(
    app_name="supply_chain_app",
    user_id="user-1",
    session_id="session-1",
)
state = session.state  # Dict-like state object

# output_key saves agent response to state automatically
agent = Agent(
    name="analyst",
    model="gemini-2.5-flash",
    output_key="analysis_result",  # Auto-saved to state
    instruction="Analyze the data.",
)

# Memory service for cross-session recall
from google.adk.sessions import InMemoryMemoryService

memory_service = InMemoryMemoryService()

# Context features:
# ✅ Context caching (reduce token usage)
# ✅ Context compression (auto-summarize long contexts)
# ✅ Session rewind (go back to earlier state)
# ⚠️ No managed persistence like Cosmos DB
# ⚠️ No per-user long-term profile learning
'''

# ─────────────────────────────────────────────
# Section 4: Multi-Agent Orchestration
# ─────────────────────────────────────────────

MULTI_AGENT_BASIC = '''\
from google.adk.agents import Agent, SequentialAgent, ParallelAgent

# ADK: Workflow agents for deterministic flow control
data_agent = Agent(
    name="data_analyst",
    model="gemini-2.5-flash",
    description="Analyzes supply chain data from Snowflake.",
    instruction="Analyze supply chain data.",
    tools=[query_snowflake],
)

fulfillment_agent = Agent(
    name="fulfillment_manager",
    model="gemini-2.5-flash",
    description="Manages order fulfillment via BlueYonder.",
    instruction="Manage BlueYonder fulfillment.",
    tools=[check_order_status],
)

# Sequential: agents run one after another
pipeline = SequentialAgent(
    name="pipeline",
    sub_agents=[data_agent, fulfillment_agent],
)

# Parallel: agents run concurrently
parallel = ParallelAgent(
    name="parallel_analysis",
    sub_agents=[data_agent, fulfillment_agent],
)

# LLM-driven transfer: agents can delegate to each other
# via sub_agents on an Agent (dynamic routing)
router = Agent(
    name="router",
    model="gemini-2.5-flash",
    instruction="Route to the right specialist.",
    sub_agents=[data_agent, fulfillment_agent],
)
'''

MULTI_AGENT_PATTERNS = '''\
from google.adk.agents import LoopAgent

# Loop agent — repeats until exit condition
loop = LoopAgent(
    name="retry_analysis",
    sub_agents=[data_agent],
    max_iterations=3,
)

# ADK 2.0: Graph-based workflows
# (New in ADK 2.0 — similar to MAF graph orchestration)
# https://google.github.io/adk-docs/workflows/
# Features: graph routes, data handling, human input,
#           collaborative agents, dynamic workflows

# Custom agents via BaseAgent for unique logic
from google.adk.agents import BaseAgent

class CustomRouter(BaseAgent):
    """Custom agent with your own execution logic."""
    async def _run_async_impl(self, ctx):
        # Implement custom routing, validation, etc.
        pass

# A2A Protocol for cross-framework agent communication
# Built-in support for exposing/consuming A2A agents
# https://google.github.io/adk-docs/a2a/
'''

# ─────────────────────────────────────────────
# Section 5: Deployment
# ─────────────────────────────────────────────

DEPLOY_DOCKERFILE = '''\
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ADK provides built-in API server via CLI
EXPOSE 8080

CMD ["adk", "api_server", \\
     "--agent", "app.agent", \\
     "--host", "0.0.0.0", \\
     "--port", "8080"]

# Also available:
# adk web  — launches built-in Dev UI
# adk run  — CLI-based agent interaction
'''

DEPLOY_CLOUD_RUN = '''\
# Deploy to Google Cloud — multiple options

# Option 1: Vertex AI Agent Engine (managed)
# https://google.github.io/adk-docs/deploy/agent-engine/
# Fully managed agent hosting on Google Cloud

# Option 2: Cloud Run
gcloud builds submit --tag gcr.io/$PROJECT/supply-chain-agent

gcloud run deploy supply-chain-agent \\
    --image gcr.io/$PROJECT/supply-chain-agent \\
    --platform managed \\
    --region us-central1

# Option 3: GKE (Kubernetes)
# https://google.github.io/adk-docs/deploy/gke/

# Option 4: Agent Starter Pack
# Pre-configured deployment templates
# https://google.github.io/adk-docs/deploy/agent-engine/asp/

# ADK deployment features:
# ✅ Vertex AI Agent Engine (managed hosting)
# ✅ Cloud Run (serverless containers)
# ✅ GKE (Kubernetes orchestration)
# ✅ Agent Starter Pack (templates)
# ⚠️ Authentication via Cloud IAM (manual setup)
'''

DEPLOY_NO_EVAL = '''\
# ADK: Built-in evaluation framework
# https://google.github.io/adk-docs/evaluate/

# ADK provides eval criteria, user simulation, and optimization:
# - Run via CLI: adk eval
# - Run via Dev UI: adk web (Evaluation tab)
# - Optimization: https://google.github.io/adk-docs/optimize/

# Define test cases with expected trajectories
test_cases = [
    {
        "input": "What is SKU-4521 inventory?",
        "expected_tool_calls": ["query_inventory"],
        "expected_response_contains": "SKU-4521",
    },
]

# Evaluation criteria include:
# ✅ Response quality assessment
# ✅ Tool call trajectory evaluation
# ✅ User simulation for multi-turn testing
# ✅ Safety evaluation patterns
# ✅ Custom metrics
# ✅ Prompt optimization (via Optimization docs)

# Deploy evaluation:
# $ adk eval --agent app.agent --test test_cases.json
'''

# ─────────────────────────────────────────────
# Section 6: 3rd Party Integration
# ─────────────────────────────────────────────

INTEGRATION_SNOWFLAKE = '''\
# ADK: Manual Snowflake integration
import snowflake.connector

def query_inventory(sku: str) -> dict:
    """Query Snowflake — manual credential management."""
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],       # ⚠️ Manual creds
        password=os.environ["SNOWFLAKE_PASSWORD"], # ⚠️ No managed ID
        warehouse="SUPPLY_CHAIN_WH",
        database="INVENTORY_DB",
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT warehouse, qty FROM inventory WHERE sku = %s", (sku,)
    )
    rows = cursor.fetchall()
    conn.close()
    return {"results": [{"warehouse": r[0], "qty": r[1]} for r in rows]}

agent = Agent(
    name="snowflake_agent",
    model="gemini-2.5-flash",
    instruction="Query Snowflake for supply chain data.",
    tools=[query_inventory],
)

# ⚠️ No MCP built-in for Snowflake
# ⚠️ Manual credential rotation required
# ⚠️ No Azure AD SSO for Snowflake auth
'''

INTEGRATION_BLUEYONDER = '''\
# ADK: Manual BlueYonder REST integration
import httpx

def get_order_status(order_id: str) -> dict:
    """Get BlueYonder order status — manual auth."""
    resp = httpx.get(
        f"{os.environ['BY_API_URL']}/orders/{order_id}/status",
        headers={
            "Authorization": f"Bearer {os.environ['BY_API_KEY']}"
            # ⚠️ Static API key — manual rotation
        },
    )
    resp.raise_for_status()
    return resp.json()

def reschedule_delivery(order_id: str, new_date: str) -> dict:
    """Reschedule via BlueYonder — manual auth."""
    resp = httpx.post(
        f"{os.environ['BY_API_URL']}/orders/{order_id}/reschedule",
        json={"new_delivery_date": new_date},
        headers={
            "Authorization": f"Bearer {os.environ['BY_API_KEY']}"
        },
    )
    resp.raise_for_status()
    return {"status": "rescheduled", "new_date": new_date}

# Same pattern as MAF, but:
# ⚠️ No managed identity — API keys in env vars
# ⚠️ No Azure Key Vault integration
'''

INTEGRATION_FABRIC = '''\
# ADK: No native Microsoft Fabric integration
# Must build custom connectors for everything

import httpx

def query_fabric_lakehouse(query: str) -> dict:
    """Custom Fabric connector — complex auth flow."""
    # Step 1: Get OAuth token for Fabric API
    # (Must register app in Azure AD manually)
    token_resp = httpx.post(
        "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["AZURE_CLIENT_ID"],
            "client_secret": os.environ["AZURE_CLIENT_SECRET"],  # ⚠️
            "scope": "https://analysis.windows.net/powerbi/api/.default",
        },
    )
    token = token_resp.json()["access_token"]

    # Step 2: Query Fabric API
    resp = httpx.post(
        f"https://api.fabric.microsoft.com/v1/workspaces/"
        f"{os.environ['FABRIC_WORKSPACE_ID']}/queries",
        json={"query": query},
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp.json()

# ❌ No Azure AI Search integration (build RAG manually)
# ❌ No FabricIQ native query support
# ❌ No WorkIQ workforce intelligence API
# ❌ No same-identity-plane — separate auth for each service
# ❌ Client secrets in environment variables
'''
