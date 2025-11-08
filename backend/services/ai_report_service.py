"""
AI-powered report generation service using Claude API
"""
import anthropic
from typing import Dict, Any, List, Optional
import json
from backend.config import get_settings


class AIReportService:
    """
    Service for AI-powered report generation and enhancement using Claude API
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)

    async def generate_report_section(
        self,
        section_name: str,
        test_data: Dict[str, Any],
        context: Optional[str] = None,
    ) -> str:
        """
        Generate a report section using AI based on test data

        Args:
            section_name: Name of the section (e.g., "Introduction", "Test Results")
            test_data: Dictionary containing test data
            context: Additional context for generation

        Returns:
            Generated section content
        """
        prompt = self._build_generation_prompt(section_name, test_data, context)

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=self.settings.ai_max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text

        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")

    async def check_spelling_and_grammar(self, text: str) -> Dict[str, Any]:
        """
        Check spelling and grammar using AI

        Args:
            text: Text to check

        Returns:
            Dictionary with issues found and corrections
        """
        prompt = f"""You are a professional editor for solar PV testing laboratory reports.
Review the following text for spelling and grammar errors. Pay special attention to:
- Technical terms related to solar PV (photovoltaic, irradiance, I-V curve, etc.)
- Standard names (IEC 61215, UL 1703, etc.)
- Units and measurements
- Professional tone and clarity

Text to review:
{text}

Provide your response in JSON format with the following structure:
{{
    "has_errors": true/false,
    "typos": [
        {{"original": "...", "correction": "...", "position": "line/word", "reason": "..."}}
    ],
    "grammar_issues": [
        {{"issue": "...", "suggestion": "...", "position": "...", "severity": "low/medium/high"}}
    ],
    "technical_term_issues": [
        {{"term": "...", "issue": "...", "correct_form": "..."}}
    ],
    "overall_assessment": "Brief assessment of the text quality"
}}
"""

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=self.settings.ai_max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            return json.loads(response_text.strip())

        except Exception as e:
            return {
                "has_errors": False,
                "typos": [],
                "grammar_issues": [],
                "technical_term_issues": [],
                "overall_assessment": f"Error during checking: {str(e)}",
            }

    async def validate_compliance(
        self, report_content: str, standard: str = "IEC 61215"
    ) -> Dict[str, Any]:
        """
        Validate report compliance with testing standards

        Args:
            report_content: Full report content
            standard: Testing standard to check against

        Returns:
            Compliance validation results
        """
        prompt = f"""You are an expert in solar PV testing standards, specifically {standard}.
Review the following report content for compliance with {standard} requirements.
Check for:
- Required sections and information
- Proper terminology and units
- Adherence to reporting format
- Completeness of test data
- Proper citations and references

Report content:
{report_content[:3000]}  # Limit to avoid token overflow

Provide your response in JSON format:
{{
    "compliant": true/false,
    "missing_sections": ["..."],
    "terminology_issues": [{{"issue": "...", "recommendation": "..."}}],
    "format_issues": ["..."],
    "completeness_score": 0-100,
    "recommendations": ["..."]
}}
"""

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=self.settings.ai_max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]

            return json.loads(response_text.strip())

        except Exception as e:
            return {
                "compliant": None,
                "error": str(e),
                "missing_sections": [],
                "recommendations": [],
            }

    async def enhance_report_text(self, text: str, tone: str = "professional") -> str:
        """
        Enhance report text for better readability and professionalism

        Args:
            text: Original text
            tone: Desired tone (professional, technical, formal)

        Returns:
            Enhanced text
        """
        prompt = f"""You are a professional technical writer for a solar PV testing laboratory.
Enhance the following text to make it more {tone} while maintaining technical accuracy.
Keep all technical data, numbers, and measurements exactly as provided.
Improve sentence structure, clarity, and flow.

Original text:
{text}

Provide only the enhanced text without explanations or comments.
"""

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=self.settings.ai_max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text.strip()

        except Exception as e:
            # Return original text if enhancement fails
            return text

    async def generate_executive_summary(
        self, test_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate executive summary from test results

        Args:
            test_results: List of test result dictionaries

        Returns:
            Executive summary text
        """
        # Prepare condensed test data
        summary_data = []
        for result in test_results[:10]:  # Limit to avoid token overflow
            summary_data.append(
                {
                    "test_name": result.get("test_name"),
                    "result": result.get("overall_result"),
                    "key_findings": result.get("notes", "")[:200],
                }
            )

        prompt = f"""You are writing an executive summary for a solar PV module testing report.
Based on the following test results, create a concise executive summary (2-3 paragraphs) that:
- Summarizes the overall testing outcomes
- Highlights key findings and any issues
- Provides a clear conclusion on module performance
- Uses professional, technical language

Test Results:
{json.dumps(summary_data, indent=2)}

Write the executive summary:
"""

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text.strip()

        except Exception as e:
            return f"Executive Summary: Unable to generate - {str(e)}"

    async def interpret_test_results(
        self, test_name: str, measurements: Dict[str, Any], criteria: Dict[str, str]
    ) -> str:
        """
        Generate interpretation of test results

        Args:
            test_name: Name of the test
            measurements: Measurement data
            criteria: Pass/fail criteria

        Returns:
            Interpretation text
        """
        prompt = f"""You are a solar PV testing engineer. Interpret the following test results:

Test: {test_name}

Measurements:
{json.dumps(measurements, indent=2)}

Pass/Fail Criteria:
{json.dumps(criteria, indent=2)}

Provide a professional interpretation that:
- Explains what the measurements mean
- Compares results against criteria
- Provides context about why this matters
- Suggests any implications or next steps if applicable

Keep it concise (2-3 sentences) and technical but clear.
"""

        try:
            message = self.client.messages.create(
                model=self.settings.ai_model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text.strip()

        except Exception as e:
            return f"Standard test results for {test_name}"

    def _build_generation_prompt(
        self, section_name: str, test_data: Dict[str, Any], context: Optional[str]
    ) -> str:
        """Build prompt for section generation"""

        base_prompt = f"""You are a technical writer for a NABL-accredited solar PV testing laboratory.
Generate the "{section_name}" section of a test report.

Test Data:
{json.dumps(test_data, indent=2, default=str)[:2000]}

{f"Additional Context: {context}" if context else ""}

Requirements:
- Use professional, technical language
- Follow IEC/UL standard reporting formats
- Be precise with technical terms and units
- Include all relevant data
- Maintain objectivity and accuracy

Generate the {section_name} section:
"""
        return base_prompt

    async def check_data_completeness(
        self, test_data: Dict[str, Any], required_fields: List[str]
    ) -> Dict[str, Any]:
        """
        Check if test data is complete

        Args:
            test_data: Test data to check
            required_fields: List of required field names

        Returns:
            Completeness check results
        """
        missing_fields = []
        for field in required_fields:
            if field not in test_data or not test_data[field]:
                missing_fields.append(field)

        return {
            "is_complete": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "completeness_percentage": (
                (len(required_fields) - len(missing_fields)) / len(required_fields)
            )
            * 100
            if required_fields
            else 100,
        }
