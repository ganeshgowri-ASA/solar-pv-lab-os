"""
Template service for managing report templates
"""
from jinja2 import Environment, FileSystemLoader, Template
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from backend.config import get_settings
from backend.models.report_models import ReportTemplate, ReportType


class TemplateService:
    """
    Service for managing and rendering report templates
    """

    def __init__(self):
        self.settings = get_settings()
        self.templates_dir = Path(self.settings.templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True,
        )

        # Built-in templates
        self.builtin_templates = self._initialize_builtin_templates()

    def _initialize_builtin_templates(self) -> Dict[str, ReportTemplate]:
        """Initialize built-in report templates"""

        templates = {
            "test_result_iec61215": ReportTemplate(
                template_id="test_result_iec61215",
                name="Test Result Report - IEC 61215",
                report_type=ReportType.TEST_RESULT,
                description="Standard test result report following IEC 61215 format",
                sections=[
                    "cover_page",
                    "executive_summary",
                    "test_information",
                    "sample_information",
                    "test_results",
                    "analysis",
                    "conclusions",
                    "appendix",
                ],
                required_fields=[
                    "test_id",
                    "sample_id",
                    "test_date",
                    "test_method",
                    "results",
                ],
                include_toc=True,
                include_page_numbers=True,
                template_content=self._get_iec61215_template(),
            ),
            "performance_report": ReportTemplate(
                template_id="performance_report",
                name="Performance Report",
                report_type=ReportType.PERFORMANCE,
                description="Module performance evaluation report",
                sections=[
                    "cover_page",
                    "summary",
                    "iv_characteristics",
                    "power_output",
                    "efficiency",
                    "temperature_coefficients",
                    "recommendations",
                ],
                required_fields=["sample_id", "test_date", "iv_data", "power_data"],
                template_content=self._get_performance_template(),
            ),
            "compliance_report": ReportTemplate(
                template_id="compliance_report",
                name="Compliance Report - NABL/ISO",
                report_type=ReportType.COMPLIANCE,
                description="Compliance report for NABL/ISO requirements",
                sections=[
                    "cover_page",
                    "scope",
                    "standards",
                    "test_methods",
                    "results",
                    "compliance_status",
                    "signatures",
                ],
                required_fields=["test_id", "standards", "compliance_criteria"],
                template_content=self._get_compliance_template(),
            ),
        }

        return templates

    def get_template(self, template_id: str) -> Optional[ReportTemplate]:
        """
        Get template by ID

        Args:
            template_id: Template identifier

        Returns:
            ReportTemplate object or None
        """
        return self.builtin_templates.get(template_id)

    def list_templates(self) -> List[ReportTemplate]:
        """
        List all available templates

        Returns:
            List of ReportTemplate objects
        """
        return list(self.builtin_templates.values())

    def render_template(
        self, template_id: str, context: Dict[str, Any]
    ) -> str:
        """
        Render template with given context

        Args:
            template_id: Template identifier
            context: Context data for rendering

        Returns:
            Rendered template string
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")

        # Create Jinja2 template from content
        jinja_template = Template(template.template_content)

        # Add default context
        full_context = {
            **self._get_default_context(),
            **context,
        }

        return jinja_template.render(full_context)

    def _get_default_context(self) -> Dict[str, Any]:
        """Get default context for all templates"""
        from datetime import datetime

        return {
            "lab_name": self.settings.lab_name,
            "lab_nabl_cert": self.settings.lab_nabl_cert,
            "lab_address": self.settings.lab_address,
            "lab_phone": self.settings.lab_phone,
            "lab_email": self.settings.lab_email,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "current_year": datetime.now().year,
        }

    def _get_iec61215_template(self) -> str:
        """Get IEC 61215 test result template"""
        return """
# TEST RESULT REPORT

## Laboratory Information
**Laboratory Name:** {{ lab_name }}
**NABL Certificate No:** {{ lab_nabl_cert }}
**Address:** {{ lab_address }}
**Phone:** {{ lab_phone }}
**Email:** {{ lab_email }}

---

## Report Information
**Report ID:** {{ report_id }}
**Report Date:** {{ report_date }}
**Report Version:** {{ report_version }}

---

## Client Information
**Client Name:** {{ client_name }}
{% if client_address %}
**Client Address:** {{ client_address }}
{% endif %}
{% if project_name %}
**Project Name:** {{ project_name }}
{% endif %}

---

## Executive Summary
{{ executive_summary }}

---

## Test Information

{% for test in test_results %}
### {{ test.test_name }}

**Test ID:** {{ test.test_id }}
**Test Method:** {{ test.test_method }}
**Standard:** {{ test.standard }}
**Test Date:** {{ test.test_date }}
**Operator:** {{ test.operator }}

#### Sample Information
- **Sample ID:** {{ test.sample_id }}
- **Manufacturer:** {{ test.manufacturer }}
- **Model:** {{ test.model }}
- **Serial Number:** {{ test.serial_number }}

#### Test Parameters
{% for key, value in test.parameters.items() %}
- **{{ key }}:** {{ value }}
{% endfor %}

#### Measurements
{% for key, value in test.measurements.items() %}
- **{{ key }}:** {{ value }}
{% endfor %}

#### Results
{% for key, value in test.calculated_values.items() %}
- **{{ key }}:** {{ value }}
{% endfor %}

#### Pass/Fail Criteria
{% for key, value in test.pass_fail_criteria.items() %}
- **{{ key }}:** {{ value }}
{% endfor %}

**Overall Result:** **{{ test.overall_result }}**

{% if test.interpretation %}
#### Interpretation
{{ test.interpretation }}
{% endif %}

{% if test.notes %}
#### Notes
{{ test.notes }}
{% endif %}

---

{% endfor %}

## Conclusions
{{ conclusions }}

---

## Approvals

**Tested by:** _________________ Date: _____________

**Reviewed by:** _________________ Date: _____________

**Approved by:** _________________ Date: _____________

---

*This report shall not be reproduced except in full without written approval of the laboratory.*
*End of Report*
"""

    def _get_performance_template(self) -> str:
        """Get performance report template"""
        return """
# SOLAR PV MODULE PERFORMANCE REPORT

## Laboratory Information
{{ lab_name }} | {{ lab_nabl_cert }}

---

## Module Information
**Sample ID:** {{ sample_id }}
**Manufacturer:** {{ manufacturer }}
**Model:** {{ model }}
**Test Date:** {{ test_date }}

---

## Executive Summary
{{ executive_summary }}

---

## I-V Characteristics

### Key Parameters
- **Open Circuit Voltage (Voc):** {{ voc }} V
- **Short Circuit Current (Isc):** {{ isc }} A
- **Maximum Power (Pmax):** {{ pmax }} W
- **Voltage at Pmax (Vmp):** {{ vmp }} V
- **Current at Pmax (Imp):** {{ imp }} A
- **Fill Factor (FF):** {{ fill_factor }}

### I-V Curve Analysis
{{ iv_analysis }}

---

## Power Output Analysis
{{ power_analysis }}

---

## Efficiency
**Module Efficiency:** {{ efficiency }}%

{{ efficiency_analysis }}

---

## Temperature Coefficients
{% if temp_coefficients %}
- **α (Isc):** {{ temp_coefficients.alpha }} %/°C
- **β (Voc):** {{ temp_coefficients.beta }} %/°C
- **γ (Pmax):** {{ temp_coefficients.gamma }} %/°C
{% endif %}

---

## Recommendations
{{ recommendations }}

---

*End of Performance Report*
"""

    def _get_compliance_template(self) -> str:
        """Get compliance report template"""
        return """
# COMPLIANCE REPORT

## Laboratory Information
{{ lab_name }}
NABL Accredited - {{ lab_nabl_cert }}

---

## Report Details
**Report ID:** {{ report_id }}
**Date:** {{ report_date }}

---

## Client Information
**Client:** {{ client_name }}

---

## Scope of Testing
{{ scope }}

---

## Standards and Test Methods
{% for standard in standards %}
- {{ standard }}
{% endfor %}

---

## Test Results Summary

{% for test in test_results %}
### {{ test.test_name }}
- **Standard:** {{ test.standard }}
- **Result:** {{ test.overall_result }}
- **Status:** {% if test.overall_result == "PASS" %}✓ COMPLIANT{% else %}✗ NON-COMPLIANT{% endif %}
{% endfor %}

---

## Overall Compliance Status
{{ compliance_status }}

---

## Signatures

**Lab Manager:** _________________

**Technical Manager:** _________________

**Date:** {{ current_date }}

---

*This compliance report is issued in accordance with NABL requirements.*
"""

    def create_custom_template(
        self,
        template_id: str,
        name: str,
        report_type: ReportType,
        template_content: str,
        **kwargs,
    ) -> ReportTemplate:
        """
        Create a custom template

        Args:
            template_id: Unique template identifier
            name: Template name
            report_type: Type of report
            template_content: Jinja2 template content
            **kwargs: Additional template parameters

        Returns:
            Created ReportTemplate
        """
        template = ReportTemplate(
            template_id=template_id,
            name=name,
            report_type=report_type,
            description=kwargs.get("description", "Custom template"),
            template_content=template_content,
            **{k: v for k, v in kwargs.items() if k != "description"},
        )

        self.builtin_templates[template_id] = template
        return template

    def validate_template(self, template_content: str) -> Dict[str, Any]:
        """
        Validate template syntax

        Args:
            template_content: Template content to validate

        Returns:
            Validation results
        """
        try:
            # Try to parse template
            Template(template_content)
            return {"valid": True, "errors": []}

        except Exception as e:
            return {"valid": False, "errors": [str(e)]}
