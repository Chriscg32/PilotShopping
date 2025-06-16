from typing import Dict, Any, List
import ast
import inspect
from app.core.base_agent import BaseAgent

class CodeImprovementAgent(BaseAgent):
    """Agent that analyzes and improves code quality automatically."""
    
    def __init__(self):
        super().__init__("code_improvement")
        self.improvement_patterns = self._load_improvement_patterns()
    
    def _load_improvement_patterns(self) -> Dict[str, Any]:
        """Load code improvement patterns."""
        return {
            "performance": [
                {
                    "pattern": "nested_loops",
                    "description": "Nested loops with high complexity",
                    "suggestion": "Consider using list comprehensions or vectorized operations",
                    "priority": "medium"
                },
                {
                    "pattern": "repeated_database_calls",
                    "description": "Multiple database calls in loop",
                    "suggestion": "Batch database operations or use bulk queries",
                    "priority": "high"
                }
            ],
            "reliability": [
                {
                    "pattern": "missing_error_handling",
                    "description": "Functions without try-catch blocks",
                    "suggestion": "Add proper error handling and logging",
                    "priority": "high"
                },
                {
                    "pattern": "hardcoded_values",
                    "description": "Hardcoded configuration values",
                    "suggestion": "Move to configuration files or environment variables",
                    "priority": "medium"
                }
            ]
        }
    
    async def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze entire codebase for improvement opportunities."""
        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "issues_found": [],
            "suggestions": [],
            "auto_fixes_available": []
        }
        
        # Analyze Python files in the project
        import os
        for root, dirs, files in os.walk("app/"):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_analysis = await self._analyze_file(file_path)
                    analysis_results["files_analyzed"] += 1
                    analysis_results["issues_found"].extend(file_analysis["issues"])
                    analysis_results["suggestions"].extend(file_analysis["suggestions"])
        
        return analysis_results
    
    async def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze individual Python file."""
        issues = []
        suggestions = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                tree = ast.parse(content)
            
            # Check for common issues
            for node in ast.walk(tree):
                # Check for missing error handling
                if isinstance(node, ast.FunctionDef):
                    has_try_except = any(isinstance(child, ast.Try) for child in ast.walk(node))
                    if not has_try_except and len(node.body) > 5:  # Only for non-trivial functions
                        issues.append({
                            "type": "missing_error_handling",
                            "file": file_path,
                            "function": node.name,
                            "line": node.lineno,
                            "severity": "medium"
                        })
                
                # Check for nested loops
                if isinstance(node, ast.For):
                    nested_loops = [child for child in ast.walk(node) if isinstance(child, ast.For) and child != node]
                    if nested_loops:
                        issues.append({
                            "type": "nested_loops",
                            "file": file_path,
                            "line": node.lineno,
                            "severity": "low",
                            "suggestion": "Consider optimizing nested loop structure"
                        })
        
        except Exception as e:
            issues.append({
                "type": "analysis_error",
                "file": file_path,
                "error": str(e),
                "severity": "low"
            })
        
        return {"issues": issues, "suggestions": suggestions}
    
    async def generate_improved_code(self, file_path: str, issue: Dict[str, Any]) -> str:
        """Generate improved version of code."""
        if issue["type"] == "missing_error_handling":
            return await self._add_error_handling(file_path, issue)
        elif issue["type"] == "nested_loops":
            return await self._optimize_nested_loops(file_path, issue)
        elif issue["type"] == "hardcoded_values":
            return await self._extract_configuration(file_path, issue)
        else:
            return "# No automatic fix available for this issue"
    
    async def _add_error_handling(self, file_path: str, issue: Dict[str, Any]) -> str:
        """Add error handling to a function."""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        function_name = issue["function"]
        line_num = issue["line"] - 1  # Convert to 0-based index
        
        # Find function definition and add try-except
        improved_code = f"""
async def {function_name}_improved(self, *args, **kwargs):
    \"\"\"Improved version with error handling.\"\"\"
    try:
        # Original function logic here
        result = await self.{function_name}_original(*args, **kwargs)
        return result
    except Exception as e:
        self.logger.error(f"Error in {function_name}: {{str(e)}}")
        await self.handle_error(e, "{function_name}")
        raise
    finally:
        # Cleanup logic if needed
        pass
"""
        return improved_code
    
    async def _optimize_nested_loops(self, file_path: str, issue: Dict[str, Any]) -> str:
        """Optimize nested loops."""
        return """
# Optimized version using list comprehension or vectorized operations
# Example transformation:
# 
# Original nested loops:
# results = []
# for item in list1:
#     for subitem in list2:
#         if condition(item, subitem):
#             results.append(process(item, subitem))
#
# Optimized version:
# results = [
#     process(item, subitem) 
#     for item in list1 
#     for subitem in list2 
#     if condition(item, subitem)
# ]
"""
    
    async def auto_apply_improvements(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically apply safe code improvements."""
        applied_fixes = []
        
        for issue in analysis_results["issues_found"]:
            if issue["severity"] == "low" and issue["type"] in ["formatting", "unused_imports"]:
                # Apply safe, low-risk fixes automatically
                try:
                    fix_result = await self._apply_safe_fix(issue)
                    applied_fixes.append({
                        "issue": issue,
                        "fix_applied": fix_result,
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    applied_fixes.append({
                        "issue": issue,
                        "fix_failed": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
        
        return {
            "fixes_applied": len(applied_fixes),
            "details": applied_fixes
        }

# Global code improvement agent
code_improvement_agent = CodeImprovementAgent()