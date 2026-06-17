import ast
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class CodeMetrics:
    
    def calculate(self, parsed_code: Optional[Any], language: str) -> Dict[str, Any]:
        metrics = {
            'cyclomatic_complexity': 0,
            'maintainability_index': 50,
            'function_count': 0,
            'class_count': 0,
            'comment_ratio': 0.0,
            'lines_of_code': 0
        }
        
        try:
            if language == 'python' and parsed_code:
                metrics.update(self._calculate_python_metrics(parsed_code))
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
        
        return metrics
    
    def _calculate_python_metrics(self, tree: ast.AST) -> Dict[str, Any]:
        metrics = {}
        
        function_count = 0
        class_count = 0
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_count += 1
                complexity += self._calculate_function_complexity(node)
            elif isinstance(node, ast.ClassDef):
                class_count += 1
        
        metrics.update({
            'function_count': function_count,
            'class_count': class_count,
            'cyclomatic_complexity': complexity,
            'maintainability_index': max(0, 171 - 5.2 * complexity - 0.23 * function_count)
        })
        
        return metrics
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        complexity = 1
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity