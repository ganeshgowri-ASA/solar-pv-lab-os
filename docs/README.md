# Solar PV Lab OS - AI-Powered Report Generator

## 🌟 Overview

The AI-Powered Report Generator is a comprehensive solution designed to **eliminate typos**, **automate report creation**, and **reduce report generation time from 2-4 hours to 5-10 minutes** for solar PV testing laboratories.

### Key Features

✅ **AI-Powered Generation** - Auto-generate reports from test data using Claude API
✅ **Zero Typos** - AI-powered grammar and spell checking
✅ **Multi-Format Export** - PDF, Word, Excel outputs
✅ **Quality Assurance** - Automated validation and compliance checking
✅ **Template Engine** - Flexible templates for IEC/UL standards
✅ **Data Extraction** - Parse Excel, CSV, JSON, XML, IVC files
✅ **Version Control** - Track changes and revisions
✅ **Fast Generation** - Complete reports in 5-10 minutes

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/ganeshgowri-ASA/solar-pv-lab-os.git
cd solar-pv-lab-os

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the Application

#### Option A: Streamlit UI (Recommended)

```bash
streamlit run frontends/streamlit_app/report_generator.py
```

Access at: http://localhost:8501

#### Option B: FastAPI Backend

```bash
python backend/main.py
```

API Docs at: http://localhost:8000/docs

## 📊 Usage

### Streamlit UI

1. **Navigate to "Generate Report" tab**
2. **Fill in report details** (title, client, etc.)
3. **Select report type and template**
4. **Enter test results** (or upload data files)
5. **Choose output formats** (PDF, Word, Excel)
6. **Enable AI features** (spell check, grammar, compliance)
7. **Click "Generate Report"**
8. **Download your reports** - All files ready in seconds!

### API Usage

```python
import requests

# Generate report via API
response = requests.post(
    "http://localhost:8000/api/reports/generate",
    json={
        "report_type": "test_result",
        "template_id": "test_result_iec61215",
        "report_title": "Solar Module Test Report",
        "client_name": "ABC Solar Inc.",
        "test_results": [
            {
                "test_id": "TEST-001",
                "test_name": "I-V Characteristic Test",
                "test_method": "IEC 61215-2:2016",
                "standard": "IEC 61215",
                "test_date": "2024-01-15T10:30:00",
                "operator": "John Doe",
                "sample_id": "SAMPLE-001",
                "manufacturer": "SolarTech",
                "model": "ST-300",
                "serial_number": "SN123456",
                "measurements": {
                    "Voc": "45.2 V",
                    "Isc": "8.95 A",
                    "Pmax": "300.1 W"
                },
                "overall_result": "PASS"
            }
        ],
        "output_formats": ["pdf", "word"],
        "enable_ai_enhancement": true,
        "enable_spell_check": true
    }
)

result = response.json()
print(f"Report generated: {result['report_id']}")
print(f"Files: {result['files']}")
```

## 🎯 Core Features

### 1. AI Report Generation

- **Auto-generate** report sections from test data
- **Natural language processing** for technical content
- **Professional tone** enforcement
- **Standard compliance** checking (IEC 61215, UL 1703, etc.)

### 2. Quality Assurance

- **Spell checking** - Eliminate typos
- **Grammar checking** - Professional writing
- **Technical term validation** - Solar PV terminology
- **Data completeness** checking
- **Compliance validation** - IEC/UL standards

### 3. Multi-Format Export

- **PDF** - Professional reports with styling
- **Word** - Editable documents (.docx)
- **Excel** - Data sheets with test results

### 4. Template Engine

Pre-built templates:
- Test Result Report (IEC 61215)
- Performance Report
- Compliance Report (NABL/ISO)
- Executive Summary

Custom templates supported via Jinja2 syntax.

### 5. Data Extraction

Supports:
- Excel (.xlsx, .xls)
- CSV files
- JSON data
- XML files
- I-V curve files (.ivc)

### 6. Version Control

- Track report revisions
- Compare versions
- Archive management
- Change history

## 📁 Project Structure

```
solar-pv-lab-os/
├── backend/
│   ├── api/
│   │   └── report_generator.py      # FastAPI endpoints
│   ├── services/
│   │   ├── ai_report_service.py     # Claude AI integration
│   │   ├── data_extraction_service.py
│   │   ├── template_service.py
│   │   ├── quality_service.py
│   │   ├── report_generation_service.py
│   │   └── version_control_service.py
│   ├── models/
│   │   └── report_models.py         # Data models
│   ├── config.py                    # Configuration
│   └── main.py                      # FastAPI app
├── frontends/
│   └── streamlit_app/
│       └── report_generator.py      # Streamlit UI
├── templates/
│   └── report_templates/            # Report templates
├── sample_data/
│   ├── test_results/                # Sample test data
│   ├── equipment_files/             # Sample equipment files
│   └── generated_reports/           # Output directory
├── docs/                            # Documentation
├── requirements.txt
└── .env.example
```

## 🔧 Configuration

### Environment Variables

```bash
# AI Configuration
ANTHROPIC_API_KEY=your_api_key_here
AI_MODEL=claude-3-5-sonnet-20241022
AI_MAX_TOKENS=4096

# Lab Information
LAB_NAME=Your Lab Name
LAB_NABL_CERT=TC-XXXX
LAB_ADDRESS=Your Address
LAB_PHONE=+91-XXXXXXXXXX
LAB_EMAIL=lab@example.com

# Paths
REPORTS_OUTPUT_DIR=./sample_data/generated_reports
TEMPLATES_DIR=./templates/report_templates
```

## 📖 API Documentation

### Endpoints

#### Generate Report
```
POST /api/reports/generate
```

#### List Templates
```
GET /api/reports/templates
```

#### Quality Check
```
POST /api/reports/quality-check
```

#### Download Report
```
GET /api/reports/download/{report_id}/{format}
```

Full API documentation: http://localhost:8000/docs

## 🎓 Examples

### Example 1: Simple Report

```python
from backend.models.report_models import ReportRequest, TestResult, ReportType
from backend.services.report_generation_service import ReportGenerationService

# Create test result
test_result = TestResult(
    test_id="TEST-001",
    test_name="I-V Test",
    # ... other fields
)

# Create request
request = ReportRequest(
    report_type=ReportType.TEST_RESULT,
    report_title="Module Test Report",
    client_name="Test Client",
    test_results=[test_result],
    output_formats=["pdf"]
)

# Generate
service = ReportGenerationService()
response = await service.generate_report(request)
```

### Example 2: Data Extraction

```python
from backend.services.data_extraction_service import DataExtractionService

service = DataExtractionService()

# Extract from Excel
data = await service.extract_from_excel("test_data.xlsx")

# Extract from I-V curve file
iv_data = await service.extract_from_ivc("iv_curve.ivc")
```

## ⚡ Performance

- **Report Generation**: 5-10 minutes (vs 2-4 hours manual)
- **Typo Rate**: Near zero with AI checking
- **Format Support**: PDF, Word, Excel
- **Concurrent Reports**: Multiple reports in parallel

## 🛡️ Quality Metrics

- **AI Quality Score**: 0-100 scale
- **Spell Check**: Claude-powered
- **Grammar Check**: Professional writing validation
- **Compliance Check**: IEC/UL standard validation
- **Data Completeness**: Automatic verification

## 🔒 Security

- API key management via environment variables
- No hardcoded credentials
- Secure file handling
- Version-controlled reports

## 🤝 Integration

### GenSpark Integration
```python
# API endpoint for GenSpark
POST http://localhost:8000/api/reports/generate
```

### Snowflake Integration
- RESTful API endpoints
- JSON request/response
- Standard HTTP methods

## 📝 License

MIT License - See LICENSE file

## 👥 Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/ganeshgowri-ASA/solar-pv-lab-os/issues
- Email: support@example.com

## 🎉 Benefits

### Before AI Report Generator:
❌ Manual typing → 2-4 hours per report
❌ Typos and errors → Quality issues
❌ Inconsistent formatting
❌ Manual data entry → Errors
❌ No quality checking

### After AI Report Generator:
✅ Automated generation → 5-10 minutes
✅ Zero typos → AI checking
✅ Consistent templates
✅ Auto data extraction
✅ Quality assurance built-in

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Custom branding/logos
- [ ] Digital signatures
- [ ] Email delivery automation
- [ ] Advanced analytics
- [ ] Mobile app

---

**Built with ❤️ for Solar PV Testing Labs**
