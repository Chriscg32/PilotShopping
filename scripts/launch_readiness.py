#!/usr/bin/env python3
"""
ButterflyBlue Creations - Automated Launch Readiness System
This script determines if the system is ready for production launch.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import requests
import subprocess
import psutil

class LaunchReadinessSystem:
    """Comprehensive launch readiness assessment system."""
    
    def __init__(self, environment: str = "production"):
        self.environment = environment
        self.base_url = self._get_base_url()
        self.criteria = self._load_launch_criteria()
        self.results = {}
        
    def _get_base_url(self) -> str:
        """Get base URL for environment."""
        urls = {
            "development": "http://localhost:8000",
            "staging": "https://staging.butterflyblue.com",
            "production": "https://api.butterflyblue.com"
        }
        return urls.get(self.environment, urls["development"])
    
    def _load_launch_criteria(self) -> Dict[str, Any]:
        """Load launch readiness criteria."""
        return {
            "performance": {
                "max_response_time": 2.0,  # seconds
                "min_success_rate": 99.5,  # percentage
                "max_error_rate": 0.1      # percentage
            },
            "reliability": {
                "min_uptime": 99.9,        # percentage
                "max_recovery_time": 30,   # seconds
                "chaos_test_pass": True
            },
            "security": {
                "max_vulnerabilities": 0,
                "ssl_valid": True,
                "auth_working": True
            },
            "functionality": {
                "all_agents_working": True,
                "payments_working": True,
                "integrations_working": True
            },
            "quality": {
                "min_test_coverage": 90,   # percentage
                "all_tests_passing": True,
                "no_critical_bugs": True
            }
        }
    
    async def run_comprehensive_assessment(self) -> Dict[str, Any]:
        """Run complete launch readiness assessment."""
        print(f"🦋 ButterflyBlue Launch Readiness Assessment")
        print(f"Environment: {self.environment}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Run all assessment categories
        assessments = [
            ("Performance", self._assess_performance),
            ("Reliability", self._assess_reliability),
            ("Security", self._assess_security),
            ("Functionality", self._assess_functionality),
            ("Quality", self._assess_quality)
        ]
        
        for category, assessment_func in assessments:
            print(f"\n🔍 Assessing {category}...")
            try:
                self.results[category.lower()] = await assessment_func()
                status = "✅ PASS" if self.results[category.lower()]["passed"] else "❌ FAIL"
                print(f"{status} {category} Assessment")
            except Exception as e:
                print(f"❌ FAIL {category} Assessment - Error: {str(e)}")
                self.results[category.lower()] = {"passed": False, "error": str(e)}
        
        # Generate final decision
        final_decision = self._make_launch_decision()
        
        # Generate report
        report = self._generate_report(final_decision)
        
        return {
            "ready_for_launch": final_decision["ready"],
            "assessment_results": self.results,
            "blockers": final_decision["blockers"],
            "recommendations": final_decision["recommendations"],
            "report": report
        }
    
    async def _assess_performance(self) -> Dict[str, Any]:
        """Assess system performance."""
        results = {
            "response_times": [],
            "success_rate": 0,
            "error_rate": 0,
            "passed": False
        }
        
        # Test multiple endpoints
        endpoints = [
            "/health",
            "/api/agents/marketing/health",
            "/api/agents/finance/health",
            "/api/agents/engineering/health",
            "/api/agents/design/health"
        ]
        
        total_requests = 0
        successful_requests = 0
        
        for endpoint in endpoints:
            for _ in range(10):  # 10 requests per endpoint
                try:
                    start_time = asyncio.get_event_loop().time()
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                    end_time = asyncio.get_event_loop().time()
                    
                    response_time = end_time - start_time
                    results["response_times"].append(response_time)
                    
                    total_requests += 1
                    if response.status_code == 200:
                        successful_requests += 1
                        
                except Exception as e:
                    total_requests += 1
                    results["response_times"].append(10.0)  # Timeout
        
        # Calculate metrics
        avg_response_time = sum(results["response_times"]) / len(results["response_times"])
        results["success_rate"] = (successful_requests / total_requests) * 100
        results["error_rate"] = ((total_requests - successful_requests) / total_requests) * 100
        results["avg_response_time"] = avg_response_time
        
        # Check against criteria
        criteria = self.criteria["performance"]
        results["passed"] = (
            avg_response_time <= criteria["max_response_time"] and
            results["success_rate"] >= criteria["min_success_rate"] and
            results["error_rate"] <= criteria["max_error_rate"]
        )
        
        return results
    
    async def _assess_reliability(self) -> Dict[str, Any]:
        """Assess system reliability."""
        results = {
            "uptime": 0,
            "chaos_tests_passed": False,
            "recovery_time": 0,
            "passed": False
        }
        
        try:
            # Check uptime
            uptime_response = requests.get(f"{self.base_url}/api/system/uptime")
            if uptime_response.status_code == 200:
                uptime_data = uptime_response.json()
                results["uptime"] = uptime_data.get("uptime_percentage", 0)
            
            # Run chaos tests
            chaos_response = requests.post(f"{self.base_url}/api/system/chaos-test")
            if chaos_response.status_code == 200:
                chaos_data = chaos_response.json()
                results["chaos_tests_passed"] = chaos_data.get("all_passed", False)
                results["recovery_time"] = chaos_data.get("max_recovery_time", 999)
            
            # Check against criteria
            criteria = self.criteria["reliability"]
            results["passed"] = (
                results["uptime"] >= criteria["min_uptime"] and
                results["chaos_tests_passed"] == criteria["chaos_test_pass"] and
                results["recovery_time"] <= criteria["max_recovery_time"]
            )
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    async def _assess_security(self) -> Dict[str, Any]:
        """Assess system security."""
        results = {
            "vulnerabilities": 0,
            "ssl_valid": False,
            "auth_working": False,
            "security_headers": False,
            "passed": False
        }
        
        try:
            # Check SSL certificate
            ssl_response = requests.get(f"{self.base_url}/health", verify=True)
            results["ssl_valid"] = ssl_response.status_code == 200
            
            # Check security headers
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            headers_present = sum(1 for header in security_headers if header in ssl_response.headers)
            results["security_headers"] = headers_present >= 3
            
            # Test authentication
            auth_response = requests.post(f"{self.base_url}/api/auth/test", json={
                "username": "test_user",
                "password": "test_password"
            })
            results["auth_working"] = auth_response.status_code in [200, 401]  # Either works or properly rejects
            
            # Run security scan (simplified)
            vuln_response = requests.get(f"{self.base_url}/api/system/security-scan")
            if vuln_response.status_code == 200:
                scan_data = vuln_response.json()
                results["vulnerabilities"] = scan_data.get("critical_vulnerabilities", 999)
            
            # Check against criteria
            criteria = self.criteria["security"]
            results["passed"] = (
                results["vulnerabilities"] <= criteria["max_vulnerabilities"] and
                results["ssl_valid"] == criteria["ssl_valid"] and
                results["auth_working"] == criteria["auth_working"] and
                results["security_headers"]
            )
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    async def _assess_functionality(self) -> Dict[str, Any]:
        """Assess core functionality."""
        results = {
            "agents_working": {},
            "payments_working": False,
            "integrations_working": {},
            "passed": False
        }
        
        try:
            # Test all agents
            agents = ["marketing", "finance", "engineering", "design", "customer_service"]
            for agent in agents:
                try:
                    agent_response = requests.post(f"{self.base_url}/api/agents/{agent}/test", json={
                        "test_type": "basic_functionality"
                    })
                    results["agents_working"][agent] = agent_response.status_code == 200
                except:
                    results["agents_working"][agent] = False
            
            # Test payment processing
            payment_response = requests.post(f"{self.base_url}/api/payments/test", json={
                "amount": 100,
                "currency": "USD",
                "test_mode": True
            })
            results["payments_working"] = payment_response.status_code == 200
            
            # Test key integrations
            integrations = ["huggingface", "paystack", "paypal", "email"]
            for integration in integrations:
                try:
                    int_response = requests.get(f"{self.base_url}/api/integrations/{integration}/health")
                    results["integrations_working"][integration] = int_response.status_code == 200
                except:
                    results["integrations_working"][integration] = False
            
            # Check against criteria
            criteria = self.criteria["functionality"]
            results["passed"] = (
                all(results["agents_working"].values()) == criteria["all_agents_working"] and
                results["payments_working"] == criteria["payments_working"] and
                all(results["integrations_working"].values()) == criteria["integrations_working"]
            )
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    async def _assess_quality(self) -> Dict[str, Any]:
        """Assess code quality and testing."""
        results = {
            "test_coverage": 0,
            "tests_passing": False,
            "critical_bugs": 0,
            "passed": False
        }
        
        try:
            # Get test coverage
            coverage_result = subprocess.run(
                ["python", "-m", "pytest", "--cov=app", "--cov-report=json"],
                capture_output=True,
                text=True
            )
            
            if coverage_result.returncode == 0:
                # Parse coverage report
                with open("coverage.json", "r") as f:
                    coverage_data = json.load(f)
                    results["test_coverage"] = coverage_data["totals"]["percent_covered"]
                    results["tests_passing"] = True
            
            # Check for critical bugs (simplified - would integrate with bug tracker)
            bugs_response = requests.get(f"{self.base_url}/api/system/bugs")
            if bugs_response.status_code == 200:
                bugs_data = bugs_response.json()
                results["critical_bugs"] = bugs_data.get("critical_count", 0)
            
            # Check against criteria
            criteria = self.criteria["quality"]
            results["passed"] = (
                results["test_coverage"] >= criteria["min_test_coverage"] and
                results["tests_passing"] == criteria["all_tests_passing"] and
                results["critical_bugs"] == 0
            )
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def _make_launch_decision(self) -> Dict[str, Any]:
        """Make final launch decision based on all assessments."""
        passed_assessments = [k for k, v in self.results.items() if v.get("passed", False)]
        failed_assessments = [k for k, v in self.results.items() if not v.get("passed", False)]
        
        ready_for_launch = len(failed_assessments) == 0
        
        blockers = []
        recommendations = []
        
        if not ready_for_launch:
            for assessment in failed_assessments:
                result = self.results[assessment]
                if assessment == "performance":
                    if result.get("avg_response_time", 0) > 2.0:
                        blockers.append(f"Response time too high: {result['avg_response_time']:.2f}s (max: 2.0s)")
                    if result.get("success_rate", 0) < 99.5:
                        blockers.append(f"Success rate too low: {result['success_rate']:.1f}% (min: 99.5%)")
                
                elif assessment == "security":
                    if result.get("vulnerabilities", 0) > 0:
                        blockers.append(f"Critical vulnerabilities found: {result['vulnerabilities']}")
                    if not result.get("ssl_valid", False):
                        blockers.append("SSL certificate invalid or missing")
                
                elif assessment == "functionality":
                    failed_agents = [k for k, v in result.get("agents_working", {}).items() if not v]
                    if failed_agents:
                        blockers.append(f"Agents not working: {', '.join(failed_agents)}")
                    if not result.get("payments_working", False):
                        blockers.append("Payment processing not working")
                
                elif assessment == "quality":
                    if result.get("test_coverage", 0) < 90:
                        blockers.append(f"Test coverage too low: {result['test_coverage']:.1f}% (min: 90%)")
                    if result.get("critical_bugs", 0) > 0:
                        blockers.append(f"Critical bugs present: {result['critical_bugs']}")
        
        # Generate recommendations
        if ready_for_launch:
            recommendations.append("✅ System is ready for production launch!")
            recommendations.append("🚀 All quality gates passed")
            recommendations.append("📊 Monitor system closely post-launch")
        else:
            recommendations.append("❌ System NOT ready for launch")
            recommendations.append("🔧 Address all blockers before proceeding")
            recommendations.append("🧪 Re-run assessment after fixes")
        
        return {
            "ready": ready_for_launch,
            "passed_assessments": passed_assessments,
            "failed_assessments": failed_assessments,
            "blockers": blockers,
            "recommendations": recommendations
        }
    
    def _generate_report(self, decision: Dict[str, Any]) -> str:
        """Generate comprehensive launch readiness report."""
        report = f"""
🦋 ButterflyBlue Creations - Launch Readiness Report
{'='*60}

Environment: {self.environment}
Assessment Time: {datetime.now().isoformat()}
Launch Ready: {'✅ YES' if decision['ready'] else '❌ NO'}

ASSESSMENT RESULTS:
{'-'*30}
"""
        
        for category, result in self.results.items():
            status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
            report += f"{category.upper()}: {status}\n"
            
            if category == "performance":
                report += f"  - Avg Response Time: {result.get('avg_response_time', 0):.2f}s\n"
                report += f"  - Success Rate: {result.get('success_rate', 0):.1f}%\n"
                report += f"  - Error Rate: {result.get('error_rate', 0):.1f}%\n"
            
            elif category == "security":
                report += f"  - Vulnerabilities: {result.get('vulnerabilities', 'Unknown')}\n"
                report += f"  - SSL Valid: {result.get('ssl_valid', False)}\n"
                report += f"  - Auth Working: {result.get('auth_working', False)}\n"
            
            elif category == "functionality":
                working_agents = sum(1 for v in result.get('agents_working', {}).values() if v)
                total_agents = len(result.get('agents_working', {}))
                report += f"  - Agents Working: {working_agents}/{total_agents}\n"
                report += f"  - Payments Working: {result.get('payments_working', False)}\n"
            
            elif category == "quality":
                report += f"  - Test Coverage: {result.get('test_coverage', 0):.1f}%\n"
                report += f"  - Tests Passing: {result.get('tests_passing', False)}\n"
                report += f"  - Critical Bugs: {result.get('critical_bugs', 'Unknown')}\n"
            
            report += "\n"
        
        if decision["blockers"]:
            report += f"BLOCKERS:\n{'-'*30}\n"
            for blocker in decision["blockers"]:
                report += f"❌ {blocker}\n"
            report += "\n"
        
        report += f"RECOMMENDATIONS:\n{'-'*30}\n"
        for rec in decision["recommendations"]:
            report += f"{rec}\n"
        
        return report

async def main():
    """Main function to run launch readiness assessment."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ButterflyBlue Launch Readiness Assessment")
    parser.add_argument("--environment", default="production", choices=["development", "staging", "production"])
    parser.add_argument("--output", default="console", choices=["console", "json", "file"])
    args = parser.parse_args()
    
    # Run assessment
    system = LaunchReadinessSystem(args.environment)
    results = await system.run_comprehensive_assessment()
    
    # Output results
    if args.output == "console":
        print(results["report"])
    elif args.output == "json":
        print(json.dumps(results, indent=2))
    elif args.output == "file":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"launch_readiness_{args.environment}_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(results["report"])
        print(f"Report saved to {filename}")
    
    # Exit with appropriate code
    sys.exit(0 if results["ready_for_launch"] else 1)

if __name__ == "__main__":
    asyncio.run(main())