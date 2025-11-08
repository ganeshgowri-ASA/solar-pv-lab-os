"""
AI Assistant API - FastAPI endpoints for AI-powered assistance
Provides REST API for chat, analysis, review, troubleshooting, and decision support
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_engine import get_ai_engine, AIEngine


# Pydantic models for request/response

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message")
    session_id: str = Field(..., description="Session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    include_context: bool = Field(True, description="Include knowledge base context")


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    message: Optional[str] = None
    session_id: Optional[str] = None
    context_used: Optional[bool] = None
    usage: Optional[Dict[str, int]] = None
    timestamp: str
    error: Optional[str] = None


class AnalyzeRequest(BaseModel):
    """Data analysis request model"""
    data: Dict[str, Any] = Field(..., description="Data to analyze")
    test_type: str = Field(..., description="Type of test")
    analysis_type: str = Field("comprehensive", description="Type of analysis")
    session_id: Optional[str] = Field(None, description="Session ID for context")


class AnalyzeResponse(BaseModel):
    """Data analysis response model"""
    success: bool
    analysis: Optional[str] = None
    analysis_type: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    timestamp: str
    error: Optional[str] = None


class ReviewRequest(BaseModel):
    """Report review request model"""
    report_data: Dict[str, Any] = Field(..., description="Report to review")
    standards: Optional[List[str]] = Field(None, description="Applicable standards")
    check_types: Optional[List[str]] = Field(None, description="Specific checks")


class ReviewResponse(BaseModel):
    """Report review response model"""
    success: bool
    review: Optional[str] = None
    structured_review: Optional[Dict[str, Any]] = None
    standards_checked: Optional[List[str]] = None
    usage: Optional[Dict[str, int]] = None
    timestamp: str
    error: Optional[str] = None


class TroubleshootRequest(BaseModel):
    """Troubleshooting request model"""
    issue_description: str = Field(..., description="Problem description")
    equipment: Optional[str] = Field(None, description="Equipment involved")
    test_type: Optional[str] = Field(None, description="Type of test")
    error_data: Optional[Dict[str, Any]] = Field(None, description="Error data")
    session_id: Optional[str] = Field(None, description="Session ID")


class TroubleshootResponse(BaseModel):
    """Troubleshooting response model"""
    success: bool
    guidance: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    timestamp: str
    error: Optional[str] = None


class DecisionRequest(BaseModel):
    """Decision support request model"""
    decision_context: str = Field(..., description="Decision context")
    options: List[Dict[str, Any]] = Field(..., description="Available options")
    criteria: Optional[List[str]] = Field(None, description="Decision criteria")
    session_id: Optional[str] = Field(None, description="Session ID")


class DecisionResponse(BaseModel):
    """Decision support response model"""
    success: bool
    recommendation: Optional[str] = None
    usage: Optional[Dict[str, int]] = None
    timestamp: str
    error: Optional[str] = None


class InsightsRequest(BaseModel):
    """Insights request model"""
    data_scope: str = Field("recent", description="Scope of data")
    insight_types: Optional[List[str]] = Field(None, description="Types of insights")


class InsightsResponse(BaseModel):
    """Insights response model"""
    success: bool
    scope: Optional[str] = None
    insights: Optional[List[Any]] = None
    timestamp: str
    error: Optional[str] = None


class IntentRequest(BaseModel):
    """Intent detection request model"""
    message: str = Field(..., description="User message")


class IntentResponse(BaseModel):
    """Intent detection response model"""
    intent: str
    confidence: float
    message: str


# Create FastAPI app
app = FastAPI(
    title="Solar PV Lab AI Assistant API",
    description="AI-powered assistant for solar PV laboratory operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get AI engine
def get_ai_engine_dependency() -> AIEngine:
    """Dependency for AI engine"""
    return get_ai_engine()


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Solar PV Lab AI Assistant API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/api/v1/ai/chat",
            "analyze": "/api/v1/ai/analyze",
            "review": "/api/v1/ai/review",
            "troubleshoot": "/api/v1/ai/troubleshoot",
            "decision": "/api/v1/ai/decision",
            "insights": "/api/v1/ai/insights",
            "intent": "/api/v1/ai/intent"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/ai/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Chat with AI assistant

    Provides conversational interface with context awareness and knowledge base integration.
    """
    try:
        response = ai_engine.chat(
            message=request.message,
            session_id=request.session_id,
            user_id=request.user_id,
            include_context=request.include_context
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/analyze", response_model=AnalyzeResponse)
async def analyze_data(
    request: AnalyzeRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Analyze test data with AI

    Provides automated insights, anomaly detection, trend identification, and predictions.
    """
    try:
        response = ai_engine.analyze_test_data(
            data=request.data,
            test_type=request.test_type,
            analysis_type=request.analysis_type,
            session_id=request.session_id
        )
        return AnalyzeResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/review", response_model=ReviewResponse)
async def review_report(
    request: ReviewRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Review test report for quality and compliance

    Checks completeness, accuracy, consistency, and compliance with standards.
    """
    try:
        response = ai_engine.review_test_report(
            report_data=request.report_data,
            standards=request.standards,
            check_types=request.check_types
        )
        return ReviewResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/troubleshoot", response_model=TroubleshootResponse)
async def troubleshoot(
    request: TroubleshootRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Get AI-powered troubleshooting guidance

    Provides step-by-step guidance for resolving equipment and test issues.
    """
    try:
        response = ai_engine.get_troubleshooting_help(
            issue_description=request.issue_description,
            equipment=request.equipment,
            test_type=request.test_type,
            error_data=request.error_data,
            session_id=request.session_id
        )
        return TroubleshootResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/decision", response_model=DecisionResponse)
async def decision_support(
    request: DecisionRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Get AI-powered decision support

    Provides recommendations for resource allocation, priority setting, and optimization.
    """
    try:
        response = ai_engine.get_decision_support(
            decision_context=request.decision_context,
            options=request.options,
            criteria=request.criteria,
            session_id=request.session_id
        )
        return DecisionResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/insights", response_model=InsightsResponse)
async def get_insights(
    request: InsightsRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Get automated insights from system data

    Provides trends, anomalies, predictions, and recommendations based on historical data.
    """
    try:
        response = ai_engine.get_insights(
            data_scope=request.data_scope,
            insight_types=request.insight_types
        )
        return InsightsResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ai/intent", response_model=IntentResponse)
async def detect_intent(
    request: IntentRequest,
    ai_engine: AIEngine = Depends(get_ai_engine_dependency)
):
    """
    Detect user intent from message

    Analyzes message to determine user's intention (analyze, troubleshoot, question, etc.).
    """
    try:
        response = ai_engine.detect_intent(message=request.message)
        return IntentResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
