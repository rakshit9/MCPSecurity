# 🚀 Antigravity - Setup Guide

## Prerequisites

- Python 3.11+ (tested with 3.13.7)
- Git
- OpenAI API Key (required for LLM features)

## 📦 Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd antigravity
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

**Required Configuration:**
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
OPENAI_MODEL=gpt-4
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 5. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste it into `.env` file

### 6. Run the Server

```bash
python main.py
```

Server will start at: http://localhost:8000

### 7. Test the Installation

```bash
# Run unit tests
python test_guardrails.py

# Test API endpoints
./test_api.sh

# Or visit the API docs
open http://localhost:8000/docs
```

## 🔒 Security Notes

### ⚠️ NEVER commit the following files:
- `.env` - Contains your API keys (already in .gitignore)
- `logs/*.log` - May contain sensitive data
- `__pycache__/` - Python cache files

### ✅ Safe to commit:
- `.env.example` - Template without secrets
- All `.py` source files
- `requirements.txt`
- Documentation files

## 🧪 Verify Installation

Run this test to verify everything works:

```bash
curl -X POST http://localhost:8000/guardrails/validate \
  -H "Content-Type: application/json" \
  -d '{"text":"Test prompt"}'
```

Expected response:
```json
{
  "is_safe": true,
  "violations": [],
  "risk_score": 0,
  "total_violations": 0
}
```

## 📁 Project Structure

```
antigravity/
├── .env                     ⚠️  DO NOT COMMIT (your secrets)
├── .env.example            ✅ Commit this (template)
├── .gitignore              ✅ Protects secrets
├── requirements.txt        ✅ Dependencies
├── main.py                 ✅ Server entry point
├── config/                 ✅ Configuration
├── guardrails/             ✅ Security modules
├── mcp_server/             ✅ API routes
├── opa/                    🔜 Coming in Step 3
├── static_analysis/        🔜 Coming in Step 6
└── langgraph_flow/         🔜 Coming in Step 7
```

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not configured"
**Solution:** Make sure you've created `.env` file and added your API key.

### Issue: Port 8000 already in use
**Solution:** 
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or change port in .env
MCP_SERVER_PORT=8001
```

### Issue: Import errors
**Solution:** Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Next Steps

1. ✅ Complete Step 1: Project Setup
2. ✅ Complete Step 2: Input Guardrails
3. 🔜 Step 3: OPA Policy Engine
4. 🔜 Step 4: MCP Server Advanced
5. 🔜 Step 5: Output Guardrails
6. 🔜 Step 6: Static Analysis
7. 🔜 Step 7: LangGraph Integration

## 🆘 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review API docs at http://localhost:8000/docs
3. Run tests to identify specific issues

## 📄 License

MIT License - See LICENSE file

