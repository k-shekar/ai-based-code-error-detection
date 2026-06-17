import asyncio
import logging
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from analysis_engine import AnalysisEngine
from models.ml_models import MLModelManager
from api.routes import analysis_router, health_router
from config import Settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = Settings()
analysis_engine: Optional[AnalysisEngine] = None
ml_manager: Optional[MLModelManager] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global analysis_engine, ml_manager
    
    logger.info("Starting AI Code Error Detection System...")
    
    try:
        ml_manager = MLModelManager(settings.model_path)
        await ml_manager.load_models()
        
        analysis_engine = AnalysisEngine(ml_manager, settings)
        
        logger.info("System initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Code Error Detection System...")
    
    if ml_manager:
        await ml_manager.cleanup()
    
    logger.info("Shutdown complete")

app = FastAPI(
    title="AI Code Error Detection API",
    description="Intelligent code analysis with ML-powered error detection",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(analysis_router, prefix="/api/v1", tags=["analysis"])

# Mount static files - adjust path based on current working directory
import os
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
if os.path.exists(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")
    
    @app.get("/")
    async def root():
        return FileResponse(os.path.join(web_dir, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "AI Code Error Detection API", "status": "running", "docs": "/docs"}

def main():
    uvicorn.run(
        "main_simple:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()