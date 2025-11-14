"""
Solar PV Lab OS - Main Streamlit Application
AI-Powered Solar PV Testing Lab Operating System

Main entry point for the Streamlit application providing:
- AI Chat Assistant
- AI Insights & Analysis
- Data Analysis Tools
- Report Review
- Troubleshooting Support
- Decision Support
"""

import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontends', 'streamlit_app'))

# Import components
try:
    from frontends.streamlit_app.ai_chat import AIChatInterface
    from frontends.streamlit_app.ai_insights import AIInsightsInterface
except ImportError:
    # Fallback for direct imports
    from ai_chat import AIChatInterface
    from ai_insights import AIInsightsInterface


# Page configuration
st.set_page_config(
    page_title="Solar PV Lab OS",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def render_home():
    """Render the home page"""
    st.markdown('<div class="main-header">☀️ Solar PV Lab OS</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Solar PV Testing Lab Operating System</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Introduction
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Welcome to Solar PV Lab OS

        A comprehensive solution for solar photovoltaic laboratory management powered by
        **Claude AI (Sonnet 4.5)** - providing intelligent assistance for all your testing needs.

        #### 🎯 Key Features:

        - **🤖 AI Chat Assistant** - Natural language interface for questions and guidance
        - **📊 Data Analysis** - Automated insights and anomaly detection
        - **📋 Report Review** - Quality checking and compliance verification
        - **🔧 Troubleshooting** - AI-powered equipment issue resolution
        - **🎯 Decision Support** - Resource recommendations and optimization
        - **💡 Automated Insights** - Trend identification and predictions
        """)

    with col2:
        st.info("""
        **Quick Start:**

        1. Select a feature from the sidebar
        2. For AI Chat, just start asking questions
        3. For Analysis, upload your test data
        4. Get instant AI-powered insights
        """)

        st.success("""
        **Built-in Knowledge:**

        ✓ IEC 61215 Standard
        ✓ IEC 61730 Standard
        ✓ UL 1703 Standard
        ✓ Test Procedures
        ✓ Equipment Specs
        ✓ Best Practices
        """)

    # Feature cards
    st.markdown("---")
    st.subheader("📦 Available Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-box">
        <h4>🤖 AI Chat</h4>
        <p>Conversational AI assistant for instant answers about PV testing, standards, and procedures.</p>
        <ul>
        <li>Multi-turn conversations</li>
        <li>Context-aware responses</li>
        <li>Knowledge base integration</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
        <h4>🔍 AI Insights</h4>
        <p>Comprehensive analysis tools for data, reports, and decision-making.</p>
        <ul>
        <li>Data analysis</li>
        <li>Report review</li>
        <li>Troubleshooting</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-box">
        <h4>📊 Analytics</h4>
        <p>Advanced analytics and insights from your testing data.</p>
        <ul>
        <li>Trend identification</li>
        <li>Anomaly detection</li>
        <li>Predictions</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # API Information
    st.markdown("---")
    st.subheader("🔌 API Integration")

    col1, col2 = st.columns(2)

    with col1:
        st.code("""
# Start the API Backend
./start_api.sh

# API will be available at:
http://localhost:8000
        """, language="bash")

    with col2:
        st.code("""
# Example API Call
curl -X POST http://localhost:8000/api/v1/ai/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What is IEC 61215?",
       "session_id": "test-123"}'
        """, language="bash")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Solar PV Lab OS</strong> - Built with ❤️ for the Solar PV Testing Community</p>
    <p>Powered by <strong>Claude Sonnet 4.5</strong> 🚀 | FastAPI | Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application logic"""

    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/FF6B35/FFFFFF?text=Solar+PV+Lab", use_column_width=True)

        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "AI Chat", "AI Insights", "About"],
            icons=["house", "chat-dots", "graph-up", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f0f2f6"},
                "icon": {"color": "#FF6B35", "font-size": "18px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#FF6B35"},
            }
        )

        st.markdown("---")

        # API Status Check
        st.subheader("🔌 API Status")
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ API Online")
            else:
                st.error("❌ API Error")
        except:
            st.warning("⚠️ API Offline")
            st.caption("Start API with: `./start_api.sh`")

        st.markdown("---")

        # Quick Links
        st.subheader("📚 Resources")
        st.markdown("""
        - [API Documentation](docs/API_DOCUMENTATION.md)
        - [Session 8 Summary](docs/SESSION_8_SUMMARY.md)
        - [GitHub Repository](https://github.com/ganeshgowri-ASA/solar-pv-lab-os)
        """)

        st.markdown("---")
        st.caption("Version 1.0.0 | Session 8")

    # Main content area based on selection
    if selected == "Home":
        render_home()

    elif selected == "AI Chat":
        chat_interface = AIChatInterface(api_base_url="http://localhost:8000")
        chat_interface.render()

    elif selected == "AI Insights":
        insights_interface = AIInsightsInterface(api_base_url="http://localhost:8000")
        insights_interface.render()

    elif selected == "About":
        st.title("📖 About Solar PV Lab OS")

        st.markdown("""
        ### Overview

        Solar PV Lab OS is a comprehensive, AI-powered operating system for solar photovoltaic
        testing laboratories. Built with modern technologies and powered by Anthropic's Claude AI,
        it provides intelligent assistance for all aspects of lab operations.

        ### Technology Stack

        **Backend:**
        - FastAPI for REST API
        - Anthropic Claude API (Sonnet 4.5)
        - Python 3.9+

        **Frontend:**
        - Streamlit for user interfaces
        - Modern, responsive design
        - Real-time updates

        **AI Capabilities:**
        - Natural language processing
        - Context-aware conversations
        - Knowledge base integration (RAG)
        - Multi-turn dialogues
        - Intent detection

        ### Features

        #### Conversational AI
        - Ask questions in natural language
        - Get instant answers about standards and procedures
        - Context-aware responses based on conversation history

        #### Data Analysis
        - Upload test data (JSON, CSV)
        - Automated anomaly detection
        - Trend identification
        - Predictive insights

        #### Report Review
        - Quality checking
        - Standards compliance verification
        - Error detection
        - Improvement suggestions

        #### Troubleshooting
        - Equipment issue diagnosis
        - Step-by-step guidance
        - Root cause analysis
        - Preventive recommendations

        #### Decision Support
        - Multi-criteria evaluation
        - Resource recommendations
        - Risk assessment
        - Evidence-based suggestions

        ### Built-in Knowledge Base

        The system includes comprehensive knowledge of:

        **Standards:**
        - IEC 61215 - Design qualification and type approval
        - IEC 61730 - PV module safety qualification
        - UL 1703 - Flat-plate photovoltaic modules
        - IEC 61853 - PV module performance testing

        **Test Procedures:**
        - I-V Curve measurement
        - Thermal cycling
        - Insulation testing
        - Mechanical load testing
        - Humidity freeze
        - Damp heat
        - And more...

        **Equipment:**
        - Solar simulators
        - Thermal chambers
        - I-V tracers
        - Insulation testers

        ### Use Cases

        1. **Training** - Reduce onboarding time for new technicians
        2. **Quality Assurance** - Automated report validation
        3. **Problem Resolution** - Faster troubleshooting
        4. **Data Insights** - Discover patterns in test results
        5. **Decision Making** - Evidence-based recommendations
        6. **Compliance** - Ensure adherence to standards

        ### Performance

        - Response Time: < 5s for most queries
        - Context Window: 10 messages (configurable)
        - Token Efficiency: Optimized prompts
        - Scalable: Handles concurrent users

        ### License

        This project is licensed under the MIT License.

        ### Acknowledgments

        - **Anthropic** for Claude API
        - **Streamlit** for the UI framework
        - **FastAPI** for the web framework
        - **Solar PV Testing Community** for domain knowledge

        ---

        **Version:** 1.0.0
        **Session:** 8 - AI Assistant & Claude Intelligence
        **Status:** ✅ Production Ready
        """)


if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import streamlit_option_menu
    except ImportError:
        st.error("""
        Missing required package: streamlit-option-menu

        Please install with:
        pip install streamlit-option-menu
        """)
        st.stop()

    main()
