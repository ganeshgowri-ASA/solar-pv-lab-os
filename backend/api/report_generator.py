"""
FastAPI endpoints for report generation
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List, Optional
from pathlib import Path

from backend.models.report_models import (
    ReportRequest,
    ReportResponse,
    ReportTemplate,
    QualityCheckResult,
)
from backend.services.report_generation_service import ReportGenerationService
from backend.services.template_service import TemplateService
from backend.services.quality_service import QualityService
from backend.services.data_extraction_service import DataExtractionService

router = APIRouter(prefix="/api/reports", tags=["Reports"])

# Service instances
report_service = ReportGenerationService()
template_service = TemplateService()
quality_service = QualityService()
data_service = DataExtractionService()


@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a report based on the provided request

    Args:
        request: Report generation request

    Returns:
        ReportResponse with generated files and metadata
    """
    try:
        response = await report_service.generate_report(request)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.get("/templates", response_model=List[ReportTemplate])
async def list_templates():
    """
    List all available report templates

    Returns:
        List of ReportTemplate objects
    """
    try:
        templates = template_service.list_templates()
        return templates

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")


@router.get("/templates/{template_id}", response_model=ReportTemplate)
async def get_template(template_id: str):
    """
    Get a specific template by ID

    Args:
        template_id: Template identifier

    Returns:
        ReportTemplate object
    """
    template = template_service.get_template(template_id)

    if not template:
        raise HTTPException(status_code=404, detail=f"Template not found: {template_id}")

    return template


@router.post("/upload/excel")
async def upload_excel(file: UploadFile = File(...)):
    """
    Upload Excel file for data extraction

    Args:
        file: Excel file

    Returns:
        Extracted data
    """
    try:
        # Save uploaded file temporarily
        temp_path = Path(f"/tmp/{file.filename}")
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract data
        data = await data_service.extract_from_excel(str(temp_path))

        # Clean up
        temp_path.unlink()

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excel upload failed: {str(e)}")


@router.post("/quality-check")
async def check_quality(content: str):
    """
    Perform quality check on report content

    Args:
        content: Report content to check

    Returns:
        QualityCheckResult
    """
    try:
        # For quality check, we need minimal test results
        result = await quality_service.perform_quality_check(content, [])
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality check failed: {str(e)}")


@router.get("/download/{report_id}/{format}")
async def download_report(report_id: str, format: str):
    """
    Download generated report

    Args:
        report_id: Report ID
        format: File format (pdf, word, excel)

    Returns:
        File download
    """
    try:
        from backend.config import get_settings

        settings = get_settings()
        output_dir = Path(settings.reports_output_dir)

        # Find file
        files = list(output_dir.glob(f"{report_id}*.{format}*"))

        if not files:
            raise HTTPException(status_code=404, detail="Report file not found")

        file_path = files[0]

        return FileResponse(
            path=file_path,
            filename=file_path.name,
            media_type="application/octet-stream",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.post("/validate/data")
async def validate_test_data(test_data: dict):
    """
    Validate test result data

    Args:
        test_data: Test data to validate

    Returns:
        Validation results
    """
    try:
        from backend.models.report_models import TestResult, TestStandard

        # Convert dict to TestResult (basic validation)
        test_result = TestResult(**test_data)

        # Perform validation
        validation = await quality_service.validate_test_data(test_result)

        return validation

    except Exception as e:
        return {
            "is_valid": False,
            "issues": [str(e)],
        }


@router.get("/health")
async def health_check():
    """
    Health check endpoint

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "service": "AI Report Generator",
        "version": "1.0.0",
    }


@router.get("/stats")
async def get_stats():
    """
    Get statistics about generated reports

    Returns:
        Statistics dictionary
    """
    try:
        from backend.config import get_settings

        settings = get_settings()
        output_dir = Path(settings.reports_output_dir)

        if not output_dir.exists():
            return {
                "total_reports": 0,
                "total_size_mb": 0,
            }

        # Count files
        pdf_files = list(output_dir.glob("*.pdf"))
        word_files = list(output_dir.glob("*.docx"))
        excel_files = list(output_dir.glob("*.xlsx"))

        # Calculate total size
        total_size = sum(f.stat().st_size for f in output_dir.iterdir() if f.is_file())

        return {
            "total_reports": len(pdf_files) + len(word_files) + len(excel_files),
            "pdf_count": len(pdf_files),
            "word_count": len(word_files),
            "excel_count": len(excel_files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
