"""
Quality assurance service for report validation
"""
from typing import Dict, Any, List
from backend.models.report_models import QualityCheckResult, TestResult
from backend.services.ai_report_service import AIReportService


class QualityService:
    """
    Service for quality assurance and validation of reports
    """

    def __init__(self):
        self.ai_service = AIReportService()

    async def perform_quality_check(
        self, report_content: str, test_results: List[TestResult]
    ) -> QualityCheckResult:
        """
        Perform comprehensive quality check on report

        Args:
            report_content: Full report content
            test_results: List of test results

        Returns:
            QualityCheckResult with all findings
        """
        # Initialize result
        quality_result = QualityCheckResult()

        # 1. Spelling and grammar check
        grammar_check = await self.ai_service.check_spelling_and_grammar(
            report_content
        )

        if grammar_check.get("has_errors"):
            quality_result.has_errors = True
            quality_result.typos_found = [
                {
                    "original": typo.get("original", ""),
                    "correction": typo.get("correction", ""),
                    "reason": typo.get("reason", ""),
                }
                for typo in grammar_check.get("typos", [])
            ]

            quality_result.grammar_issues = [
                {
                    "issue": issue.get("issue", ""),
                    "suggestion": issue.get("suggestion", ""),
                    "severity": issue.get("severity", "low"),
                }
                for issue in grammar_check.get("grammar_issues", [])
            ]

        # 2. Data completeness check
        missing_data = self._check_data_completeness(test_results)
        if missing_data:
            quality_result.has_errors = True
            quality_result.missing_data = missing_data

        # 3. Compliance check (for first test standard)
        if test_results:
            standard = test_results[0].standard.value
            compliance_check = await self.ai_service.validate_compliance(
                report_content, standard
            )

            if not compliance_check.get("compliant"):
                quality_result.compliance_issues = [
                    {
                        "section": "missing",
                        "issue": section,
                    }
                    for section in compliance_check.get("missing_sections", [])
                ]

                if compliance_check.get("recommendations"):
                    quality_result.suggestions.extend(
                        compliance_check.get("recommendations", [])
                    )

        # 4. Calculate overall quality score
        quality_result.overall_quality_score = self._calculate_quality_score(
            quality_result
        )

        return quality_result

    def _check_data_completeness(self, test_results: List[TestResult]) -> List[str]:
        """
        Check if all required data is present

        Args:
            test_results: List of test results

        Returns:
            List of missing data fields
        """
        missing_fields = []

        for test in test_results:
            # Check required fields
            if not test.test_name:
                missing_fields.append(f"Test {test.test_id}: Missing test name")

            if not test.test_method:
                missing_fields.append(f"Test {test.test_id}: Missing test method")

            if not test.sample_id:
                missing_fields.append(f"Test {test.test_id}: Missing sample ID")

            if not test.measurements:
                missing_fields.append(f"Test {test.test_id}: No measurements recorded")

            if not test.overall_result:
                missing_fields.append(f"Test {test.test_id}: No overall result")

        return missing_fields

    def _calculate_quality_score(self, quality_result: QualityCheckResult) -> float:
        """
        Calculate overall quality score (0-100)

        Args:
            quality_result: Quality check result

        Returns:
            Quality score
        """
        score = 100.0

        # Deduct points for issues
        score -= len(quality_result.typos_found) * 2
        score -= len(quality_result.grammar_issues) * 1.5
        score -= len(quality_result.missing_data) * 5
        score -= len(quality_result.compliance_issues) * 3

        # Ensure score doesn't go below 0
        return max(0.0, score)

    async def validate_test_data(
        self, test_result: TestResult
    ) -> Dict[str, Any]:
        """
        Validate individual test result data

        Args:
            test_result: Test result to validate

        Returns:
            Validation results
        """
        issues = []

        # Check for negative values where they shouldn't be
        for key, value in test_result.measurements.items():
            if isinstance(value, (int, float)) and value < 0:
                if key.lower() in ["power", "efficiency", "voltage", "current"]:
                    issues.append(f"Negative value for {key}: {value}")

        # Check for missing critical data
        critical_fields = ["test_name", "test_method", "sample_id", "overall_result"]
        for field in critical_fields:
            if not getattr(test_result, field, None):
                issues.append(f"Missing critical field: {field}")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
        }

    def check_units_consistency(
        self, measurements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if units are used consistently

        Args:
            measurements: Dictionary of measurements

        Returns:
            Consistency check results
        """
        issues = []

        # Common unit patterns
        voltage_pattern = ["V", "v", "volt", "volts"]
        current_pattern = ["A", "a", "amp", "amps", "ampere"]
        power_pattern = ["W", "w", "watt", "watts"]

        # Check for unit consistency
        for key, value in measurements.items():
            key_lower = key.lower()

            # Check voltage units
            if "voltage" in key_lower or "voc" in key_lower or "vmp" in key_lower:
                if not any(unit in str(value) for unit in voltage_pattern):
                    issues.append(f"Voltage measurement may be missing units: {key}")

            # Check current units
            if "current" in key_lower or "isc" in key_lower or "imp" in key_lower:
                if not any(unit in str(value) for unit in current_pattern):
                    issues.append(f"Current measurement may be missing units: {key}")

            # Check power units
            if "power" in key_lower or "pmax" in key_lower:
                if not any(unit in str(value) for unit in power_pattern):
                    issues.append(f"Power measurement may be missing units: {key}")

        return {
            "consistent": len(issues) == 0,
            "issues": issues,
        }

    async def suggest_improvements(self, report_content: str) -> List[str]:
        """
        Get AI suggestions for report improvement

        Args:
            report_content: Report content

        Returns:
            List of improvement suggestions
        """
        # This would use the AI service to analyze and suggest improvements
        # For now, return basic suggestions
        suggestions = []

        # Check length
        if len(report_content) < 500:
            suggestions.append("Report seems too brief. Consider adding more details.")

        # Check for common issues
        if "TBD" in report_content or "TODO" in report_content:
            suggestions.append("Report contains placeholder text (TBD/TODO).")

        if report_content.count("\n\n") < 5:
            suggestions.append("Consider adding more section breaks for readability.")

        return suggestions
