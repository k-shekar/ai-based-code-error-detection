from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

health_router = APIRouter()

@health_router.get("/")
async def health_check():
    return {"status": "healthy", "service": "ai-code-error-detection"}

analysis_router = APIRouter()

class AnalysisRequest(BaseModel):
    code: str
    language: str
    file_path: Optional[str] = "unknown"

class AnalysisResponse(BaseModel):
    file_path: str
    language: str
    errors: list
    warnings: list
    suggestions: list
    metrics: Dict[str, Any]
    analysis_time: float

@analysis_router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    try:
        from models.ml_models import MLModelManager
        from analysis_engine import AnalysisEngine
        from config import Settings
        
        settings = Settings()
        ml_manager = MLModelManager(settings.model_path)
        await ml_manager.load_models()
        
        analysis_engine = AnalysisEngine(ml_manager, settings)
        
        result = await analysis_engine.analyze_code(
            code=request.code,
            language=request.language,
            file_path=request.file_path
        )
        
        return AnalysisResponse(
            file_path=result.file_path,
            language=result.language,
            errors=result.errors,
            warnings=result.warnings,
            suggestions=result.suggestions,
            metrics=result.metrics,
            analysis_time=result.analysis_time
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@analysis_router.get("/languages")
async def get_supported_languages():
    return {
        "languages": ["python", "javascript", "java", "cpp", "go"],
        "status": "active"
    }