import asyncio
import logging
from typing import Dict, List, Any
from models_types import CodeIssue, Severity

logger = logging.getLogger(__name__)

class JavaScriptAnalyzer:
    
    def __init__(self):
        self.name = "javascript_analyzer"
    
    async def analyze(self, code: str, file_path: str) -> Dict[str, List[CodeIssue]]:
        issues = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        try:
            issues['warnings'].extend(await self._check_common_issues(code))
            issues['suggestions'].extend(await self._check_best_practices(code))
            
        except Exception as e:
            logger.error(f"JavaScript analysis failed: {e}")
        
        return issues
    
    async def _check_common_issues(self, code: str) -> List[CodeIssue]:
        warnings = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'var ' in line:
                warnings.append(CodeIssue(
                    type='var_usage',
                    severity=Severity.MEDIUM,
                    message="Use 'let' or 'const' instead of 'var'",
                    line=i,
                    column=line.find('var '),
                    rule='no_var',
                    confidence=0.9,
                    suggestion="Replace 'var' with 'let' or 'const'"
                ))
            
            if '==' in line and '===' not in line:
                warnings.append(CodeIssue(
                    type='loose_equality',
                    severity=Severity.MEDIUM,
                    message="Use strict equality (===) instead of loose equality (==)",
                    line=i,
                    column=line.find('=='),
                    rule='strict_equality',
                    confidence=0.8,
                    suggestion="Use '===' for strict equality comparison"
                ))
        
        return warnings
    
    async def _check_best_practices(self, code: str) -> List[CodeIssue]:
        suggestions = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'console.log' in line:
                suggestions.append(CodeIssue(
                    type='console_log',
                    severity=Severity.LOW,
                    message="Remove console.log statements before production",
                    line=i,
                    column=line.find('console.log'),
                    rule='no_console',
                    confidence=0.7,
                    suggestion="Use a proper logging library instead"
                ))
        
        return suggestions