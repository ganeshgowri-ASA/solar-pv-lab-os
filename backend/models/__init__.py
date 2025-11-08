"""
Data models for Solar PV Lab OS
"""
from .report_models import (
    ReportType,
    ReportTemplate,
    ReportRequest,
    ReportResponse,
    TestResult,
    QualityCheckResult,
    ReportMetadata,
)

__all__ = [
    "ReportType",
    "ReportTemplate",
    "ReportRequest",
    "ReportResponse",
    "TestResult",
    "QualityCheckResult",
    "ReportMetadata",
]
