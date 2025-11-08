#!/bin/bash

# Solar PV Lab OS - API Startup Script

echo "🚀 Starting Solar PV Lab OS API..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found! Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
source .env
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set in .env file!"
    echo "Please add your API key to .env file"
    exit 1
fi

# Create logs directory
mkdir -p logs

# Start API
echo "✅ Starting API on port 8000..."
cd backend/api
python ai_assistant_api.py
