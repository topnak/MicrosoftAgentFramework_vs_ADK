# MAF vs ADK — Side-by-Side Comparison Demo

An interactive Streamlit app comparing **Microsoft Agent Framework (MAF)** vs **Google Agent Development Kit (ADK)** for enterprise conversational AI development.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Features

- **6 Story Sections** comparing MAF vs ADK side-by-side:
  1. 🏗️ Agent Creation — Definition, metadata, invocation
  2. 🔧 Tool Integration — Built-in tools, MCP, custom functions
  3. 🧠 Memory & State — Threads, long-term memory, user profiles
  4. 🔀 Multi-Agent Orchestration — Graph workflows, patterns
  5. 🚀 Deployment & Production — Containers, eval, prompt optimization
  6. 🔗 3rd Party Integration — Snowflake, BlueYonder, Fabric

- **Feature Comparison Matrix** — Quick visual overview of capabilities
- **Live Demo** — MAF conversational agent with OpenAI Responses streaming
- **Architecture Diagrams** — Side-by-side architecture comparisons

## Live Demo Setup

To enable the live MAF chat demo:

1. Copy `.env.example` to `.env`
2. Fill in your Azure AI Foundry credentials:
   ```
   FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com
   FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
   ```
3. Ensure you're logged in: `az login`
4. The demo will connect automatically on the Agent Creation page

Without `.env`, the demo runs in **mock mode** showing simulated conversations.

## Project Structure

```
ADK_MAF/
├── app.py                       # Landing page + comparison matrix
├── pages/
│   ├── 1_Agent_Creation.py      # Agent definition & invocation
│   ├── 2_Tool_Integration.py    # Tools, MCP, RAG
│   ├── 3_Memory_State.py        # Memory, threads, user profiles
│   ├── 4_Multi_Agent.py         # Orchestration patterns
│   ├── 5_Deployment.py          # Production readiness
│   └── 6_Third_Party.py         # Snowflake, BlueYonder, Fabric
├── components/
│   ├── side_by_side.py          # Reusable comparison renderer
│   ├── advantage_banner.py      # MAF advantage callout
│   ├── code_block.py            # Code display helper
│   └── page_setup.py            # CSS injection
├── live_demo/
│   ├── maf_chat.py              # Live MAF chat (OpenAI Responses)
│   └── config.py                # .env loader
├── content/
│   ├── snippets_maf.py          # MAF code snippets
│   └── snippets_adk.py          # ADK code snippets
├── assets/
│   └── style.css                # Custom styling
├── requirements.txt
├── .env.example
└── README.md
```

## Baseline

- **MAF**: Microsoft Agent Framework with OpenAI Responses protocol
- **ADK**: Google Agent Development Kit (google-adk)
- **Focus**: Enterprise conversational AI with 3rd-party integrations
