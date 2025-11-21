#!/bin/bash

echo "🚀 Setting up Antigravity MCP Gateway..."

echo "📦 Creating virtual environment with Python 3.11..."
python3.11 -m venv venv

echo "✅ Virtual environment created!"

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed!"

echo "📝 Creating .env file..."
cat > .env << EOL
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
EOL

echo "⚠️  Please edit .env and add your OPENAI_API_KEY"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "  python main.py"
echo ""

