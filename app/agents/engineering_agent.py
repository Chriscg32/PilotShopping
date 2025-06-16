from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.services.huggingface_service import get_huggingface_service

class EngineeringAgent(BaseAgent):
    """Engineering agent with Hugging Face integration."""
    
    def __init__(self):
        super().__init__(
            name="engineering",
            capabilities=[
                "code_generation",
                "api_development",
                "database_design",
                "testing_automation",
                "deployment_automation",
                "code_review",
                "documentation_generation",
                "performance_optimization"
            ]
        )
        self.hf_service = get_huggingface_service()
        self.code_templates = self._initialize_code_templates()
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process engineering tasks."""
        task_type = task.get("type")
        
        if task_type == "generate_code":
            return await self._generate_code(task)
        elif task_type == "create_api":
            return await self._create_api(task)
        elif task_type == "review_code":
            return await self._review_code(task)
        elif task_type == "generate_documentation":
            return await self._generate_documentation(task)
        elif task_type == "create_tests":
            return await self._create_tests(task)
        else:
            return {"error": f"Unknown engineering task: {task_type}"}
    
    async def _generate_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code using Hugging Face."""
        component_type = task.get("component_type", "function")
        framework = task.get("framework", "python")
        description = task.get("description", "")
        
        if not description:
            return {"error": "Code description is required"}
        
        prompt = f"""
        Generate a {framework} {component_type} that {description}:
        
        {framework}
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            model="microsoft/CodeBERT-base",
            max_length=200,
            temperature=0.3
        )
        
        if result["success"]:
            generated_code = result["text"]
            
            return {
                "result": {
                    "component_type": component_type,
                    "framework": framework,
                    "description": description,
                    "generated_code": generated_code,
                    "code_quality_score": self._assess_code_quality(generated_code),
                    "suggestions": self._get_code_suggestions(component_type, framework),
                    "generated_with": result["model"]
                }
            }
        else:
            return {"error": f"Failed to generate code: {result.get('error', 'Unknown error')}"}
    
    async def _create_api(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create API endpoints."""
        api_name = task.get("api_name", "api")
        endpoints = task.get("endpoints", [])
        framework = task.get("framework", "fastapi")
        
        if not endpoints:
            return {"error": "API endpoints are required"}
        
        api_structure = {
            "api_name": api_name,
            "framework": framework,
            "endpoints": [],
            "models": [],
            "middleware": [],
            "documentation": ""
        }
        
        # Generate endpoints
        for endpoint in endpoints:
            endpoint_code = await self._generate_endpoint_code(endpoint, framework)
            api_structure["endpoints"].append(endpoint_code)
        
        # Generate models
        models_code = await self._generate_models_code(endpoints, framework)
        api_structure["models"] = models_code
        
        # Generate documentation
        doc_result = await self._generate_api_documentation(api_name, endpoints)
        api_structure["documentation"] = doc_result.get("text", "")
        
        return {
            "result": {
                "api_structure": api_structure,
                "deployment_instructions": self._get_deployment_instructions(framework),
                "testing_suggestions": self._get_testing_suggestions(endpoints),
                "security_recommendations": self._get_security_recommendations()
            }
        }
    
    async def _generate_endpoint_code(self, endpoint: str, framework: str) -> Dict[str, Any]:
        """Generate code for a specific endpoint."""
        prompt = f"""
        Create a {framework} API endpoint for {endpoint} with CRUD operations:
        
        python
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            model="microsoft/CodeBERT-base",
            max_length=150,
            temperature=0.2
        )
        
        return {
            "endpoint": endpoint,
            "code": result.get("text", ""),
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "authentication_required": True
        }
    
    async def _generate_models_code(self, endpoints: List[str], framework: str) -> List[Dict[str, Any]]:
        """Generate data models for endpoints."""
        models = []
        
        for endpoint in endpoints:
            prompt = f"""
            Create a Pydantic model for {endpoint} endpoint:
            
            
            from pydantic import BaseModel
            
            class {endpoint.capitalize()}Model(BaseModel):
            """
            
            result = await self.hf_service.generate_text(
                prompt=prompt,
                model="microsoft/CodeBERT-base",
                max_length=100,
                temperature=0.2
            )
            
            models.append({
                "name": f"{endpoint.capitalize()}Model",
                "endpoint": endpoint,
                "code": result.get("text", "")
            })
        
        return models
    
    async def _generate_api_documentation(self, api_name: str, endpoints: List[str]) -> Dict[str, Any]:
        """Generate API documentation."""
        prompt = f"""
        Generate API documentation for {api_name} with endpoints: {', '.join(endpoints)}
        
        # {api_name.title()} API Documentation
        
        ## Overview
        """
        
        return await self.hf_service.generate_text(
            prompt=prompt,
            max_length=250,
            temperature=0.4
        )
    
    async def _review_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Review code and provide suggestions."""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        if not code:
            return {"error": "Code is required for review"}
        
        prompt = f"""
        Review this {language} code and provide suggestions for improvement:
        
        {language}
        {code}
        
        
        Code review:
        Issues found:
        Suggestions:
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            max_length=200,
            temperature=0.5
        )
        
        return {
            "result": {
                "original_code": code,
                "language": language,
                "review": result.get("text", ""),
                "quality_score": self._assess_code_quality(code),
                "security_issues": self._check_security_issues(code),
                "performance_suggestions": self._get_performance_suggestions(code),
                "best_practices": self._get_best_practices(language)
            }
        }
    
    async def _generate_documentation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code documentation."""
        code = task.get("code", "")
        language = task.get("language", "python")
        doc_type = task.get("doc_type", "function")
        
        if not code:
            return {"error": "Code is required for documentation"}
        
        result = await self.hf_service.generate_code_documentation(code, language)
        
        if result["success"]:
            return {
                "result": {
                    "original_code": code,
                    "language": language,
                    "documentation": result["text"],
                    "doc_type": doc_type,
                    "generated_with": result["model"]
                }
            }
        else:
            return {"error": f"Failed to generate documentation: {result.get('error', 'Unknown error')}"}
    
    async def _create_tests(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Create unit tests for code."""
        code = task.get("code", "")
        language = task.get("language", "python")
        test_framework = task.get("test_framework", "pytest")
        
        if not code:
            return {"error": "Code is required for test generation"}
        
        prompt = f"""
        Generate {test_framework} unit tests for this {language} code:
        
        {language}
        {code}
        
        
        Test code:
        {language}
        import {test_framework}
        """
        
        result = await self.hf_service.generate_text(
            prompt=prompt,
            model="microsoft/CodeBERT-base",
            max_length=200,
            temperature=0.3
        )
        
        return {
            "result": {
                "original_code": code,
                "language": language,
                "test_framework": test_framework,
                "test_code": result.get("text", ""),
                "test_coverage_estimate": self._estimate_test_coverage(code, result.get("text", "")),
                "additional_test_suggestions": self._get_additional_test_suggestions(code)
            }
        }
    
    def _initialize_code_templates(self) -> Dict[str, str]:
        """Initialize code templates."""
        return {
            "fastapi_endpoint": """
@router.get("/{endpoint}")
async def get_{endpoint}():
    return {{"message": "Hello from {endpoint}"}}
            """,
            "react_component": """
import React from 'react';

const {ComponentName} = () => {{
    return (
        <div>
            <h1>{ComponentName}</h1>
        </div>
    );
}}

export default {ComponentName};
            """,
            "python_function": """
def {function_name}({parameters}):
    \"\"\"
    {description}
    \"\"\"
    # Implementation here
    pass
            """
        }
    
    def _assess_code_quality(self, code: str) -> float:
        """Assess code quality with simple metrics."""
        if not code:
            return 0.0
        
        score = 0.8  # Base score
        
        # Check for comments
        if "#" in code or "/*" in code or "///" in code:
            score += 0.1
        
        # Check for proper indentation
        lines = code.split('\n')
        indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))
        if indented_lines > 0:
            score += 0.1
        
        # Check for function definitions
        if "def " in code or "function " in code or "const " in code:
            score += 0.1
        
        return min(score, 1.0)
    
    def _check_security_issues(self, code: str) -> List[str]:
        """Check for common security issues."""
        issues = []
        code_lower = code.lower()
        
        if "eval(" in code_lower:
            issues.append("Avoid using eval() - security risk")
        if "exec(" in code_lower:
            issues.append("Avoid using exec() - security risk")
        if "sql" in code_lower and ("+" in code or "%" in code):
            issues.append("Potential SQL injection vulnerability")
        if "password" in code_lower and "=" in code:
            issues.append("Avoid hardcoding passwords")
        
        return issues
    
    def _get_performance_suggestions(self, code: str) -> List[str]:
        """Get performance improvement suggestions."""
        suggestions = []
        
        if "for " in code and "append(" in code:
            suggestions.append("Consider using list comprehension instead of append in loop")
        if "import *" in code:
            suggestions.append("Avoid wildcard imports for better performance")
        if code.count("def ") > 5:
            suggestions.append("Consider breaking large files into smaller modules")
        
        return suggestions
    
    def _get_best_practices(self, language: str) -> List[str]:
        """Get best practices for the language."""
        practices = {
            "python": [
                "Follow PEP 8 style guide",
                "Use type hints for better code clarity",
                "Write docstrings for functions and classes",
                "Use virtual environments for dependencies"
            ],
            "javascript": [
                "Use const/let instead of var",
                "Use async/await for asynchronous operations",
                "Follow ESLint recommendations",
                "Use meaningful variable names"
            ],
            "react": [
                "Use functional components with hooks",
                "Implement proper error boundaries",
                "Optimize re-renders with useMemo/useCallback",
                "Follow component naming conventions"
            ]
        }
        
        return practices.get(language.lower(), ["Follow language-specific best practices"])
    
    def _get_code_suggestions(self, component_type: str, framework: str) -> List[str]:
        """Get suggestions for code improvement."""
        suggestions = [
            f"Add error handling for {component_type}",
            f"Include unit tests for {framework} {component_type}",
            "Add proper documentation",
            "Consider performance optimization"
        ]
        
        if framework.lower() == "react":
            suggestions.extend([
                "Use PropTypes or TypeScript for type checking",
                "Implement proper state management",
                "Add accessibility attributes"
            ])
        elif framework.lower() == "python":
            suggestions.extend([
                "Add type hints",
                "Follow PEP 8 conventions",
                "Use virtual environments"
            ])
        
        return suggestions
    
    def _get_deployment_instructions(self, framework: str) -> List[str]:
        """Get deployment instructions for framework."""
        instructions = {
            "fastapi": [
                "Install dependencies: pip install fastapi uvicorn",
                "Run with: uvicorn main:app --reload",
                "Deploy with Docker or cloud services",
                "Set up environment variables"
            ],
            "react": [
                "Install dependencies: npm install",
                "Build for production: npm run build",
                "Deploy to static hosting (Netlify, Vercel)",
                "Configure environment variables"
            ],
            "flask": [
                "Install dependencies: pip install flask",
                "Set FLASK_APP environment variable",
                "Run with: flask run",
                "Deploy with WSGI server (Gunicorn)"
            ]
        }
        
        return instructions.get(framework.lower(), ["Follow framework-specific deployment guide"])
    
    def _get_testing_suggestions(self, endpoints: List[str]) -> List[str]:
        """Get testing suggestions for endpoints."""
        return [
            "Implement unit tests for each endpoint",
            "Add integration tests for API workflows",
            "Test error handling and edge cases",
            "Implement load testing for performance",
            "Add authentication and authorization tests"
        ]
    
    def _get_security_recommendations(self) -> List[str]:
        """Get security recommendations."""
        return [
            "Implement proper authentication and authorization",
            "Use HTTPS for all communications",
            "Validate and sanitize all input data",
            "Implement rate limiting",
            "Use environment variables for sensitive data",
            "Implement CORS policies",
            "Add request/response logging",
            "Use secure headers (HSTS, CSP, etc.)"
        ]
    
    def _estimate_test_coverage(self, original_code: str, test_code: str) -> str:
        """Estimate test coverage percentage."""
        if not test_code:
            return "0%"
        
        # Simple heuristic based on test functions vs original functions
        original_functions = original_code.count("def ") + original_code.count("function ")
        test_functions = test_code.count("test_") + test_code.count("it(")
        
        if original_functions == 0:
            return "N/A"
        
        coverage = min((test_functions / original_functions) * 100, 100)
        return f"{coverage:.0f}%"
    
    def _get_additional_test_suggestions(self, code: str) -> List[str]:
        """Get additional testing suggestions."""
        suggestions = [
            "Add edge case testing",
            "Test error conditions",
            "Implement mock testing for external dependencies",
            "Add performance benchmarks"
        ]
        
        if "async" in code:
            suggestions.append("Test async/await functionality")
        if "database" in code.lower() or "db" in code.lower():
            suggestions.append("Add database integration tests")
        if "api" in code.lower() or "request" in code.lower():
            suggestions.append("Add API endpoint testing")
        
        return suggestions