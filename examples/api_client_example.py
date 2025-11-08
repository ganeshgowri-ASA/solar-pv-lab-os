"""
Example: Using the Report Generator API with requests library
"""
import requests
import json
from datetime import datetime


def generate_report_via_api():
    """Generate a report using the REST API"""

    # API endpoint
    base_url = "http://localhost:8000"

    # Prepare test data
    test_result = {
        "test_id": "TEST-API-001",
        "test_name": "I-V Characteristic Test",
        "test_method": "IEC 61215-2:2016",
        "standard": "IEC 61215",
        "test_date": datetime.now().isoformat(),
        "operator": "API User",
        "equipment_used": ["Solar Simulator", "I-V Tracer"],
        "sample_id": "SAMPLE-API-001",
        "manufacturer": "API Test Manufacturer",
        "model": "API-300",
        "serial_number": "API123456",
        "parameters": {"irradiance": "1000 W/m²", "temperature": "25°C"},
        "measurements": {
            "Voc": "45.2 V",
            "Isc": "8.95 A",
            "Vmp": "37.1 V",
            "Imp": "8.09 A",
            "Pmax": "300.1 W",
            "FF": "0.742",
        },
        "calculated_values": {"efficiency": "18.45%"},
        "pass_fail_criteria": {"Pmax": ">= 285W", "FF": ">= 0.70"},
        "overall_result": "PASS",
        "notes": "Test completed successfully via API",
    }

    # Prepare request payload
    request_data = {
        "report_type": "test_result",
        "template_id": "test_result_iec61215",
        "report_title": "API Generated Test Report",
        "client_name": "API Test Client",
        "client_address": "API Street, API City",
        "test_results": [test_result],
        "output_formats": ["pdf", "word"],
        "enable_ai_enhancement": True,
        "enable_spell_check": True,
        "enable_grammar_check": True,
    }

    print("🚀 Calling Report Generator API...")
    print(f"Endpoint: {base_url}/api/reports/generate")

    try:
        # Make API call
        response = requests.post(
            f"{base_url}/api/reports/generate",
            json=request_data,
            timeout=120,  # 2 minutes timeout
        )

        # Check response
        response.raise_for_status()
        result = response.json()

        print("\n✅ API Call Successful!\n")
        print(f"Report ID: {result['report_id']}")
        print(f"Message: {result['message']}")
        print(f"\nGenerated Files:")

        for format_type, file_path in result["files"].items():
            print(f"  📄 {format_type.upper()}: {file_path}")

        print(f"\nQuality Score: {result['quality_check']['overall_quality_score']:.1f}/100")

        # Download PDF
        if "pdf" in result["files"]:
            download_report(base_url, result["report_id"], "pdf")

        return result

    except requests.exceptions.Timeout:
        print("❌ Request timeout - report generation taking too long")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def download_report(base_url, report_id, format_type):
    """Download a generated report"""

    print(f"\n📥 Downloading {format_type.upper()} report...")

    try:
        response = requests.get(
            f"{base_url}/api/reports/download/{report_id}/{format_type}", stream=True
        )

        response.raise_for_status()

        # Save file
        filename = f"downloaded_report_{report_id}.{format_type if format_type != 'word' else 'docx'}"

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Downloaded: {filename}")

    except Exception as e:
        print(f"❌ Download failed: {str(e)}")


def list_templates(base_url="http://localhost:8000"):
    """List available templates"""

    print("📋 Fetching available templates...")

    try:
        response = requests.get(f"{base_url}/api/reports/templates")
        response.raise_for_status()

        templates = response.json()

        print(f"\nFound {len(templates)} template(s):\n")

        for template in templates:
            print(f"ID: {template['template_id']}")
            print(f"Name: {template['name']}")
            print(f"Type: {template['report_type']}")
            print(f"Description: {template['description']}")
            print(f"Sections: {', '.join(template['sections'][:3])}...")
            print("-" * 50)

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def check_api_health(base_url="http://localhost:8000"):
    """Check if API is running"""

    print("🔍 Checking API health...")

    try:
        response = requests.get(f"{base_url}/api/reports/health")
        response.raise_for_status()

        health = response.json()

        print(f"✅ {health['service']} is {health['status']}")
        print(f"Version: {health['version']}")

        return True

    except Exception as e:
        print(f"❌ API is not available: {str(e)}")
        return False


if __name__ == "__main__":
    base_url = "http://localhost:8000"

    # Check if API is running
    if check_api_health(base_url):
        print("\n" + "=" * 50 + "\n")

        # List templates
        list_templates(base_url)

        print("\n" + "=" * 50 + "\n")

        # Generate report
        generate_report_via_api()
    else:
        print("\n⚠️  Please start the API server first:")
        print("python backend/main.py")
