# AI Assistant API Documentation

## Overview

The Solar PV Lab AI Assistant API provides intelligent assistance for laboratory operations using Claude AI. The API offers capabilities for conversational assistance, data analysis, report review, troubleshooting, and decision support.

**Base URL:** `http://localhost:8000`

**API Version:** v1

---

## Authentication

Currently, the API does not require authentication. For production deployment, implement appropriate authentication mechanisms.

---

## Endpoints

### 1. Chat with AI Assistant

**Endpoint:** `POST /api/v1/ai/chat`

**Description:** Engage in conversational interaction with the AI assistant.

**Request Body:**
```json
{
  "message": "What are the requirements for IEC 61215 thermal cycling test?",
  "session_id": "unique-session-id",
  "user_id": "optional-user-id",
  "include_context": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "The IEC 61215 thermal cycling test (TC200) requires...",
  "session_id": "unique-session-id",
  "context_used": true,
  "usage": {
    "input_tokens": 150,
    "output_tokens": 300
  },
  "timestamp": "2025-11-08T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain IV curve testing",
    "session_id": "test-session-123",
    "include_context": true
  }'
```

---

### 2. Analyze Test Data

**Endpoint:** `POST /api/v1/ai/analyze`

**Description:** Analyze test data with AI-powered insights.

**Request Body:**
```json
{
  "data": {
    "voltage": [0, 10, 20, 30, 40],
    "current": [8.5, 8.3, 7.8, 6.1, 0.5],
    "temperature": 25.2,
    "irradiance": 1000
  },
  "test_type": "IV Curve",
  "analysis_type": "comprehensive",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": "The I-V curve shows normal behavior with...",
  "analysis_type": "comprehensive",
  "usage": {
    "input_tokens": 200,
    "output_tokens": 450
  },
  "timestamp": "2025-11-08T10:35:00Z"
}
```

**Analysis Types:**
- `comprehensive` - Complete analysis of all aspects
- `anomaly` - Focus on anomaly detection
- `trend` - Identify trends and patterns
- `prediction` - Predictive analysis

---

### 3. Review Test Report

**Endpoint:** `POST /api/v1/ai/review`

**Description:** Review test reports for quality and compliance.

**Request Body:**
```json
{
  "report_data": {
    "test_id": "TC-001",
    "module_id": "M-12345",
    "test_type": "Thermal Cycling",
    "results": {
      "initial_pmax": 300.5,
      "final_pmax": 287.3,
      "degradation": 4.39
    }
  },
  "standards": ["IEC 61215", "IEC 61730"],
  "check_types": ["completeness", "compliance"]
}
```

**Response:**
```json
{
  "success": true,
  "review": "Report Review:\n1. Completeness: All required fields present...",
  "structured_review": {
    "has_issues": false,
    "completeness_score": 0.95,
    "timestamp": "2025-11-08T10:40:00Z"
  },
  "standards_checked": ["IEC 61215", "IEC 61730"],
  "usage": {
    "input_tokens": 180,
    "output_tokens": 320
  },
  "timestamp": "2025-11-08T10:40:00Z"
}
```

---

### 4. Get Troubleshooting Help

**Endpoint:** `POST /api/v1/ai/troubleshoot`

**Description:** Get AI-powered troubleshooting guidance.

**Request Body:**
```json
{
  "issue_description": "Solar simulator showing unstable irradiance readings",
  "equipment": "Solar Simulator",
  "test_type": "Performance Testing",
  "error_data": {
    "error_code": "E-123",
    "reading_variance": 15.3
  },
  "session_id": "troubleshoot-session"
}
```

**Response:**
```json
{
  "success": true,
  "guidance": "Troubleshooting Steps:\n1. Check lamp age and condition...",
  "usage": {
    "input_tokens": 120,
    "output_tokens": 400
  },
  "timestamp": "2025-11-08T10:45:00Z"
}
```

---

### 5. Decision Support

**Endpoint:** `POST /api/v1/ai/decision`

**Description:** Get AI recommendations for decisions.

**Request Body:**
```json
{
  "decision_context": "Need to choose solar simulator for new lab",
  "options": [
    {
      "name": "Simulator A",
      "cost": 50000,
      "description": "Class AAA, 1000W/m² uniform"
    },
    {
      "name": "Simulator B",
      "cost": 35000,
      "description": "Class ABA, 1000W/m²"
    }
  ],
  "criteria": ["cost", "performance", "reliability"],
  "session_id": "decision-session"
}
```

**Response:**
```json
{
  "success": true,
  "recommendation": "Recommendation:\nBased on your criteria...",
  "usage": {
    "input_tokens": 160,
    "output_tokens": 380
  },
  "timestamp": "2025-11-08T10:50:00Z"
}
```

---

### 6. Get Automated Insights

**Endpoint:** `POST /api/v1/ai/insights`

**Description:** Get automated insights from system data.

**Request Body:**
```json
{
  "data_scope": "recent",
  "insight_types": ["trends", "recommendations"]
}
```

**Response:**
```json
{
  "success": true,
  "scope": "recent",
  "insights": [
    "Trend: Module degradation rates increasing",
    "Recommendation: Review thermal cycling parameters"
  ],
  "timestamp": "2025-11-08T10:55:00Z"
}
```

---

### 7. Detect Intent

**Endpoint:** `POST /api/v1/ai/intent`

**Description:** Detect user intent from message.

**Request Body:**
```json
{
  "message": "How do I analyze my test data?"
}
```

**Response:**
```json
{
  "intent": "analyze_data",
  "confidence": 0.85,
  "message": "How do I analyze my test data?"
}
```

**Intent Types:**
- `analyze_data` - User wants to analyze data
- `troubleshoot` - User has a problem
- `question` - User asking a question
- `review_report` - User wants report review
- `decision_support` - User needs decision help
- `chat` - General conversation

---

### 8. Health Check

**Endpoint:** `GET /health`

**Description:** Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T11:00:00Z"
}
```

---

### 9. Root Endpoint

**Endpoint:** `GET /`

**Description:** Get API information and available endpoints.

**Response:**
```json
{
  "service": "Solar PV Lab AI Assistant API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "chat": "/api/v1/ai/chat",
    "analyze": "/api/v1/ai/analyze",
    "review": "/api/v1/ai/review",
    "troubleshoot": "/api/v1/ai/troubleshoot",
    "decision": "/api/v1/ai/decision",
    "insights": "/api/v1/ai/insights",
    "intent": "/api/v1/ai/intent"
  }
}
```

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "success": false,
  "error": "Error description",
  "timestamp": "2025-11-08T11:00:00Z"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, implement appropriate rate limiting based on your requirements.

---

## Python Client Example

```python
import requests

# Initialize
api_url = "http://localhost:8000"

# Chat example
response = requests.post(
    f"{api_url}/api/v1/ai/chat",
    json={
        "message": "What is IEC 61215?",
        "session_id": "my-session",
        "include_context": True
    }
)

result = response.json()
print(result["message"])

# Analyze data example
test_data = {
    "voltage": [0, 10, 20, 30, 40],
    "current": [8.5, 8.3, 7.8, 6.1, 0.5]
}

response = requests.post(
    f"{api_url}/api/v1/ai/analyze",
    json={
        "data": test_data,
        "test_type": "IV Curve",
        "analysis_type": "comprehensive"
    }
)

analysis = response.json()
print(analysis["analysis"])
```

---

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These provide interactive API documentation where you can test endpoints directly.

---

## Support

For issues or questions, please refer to the main README or open an issue in the repository.
