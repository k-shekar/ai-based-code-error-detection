from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CodeIssue:
    type: str
    severity: Severity
    message: str
    line: int
    column: int
    rule: str
    confidence: float
    suggestion: Optional[str] = None

@dataclass
class AnalysisResult:
    file_path: str
    language: str
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    ml_predictions: Dict[str, Any]
    analysis_time: float