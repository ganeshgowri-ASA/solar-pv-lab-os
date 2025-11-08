"""
Example: Generate a sample report using the AI Report Generator
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import datetime
from backend.models.report_models import (
    ReportRequest,
    ReportType,
    ReportFormat,
    TestResult,
    TestStandard,
)
from backend.services.report_generation_service import ReportGenerationService


async def main():
    """Generate a sample I-V characteristic test report"""

    print("🌞 Solar PV Lab OS - AI Report Generator")
    print("=" * 50)
    print("Generating sample report...\n")

    # Create test result data
    test_result = TestResult(
        test_id="TEST-001",
        test_name="I-V Characteristic Test",
        test_method="IEC 61215-2:2016 - MST 01",
        standard=TestStandard.IEC_61215,
        test_date=datetime.now(),
        operator="John Doe",
        equipment_used=["Solar Simulator SS-150A", "I-V Tracer IVT-3000"],
        sample_id="SAMPLE-2024-001",
        manufacturer="SolarTech Industries",
        model="ST-300-72M",
        serial_number="ST2024001234",
        parameters={
            "Irradiance": "1000 W/m²",
            "Spectrum": "AM 1.5G",
            "Module Temperature": "25±2°C",
            "Ambient Temperature": "23°C",
        },
        measurements={
            "Voc": "45.2 V",
            "Isc": "8.95 A",
            "Vmp": "37.1 V",
            "Imp": "8.09 A",
            "Pmax": "300.1 W",
            "FF": "0.742",
        },
        calculated_values={
            "Efficiency": "18.45%",
            "Power Density": "184.4 W/m²",
        },
        pass_fail_criteria={
            "Pmax": "≥ 285W (95% of rated)",
            "Fill Factor": "≥ 0.70",
            "Efficiency": "≥ 17.5%",
        },
        overall_result="PASS",
        notes="Module performed within specifications. All parameters met the required criteria.",
    )

    # Create report request
    request = ReportRequest(
        report_type=ReportType.TEST_RESULT,
        template_id="test_result_iec61215",
        report_title="Solar Module I-V Characteristic Test Report",
        client_name="ABC Solar Industries",
        client_address="123 Solar Street, Green City, 12345",
        project_name="Q1 2024 Module Testing",
        test_results=[test_result],
        output_formats=[ReportFormat.PDF, ReportFormat.WORD],
        enable_ai_enhancement=True,
        enable_spell_check=True,
        enable_grammar_check=True,
        enable_compliance_check=True,
    )

    # Generate report
    print("📝 Creating report with AI enhancement...")
    service = ReportGenerationService()

    try:
        response = await service.generate_report(request)

        if response.success:
            print("\n✅ Report Generated Successfully!\n")
            print(f"Report ID: {response.report_id}")
            print(f"Generation Time: {response.metadata.generation_time_seconds:.2f}s")
            print(f"\nGenerated Files:")

            for format_type, file_path in response.files.items():
                file_size = response.metadata.file_sizes.get(format_type, 0) / 1024
                print(f"  📄 {format_type.upper()}: {file_path} ({file_size:.2f} KB)")

            # Quality check results
            if response.quality_check:
                print(f"\n📊 Quality Score: {response.quality_check.overall_quality_score:.1f}/100")

                if response.quality_check.has_errors:
                    print("\n⚠️  Quality Issues Found:")

                    if response.quality_check.typos_found:
                        print(f"  - Typos: {len(response.quality_check.typos_found)}")

                    if response.quality_check.grammar_issues:
                        print(f"  - Grammar: {len(response.quality_check.grammar_issues)}")

                    if response.quality_check.missing_data:
                        print(f"  - Missing Data: {len(response.quality_check.missing_data)}")
                else:
                    print("✅ No quality issues found!")

            print("\n" + "=" * 50)
            print("✨ Report generation complete!")

        else:
            print(f"\n❌ Report generation failed: {response.message}")

            if response.errors:
                print("\nErrors:")
                for error in response.errors:
                    print(f"  - {error}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
