import asyncio
import logging
from typing import Dict, List, Any
from models_types import CodeIssue, Severity

logger = logging.getLogger(__name__)

class JavaAnalyzer:
    
    def __init__(self):
        self.name = "java_analyzer"
    
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
            logger.error(f"Java analysis failed: {e}")
        
        return issues
    
    async def _check_common_issues(self, code: str) -> List[CodeIssue]:
        warnings = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'catch' in line and '{' in line:
                if '}' in lines[i] if i < len(lines) else False:
                    warnings.append(CodeIssue(
                        type='empty_catch',
                        severity=Severity.HIGH,
                        message="Empty catch block suppresses exceptions",
                        line=i,
                        column=line.find('catch'),
                        rule='empty_catch_block',
                        confidence=0.8,
                        suggestion="Handle the exception or at least log it"
                    ))
        
        return warnings
    
    async def _check_best_practices(self, code: str) -> List[CodeIssue]:
        suggestions = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if 'System.out.println' in line:
                suggestions.append(CodeIssue(
                    type='system_out',
                    severity=Severity.LOW,
                    message="Use a logging framework instead of System.out.println",
                    line=i,
                    column=line.find('System.out.println'),
                    rule='no_system_out',
                    confidence=0.7,
                    suggestion="Use a logging framework like SLF4J or Log4j"
                ))
        
        return suggestions