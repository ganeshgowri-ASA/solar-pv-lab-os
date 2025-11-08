# API Guide - Solar PV Lab OS Report Generator

## Overview

The Report Generator API provides RESTful endpoints for automated report generation, template management, quality checking, and data extraction.

**Base URL**: `http://localhost:8000`

**API Documentation**: `http://localhost:8000/docs` (Interactive Swagger UI)

## Authentication

Currently, the API does not require authentication. In production, implement API key authentication:

```python
headers = {
    "X-API-Key": "your_api_key"
}
```

## Endpoints

### 1. Generate Report

Generate a complete report from test data.

**Endpoint**: `POST /api/reports/generate`

**Request Body**:
```json
{
  "report_type": "test_result",
  "template_id": "test_result_iec61215",
  "report_title": "Solar Module Test Report",
  "client_name": "ABC Solar Inc.",
  "client_address": "123 Solar Street, City",
  "project_name": "Project Alpha",
  "report_date": "2024-01-15T10:30:00",
  "test_results": [
    {
      "test_id": "TEST-001",
      "test_name": "I-V Characteristic Test",
      "test_method": "IEC 61215-2:2016",
      "standard": "IEC 61215",
      "test_date": "2024-01-15T10:30:00",
      "operator": "John Doe",
      "equipment_used": ["Solar Simulator", "I-V Tracer"],
      "sample_id": "SAMPLE-001",
      "manufacturer": "SolarTech Industries",
      "model": "ST-300-72M",
      "serial_number": "SN123456",
      "parameters": {
        "irradiance": "1000 W/m²",
        "temperature": "25°C"
      },
      "measurements": {
        "Voc": "45.2 V",
        "Isc": "8.95 A",
        "Vmp": "37.1 V",
        "Imp": "8.09 A",
        "Pmax": "300.1 W",
        "FF": "0.742"
      },
      "calculated_values": {
        "efficiency": "18.45%"
      },
      "pass_fail_criteria": {
        "Pmax": ">= 285W",
        "FF": ">= 0.70"
      },
      "overall_result": "PASS",
      "notes": "Module performed within specifications."
    }
  ],
  "output_formats": ["pdf", "word", "excel"],
  "enable_ai_enhancement": true,
  "enable_spell_check": true,
  "enable_grammar_check": true,
  "enable_compliance_check": true
}
```

**Response**:
```json
{
  "success": true,
  "report_id": "a1b2c3d4",
  "message": "Report generated successfully in 3 format(s)",
  "files": {
    "pdf": "/path/to/report.pdf",
    "word": "/path/to/report.docx",
    "excel": "/path/to/report.xlsx"
  },
  "metadata": {
    "report_id": "a1b2c3d4",
    "version": "1.0",
    "created_at": "2024-01-15T10:35:00",
    "generation_time_seconds": 8.5,
    "ai_enhanced": true,
    "quality_checked": true,
    "file_paths": {...},
    "file_sizes": {...}
  },
  "quality_check": {
    "has_errors": false,
    "typos_found": [],
    "grammar_issues": [],
    "missing_data": [],
    "compliance_issues": [],
    "suggestions": [],
    "overall_quality_score": 98.5
  }
}
```

**Python Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/reports/generate",
    json={
        "report_type": "test_result",
        "report_title": "Test Report",
        "client_name": "Client ABC",
        "test_results": [...],
        "output_formats": ["pdf"]
    }
)

result = response.json()
print(f"Report ID: {result['report_id']}")
print(f"PDF Path: {result['files']['pdf']}")
```

### 2. List Templates

Get all available report templates.

**Endpoint**: `GET /api/reports/templates`

**Response**:
```json
[
  {
    "template_id": "test_result_iec61215",
    "name": "Test Result Report - IEC 61215",
    "report_type": "test_result",
    "description": "Standard test result report following IEC 61215 format",
    "version": "1.0",
    "sections": [
      "cover_page",
      "executive_summary",
      "test_information",
      "results",
      "conclusions"
    ],
    "required_fields": [
      "test_id",
      "sample_id",
      "test_date"
    ]
  }
]
```

**Python Example**:
```python
response = requests.get("http://localhost:8000/api/reports/templates")
templates = response.json()

for template in templates:
    print(f"{template['name']} ({template['template_id']})")
```

### 3. Get Template

Get a specific template by ID.

**Endpoint**: `GET /api/reports/templates/{template_id}`

**Response**: Single template object (same structure as list item above)

### 4. Upload Excel File

Upload Excel file for data extraction.

**Endpoint**: `POST /api/reports/upload/excel`

**Request**: Multipart form data with file

**Response**:
```json
{
  "success": true,
  "sheets": {
    "Sheet1": [
      {"column1": "value1", "column2": "value2"}
    ]
  },
  "sheet_names": ["Sheet1", "Sheet2"]
}
```

**Python Example**:
```python
files = {'file': open('test_data.xlsx', 'rb')}
response = requests.post(
    "http://localhost:8000/api/reports/upload/excel",
    files=files
)
data = response.json()
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/reports/upload/excel" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_data.xlsx"
```

### 5. Quality Check

Perform quality check on report content.

**Endpoint**: `POST /api/reports/quality-check`

**Request Body**:
```json
{
  "content": "Your report content here..."
}
```

**Response**:
```json
{
  "has_errors": false,
  "typos_found": [
    {
      "original": "teh",
      "correction": "the",
      "reason": "Common typo"
    }
  ],
  "grammar_issues": [
    {
      "issue": "Subject-verb disagreement",
      "suggestion": "Change 'was' to 'were'",
      "severity": "medium"
    }
  ],
  "overall_quality_score": 95.0
}
```

### 6. Download Report

Download a generated report file.

**Endpoint**: `GET /api/reports/download/{report_id}/{format}`

**Parameters**:
- `report_id`: Report identifier
- `format`: File format (pdf, word, excel)

**Response**: File download

**Python Example**:
```python
response = requests.get(
    "http://localhost:8000/api/reports/download/a1b2c3d4/pdf",
    stream=True
)

with open("report.pdf", "wb") as f:
    f.write(response.content)
```

### 7. Validate Test Data

Validate test result data structure.

**Endpoint**: `POST /api/reports/validate/data`

**Request Body**: Test result object

**Response**:
```json
{
  "is_valid": true,
  "issues": []
}
```

### 8. Health Check

Check API health status.

**Endpoint**: `GET /api/reports/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "AI Report Generator",
  "version": "1.0.0"
}
```

### 9. Statistics

Get report generation statistics.

**Endpoint**: `GET /api/reports/stats`

**Response**:
```json
{
  "total_reports": 150,
  "pdf_count": 100,
  "word_count": 75,
  "excel_count": 50,
  "total_size_mb": 245.6
}
```

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Examples

**Invalid Template**:
```json
{
  "detail": "Template not found: invalid_template_id"
}
```

**Generation Failed**:
```json
{
  "detail": "Report generation failed: Missing required field 'test_id'"
}
```

## Rate Limiting

Currently no rate limiting. In production, implement:
- 100 requests per minute per API key
- 1000 requests per hour per API key

## Best Practices

### 1. Use Async Requests

```python
import asyncio
import aiohttp

async def generate_report(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/api/reports/generate",
            json=data
        ) as response:
            return await response.json()

result = asyncio.run(generate_report(report_data))
```

### 2. Handle Errors Gracefully

```python
try:
    response = requests.post(url, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### 3. Validate Data Before Sending

```python
# Validate test data first
validation_response = requests.post(
    "http://localhost:8000/api/reports/validate/data",
    json=test_data
)

if validation_response.json()["is_valid"]:
    # Proceed with report generation
    pass
```

### 4. Use Appropriate Timeouts

```python
# Large reports may take time
response = requests.post(
    url,
    json=data,
    timeout=120  # 2 minutes
)
```

## Integration Examples

### GenSpark Integration

```python
# GenSpark client calling the API
import requests

class ReportGeneratorClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_report(self, test_data):
        endpoint = f"{self.base_url}/api/reports/generate"
        response = requests.post(endpoint, json=test_data)
        return response.json()

# Usage
client = ReportGeneratorClient("http://localhost:8000")
result = client.generate_report(test_data)
```

### Snowflake Integration

```python
# Snowflake stored procedure
import snowflake.snowpark as snowpark
import requests
import json

def generate_report_from_snowflake(session, test_id):
    # Get test data from Snowflake
    df = session.table("TEST_RESULTS").filter(f"TEST_ID = '{test_id}'")
    test_data = df.to_pandas().to_dict('records')[0]

    # Call API
    response = requests.post(
        "http://report-generator-api/api/reports/generate",
        json={
            "report_type": "test_result",
            "test_results": [test_data],
            "output_formats": ["pdf"]
        }
    )

    return response.json()["report_id"]
```

## Webhooks (Future)

Future webhook support for async notifications:

```json
{
  "webhook_url": "https://your-app.com/webhook",
  "events": ["report.generated", "report.failed"]
}
```

## SDK (Future)

Python SDK for easier integration:

```python
from solar_pv_lab_sdk import ReportGenerator

client = ReportGenerator(api_key="your_key")

report = client.create_report(
    report_type="test_result",
    test_results=[...],
    formats=["pdf", "word"]
)

print(f"Report generated: {report.id}")
report.download("pdf", "output.pdf")
```

---

For more information, visit the interactive API documentation at:
**http://localhost:8000/docs**
