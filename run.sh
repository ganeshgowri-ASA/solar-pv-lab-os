#!/bin/bash

# Solar PV Lab OS - AI Report Generator
# Quick Start Script

echo "🌞 Solar PV Lab OS - AI Report Generator"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Press Enter to continue after adding your API key..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

echo ""
echo "Choose an option:"
echo "1) Launch Streamlit UI (Recommended)"
echo "2) Launch FastAPI Backend"
echo "3) Run Example Script"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Streamlit UI..."
        echo "📱 Open your browser to: http://localhost:8501"
        echo ""
        streamlit run frontends/streamlit_app/report_generator.py
        ;;
    2)
        echo ""
        echo "🚀 Starting FastAPI Backend..."
        echo "📚 API Docs: http://localhost:8000/docs"
        echo "🔗 API: http://localhost:8000"
        echo ""
        python backend/main.py
        ;;
    3)
        echo ""
        echo "🚀 Running Example Script..."
        echo ""
        python examples/generate_sample_report.py
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run again."
        exit 1
        ;;
esac
