"""Microsoft Agent Framework code snippets — Foundry v2 Responses API baseline."""

# ─────────────────────────────────────────────
# Section 1: Agent Creation
# ─────────────────────────────────────────────

AGENT_CREATION_BASIC = '''\
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
import asyncio

async def main():
    # Create agent using the new agent-framework package
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        credential=AzureCliCredential(),
    ).as_agent(
        name="supply-chain-assistant",
        instructions="""You are an enterprise supply chain assistant.
        Help users query inventory, track orders, and optimize
        fulfillment using Snowflake and BlueYonder data.""",
    )

    result = await agent.run("What is our current inventory?")
    print(result)

asyncio.run(main())
'''

AGENT_YAML = '''\
# agent.yaml — declarative agent metadata
name: supply-chain-assistant
description: Enterprise supply chain AI agent
model: gpt-4o
instructions: |
  You are an enterprise supply chain assistant.
  Integrate with Snowflake for data queries and
  BlueYonder for order fulfillment.
tools:
  - type: function
    name: query_snowflake
  - type: azure_ai_search
    index_name: product-catalog
  - type: web_search_preview
'''

AGENT_RESPONSES_API = '''\
# Invoke via OpenAI Responses API v2
openai_client = project.get_openai_client()

response = openai_client.responses.create(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    input="What is our current inventory for SKU-4521?",
    extra_body={
        "agent": {
            "name": "supply-chain-assistant",
            "type": "agent_reference",
        }
    },
)

print(response.output_text)
'''

AGENT_STREAMING = '''\
# Streaming with Responses API v2
stream = openai_client.responses.create(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    input="Show me the top 5 delayed shipments",
    stream=True,
    extra_body={
        "agent": {
            "name": "supply-chain-assistant",
            "type": "agent_reference",
        }
    },
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.output_item.done":
        if hasattr(event.item, "annotations"):
            for ann in event.item.annotations:
                print(f"\\n[Source: {ann.url}]")
'''

# ─────────────────────────────────────────────
# Section 2: Tool Integration
# ─────────────────────────────────────────────

TOOLS_FUNCTION = '''\
from azure.ai.agents.models import FunctionTool

def query_snowflake(query: str, warehouse: str = "COMPUTE_WH") -> str:
    """Execute a read-only query against Snowflake data warehouse."""
    # Actual Snowflake connector call here
    return f"Results for: {query}"

def check_order_status(order_id: str) -> str:
    """Check BlueYonder order fulfillment status."""
    return f"Order {order_id}: In Transit, ETA 2 days"

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="multi-tool-agent",
    instructions="Use tools to answer supply chain questions.",
    tools=FunctionTool([query_snowflake, check_order_status]),
)
'''

TOOLS_AI_SEARCH = '''\
from azure.ai.agents.models import AzureAISearchToolDefinition

# Built-in Azure AI Search — RAG with vector search
search_tool = AzureAISearchToolDefinition(
    index_connection_id="your-ai-search-connection",
    index_name="product-catalog",
    query_type="vector_semantic_hybrid",
    top_k=5,
)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="rag-agent",
    instructions="Search the product catalog to answer questions.",
    tools=[search_tool],
)
'''

TOOLS_BUILTIN = '''\
from azure.ai.agents.models import (
    WebSearchPreviewToolDefinition,
    CodeInterpreterToolDefinition,
    BingGroundingToolDefinition,
    ToolSet,
)

# Compose multiple built-in tools
toolset = ToolSet()
toolset.definitions.append(WebSearchPreviewToolDefinition())   # Free web search
toolset.definitions.append(CodeInterpreterToolDefinition())    # Sandbox Python
toolset.definitions.append(BingGroundingToolDefinition(        # Enterprise Bing
    bing_connection_id="your-bing-connection",
))

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="analyst-agent",
    instructions="Use web search and code interpreter to analyze data.",
    toolset=toolset,
)
'''

TOOLS_MCP = '''\
from azure.ai.agents.models import McpToolDefinition

# Connect to ANY external service via MCP
snowflake_mcp = McpToolDefinition(
    server_label="snowflake-mcp",
    server_url="https://snowflake-mcp-server.azurewebsites.net/sse",
    allowed_tools=["execute_query", "list_tables", "describe_table"],
)

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="mcp-agent",
    instructions="Use the Snowflake MCP server to query data.",
    tools=[snowflake_mcp],
)
'''

# ─────────────────────────────────────────────
# Section 3: Memory & State
# ─────────────────────────────────────────────

MEMORY_THREAD = '''\
# Thread-based conversation persistence (Cosmos DB-backed)
thread = project.agents.threads.create()

# Add user message
project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="What were my last 3 orders?",
)

# Run agent on thread — full conversation history preserved
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# Continue conversation in same thread
project.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Cancel the most recent one",
)
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)
'''

MEMORY_LONG_TERM = '''\
# MAF supports multiple memory/state backends:
# - Azure Cosmos DB for persistent threads/state
# - Redis for fast session state
# - Mem0 for long-term memory with embeddings

# Using agent-framework with Cosmos DB persistence
from agent_framework.azure_cosmos import CosmosSessionStore

store = CosmosSessionStore(
    endpoint=os.environ["COSMOS_ENDPOINT"],
    credential=DefaultAzureCredential(),
    database_name="agent_memory",
    container_name="sessions",
)

# Or Redis for fast key-value state
from agent_framework.redis import RedisSessionStore

redis_store = RedisSessionStore(
    redis_url="redis://localhost:6379",
)

# Mem0 integration for semantic long-term memory
from agent_framework.mem0 import Mem0MemoryStore

mem0_store = Mem0MemoryStore(
    api_key=os.environ["MEM0_API_KEY"],
)

# Memory persists across sessions automatically
# Thread history maintained in Cosmos DB
# User context accumulates over time via Mem0
'''

# ─────────────────────────────────────────────
# Section 4: Multi-Agent Orchestration
# ─────────────────────────────────────────────

MULTI_AGENT_GRAPH = '''\
from agent_framework import AgentWorkflow

# Graph-based orchestration with streaming,
# checkpointing, human-in-the-loop, and time-travel

# Define the workflow graph
workflow = AgentWorkflow()

# Add agent nodes — each is a specialized agent
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("data_analyst", data_agent)
workflow.add_node("fulfillment", fulfillment_agent)
workflow.add_node("summarizer", summarizer_agent)

# Deterministic routing with conditions
workflow.add_edge("supervisor", "data_analyst", condition="data_query")
workflow.add_edge("supervisor", "fulfillment", condition="order_mgmt")
workflow.add_edge("data_analyst", "supervisor")  # Report back
workflow.add_edge("fulfillment", "supervisor")

# Run with streaming and checkpointing
result = await workflow.run(
    "Show delayed orders and reschedule them",
    stream=True,
    checkpoint=True,  # Enable time-travel debugging
)
'''

MULTI_AGENT_PATTERNS = '''\
# Advanced orchestration patterns

# Fan-out / Fan-in — parallel agent execution
workflow.add_fan_out("supervisor", ["data_analyst", "fulfillment"])
workflow.add_fan_in(["data_analyst", "fulfillment"], "summarizer")

# Human-in-the-loop — pause for approval
workflow.add_human_checkpoint(
    "fulfillment",
    prompt="Approve order cancellation?",
    on_approve="confirm_cancel",
    on_reject="supervisor",
)

# Loop — retry with feedback
workflow.add_loop(
    "data_analyst",
    max_iterations=3,
    exit_condition="data_quality_check_passed",
)
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

# Foundry hosting adapter — standard port 8088
EXPOSE 8088

CMD ["python", "-m", "azure.ai.agentserver.agentframework", \\
     "--agent-module", "app:agent"]
'''

DEPLOY_AGENT_YAML = '''\
# agent.yaml — version-controlled agent metadata
name: supply-chain-assistant
version: 1.2.0
description: Enterprise supply chain AI agent with Snowflake & BlueYonder
model:
  deployment: gpt-4o
  parameters:
    temperature: 0.1
tools:
  - query_snowflake
  - check_order_status
  - azure_ai_search:product-catalog
environment:
  SNOWFLAKE_ACCOUNT: "{{secrets.SNOWFLAKE_ACCOUNT}}"
  BY_API_KEY: "{{secrets.BY_API_KEY}}"
'''

DEPLOY_FOUNDRY = '''\
# Deploy to Azure AI Foundry — managed hosting
az acr build --registry myregistry \\
    --image supply-chain-agent:1.2.0 .

# Create hosted agent in Foundry
az ai foundry agent create \\
    --name supply-chain-assistant \\
    --image myregistry.azurecr.io/supply-chain-agent:1.2.0 \\
    --project-endpoint $FOUNDRY_PROJECT_ENDPOINT

# Production features automatic:
# ✅ Managed Identity (no API keys)
# ✅ RBAC access control
# ✅ Application Insights tracing
# ✅ Auto-scaling
# ✅ Private networking support
'''

DEPLOY_EVAL = '''\
# Built-in evaluation framework
from azure.ai.projects import AIProjectClient

# Batch evaluation with quality metrics
eval_run = project.evaluations.create(
    agent_id=agent.id,
    dataset="supply-chain-test-cases",
    evaluators=[
        "intent_resolution",
        "task_adherence",
        "tool_call_accuracy",
        "groundedness",
    ],
)

# Prompt optimization from traces
optimization = project.prompt_optimizer.create(
    agent_id=agent.id,
    dataset_from_traces=True,  # Harvest real production data
    objective="Improve tool call accuracy for Snowflake queries",
)
'''

# ─────────────────────────────────────────────
# Section 6: 3rd Party Integration
# ─────────────────────────────────────────────

INTEGRATION_SNOWFLAKE = '''\
from azure.ai.agents.models import McpToolDefinition, FunctionTool

# Option 1: MCP Server for Snowflake
snowflake_mcp = McpToolDefinition(
    server_label="snowflake-mcp",
    server_url="https://snowflake-mcp.azurewebsites.net/sse",
    allowed_tools=["execute_query", "list_tables"],
    # Managed Identity — no credentials in code
)

# Option 2: Function Tool with Snowflake connector
import snowflake.connector

def query_inventory(sku: str) -> str:
    """Query Snowflake for inventory levels by SKU."""
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        authenticator="externalbrowser",  # SSO via Azure AD
        warehouse="SUPPLY_CHAIN_WH",
        database="INVENTORY_DB",
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT warehouse, qty FROM inventory WHERE sku = %s", (sku,)
    )
    rows = cursor.fetchall()
    conn.close()
    return str([{"warehouse": r[0], "qty": r[1]} for r in rows])

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="snowflake-agent",
    tools=[snowflake_mcp, FunctionTool([query_inventory])],
    instructions="Query Snowflake for supply chain data.",
)
'''

INTEGRATION_BLUEYONDER = '''\
from azure.ai.agents.models import FunctionTool
import httpx

BY_BASE_URL = os.environ["BLUEYONDER_API_URL"]

def get_order_status(order_id: str) -> str:
    """Get order fulfillment status from BlueYonder."""
    resp = httpx.get(
        f"{BY_BASE_URL}/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {_get_by_token()}"},
    )
    resp.raise_for_status()
    return resp.json()

def reschedule_delivery(order_id: str, new_date: str) -> str:
    """Reschedule delivery in BlueYonder fulfillment system."""
    resp = httpx.post(
        f"{BY_BASE_URL}/orders/{order_id}/reschedule",
        json={"new_delivery_date": new_date},
        headers={"Authorization": f"Bearer {_get_by_token()}"},
    )
    resp.raise_for_status()
    return f"Order {order_id} rescheduled to {new_date}"

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="fulfillment-agent",
    tools=FunctionTool([get_order_status, reschedule_delivery]),
    instructions="Manage orders via BlueYonder fulfillment.",
)
'''

INTEGRATION_FABRIC = '''\
from azure.ai.agents.models import (
    AzureAISearchToolDefinition,
    FunctionTool,
)
from azure.identity import DefaultAzureCredential
import httpx

# FabricIQ — query Fabric lakehouse via Azure AI Search
# Same identity plane: Azure AD → Fabric → AI Search → Agent
fabric_search = AzureAISearchToolDefinition(
    index_connection_id="fabric-lakehouse-index",
    index_name="supply-chain-lakehouse",
    query_type="vector_semantic_hybrid",
    top_k=10,
)

# WorkIQ — workforce intelligence via Fabric REST API
def get_workforce_metrics(region: str, date: str) -> str:
    """Get WorkIQ workforce intelligence metrics from Fabric."""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://analysis.windows.net/powerbi/api/.default")
    resp = httpx.get(
        f"https://api.fabric.microsoft.com/v1/workspaces/"
        f"{{workspace_id}}/datasets/workiq/metrics",
        params={"region": region, "date": date},
        headers={"Authorization": f"Bearer {token.token}"},
    )
    resp.raise_for_status()
    return resp.json()

agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="fabric-intelligence-agent",
    tools=[fabric_search, FunctionTool([get_workforce_metrics])],
    instructions="""You are a Fabric intelligence agent.
    Use Azure AI Search for FabricIQ lakehouse queries.
    Use WorkIQ API for workforce intelligence metrics.
    All authenticated via Azure AD — zero credential management.""",
)
'''
