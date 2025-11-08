"""
Data models for report generation
"""
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class ReportType(str, Enum):
    """Types of reports that can be generated"""
    TEST_RESULT = "test_result"
    TYPE_TEST = "type_test"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    EXECUTIVE_SUMMARY = "executive_summary"
    CUSTOM = "custom"


class ReportFormat(str, Enum):
    """Output formats for reports"""
    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"


class TestStandard(str, Enum):
    """Testing standards"""
    IEC_61215 = "IEC 61215"
    IEC_61730 = "IEC 61730"
    UL_1703 = "UL 1703"
    IEC_62804 = "IEC 62804"
    IEC_61853 = "IEC 61853"
    CUSTOM = "custom"


class TestResult(BaseModel):
    """Test result data structure"""
    test_id: str
    test_name: str
    test_method: str
    standard: TestStandard
    test_date: datetime
    operator: str
    equipment_used: List[str] = []

    # Sample information
    sample_id: str
    manufacturer: str
    model: str
    serial_number: str

    # Test parameters
    parameters: Dict[str, Any] = {}

    # Results
    measurements: Dict[str, Any] = {}
    calculated_values: Dict[str, Any] = {}
    pass_fail_criteria: Dict[str, str] = {}
    overall_result: str  # "PASS", "FAIL", "CONDITIONAL"

    # Additional data
    graphs: List[str] = []  # Paths to graph images
    images: List[str] = []  # Paths to test images
    notes: str = ""


class ReportTemplate(BaseModel):
    """Report template configuration"""
    template_id: str
    name: str
    report_type: ReportType
    description: str
    version: str = "1.0"

    # Template structure
    sections: List[str] = []
    required_fields: List[str] = []
    optional_fields: List[str] = []

    # Formatting
    header_text: str = ""
    footer_text: str = ""
    include_toc: bool = True
    include_page_numbers: bool = True

    # Branding
    logo_path: Optional[str] = None
    watermark: Optional[str] = None

    # Template content (Jinja2 template)
    template_content: str = ""


class ReportRequest(BaseModel):
    """Request to generate a report"""
    report_type: ReportType
    template_id: Optional[str] = None

    # Test data
    test_results: List[TestResult] = []

    # Additional data sources
    excel_file: Optional[str] = None
    equipment_files: List[str] = []

    # Report metadata
    report_title: str
    client_name: str
    client_address: Optional[str] = None
    project_name: Optional[str] = None
    report_date: datetime = Field(default_factory=datetime.now)

    # Output preferences
    output_formats: List[ReportFormat] = [ReportFormat.PDF]
    include_raw_data: bool = False
    include_graphs: bool = True

    # AI settings
    enable_ai_enhancement: bool = True
    enable_spell_check: bool = True
    enable_grammar_check: bool = True
    enable_compliance_check: bool = True

    # Additional options
    digital_signature: bool = False
    watermark: Optional[str] = None
    custom_fields: Dict[str, Any] = {}


class QualityCheckResult(BaseModel):
    """Results from AI quality checking"""
    has_errors: bool = False
    typos_found: List[Dict[str, str]] = []
    grammar_issues: List[Dict[str, str]] = []
    missing_data: List[str] = []
    compliance_issues: List[Dict[str, str]] = []
    suggestions: List[str] = []
    overall_quality_score: float = 0.0  # 0-100


class ReportMetadata(BaseModel):
    """Metadata for generated report"""
    report_id: str
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str = "AI Report Generator"

    # Generation info
    generation_time_seconds: float = 0.0
    ai_enhanced: bool = False
    quality_checked: bool = False

    # File info
    file_paths: Dict[str, str] = {}  # format -> path
    file_sizes: Dict[str, int] = {}  # format -> size in bytes

    # Quality info
    quality_check_results: Optional[QualityCheckResult] = None


class ReportResponse(BaseModel):
    """Response after report generation"""
    success: bool
    report_id: str
    message: str

    # Generated files
    files: Dict[str, str] = {}  # format -> file path

    # Metadata
    metadata: ReportMetadata

    # Quality check results
    quality_check: Optional[QualityCheckResult] = None

    # Errors/warnings
    errors: List[str] = []
    warnings: List[str] = []


class ReportVersion(BaseModel):
    """Report version tracking"""
    report_id: str
    version: str
    created_at: datetime
    changes: List[str] = []
    file_path: str
    created_by: str
