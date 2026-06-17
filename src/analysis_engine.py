import ast
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from models_types import CodeIssue, Severity, AnalysisResult
from analyzers.python_analyzer import PythonAnalyzer
from analyzers.javascript_analyzer import JavaScriptAnalyzer
from analyzers.java_analyzer import JavaAnalyzer
from models.ml_models import MLModelManager
from utils.code_parser import CodeParser
from utils.metrics import CodeMetrics

logger = logging.getLogger(__name__)

class AnalysisEngine:
    
    def __init__(self, ml_manager: MLModelManager, settings):
        self.ml_manager = ml_manager
        self.settings = settings
        self.code_parser = CodeParser()
        self.metrics_calculator = CodeMetrics()
        
        self.analyzers = {
            'python': PythonAnalyzer(),
            'javascript': JavaScriptAnalyzer(),
            'java': JavaAnalyzer(),
        }
        
        logger.info("Analysis engine initialized")
    
    async def analyze_code(
        self, 
        code: str, 
        language: str, 
        file_path: str = "unknown"
    ) -> AnalysisResult:
        start_time = asyncio.get_event_loop().time()
        
        try:
            parsed_code = self.code_parser.parse(code, language)
            metrics = self.metrics_calculator.calculate(parsed_code, language)
            
            static_results = await self._run_static_analysis(
                code, language, file_path
            )
            
            ml_results = await self._run_ml_analysis(
                code, language, parsed_code, metrics
            )
            
            combined_results = self._combine_results(static_results, ml_results)
            
            analysis_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                file_path=file_path,
                language=language,
                errors=combined_results['errors'],
                warnings=combined_results['warnings'],
                suggestions=combined_results['suggestions'],
                metrics=metrics,
                ml_predictions=ml_results,
                analysis_time=analysis_time
            )
            
        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {e}")
            raise
    
    async def _run_static_analysis(
        self, 
        code: str, 
        language: str, 
        file_path: str
    ) -> Dict[str, List[CodeIssue]]:
        
        if language not in self.analyzers:
            logger.warning(f"No analyzer available for language: {language}")
            return {'errors': [], 'warnings': [], 'suggestions': []}
        
        analyzer = self.analyzers[language]
        return await analyzer.analyze(code, file_path)
    
    async def _run_ml_analysis(
        self, 
        code: str, 
        language: str, 
        parsed_code: Any, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        try:
            features = self._extract_ml_features(code, parsed_code, metrics)
            
            bug_prediction = await self.ml_manager.predict_bugs(
                features, language
            )
            
            security_analysis = await self.ml_manager.analyze_security(
                features, language
            )
            
            quality_assessment = await self.ml_manager.assess_quality(
                features, language
            )
            
            return {
                'bug_prediction': bug_prediction,
                'security_analysis': security_analysis,
                'quality_assessment': quality_assessment
            }
            
        except Exception as e:
            logger.error(f"ML analysis failed: {e}")
            return {}
    
    def _extract_ml_features(
        self, 
        code: str, 
        parsed_code: Any, 
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        features = {
            'code_length': len(code),
            'line_count': len(code.split('\n')),
            'complexity': metrics.get('cyclomatic_complexity', 0),
            'maintainability_index': metrics.get('maintainability_index', 0),
            'function_count': metrics.get('function_count', 0),
            'class_count': metrics.get('class_count', 0),
            'comment_ratio': metrics.get('comment_ratio', 0),
        }
        
        if parsed_code:
            features.update(self._extract_ast_features(parsed_code))
        
        return features
    
    def _extract_ast_features(self, parsed_code: Any) -> Dict[str, Any]:
        
        features = {}
        
        if isinstance(parsed_code, ast.AST):
            features.update({
                'ast_node_count': len(list(ast.walk(parsed_code))),
                'max_nesting_depth': self._calculate_nesting_depth(parsed_code),
                'has_try_except': any(isinstance(node, ast.Try) 
                                    for node in ast.walk(parsed_code)),
                'has_async': any(isinstance(node, (ast.AsyncFunctionDef, ast.Await)) 
                               for node in ast.walk(parsed_code)),
            })
        
        return features
    
    def _calculate_nesting_depth(self, node: ast.AST, depth: int = 0) -> int:
        
        max_depth = depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                child_depth = self._calculate_nesting_depth(child, depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _combine_results(
        self, 
        static_results: Dict[str, List[CodeIssue]], 
        ml_results: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        
        combined = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        for category, issues in static_results.items():
            if category in combined:
                combined[category].extend([
                    self._issue_to_dict(issue) for issue in issues
                ])
        
        if ml_results.get('bug_prediction', {}).get('high_risk_areas'):
            for area in ml_results['bug_prediction']['high_risk_areas']:
                combined['warnings'].append({
                    'type': 'ml_bug_prediction',
                    'severity': 'medium',
                    'message': f"High bug probability detected: {area['reason']}",
                    'line': area.get('line', 0),
                    'column': area.get('column', 0),
                    'confidence': area.get('confidence', 0.0),
                    'rule': 'ml_bug_predictor'
                })
        
        if ml_results.get('security_analysis', {}).get('vulnerabilities'):
            for vuln in ml_results['security_analysis']['vulnerabilities']:
                combined['errors'].append({
                    'type': 'security_vulnerability',
                    'severity': vuln.get('severity', 'medium'),
                    'message': vuln['description'],
                    'line': vuln.get('line', 0),
                    'column': vuln.get('column', 0),
                    'confidence': vuln.get('confidence', 0.0),
                    'rule': f"security_{vuln['type']}"
                })
        
        return combined
    
    def _issue_to_dict(self, issue: CodeIssue) -> Dict[str, Any]:
        
        return {
            'type': issue.type,
            'severity': issue.severity.value,
            'message': issue.message,
            'line': issue.line,
            'column': issue.column,
            'rule': issue.rule,
            'confidence': issue.confidence,
            'suggestion': issue.suggestion
        }