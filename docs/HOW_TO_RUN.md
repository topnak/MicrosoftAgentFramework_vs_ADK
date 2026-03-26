# How to Run & Implement

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.11+ | Runtime |
| pip | Latest | Package management |
| Git | Any | Version control |
| Azure CLI | 2.60+ | (Optional) For live demo — `az login` |
| Azure Subscription | Any | (Optional) For live demo — Foundry project |

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/topnak/MicrosoftAgentFramework_vs_ADK.git
cd MicrosoftAgentFramework_vs_ADK
```

---

## Step 2: Set Up Python Environment

### Option A: venv (recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate
```

### Option B: conda

```bash
conda create -n maf-adk python=3.11 -y
conda activate maf-adk
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — UI framework
- `python-dotenv` — Environment variable loading
- `pandas` — Data tables
- `azure-identity` — Azure authentication (for live demo)
- `azure-ai-projects` — Foundry client (for live demo)
- `openai` — Responses API client (for live demo)

---

## Step 4: Run the Application

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your default browser.

### Common Streamlit Options

```bash
# Run on a different port
streamlit run app.py --server.port 8080

# Run headless (no auto-open browser)
streamlit run app.py --server.headless true

# Run accessible from network
streamlit run app.py --server.address 0.0.0.0
```

---

## Step 5: Navigate the Demo

### Landing Page
- Executive summary of both frameworks
- 21-feature comparison matrix (scrollable table)
- Story section navigation cards

### Story Sections (Sidebar)
Use the sidebar to navigate through all 6 chapters:

| Page | Content |
|------|---------|
| 🏗️ Agent Creation | Side-by-side code for agent definition, `agent.yaml`, Responses API v2 |
| 🔧 Tool Integration | Function tools, built-in tools (AI Search, Bing, Code Interpreter), MCP |
| 🧠 Memory & State | Thread persistence, long-term memory, user profile memory |
| 🔀 Multi-Agent | Graph orchestration, fan-out/fan-in, human-in-the-loop |
| 🚀 Deployment | Dockerfile, Foundry deploy, evaluation framework, prompt optimization |
| 🔗 3rd Party | Snowflake (MCP+SSO), BlueYonder (Key Vault), Fabric FabricIQ/WorkIQ |

Each section shows:
- **Left column (blue)**: Microsoft Agent Framework code
- **Right column (green)**: Google ADK equivalent
- **Bottom banner**: MAF advantages for that section

---

## Step 6: Enable Live Demo (Optional)

The live demo on the Agent Creation page connects to a real MAF agent via Azure AI Foundry.

### 6a. Login to Azure

```bash
az login
```

### 6b. Create `.env` file

```bash
# Copy template
cp .env.example .env
```

Edit `.env`:

```
FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### 6c. Verify Configuration

Restart the Streamlit app and navigate to **Page 1: Agent Creation**. Scroll down to see the live chat interface. If configured correctly, you'll see "Connected to Azure AI Foundry ✅".

### Without `.env` (Mock Mode)

If `.env` is not configured, the live demo runs in **mock mode** — showing a simulated supply-chain conversation with Snowflake queries and BlueYonder fulfillment actions. This is fully functional for presentation purposes.

---

## Mobile / Tablet Viewing

The app is responsive and works on mobile devices:
- Side-by-side columns **stack vertically** on screens < 768px
- Code blocks reduce font size on small screens
- Framework labels and banners scale appropriately

For best experience present the demo on a **desktop or tablet in landscape mode**.

---

## Project Structure Reference

```
MicrosoftAgentFramework_vs_ADK/
├── app.py                          # Landing page
├── pages/                          # 6 story chapters
│   ├── 1_Agent_Creation.py
│   ├── 2_Tool_Integration.py
│   ├── 3_Memory_State.py
│   ├── 4_Multi_Agent.py
│   ├── 5_Deployment.py
│   └── 6_Third_Party.py
├── components/                     # Reusable UI components
│   ├── side_by_side.py
│   ├── advantage_banner.py
│   ├── code_block.py
│   └── page_setup.py
├── live_demo/                      # Live MAF chat demo
│   ├── maf_chat.py
│   └── config.py
├── content/                        # Code snippets
│   ├── snippets_maf.py
│   └── snippets_adk.py
├── assets/
│   └── style.css
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md
│   ├── SUMMARY.md
│   └── HOW_TO_RUN.md              # (this file)
├── requirements.txt
├── .env.example
├── .copilot-instructions.md
├── IMPLEMENTATION_SUMMARY.md
└── README.md
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| `ImportError: components.side_by_side` | Run from project root: `cd MicrosoftAgentFramework_vs_ADK && streamlit run app.py` |
| Blank page on load | Check terminal for errors; ensure Python 3.11+ |
| Live demo shows "not configured" | Create `.env` file from `.env.example` with Foundry credentials |
| Live demo authentication error | Run `az login` and verify your account has Foundry access |
| Columns not stacking on mobile | Ensure `assets/style.css` is present; CSS media queries handle stacking |
| Port 8501 already in use | Use `streamlit run app.py --server.port 8080` |
