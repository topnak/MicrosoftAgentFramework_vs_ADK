"""Microsoft Agent Framework code snippets — based on official repo (github.com/microsoft/agent-framework)."""

import os

# ─────────────────────────────────────────────
# Section 1: Agent Creation
# ─────────────────────────────────────────────

AGENT_CREATION_BASIC = '''\
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

async def main():
    # Provider-leading client → .as_agent() pattern
    agent = AzureOpenAIResponsesClient(
        # endpoint / deployment_name / api_version from env vars
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
# Invoke via OpenAI Responses protocol
# Agent Framework wraps this behind agent.run()
agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="supply-chain-assistant",
    instructions="Answer supply chain questions.",
)

# Simple invocation
result = await agent.run("What is our current inventory for SKU-4521?")
print(result)

# Or use the underlying OpenAI client directly
from openai import AzureOpenAI
client = AzureOpenAI(azure_ad_token_provider=...)
response = client.responses.create(
    model="gpt-4o",
    input="What is our current inventory for SKU-4521?",
)
print(response.output_text)
'''

AGENT_STREAMING = '''\
# Streaming with OpenAI Responses protocol
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2025-03-01-preview",
)

stream = client.responses.create(
    model="gpt-4o",
    input="Show me the top 5 delayed shipments",
    stream=True,
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
def query_snowflake(query: str, warehouse: str = "COMPUTE_WH") -> str:
    """Execute a read-only query against Snowflake data warehouse."""
    return f"Results for: {query}"

def check_order_status(order_id: str) -> str:
    """Check BlueYonder order fulfillment status."""
    return f"Order {order_id}: In Transit, ETA 2 days"

# Agent Framework auto-wraps functions as tools
agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="multi-tool-agent",
    instructions="Use tools to answer supply chain questions.",
    tools=[query_snowflake, check_order_status],
)
'''

TOOLS_AI_SEARCH = '''\
from agent_framework.azure_ai_search import AzureAISearchTool

# Built-in Azure AI Search — RAG with vector/semantic/hybrid
search_tool = AzureAISearchTool(
    index_name="product-catalog",
    search_endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    credential=AzureCliCredential(),
)

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="rag-agent",
    instructions="Search the product catalog to answer questions.",
    tools=[search_tool],
)
'''

TOOLS_BUILTIN = '''\
# Built-in tools provided by Agent Framework
# Available via the OpenAI Responses tool types:

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="analyst-agent",
    instructions="Use web search and code interpreter to analyze data.",
    tools=[
        {"type": "web_search_preview"},       # Free web search
        {"type": "code_interpreter"},          # Sandbox Python
        search_tool,                            # Azure AI Search
    ],
)

# Also available:
# - Bing Grounding (enterprise web search with citations)
# - File Search (vector-store-backed document search)
'''

TOOLS_MCP = '''\
from agent_framework.core.tools import McpTool

# Connect to ANY external service via MCP
snowflake_mcp = McpTool(
    server_url="https://snowflake-mcp-server.azurewebsites.net/sse",
    allowed_tools=["execute_query", "list_tables", "describe_table"],
)

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="mcp-agent",
    instructions="Use the Snowflake MCP server to query data.",
    tools=[snowflake_mcp],
)
'''

# ─────────────────────────────────────────────
# Section 3: Memory & State
# ─────────────────────────────────────────────

MEMORY_THREAD = '''\
# Conversation persistence via session stores
from agent_framework.azure_cosmos import CosmosSessionStore

# Create a Cosmos DB-backed session store
store = CosmosSessionStore(
    endpoint=os.environ["COSMOS_ENDPOINT"],
    credential=DefaultAzureCredential(),
    database_name="agent_memory",
    container_name="sessions",
)

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="supply-chain-assistant",
    instructions="Help with supply chain queries.",
    session_store=store,  # Auto-persists conversations
)

# First turn — history auto-saved
result = await agent.run("What were my last 3 orders?")

# Continue conversation — full history preserved
result = await agent.run("Cancel the most recent one")
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
from agent_framework.orchestrations import AgentWorkflow

# Graph-based workflow with streaming,
# checkpointing, human-in-the-loop, and time-travel

workflow = AgentWorkflow()

# Add agent nodes — each is a specialized agent
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("data_analyst", data_agent)
workflow.add_node("fulfillment", fulfillment_agent)
workflow.add_node("summarizer", summarizer_agent)

# Deterministic routing with conditional edges
workflow.add_edge("supervisor", "data_analyst", condition="data_query")
workflow.add_edge("supervisor", "fulfillment", condition="order_mgmt")
workflow.add_edge("data_analyst", "supervisor")  # Report back
workflow.add_edge("fulfillment", "supervisor")

# Run with streaming and checkpointing
result = await workflow.run(
    "Show delayed orders and reschedule them",
    stream=True,
    checkpoint=True,  # Enables time-travel debugging
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

# Deploy via Azure Container Apps or AKS
az containerapp create \\
    --name supply-chain-agent \\
    --resource-group mygroup \\
    --image myregistry.azurecr.io/supply-chain-agent:1.2.0 \\
    --target-port 8088

# Production features:
# ✅ Managed Identity (no API keys via DefaultAzureCredential)
# ✅ RBAC access control
# ✅ Application Insights + OpenTelemetry tracing
# ✅ Auto-scaling
# ✅ Private networking support
'''

DEPLOY_EVAL = '''\
# Evaluation via Azure AI Foundry
# Supports quality metrics and prompt optimization

# Use Foundry evaluations SDK or Azure AI CLI:
# az ai foundry evaluation create \\
#     --agent-name supply-chain-assistant \\
#     --dataset supply-chain-test-cases \\
#     --evaluators intent task groundedness

# Built-in evaluators include:
# ✅ Intent resolution
# ✅ Task adherence
# ✅ Tool call accuracy
# ✅ Groundedness (citation checking)

# Prompt optimization from production traces
# Foundry can harvest traces from Application Insights
# and optimize instructions automatically.

# AF Labs provides experimental benchmarking and
# reinforcement learning packages:
# https://github.com/microsoft/agent-framework/tree/main/python/packages/lab
'''

# ─────────────────────────────────────────────
# Section 6: 3rd Party Integration
# ─────────────────────────────────────────────

INTEGRATION_SNOWFLAKE = '''\
from azure.ai.agents.models import McpToolDefinition, FunctionTool

# Option 1: MCP Server for Snowflake
snowflake_mcp = McpTool(
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

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="snowflake-agent",
    tools=[snowflake_mcp, query_inventory],
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

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="fulfillment-agent",
    tools=[get_order_status, reschedule_delivery],
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

agent = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
).as_agent(
    name="fabric-intelligence-agent",
    tools=[fabric_search, get_workforce_metrics],
    instructions="""You are a Fabric intelligence agent.
    Use Azure AI Search for FabricIQ lakehouse queries.
    Use WorkIQ API for workforce intelligence metrics.
    All authenticated via Azure AD — zero credential management.""",
)
'''
