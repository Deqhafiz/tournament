#!/bin/bash
# Convenience script to run the AI agent

echo "🌀 Starting Chaotic Autonomous AI Agent..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import chromadb" 2>/dev/null; then
    echo "Dependencies not installed. Installing from requirements.txt..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your credentials."
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your API keys."
    exit 1
fi

# Run the agent
echo ""
echo "🚀 Launching agent..."
echo ""
python agent.py
