"""
Claude Service - Integration with Anthropic's Claude API
Provides intelligent AI assistance for Solar PV Lab operations
"""

import os
import anthropic
from typing import List, Dict, Optional, Any
import json
from datetime import datetime


class ClaudeService:
    """Service for interacting with Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude service

        Args:
            api_key: Anthropic API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"  # Latest Claude model
        self.max_tokens = 4096

    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Send a chat message to Claude

        Args:
            message: User message
            conversation_history: Previous messages in conversation
            system_prompt: System instruction for Claude
            temperature: Sampling temperature (0-1)

        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build messages list
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": message})

            # Default system prompt for Solar PV Lab
            if not system_prompt:
                system_prompt = self._get_default_system_prompt()

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=messages
            )

            # Extract response
            assistant_message = response.content[0].text

            return {
                "success": True,
                "message": assistant_message,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def analyze_data(
        self,
        data: Dict[str, Any],
        analysis_type: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze data using Claude's intelligence

        Args:
            data: Data to analyze (test results, measurements, etc.)
            analysis_type: Type of analysis (anomaly, trend, prediction, etc.)
            context: Additional context about the data

        Returns:
            Analysis results
        """
        try:
            # Build analysis prompt
            prompt = self._build_analysis_prompt(data, analysis_type, context)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.3,  # Lower temperature for analytical tasks
                system=self._get_analysis_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            analysis_result = response.content[0].text

            return {
                "success": True,
                "analysis": analysis_result,
                "analysis_type": analysis_type,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def review_report(
        self,
        report_data: Dict[str, Any],
        standards: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Review a test report for quality and compliance

        Args:
            report_data: Report to review
            standards: Applicable standards (IEC, UL, etc.)

        Returns:
            Review results with suggestions
        """
        try:
            prompt = self._build_review_prompt(report_data, standards)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.2,  # Very low temperature for precise reviews
                system=self._get_review_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            review_result = response.content[0].text

            return {
                "success": True,
                "review": review_result,
                "standards_checked": standards or [],
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_troubleshooting_help(
        self,
        issue_description: str,
        equipment: Optional[str] = None,
        test_type: Optional[str] = None,
        error_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get troubleshooting guidance from Claude

        Args:
            issue_description: Description of the problem
            equipment: Equipment involved
            test_type: Type of test being performed
            error_data: Any error messages or data

        Returns:
            Troubleshooting guidance
        """
        try:
            prompt = self._build_troubleshooting_prompt(
                issue_description,
                equipment,
                test_type,
                error_data
            )

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.5,
                system=self._get_troubleshooting_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            guidance = response.content[0].text

            return {
                "success": True,
                "guidance": guidance,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_decision_support(
        self,
        decision_context: str,
        options: List[Dict[str, Any]],
        criteria: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get decision support from Claude

        Args:
            decision_context: Context of the decision
            options: Available options to choose from
            criteria: Decision criteria

        Returns:
            Decision recommendation with reasoning
        """
        try:
            prompt = self._build_decision_prompt(decision_context, options, criteria)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.4,
                system=self._get_decision_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )

            recommendation = response.content[0].text

            return {
                "success": True,
                "recommendation": recommendation,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    # Private helper methods for building prompts

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for general chat"""
        return """You are an AI assistant specializing in solar photovoltaic (PV) laboratory testing and certification.

You have expertise in:
- IEC 61215, IEC 61730, UL 1703, and other PV standards
- PV module testing procedures (performance, safety, durability)
- Test equipment operation and calibration
- Data analysis and quality control
- Troubleshooting test issues
- Report generation and compliance

Provide accurate, helpful, and safety-conscious guidance. Always reference relevant standards when applicable. Be clear and concise in your explanations."""

    def _get_analysis_system_prompt(self) -> str:
        """Get system prompt for data analysis tasks"""
        return """You are a data analysis expert for solar PV laboratory testing.

Your role is to:
- Identify anomalies and outliers in test data
- Detect trends and patterns
- Provide statistical insights
- Suggest root causes for unexpected results
- Recommend corrective actions

Always provide quantitative analysis when possible and explain your reasoning clearly."""

    def _get_review_system_prompt(self) -> str:
        """Get system prompt for report review tasks"""
        return """You are a quality assurance specialist for solar PV test reports.

Your role is to:
- Check completeness of test reports
- Verify compliance with standards
- Identify errors or inconsistencies
- Suggest improvements
- Ensure data quality and accuracy

Be thorough and meticulous. Flag any issues that could affect certification or compliance."""

    def _get_troubleshooting_system_prompt(self) -> str:
        """Get system prompt for troubleshooting tasks"""
        return """You are a troubleshooting expert for solar PV laboratory equipment and testing.

Your role is to:
- Diagnose test equipment problems
- Identify root causes of test failures
- Provide step-by-step solutions
- Suggest preventive measures
- Recommend best practices

Always prioritize safety and provide practical, actionable guidance."""

    def _get_decision_system_prompt(self) -> str:
        """Get system prompt for decision support tasks"""
        return """You are a decision support advisor for solar PV laboratory operations.

Your role is to:
- Evaluate options objectively
- Consider multiple criteria
- Assess risks and benefits
- Provide evidence-based recommendations
- Explain your reasoning clearly

Be balanced and comprehensive in your analysis."""

    def _build_analysis_prompt(
        self,
        data: Dict[str, Any],
        analysis_type: str,
        context: Optional[str] = None
    ) -> str:
        """Build prompt for data analysis"""
        prompt = f"Analysis Type: {analysis_type}\n\n"

        if context:
            prompt += f"Context: {context}\n\n"

        prompt += f"Data to Analyze:\n{json.dumps(data, indent=2)}\n\n"
        prompt += "Please provide a detailed analysis including:\n"
        prompt += "1. Key findings\n"
        prompt += "2. Anomalies or concerns\n"
        prompt += "3. Trends or patterns\n"
        prompt += "4. Recommendations\n"

        return prompt

    def _build_review_prompt(
        self,
        report_data: Dict[str, Any],
        standards: Optional[List[str]] = None
    ) -> str:
        """Build prompt for report review"""
        prompt = "Please review the following test report:\n\n"
        prompt += f"{json.dumps(report_data, indent=2)}\n\n"

        if standards:
            prompt += f"Applicable Standards: {', '.join(standards)}\n\n"

        prompt += "Please check for:\n"
        prompt += "1. Completeness of required data\n"
        prompt += "2. Compliance with standards\n"
        prompt += "3. Data consistency and accuracy\n"
        prompt += "4. Any errors or missing information\n"
        prompt += "5. Suggestions for improvement\n"

        return prompt

    def _build_troubleshooting_prompt(
        self,
        issue_description: str,
        equipment: Optional[str] = None,
        test_type: Optional[str] = None,
        error_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build prompt for troubleshooting"""
        prompt = f"Issue Description: {issue_description}\n\n"

        if equipment:
            prompt += f"Equipment: {equipment}\n"
        if test_type:
            prompt += f"Test Type: {test_type}\n"
        if error_data:
            prompt += f"\nError Data:\n{json.dumps(error_data, indent=2)}\n"

        prompt += "\nPlease provide:\n"
        prompt += "1. Possible root causes\n"
        prompt += "2. Step-by-step troubleshooting procedure\n"
        prompt += "3. Solutions or workarounds\n"
        prompt += "4. Preventive measures\n"

        return prompt

    def _build_decision_prompt(
        self,
        decision_context: str,
        options: List[Dict[str, Any]],
        criteria: Optional[List[str]] = None
    ) -> str:
        """Build prompt for decision support"""
        prompt = f"Decision Context: {decision_context}\n\n"

        prompt += "Options:\n"
        for i, option in enumerate(options, 1):
            prompt += f"\nOption {i}:\n{json.dumps(option, indent=2)}\n"

        if criteria:
            prompt += f"\nDecision Criteria: {', '.join(criteria)}\n"

        prompt += "\nPlease provide:\n"
        prompt += "1. Evaluation of each option\n"
        prompt += "2. Recommended choice with reasoning\n"
        prompt += "3. Potential risks and mitigation strategies\n"
        prompt += "4. Implementation considerations\n"

        return prompt


# Singleton instance
_claude_service_instance = None


def get_claude_service() -> ClaudeService:
    """Get singleton instance of Claude service"""
    global _claude_service_instance
    if _claude_service_instance is None:
        _claude_service_instance = ClaudeService()
    return _claude_service_instance
