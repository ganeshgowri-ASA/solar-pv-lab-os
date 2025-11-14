# Solar PV Lab OS

**AI-Powered Solar PV Testing Lab Operating System**

A complete modular solution for solar photovoltaic laboratory management, test automation, AI-powered assistance, quality management, and analytics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Claude](https://img.shields.io/badge/AI-Claude%20Sonnet%204.5-purple.svg)

---

## 🌟 Features

### 1. **AI Assistant & Intelligence** (Session 8)
- 🤖 **Conversational AI** - Natural language interface with Claude API
- 📊 **Data Analysis** - Automated insights, anomaly detection, trend identification
- 📋 **Report Review** - Quality checking and compliance verification
- 🔧 **Troubleshooting** - AI-powered equipment and test issue resolution
- 🎯 **Decision Support** - Resource recommendations and optimization

### 2. **Core Capabilities**
- **Context-Aware Conversations** - Multi-turn dialogues with session memory
- **Knowledge Base Integration** - Standards, procedures, and best practices
- **Predictive Analysis** - Root cause analysis and predictions
- **Multi-Modal Support** - Data, reports, and decision analysis

---

## 🏗️ Architecture

```
solar-pv-lab-os/
├── backend/
│   ├── api/
│   │   └── ai_assistant_api.py      # FastAPI endpoints
│   ├── services/
│   │   ├── claude_service.py         # Claude API integration
│   │   ├── ai_engine.py              # Core AI intelligence
│   │   └── context_manager.py        # Conversation & RAG
│   ├── models/                       # Data models
│   └── utils/                        # Utilities
├── frontends/
│   └── streamlit_app/
│       ├── ai_chat.py                # Chat interface
│       └── ai_insights.py            # Analysis interface
├── config/
│   └── config.py                     # Configuration management
├── docs/
│   └── API_DOCUMENTATION.md          # API documentation
├── tests/                            # Test suites
├── requirements.txt                  # Python dependencies
└── .env.example                      # Environment template
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- pip or conda for package management

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ganeshgowri-ASA/solar-pv-lab-os.git
cd solar-pv-lab-os
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. **Set up your API key**
```bash
# In .env file:
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### Running the Application

#### Start the Backend API
```bash
cd backend/api
python ai_assistant_api.py
```

The API will be available at `http://localhost:8000`

#### Start the Streamlit Interface

**Chat Interface:**
```bash
streamlit run frontends/streamlit_app/ai_chat.py
```

**Insights Interface:**
```bash
streamlit run frontends/streamlit_app/ai_insights.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### AI Chat Interface

1. **Open the chat interface**
2. **Ask questions** about PV testing, standards, procedures
3. **Get guidance** on troubleshooting and best practices
4. **Analyze data** by describing your requirements

**Example Queries:**
- "What are the requirements for IEC 61215 thermal cycling?"
- "How do I troubleshoot unstable irradiance readings?"
- "Can you analyze this IV curve data?"
- "What are best practices for data quality control?"

### Data Analysis

1. **Navigate to AI Insights** → **Data Analysis** tab
2. **Upload or paste** your test data (JSON or CSV)
3. **Select test type** and analysis type
4. **Get AI-powered insights** with recommendations

### Report Review

1. **Go to Report Review** tab
2. **Paste your report data** (JSON format)
3. **Select applicable standards** (IEC 61215, IEC 61730, etc.)
4. **Receive comprehensive review** with issues and suggestions

### Troubleshooting

1. **Access Troubleshooting** tab
2. **Describe your issue** in detail
3. **Specify equipment and test type**
4. **Get step-by-step guidance**

---

## 🔌 API Reference

### Quick API Examples

**Chat:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain IV curve testing",
    "session_id": "test-123",
    "include_context": true
  }'
```

**Analyze Data:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"voltage": [0,10,20], "current": [8.5,8.3,7.8]},
    "test_type": "IV Curve",
    "analysis_type": "comprehensive"
  }'
```

**Full API Documentation:** See [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

**Interactive Docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 💡 Key Features Deep Dive

### 1. Conversational AI
- Multi-turn conversations with context retention
- Session-based memory management
- Intent detection for smart routing
- Knowledge base integration

### 2. Data Analysis
- Automated anomaly detection
- Trend identification and forecasting
- Statistical analysis with explanations
- Root cause analysis

### 3. Report Review
- Completeness verification
- Standards compliance checking
- Data consistency analysis
- Error detection and suggestions

### 4. Troubleshooting
- Equipment-specific guidance
- Step-by-step procedures
- Root cause identification
- Preventive recommendations

### 5. Decision Support
- Multi-criteria evaluation
- Risk assessment
- Cost-benefit analysis
- Evidence-based recommendations

---

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest --cov=backend tests/
```

---

## 🛠️ Development

### Project Structure

- **`backend/api/`** - REST API endpoints (FastAPI)
- **`backend/services/`** - Core business logic and AI services
- **`backend/models/`** - Data models and schemas
- **`frontends/streamlit_app/`** - User interfaces
- **`config/`** - Configuration management
- **`tests/`** - Test suites

### Adding New Features

1. Add business logic to `backend/services/`
2. Create API endpoints in `backend/api/`
3. Build UI components in `frontends/streamlit_app/`
4. Add tests in `tests/`
5. Update documentation

---

## 📊 Standards & Knowledge Base

The AI Assistant has built-in knowledge of:

### Standards
- **IEC 61215** - Design qualification and type approval
- **IEC 61730** - PV module safety qualification
- **UL 1703** - Flat-plate photovoltaic modules
- **IEC 61853** - PV module performance testing

### Test Procedures
- I-V Curve measurement
- Thermal cycling
- Insulation testing
- Mechanical load testing
- Humidity freeze
- Damp heat
- And more...

### Equipment Knowledge
- Solar simulators
- Thermal chambers
- I-V tracers
- Insulation testers
- Environmental chambers

---

## 🔒 Security & Privacy

- API keys stored in environment variables
- Session-based conversation isolation
- No persistent storage of sensitive data
- CORS configuration for production

**Important:** Never commit `.env` file with actual API keys!

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude API
- **Streamlit** for the amazing UI framework
- **FastAPI** for the excellent web framework
- **Solar PV Testing Community** for domain knowledge

---

## 📞 Support

- **Documentation:** See `docs/` folder
- **API Reference:** [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- **Issues:** Open an issue on GitHub

---

## 🗺️ Roadmap

### Current (Session 8)
- ✅ AI Assistant with Claude API
- ✅ Conversational interface
- ✅ Data analysis capabilities
- ✅ Report review functionality
- ✅ Troubleshooting support
- ✅ Decision support system

### Future Sessions
- 🔜 Database integration for data persistence
- 🔜 Advanced analytics and reporting
- 🔜 Multi-user support with authentication
- 🔜 Real-time data acquisition interfaces
- 🔜 Advanced visualization dashboards
- 🔜 Automated test scheduling
- 🔜 Compliance management system

---

## 📈 Performance

- **Response Time:** < 5s for most queries
- **Context Window:** 10 messages (configurable)
- **Token Efficiency:** Optimized prompts for cost reduction
- **Concurrent Users:** Scalable architecture

---

## 🌍 Use Cases

1. **Training New Technicians** - Reduce onboarding time with AI guidance
2. **Quality Assurance** - Automated report review and validation
3. **Problem Resolution** - Faster troubleshooting with expert AI help
4. **Data Insights** - Discover patterns in test results
5. **Decision Making** - Evidence-based equipment and process decisions
6. **Standards Compliance** - Ensure adherence to IEC/UL requirements

---

**Built with ❤️ for the Solar PV Testing Community**

**Powered by Claude Sonnet 4.5** 🚀
