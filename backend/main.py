"""
FastAPI application for Solar PV Lab OS - AI Report Generator
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.report_generator import router as report_router
from backend.config import setup_directories, get_settings

# Initialize settings and directories
setup_directories()
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Report Generation System for Solar PV Testing Lab",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(report_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "api": "/api/reports",
    }


@app.get("/info")
async def info():
    """Get application information"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "lab_name": settings.lab_name,
        "ai_model": settings.ai_model,
        "features": [
            "AI-powered report generation",
            "Multi-format export (PDF, Word, Excel)",
            "Quality checking and validation",
            "Template management",
            "Data extraction from various formats",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
