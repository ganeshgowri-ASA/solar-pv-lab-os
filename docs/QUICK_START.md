# Quick Start Guide

## 5-Minute Setup

Get your AI-powered report generator running in 5 minutes!

### Step 1: Install (1 minute)

```bash
# Clone the repository
git clone https://github.com/ganeshgowri-ASA/solar-pv-lab-os.git
cd solar-pv-lab-os

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)

```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# You can get a key from: https://console.anthropic.com/
nano .env
```

Required configuration:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### Step 3: Run (30 seconds)

```bash
# Launch Streamlit UI
streamlit run frontends/streamlit_app/report_generator.py
```

Open your browser to: http://localhost:8501

### Step 4: Generate Your First Report (2 minutes)

1. Fill in basic info:
   - Report Title: "My First Test Report"
   - Client Name: "Test Client"

2. Enter test data:
   - Voc: 45.2 V
   - Isc: 8.95 A
   - Pmax: 300 W

3. Click "Generate Report"

4. Download your PDF! ✅

## Common Use Cases

### Use Case 1: Single Test Report

```python
from backend.models.report_models import *
from backend.services.report_generation_service import ReportGenerationService
import asyncio

async def generate_simple_report():
    # Create test result
    test = TestResult(
        test_id="TEST-001",
        test_name="I-V Characteristic Test",
        test_method="IEC 61215-2:2016",
        standard=TestStandard.IEC_61215,
        test_date=datetime.now(),
        operator="John Doe",
        sample_id="SAMPLE-001",
        manufacturer="SolarTech",
        model="ST-300",
        serial_number="SN123",
        measurements={"Voc": "45.2 V", "Isc": "8.95 A", "Pmax": "300 W"},
        overall_result="PASS"
    )

    # Create request
    request = ReportRequest(
        report_type=ReportType.TEST_RESULT,
        report_title="Quick Test Report",
        client_name="ABC Solar",
        test_results=[test],
        output_formats=[ReportFormat.PDF]
    )

    # Generate
    service = ReportGenerationService()
    response = await service.generate_report(request)

    print(f"✅ Report generated: {response.files['pdf']}")

asyncio.run(generate_simple_report())
```

### Use Case 2: Batch Report Generation

```python
# Generate multiple reports
test_ids = ["TEST-001", "TEST-002", "TEST-003"]

for test_id in test_ids:
    # Load test data
    test_data = load_test_data(test_id)

    # Generate report
    response = await service.generate_report(
        create_request(test_data)
    )

    print(f"✅ {test_id}: {response.report_id}")
```

### Use Case 3: API Integration

```bash
# Using curl
curl -X POST "http://localhost:8000/api/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "test_result",
    "report_title": "API Test Report",
    "client_name": "API Client",
    "test_results": [...],
    "output_formats": ["pdf"]
  }'
```

## Troubleshooting

### Issue: API Key Error

```
Error: ANTHROPIC_API_KEY not set
```

**Solution**: Add your API key to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Issue: Import Errors

```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Port Already in Use

```
Error: Port 8501 already in use
```

**Solution**: Use a different port:
```bash
streamlit run frontends/streamlit_app/report_generator.py --server.port 8502
```

### Issue: PDF Generation Fails

```
Error: PDF generation failed
```

**Solution**: Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# macOS
brew install cairo pango gdk-pixbuf libffi
```

## Performance Tips

### Tip 1: Enable AI Features Selectively

For faster generation, disable features you don't need:
```python
request = ReportRequest(
    # ...
    enable_ai_enhancement=False,      # Faster
    enable_spell_check=True,          # Keep quality
    enable_grammar_check=False,       # Skip if not needed
)
```

### Tip 2: Batch Processing

Process multiple reports in parallel:
```python
import asyncio

async def generate_many_reports(requests):
    tasks = [service.generate_report(req) for req in requests]
    results = await asyncio.gather(*tasks)
    return results
```

### Tip 3: Use Appropriate Output Formats

- **PDF only**: Fastest, smallest
- **PDF + Word**: Medium
- **All formats**: Slowest, but most flexible

## Next Steps

1. **Explore Templates** - Customize report templates
2. **API Integration** - Integrate with your systems
3. **Batch Processing** - Automate report generation
4. **Custom Templates** - Create your own templates

## Support

- **Documentation**: `/docs` folder
- **Examples**: `/sample_data` folder
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues

---

**You're ready to generate reports! 🚀**
