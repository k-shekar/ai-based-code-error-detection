import ast
import asyncio
import logging
from typing import Dict, List, Any
from models_types import CodeIssue, Severity

logger = logging.getLogger(__name__)

class PythonAnalyzer:
    
    def __init__(self):
        self.name = "python_analyzer"
    
    async def analyze(self, code: str, file_path: str) -> Dict[str, List[CodeIssue]]:
        issues = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        try:
            tree = ast.parse(code)
            
            issues['errors'].extend(await self._check_syntax_errors(code))
            issues['warnings'].extend(await self._check_code_smells(tree))
            issues['suggestions'].extend(await self._check_best_practices(tree))
            
        except SyntaxError as e:
            issues['errors'].append(CodeIssue(
                type='syntax_error',
                severity=Severity.CRITICAL,
                message=f"Syntax error: {e.msg}",
                line=e.lineno or 1,
                column=e.offset or 0,
                rule='python_syntax',
                confidence=1.0
            ))
        except Exception as e:
            logger.error(f"Python analysis failed: {e}")
        
        return issues
    
    async def _check_syntax_errors(self, code: str) -> List[CodeIssue]:
        errors = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(CodeIssue(
                type='syntax_error',
                severity=Severity.CRITICAL,
                message=f"Syntax error: {e.msg}",
                line=e.lineno or 1,
                column=e.offset or 0,
                rule='python_syntax',
                confidence=1.0
            ))
        
        return errors
    
    async def _check_code_smells(self, tree: ast.AST) -> List[CodeIssue]:
        warnings = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                warnings.append(CodeIssue(
                    type='bare_except',
                    severity=Severity.MEDIUM,
                    message="Bare except clause catches all exceptions",
                    line=node.lineno,
                    column=node.col_offset,
                    rule='bare_except',
                    confidence=0.9,
                    suggestion="Catch specific exception types instead"
                ))
            
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if node.id.startswith('_') and not node.id.startswith('__'):
                    warnings.append(CodeIssue(
                        type='unused_variable',
                        severity=Severity.LOW,
                        message=f"Variable '{node.id}' appears to be unused",
                        line=node.lineno,
                        column=node.col_offset,
                        rule='unused_variable',
                        confidence=0.6
                    ))
        
        return warnings
    
    async def _check_best_practices(self, tree: ast.AST) -> List[CodeIssue]:
        suggestions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    suggestions.append(CodeIssue(
                        type='long_function',
                        severity=Severity.LOW,
                        message=f"Function '{node.name}' is quite long ({len(node.body)} statements)",
                        line=node.lineno,
                        column=node.col_offset,
                        rule='function_length',
                        confidence=0.7,
                        suggestion="Consider breaking this function into smaller functions"
                    ))
            
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    suggestions.append(CodeIssue(
                        type='missing_docstring',
                        severity=Severity.LOW,
                        message=f"Function '{node.name}' is missing a docstring",
                        line=node.lineno,
                        column=node.col_offset,
                        rule='missing_docstring',
                        confidence=0.8,
                        suggestion="Add a docstring to document the function's purpose"
                    ))
        
        return suggestions