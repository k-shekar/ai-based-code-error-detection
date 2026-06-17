import os
from pathlib import Path
from typing import List, Optional

class Settings:
    
    def __init__(self):
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8001"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        self.database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/codeanalysis")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        self.model_path = Path(os.getenv("MODEL_PATH", "models/"))
        self.model_cache_size = int(os.getenv("MODEL_CACHE_SIZE", "100"))
        
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", str(1024 * 1024)))
        self.analysis_timeout = int(os.getenv("ANALYSIS_TIMEOUT", "30"))
        self.supported_languages = os.getenv("SUPPORTED_LANGUAGES", "python,javascript,java,cpp,go").split(",")
        
        self.api_key = os.getenv("API_KEY")
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
        
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE")
        
        self.enable_ml_analysis = os.getenv("ENABLE_ML_ANALYSIS", "true").lower() == "true"
        self.enable_security_scan = os.getenv("ENABLE_SECURITY_SCAN", "true").lower() == "true"
        self.enable_quality_metrics = os.getenv("ENABLE_QUALITY_METRICS", "true").lower() == "true"
        
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.sonarqube_url = os.getenv("SONARQUBE_URL")
        self.sonarqube_token = os.getenv("SONARQUBE_TOKEN")