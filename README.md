# MCPSecurity - Secure MCP Gateway

## 🎯 Overview
MCPSecurity is a secure MCP (Model Context Protocol) gateway that protects AI coding assistants with bidirectional security layers.

## 🔒 Features
- **Input Guardrails**: Detect secrets, PII, prompt injection before LLM
- **Output Guardrails**: Scan generated code for vulnerabilities
- **OPA Policy Engine**: RBAC/ABAC enforcement
- **Static Analysis**: AST parsing, Bandit, Semgrep integration
- **LangGraph Agents**: Multi-node security review flow
- **Auto-Remediation**: Automatically fix insecure code

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo-url>
cd MCPSecurity
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

⚠️ **IMPORTANT:** Never commit `.env` file. It contains your API keys!

### 3. Run Server
```bash
python main.py
```

📖 **Detailed Setup Guide:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🔒 Security & GitHub

### Before Pushing to GitHub:

✅ `.env` is in `.gitignore` (secrets protected)  
✅ Use `.env.example` as template  
✅ Never commit API keys or tokens  
✅ Review `.gitignore` before first commit  

### Getting Your OpenAI API Key:
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` file (NOT `.env.example`)

## 📁 Project Structure
```
MCPSecurity/
├── config/              # Configuration and settings
├── guardrails/          # Input/Output guardrails
├── opa/                 # OPA policy engine integration
├── static_analysis/     # Static code analysis tools
├── langgraph_flow/      # LangGraph agent nodes
├── mcp_server/          # FastAPI MCP server
├── logs/                # Application logs
└── main.py              # Entry point
```

## 🔧 Technology Stack
- **Python**: 3.11
- **Framework**: FastAPI
- **LLM**: OpenAI GPT-4
- **Orchestration**: LangGraph
- **Policy Engine**: OPA

## 📝 Build Status
- ✅ Step 1: Project Setup (COMPLETED)
- ✅ Step 2: Input Guardrails (COMPLETED)
- ✅ Step 3: OPA Policy Engine (COMPLETED)
- ⏳ Step 4: MCP Server Advanced (PENDING)
- ⏳ Step 5: Output Guardrails (PENDING)
- ⏳ Step 6: Static Analysis (PENDING)
- ⏳ Step 7: LangGraph Flow (PENDING)
- ⏳ Step 8: Risk Classifier (PENDING)
- ⏳ Step 9: Decision Layer (PENDING)
- ⏳ Step 10: Logging & Audit (PENDING)

## 📄 License
MIT

