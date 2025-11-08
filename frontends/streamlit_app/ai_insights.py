"""
AI Insights Component - Streamlit interface for automated insights and analysis
Provides data analysis, report review, troubleshooting, and decision support
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd


class AIInsightsInterface:
    """AI Insights Interface for Streamlit"""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize insights interface

        Args:
            api_base_url: Base URL for AI Assistant API
        """
        self.api_base_url = api_base_url
        self.analyze_endpoint = f"{api_base_url}/api/v1/ai/analyze"
        self.review_endpoint = f"{api_base_url}/api/v1/ai/review"
        self.troubleshoot_endpoint = f"{api_base_url}/api/v1/ai/troubleshoot"
        self.decision_endpoint = f"{api_base_url}/api/v1/ai/decision"
        self.insights_endpoint = f"{api_base_url}/api/v1/ai/insights"

    def render(self):
        """Render the insights interface"""
        st.title("🔍 AI Insights & Analysis")
        st.markdown("*Intelligent analysis and decision support for your lab operations*")

        # Tab navigation
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Data Analysis",
            "📋 Report Review",
            "🔧 Troubleshooting",
            "🎯 Decision Support",
            "💡 Automated Insights"
        ])

        with tab1:
            self._render_data_analysis()

        with tab2:
            self._render_report_review()

        with tab3:
            self._render_troubleshooting()

        with tab4:
            self._render_decision_support()

        with tab5:
            self._render_automated_insights()

    def _render_data_analysis(self):
        """Render data analysis interface"""
        st.header("Data Analysis")
        st.markdown("Upload or paste your test data for AI-powered analysis")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Data input methods
            input_method = st.radio(
                "Input Method",
                ["Paste JSON", "Upload File", "Sample Data"],
                horizontal=True
            )

            data = None

            if input_method == "Paste JSON":
                data_text = st.text_area(
                    "Paste your data (JSON format)",
                    height=200,
                    placeholder='{"voltage": [0, 5, 10], "current": [8.5, 8.2, 7.8]}'
                )
                if data_text:
                    try:
                        data = json.loads(data_text)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format")

            elif input_method == "Upload File":
                uploaded_file = st.file_uploader(
                    "Upload data file",
                    type=["json", "csv"]
                )
                if uploaded_file:
                    if uploaded_file.name.endswith('.json'):
                        data = json.load(uploaded_file)
                    elif uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                        data = df.to_dict(orient='list')

            else:  # Sample Data
                data = self._get_sample_data()
                st.json(data)

        with col2:
            # Analysis settings
            test_type = st.selectbox(
                "Test Type",
                ["IV Curve", "Thermal Cycling", "Insulation Test", "Mechanical Load", "Other"]
            )

            analysis_type = st.selectbox(
                "Analysis Type",
                ["Comprehensive", "Anomaly Detection", "Trend Analysis", "Prediction"]
            )

            # Analyze button
            if st.button("🔍 Analyze Data", type="primary", use_container_width=True):
                if data:
                    self._perform_data_analysis(data, test_type, analysis_type)
                else:
                    st.warning("Please provide data to analyze")

    def _render_report_review(self):
        """Render report review interface"""
        st.header("Report Review")
        st.markdown("Submit your test report for quality and compliance checking")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Report input
            report_text = st.text_area(
                "Paste report data (JSON format)",
                height=300,
                placeholder='{"test_id": "TC-001", "module_id": "M-123", ...}'
            )

        with col2:
            # Standards selection
            standards = st.multiselect(
                "Applicable Standards",
                ["IEC 61215", "IEC 61730", "UL 1703", "IEC 61853"],
                default=["IEC 61215"]
            )

            # Check types
            check_types = st.multiselect(
                "Check Types",
                ["Completeness", "Accuracy", "Consistency", "Compliance"],
                default=["Completeness", "Compliance"]
            )

            # Review button
            if st.button("📋 Review Report", type="primary", use_container_width=True):
                if report_text:
                    try:
                        report_data = json.loads(report_text)
                        self._perform_report_review(report_data, standards, check_types)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format")
                else:
                    st.warning("Please provide report data")

    def _render_troubleshooting(self):
        """Render troubleshooting interface"""
        st.header("Troubleshooting Assistant")
        st.markdown("Get AI-powered help for equipment and test issues")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Issue description
            issue_description = st.text_area(
                "Describe the issue",
                height=150,
                placeholder="E.g., Solar simulator showing unstable irradiance readings..."
            )

            # Error data (optional)
            with st.expander("Add Error Data (Optional)"):
                error_text = st.text_area(
                    "Error messages or data (JSON format)",
                    height=100,
                    placeholder='{"error_code": "E-123", "message": "Sensor timeout"}'
                )

        with col2:
            # Equipment
            equipment = st.selectbox(
                "Equipment",
                ["Solar Simulator", "Thermal Chamber", "IV Tracer", "Insulation Tester", "Other"],
                index=None,
                placeholder="Select equipment..."
            )

            # Test type
            test_type = st.selectbox(
                "Test Type",
                ["Performance Testing", "Thermal Cycling", "Insulation Test", "Mechanical Test", "Other"],
                index=None,
                placeholder="Select test type..."
            )

            # Get help button
            if st.button("🔧 Get Help", type="primary", use_container_width=True):
                if issue_description:
                    error_data = None
                    if error_text:
                        try:
                            error_data = json.loads(error_text)
                        except json.JSONDecodeError:
                            st.warning("Invalid error data JSON (proceeding without it)")

                    self._get_troubleshooting_help(
                        issue_description,
                        equipment,
                        test_type,
                        error_data
                    )
                else:
                    st.warning("Please describe the issue")

    def _render_decision_support(self):
        """Render decision support interface"""
        st.header("Decision Support")
        st.markdown("Get AI recommendations for resource allocation and optimization")

        # Decision context
        decision_context = st.text_area(
            "Decision Context",
            height=100,
            placeholder="E.g., Need to choose testing equipment for new certification lab..."
        )

        # Options
        st.subheader("Options")
        num_options = st.number_input("Number of options", min_value=2, max_value=5, value=2)

        options = []
        for i in range(num_options):
            with st.expander(f"Option {i+1}"):
                option_name = st.text_input(f"Name", key=f"opt_name_{i}")
                option_cost = st.number_input(f"Cost ($)", key=f"opt_cost_{i}", min_value=0)
                option_desc = st.text_area(f"Description", key=f"opt_desc_{i}", height=80)

                if option_name:
                    options.append({
                        "name": option_name,
                        "cost": option_cost,
                        "description": option_desc
                    })

        # Criteria
        criteria_text = st.text_input(
            "Decision Criteria (comma-separated)",
            placeholder="E.g., cost, performance, reliability, maintenance"
        )
        criteria = [c.strip() for c in criteria_text.split(",")] if criteria_text else None

        # Get recommendation
        if st.button("🎯 Get Recommendation", type="primary"):
            if decision_context and options:
                self._get_decision_support(decision_context, options, criteria)
            else:
                st.warning("Please provide decision context and at least 2 options")

    def _render_automated_insights(self):
        """Render automated insights interface"""
        st.header("Automated Insights")
        st.markdown("Get AI-generated insights from your lab data")

        col1, col2 = st.columns([1, 1])

        with col1:
            data_scope = st.selectbox(
                "Data Scope",
                ["Recent (Last 7 days)", "Last 30 days", "All Time", "Custom Date Range"]
            )

        with col2:
            insight_types = st.multiselect(
                "Insight Types",
                ["Trends", "Anomalies", "Predictions", "Recommendations"],
                default=["Trends", "Recommendations"]
            )

        if st.button("💡 Generate Insights", type="primary"):
            self._get_automated_insights(data_scope, insight_types)

    # API call methods

    def _perform_data_analysis(
        self,
        data: Dict[str, Any],
        test_type: str,
        analysis_type: str
    ):
        """Perform data analysis via API"""
        with st.spinner("Analyzing data..."):
            try:
                payload = {
                    "data": data,
                    "test_type": test_type,
                    "analysis_type": analysis_type.lower()
                }

                response = requests.post(
                    self.analyze_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("Analysis Complete!")
                        st.markdown("### Analysis Results")
                        st.markdown(result["analysis"])

                        # Show usage stats
                        if "usage" in result:
                            with st.expander("Token Usage"):
                                st.json(result["usage"])
                    else:
                        st.error(f"Analysis failed: {result.get('error')}")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    def _perform_report_review(
        self,
        report_data: Dict[str, Any],
        standards: List[str],
        check_types: List[str]
    ):
        """Perform report review via API"""
        with st.spinner("Reviewing report..."):
            try:
                payload = {
                    "report_data": report_data,
                    "standards": standards,
                    "check_types": check_types
                }

                response = requests.post(
                    self.review_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("Review Complete!")
                        st.markdown("### Review Results")
                        st.markdown(result["review"])

                        # Show structured review if available
                        if "structured_review" in result:
                            with st.expander("Structured Review Details"):
                                st.json(result["structured_review"])
                    else:
                        st.error(f"Review failed: {result.get('error')}")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    def _get_troubleshooting_help(
        self,
        issue_description: str,
        equipment: Optional[str],
        test_type: Optional[str],
        error_data: Optional[Dict[str, Any]]
    ):
        """Get troubleshooting help via API"""
        with st.spinner("Analyzing issue..."):
            try:
                payload = {
                    "issue_description": issue_description,
                    "equipment": equipment,
                    "test_type": test_type,
                    "error_data": error_data
                }

                response = requests.post(
                    self.troubleshoot_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("Troubleshooting Guidance Ready!")
                        st.markdown("### Guidance")
                        st.markdown(result["guidance"])
                    else:
                        st.error(f"Failed: {result.get('error')}")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    def _get_decision_support(
        self,
        decision_context: str,
        options: List[Dict[str, Any]],
        criteria: Optional[List[str]]
    ):
        """Get decision support via API"""
        with st.spinner("Analyzing options..."):
            try:
                payload = {
                    "decision_context": decision_context,
                    "options": options,
                    "criteria": criteria
                }

                response = requests.post(
                    self.decision_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("Recommendation Ready!")
                        st.markdown("### Recommendation")
                        st.markdown(result["recommendation"])
                    else:
                        st.error(f"Failed: {result.get('error')}")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    def _get_automated_insights(
        self,
        data_scope: str,
        insight_types: List[str]
    ):
        """Get automated insights via API"""
        with st.spinner("Generating insights..."):
            try:
                payload = {
                    "data_scope": data_scope.lower().replace(" ", "_"),
                    "insight_types": insight_types
                }

                response = requests.post(
                    self.insights_endpoint,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("Insights Generated!")
                        st.markdown("### Insights")
                        if result.get("insights"):
                            for insight in result["insights"]:
                                st.markdown(f"- {insight}")
                        else:
                            st.info("No insights available for the selected scope. This feature will populate with actual data once the system is in use.")
                    else:
                        st.error(f"Failed: {result.get('error')}")
                else:
                    st.error(f"API error: {response.status_code}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    def _get_sample_data(self) -> Dict[str, Any]:
        """Get sample test data"""
        return {
            "test_id": "IV-001",
            "module_id": "M-12345",
            "voltage": [0, 5, 10, 15, 20, 25, 30, 35, 40],
            "current": [8.5, 8.4, 8.3, 8.1, 7.8, 7.2, 6.1, 4.2, 0.5],
            "temperature": [25.1, 25.2, 25.3, 25.2, 25.3, 25.4, 25.3, 25.2, 25.1],
            "irradiance": 1000,
            "timestamp": datetime.now().isoformat()
        }


def render_standalone():
    """Render as standalone Streamlit app"""
    st.set_page_config(
        page_title="AI Insights - Solar PV Lab",
        page_icon="🔍",
        layout="wide"
    )

    insights_interface = AIInsightsInterface()
    insights_interface.render()


if __name__ == "__main__":
    render_standalone()
