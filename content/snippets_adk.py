"""Google Agent Development Kit (ADK) code snippets for comparison."""

# ─────────────────────────────────────────────
# Section 1: Agent Creation
# ─────────────────────────────────────────────

AGENT_CREATION_BASIC = '''\
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

agent = Agent(
    name="supply_chain_assistant",
    model="gemini-2.0-flash",  # or via LiteLLM: "litellm/gpt-4o"
    instruction="""You are a supply chain assistant.
    Help users query inventory and track orders.""",
)

# Create runner and session
session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="supply_chain_app",
    session_service=session_service,
)

# Run the agent
from google.adk.agents import types
content = types.Content(
    role="user",
    parts=[types.Part(text="What is inventory for SKU-4521?")]
)

async for event in runner.run_async(
    user_id="user-1",
    session_id="session-1",
    new_message=content,
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
'''

AGENT_NO_YAML = '''\
# ADK: No declarative agent metadata file
# Agent definition is purely in Python code
# No equivalent to agent.yaml for version-controlled config

# To configure for deployment, you create a custom
# entrypoint or use adk web/adk api_server CLI:
# $ adk api_server --agent supply_chain_app.agent

# Deployment configuration is typically in:
# - Dockerfile (manual)
# - app.yaml (Cloud Run)
# - No standardized agent metadata format
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
from google.adk.tools import FunctionTool

def query_snowflake(query: str, warehouse: str = "COMPUTE_WH") -> dict:
    """Execute a query against Snowflake data warehouse."""
    # Manual Snowflake connector setup required
    return {"results": f"Results for: {query}"}

def check_order_status(order_id: str) -> dict:
    """Check order fulfillment status."""
    return {"status": "In Transit", "eta": "2 days"}

# Tools are passed as list to Agent constructor
agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    instruction="Use tools to answer supply chain questions.",
    tools=[query_snowflake, check_order_status],
)
'''

TOOLS_SEARCH = '''\
from google.adk.tools import google_search

# Built-in: Only Google Search available
agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    instruction="Search the web for information.",
    tools=[google_search],
)

# ❌ No built-in Azure AI Search equivalent
# ❌ No built-in Code Interpreter
# ❌ No built-in Bing Grounding
# ❌ No built-in File Search with vector store
# → Must build custom tools for each
'''

TOOLS_NO_BUILTIN = '''\
# ADK: Enterprise tools must be built manually

# No built-in RAG / vector search tool
# You need to implement your own:
from google.cloud import aiplatform

def search_product_catalog(query: str) -> dict:
    """Custom RAG — manually coded vector search."""
    # 1. Generate embedding
    # 2. Query vector DB (Vertex AI, Pinecone, etc.)
    # 3. Return results
    # All infrastructure managed by you
    pass

# No built-in Code Interpreter
# Must use custom sandbox execution
def run_python_code(code: str) -> dict:
    """Custom code execution — no sandbox provided."""
    # Security risk: must build your own sandboxing
    pass
'''

TOOLS_MCP = '''\
# ADK: MCP support (added in later versions)
from google.adk.tools.mcp_tool import MCPToolset

# Connect to MCP server
tools, cleanup = await MCPToolset.from_server(
    connection_params=SseServerParams(
        url="https://snowflake-mcp-server.example.com/sse",
    ),
)

agent = Agent(
    name="mcp_agent",
    model="gemini-2.0-flash",
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
    # or PostgreSQL, but manual setup required
)

runner = Runner(
    agent=agent,
    app_name="supply_chain_app",
    session_service=session_service,
)
'''

MEMORY_STATE = '''\
# ADK: Manual state management via session state dict
# No built-in long-term memory or summarization

async for event in runner.run_async(
    user_id="user-1",
    session_id="session-1",
    new_message=content,
):
    # Access session state manually
    session = session_service.get_session(
        app_name="supply_chain_app",
        user_id="user-1",
        session_id="session-1",
    )
    state = session.state  # Simple key-value dict

# ❌ No automatic conversation summarization
# ❌ No user profile learning
# ❌ No embedding-based memory retrieval
# ❌ No per-user memory scoping (manual implementation)
# → Must build all memory patterns from scratch
'''

# ─────────────────────────────────────────────
# Section 4: Multi-Agent Orchestration
# ─────────────────────────────────────────────

MULTI_AGENT_BASIC = '''\
from google.adk.agents import Agent, SequentialAgent, ParallelAgent

# ADK: Fixed orchestration patterns
data_agent = Agent(
    name="data_analyst",
    model="gemini-2.0-flash",
    instruction="Analyze supply chain data.",
    tools=[query_snowflake],
)

fulfillment_agent = Agent(
    name="fulfillment_manager",
    model="gemini-2.0-flash",
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
'''

MULTI_AGENT_PATTERNS = '''\
from google.adk.agents import LoopAgent

# Loop agent — repeats until exit condition
loop = LoopAgent(
    name="retry_analysis",
    sub_agents=[data_agent],
    max_iterations=3,
)

# ❌ No graph-based orchestration
# ❌ No deterministic routing with conditions
# ❌ No built-in fan-out/fan-in with aggregation
# ❌ No human-in-the-loop checkpoint
# → For complex patterns, must use A2A protocol
#   (Agent-to-Agent) with separate HTTP services

# A2A requires:
# - Each agent as separate HTTP server
# - Manual message routing
# - External orchestration layer
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

# No standard hosting adapter — manual server setup
EXPOSE 8080

# Must build your own HTTP server or use adk cli
CMD ["adk", "api_server", \\
     "--agent", "app.agent", \\
     "--host", "0.0.0.0", \\
     "--port", "8080"]
'''

DEPLOY_CLOUD_RUN = '''\
# Deploy to Google Cloud Run — manual setup

# Build and push container
gcloud builds submit --tag gcr.io/$PROJECT/supply-chain-agent

# Deploy to Cloud Run
gcloud run deploy supply-chain-agent \\
    --image gcr.io/$PROJECT/supply-chain-agent \\
    --platform managed \\
    --region us-central1 \\
    --allow-unauthenticated

# Manual configuration required for:
# ⚠️ Authentication (Cloud IAM, manual setup)
# ⚠️ Monitoring (Cloud Monitoring, separate config)
# ⚠️ Scaling (Cloud Run settings)
# ⚠️ No built-in agent evaluation
# ⚠️ No prompt optimization pipeline
'''

DEPLOY_NO_EVAL = '''\
# ADK: No built-in evaluation framework
# Must build custom evaluation pipeline

import json

# Manual test case execution
test_cases = [
    {"input": "What is SKU-4521 inventory?", "expected": "..."},
    {"input": "Reschedule order ORD-789", "expected": "..."},
]

results = []
for tc in test_cases:
    # Run agent manually
    response = await run_agent(tc["input"])
    # Custom metric calculation
    results.append({
        "input": tc["input"],
        "output": response,
        "score": custom_similarity(response, tc["expected"]),
    })

# ❌ No built-in evaluators (intent, task, groundedness)
# ❌ No prompt optimization from production traces
# ❌ No dataset harvesting from traces
# ❌ No A/B testing framework
# → All quality assurance is manual
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
    model="gemini-2.0-flash",
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
