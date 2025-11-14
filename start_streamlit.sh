#!/bin/bash

# Solar PV Lab OS - Streamlit Startup Script

echo "🚀 Starting Solar PV Lab OS Streamlit Interface..."

# Check which interface to start
INTERFACE=${1:-chat}

if [ "$INTERFACE" = "chat" ]; then
    echo "💬 Starting Chat Interface..."
    streamlit run frontends/streamlit_app/ai_chat.py
elif [ "$INTERFACE" = "insights" ]; then
    echo "🔍 Starting Insights Interface..."
    streamlit run frontends/streamlit_app/ai_insights.py
else
    echo "❌ Invalid interface: $INTERFACE"
    echo "Usage: ./start_streamlit.sh [chat|insights]"
    exit 1
fi
