"""
Streamlit UI for AI-Powered Report Generator
"""
import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.models.report_models import (
    ReportRequest,
    ReportType,
    ReportFormat,
    TestResult,
    TestStandard,
)
from backend.services.report_generation_service import ReportGenerationService
from backend.services.template_service import TemplateService
from backend.config import get_settings

# Page configuration
st.set_page_config(
    page_title="AI Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.25rem;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.25rem;
        color: #0c5460;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🌞 AI-Powered Report Generator</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Initialize services
    if "report_service" not in st.session_state:
        st.session_state.report_service = ReportGenerationService()
        st.session_state.template_service = TemplateService()
        st.session_state.settings = get_settings()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.subheader("Laboratory Information")
        st.info(f"""
        **Lab:** {st.session_state.settings.lab_name}
        **NABL Cert:** {st.session_state.settings.lab_nabl_cert}
        **AI Model:** {st.session_state.settings.ai_model}
        """)

        st.subheader("Quick Actions")
        if st.button("🔄 Refresh Templates"):
            st.session_state.template_service = TemplateService()
            st.success("Templates refreshed!")

        if st.button("📁 Open Reports Folder"):
            st.info(f"Reports location:\n{st.session_state.settings.reports_output_dir}")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Generate Report", "📋 Templates", "✅ Quality Check", "📊 Statistics"])

    with tab1:
        generate_report_tab()

    with tab2:
        templates_tab()

    with tab3:
        quality_check_tab()

    with tab4:
        statistics_tab()


def generate_report_tab():
    """Report generation tab"""
    st.header("Generate Report")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Report Information")

        report_title = st.text_input("Report Title", "Test Result Report")
        client_name = st.text_input("Client Name", "Test Client")
        client_address = st.text_area("Client Address (Optional)", "", height=100)
        project_name = st.text_input("Project Name (Optional)", "")

        # Report type and template
        report_type = st.selectbox(
            "Report Type",
            options=[rt.value for rt in ReportType],
            format_func=lambda x: x.replace("_", " ").title(),
        )

        # Get templates for this report type
        templates = st.session_state.template_service.list_templates()
        template_options = {t.template_id: t.name for t in templates}

        template_id = st.selectbox(
            "Template",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x],
        )

    with col2:
        st.subheader("Output Options")

        output_formats = st.multiselect(
            "Output Formats",
            options=[fmt.value for fmt in ReportFormat],
            default=["pdf"],
            format_func=lambda x: x.upper(),
        )

        st.subheader("AI Features")

        enable_ai = st.checkbox("Enable AI Enhancement", value=True)
        enable_spell = st.checkbox("Spell Check", value=True)
        enable_grammar = st.checkbox("Grammar Check", value=True)
        enable_compliance = st.checkbox("Compliance Check", value=True)

    st.markdown("---")

    # Test Results Input
    st.subheader("Test Results")

    num_tests = st.number_input("Number of Tests", min_value=1, max_value=10, value=1)

    test_results = []

    for i in range(num_tests):
        with st.expander(f"Test {i+1}", expanded=(i == 0)):
            col1, col2 = st.columns(2)

            with col1:
                test_id = st.text_input(f"Test ID", f"TEST-{i+1:03d}", key=f"test_id_{i}")
                test_name = st.text_input(
                    f"Test Name",
                    f"I-V Characteristic Test",
                    key=f"test_name_{i}",
                )
                test_method = st.text_input(
                    f"Test Method",
                    "IEC 61215-2:2016",
                    key=f"test_method_{i}",
                )
                standard = st.selectbox(
                    f"Standard",
                    options=[s.value for s in TestStandard],
                    key=f"standard_{i}",
                )

            with col2:
                sample_id = st.text_input(f"Sample ID", f"SAMPLE-{i+1:03d}", key=f"sample_id_{i}")
                manufacturer = st.text_input(f"Manufacturer", "Test Manufacturer", key=f"mfr_{i}")
                model = st.text_input(f"Model", "PV-300W", key=f"model_{i}")
                serial_number = st.text_input(f"Serial Number", f"SN{i+1:06d}", key=f"sn_{i}")

            operator = st.text_input(f"Operator", "Test Engineer", key=f"operator_{i}")

            # Sample measurements
            st.write("**Key Measurements**")
            col1, col2, col3 = st.columns(3)

            with col1:
                voc = st.number_input(f"Voc (V)", value=38.5, key=f"voc_{i}")
                isc = st.number_input(f"Isc (A)", value=9.2, key=f"isc_{i}")

            with col2:
                vmp = st.number_input(f"Vmp (V)", value=31.2, key=f"vmp_{i}")
                imp = st.number_input(f"Imp (A)", value=8.7, key=f"imp_{i}")

            with col3:
                pmax = st.number_input(f"Pmax (W)", value=271.4, key=f"pmax_{i}")
                ff = st.number_input(f"Fill Factor", value=0.766, key=f"ff_{i}")

            result = st.selectbox(
                f"Overall Result",
                options=["PASS", "FAIL", "CONDITIONAL"],
                key=f"result_{i}",
            )

            notes = st.text_area(f"Notes", "", key=f"notes_{i}")

            # Create test result object
            test_result = TestResult(
                test_id=test_id,
                test_name=test_name,
                test_method=test_method,
                standard=TestStandard(standard),
                test_date=datetime.now(),
                operator=operator,
                sample_id=sample_id,
                manufacturer=manufacturer,
                model=model,
                serial_number=serial_number,
                measurements={
                    "Voc": f"{voc} V",
                    "Isc": f"{isc} A",
                    "Vmp": f"{vmp} V",
                    "Imp": f"{imp} A",
                    "Pmax": f"{pmax} W",
                    "FF": f"{ff}",
                },
                calculated_values={
                    "Efficiency": f"{(pmax / 1000) * 100:.2f}%",
                },
                pass_fail_criteria={
                    "Pmax": f">= 270 W",
                    "FF": f">= 0.75",
                },
                overall_result=result,
                notes=notes,
            )

            test_results.append(test_result)

    st.markdown("---")

    # Generate button
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if st.button("🚀 Generate Report", type="primary", use_container_width=True):
            generate_report(
                report_title=report_title,
                client_name=client_name,
                client_address=client_address,
                project_name=project_name,
                report_type=ReportType(report_type),
                template_id=template_id,
                output_formats=[ReportFormat(fmt) for fmt in output_formats],
                test_results=test_results,
                enable_ai=enable_ai,
                enable_spell=enable_spell,
                enable_grammar=enable_grammar,
                enable_compliance=enable_compliance,
            )


def generate_report(**kwargs):
    """Generate report with given parameters"""
    with st.spinner("🤖 Generating report with AI..."):
        try:
            # Create request
            request = ReportRequest(
                report_type=kwargs["report_type"],
                template_id=kwargs["template_id"],
                test_results=kwargs["test_results"],
                report_title=kwargs["report_title"],
                client_name=kwargs["client_name"],
                client_address=kwargs["client_address"],
                project_name=kwargs["project_name"],
                output_formats=kwargs["output_formats"],
                enable_ai_enhancement=kwargs["enable_ai"],
                enable_spell_check=kwargs["enable_spell"],
                enable_grammar_check=kwargs["enable_grammar"],
                enable_compliance_check=kwargs["enable_compliance"],
            )

            # Generate report
            response = asyncio.run(
                st.session_state.report_service.generate_report(request)
            )

            if response.success:
                st.success("✅ Report generated successfully!")

                # Show results
                st.subheader("Generated Files")
                for fmt, path in response.files.items():
                    st.write(f"📄 **{fmt.upper()}:** `{path}`")

                # Show metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Report ID", response.report_id)
                with col2:
                    st.metric(
                        "Generation Time",
                        f"{response.metadata.generation_time_seconds:.2f}s",
                    )
                with col3:
                    st.metric("Files Created", len(response.files))

                # Show quality check results
                if response.quality_check:
                    st.subheader("Quality Check Results")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Quality Score",
                            f"{response.quality_check.overall_quality_score:.1f}/100",
                        )

                    with col2:
                        if response.quality_check.has_errors:
                            st.error("⚠️ Issues found")
                        else:
                            st.success("✅ No issues")

                    if response.quality_check.typos_found:
                        with st.expander("Typos Found"):
                            for typo in response.quality_check.typos_found:
                                st.write(
                                    f"- {typo['original']} → {typo['correction']}"
                                )

                    if response.quality_check.grammar_issues:
                        with st.expander("Grammar Issues"):
                            for issue in response.quality_check.grammar_issues:
                                st.write(f"- {issue['issue']}: {issue['suggestion']}")

                    if response.quality_check.missing_data:
                        with st.expander("Missing Data"):
                            for missing in response.quality_check.missing_data:
                                st.write(f"- {missing}")

            else:
                st.error(f"❌ Report generation failed: {response.message}")

                if response.errors:
                    with st.expander("Error Details"):
                        for error in response.errors:
                            st.write(f"- {error}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def templates_tab():
    """Templates management tab"""
    st.header("Report Templates")

    templates = st.session_state.template_service.list_templates()

    for template in templates:
        with st.expander(f"{template.name} ({template.template_id})"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Type:** {template.report_type.value}")
                st.write(f"**Version:** {template.version}")
                st.write(f"**Description:** {template.description}")

            with col2:
                st.write(f"**Sections:** {len(template.sections)}")
                st.write(f"**Required Fields:** {len(template.required_fields)}")
                st.write(f"**TOC:** {'Yes' if template.include_toc else 'No'}")

            if st.checkbox(f"Show Template Content", key=f"show_{template.template_id}"):
                st.code(template.template_content[:500] + "...", language="markdown")


def quality_check_tab():
    """Quality check tab"""
    st.header("Quality Check")

    st.write("Paste your report content below to check for quality issues:")

    content = st.text_area("Report Content", height=300)

    if st.button("🔍 Check Quality"):
        if content:
            with st.spinner("Analyzing with AI..."):
                try:
                    from backend.services.quality_service import QualityService

                    quality_service = QualityService()

                    result = asyncio.run(
                        quality_service.perform_quality_check(content, [])
                    )

                    # Display results
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Quality Score", f"{result.overall_quality_score:.1f}/100")

                    with col2:
                        if result.has_errors:
                            st.error("⚠️ Issues Found")
                        else:
                            st.success("✅ No Issues")

                    if result.typos_found:
                        st.subheader("Typos")
                        for typo in result.typos_found:
                            st.write(f"- **{typo['original']}** → {typo['correction']}")

                    if result.grammar_issues:
                        st.subheader("Grammar Issues")
                        for issue in result.grammar_issues:
                            st.write(f"- {issue['issue']}: {issue['suggestion']}")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some content to check.")


def statistics_tab():
    """Statistics tab"""
    st.header("Report Statistics")

    try:
        output_dir = Path(st.session_state.settings.reports_output_dir)

        if not output_dir.exists():
            st.info("No reports generated yet.")
            return

        # Count files
        pdf_files = list(output_dir.glob("*.pdf"))
        word_files = list(output_dir.glob("*.docx"))
        excel_files = list(output_dir.glob("*.xlsx"))

        total_size = sum(f.stat().st_size for f in output_dir.iterdir() if f.is_file())

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Reports", len(pdf_files) + len(word_files) + len(excel_files))

        with col2:
            st.metric("PDF Reports", len(pdf_files))

        with col3:
            st.metric("Word Reports", len(word_files))

        with col4:
            st.metric("Total Size", f"{total_size / (1024*1024):.2f} MB")

        # Recent reports
        st.subheader("Recent Reports")

        all_files = sorted(
            output_dir.iterdir(),
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )[:10]

        for file in all_files:
            if file.is_file():
                st.write(
                    f"📄 {file.name} - {file.stat().st_size / 1024:.2f} KB - {datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}"
                )

    except Exception as e:
        st.error(f"Error loading statistics: {str(e)}")


if __name__ == "__main__":
    main()
