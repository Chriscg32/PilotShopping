#!/usr/bin/env python3
"""
ButterflyBlue Creations - Launch Readiness Checker
Comprehensive Go/No-Go decision automation
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import subprocess
import sys
import os

class LaunchReadinessChecker:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "UNKNOWN",
            "checks": {},
            "summary": {},
            "recommendations": []
        }
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all launch readiness checks"""
        print("🦋 ButterflyBlue Launch Readiness Check Starting...")
        print("=" * 60)
        
        checks = [
            ("Health Check", self.check_health),
            ("Agent Availability", self.check_agents),
            ("Database Connectivity", self.check_database),
            ("Security Headers", self.check_security),
            ("Performance Baseline", self.check_performance),
            ("Error Handling", self.check_error_handling),
            ("Load Capacity", self.check_load_capacity),
            ("Integration Tests", self.check_integrations),
            ("Monitoring Systems", self.check_monitoring),
            ("Documentation", self.check_documentation)
        ]
        
        passed = 0
        total = len(checks)
        
        for check_name, check_func in checks:
            print(f"\n🔍 Running: {check_name}")
            try:
                result = await check_func()
                self.results["checks"][check_name] = result
                
                if result["status"] == "PASS":
                    print(f"✅ {check_name}: PASSED")
                    passed += 1
                else:
                    print(f"❌ {check_name}: FAILED - {result.get('message', 'Unknown error')}")
                    
            except Exception as e:
                print(f"💥 {check_name}: ERROR - {str(e)}")
                self.results["checks"][check_name] = {
                    "status": "ERROR",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        # Calculate overall status
        success_rate = (passed / total) * 100
        self.results["summary"] = {
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": success_rate
        }
        
        if success_rate >= 95:
            self.results["overall_status"] = "GO"
            print(f"\n🚀 LAUNCH STATUS: GO ({success_rate:.1f}% checks passed)")
        elif success_rate >= 80:
            self.results["overall_status"] = "CONDITIONAL GO"
            print(f"\n⚠️  LAUNCH STATUS: CONDITIONAL GO ({success_rate:.1f}% checks passed)")
        else:
            self.results["overall_status"] = "NO GO"
            print(f"\n🛑 LAUNCH STATUS: NO GO ({success_rate:.1f}% checks passed)")
        
        await self.generate_recommendations()
        return self.results
    
    async def check_health(self) -> Dict[str, Any]:
        """Check application health endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/health", timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "healthy":
                            return {"status": "PASS", "response_time": response.headers.get("X-Response-Time")}
                        else:
                            return {"status": "FAIL", "message": "Health check returned unhealthy status"}
                    else:
                        return {"status": "FAIL", "message": f"Health check returned status {response.status}"}
            except Exception as e:
                return {"status": "FAIL", "message": f"Health check failed: {str(e)}"}
    
    async def check_agents(self) -> Dict[str, Any]:
        """Check all agents are available and responding"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/api/agents/status") as response:
                    if response.status == 200:
                        data = await response.json()
                        agents = data.get("agents", [])
                        
                        expected_agents = ["boss", "marketing", "customer-service", "engineering", "finance", "design"]
                        available_agents = [agent["name"] for agent in agents if agent["status"] == "online"]
                        
                        if len(available_agents) >= len(expected_agents):
                            return {"status": "PASS", "available_agents": available_agents}
                        else:
                            missing = set(expected_agents) - set(available_agents)
                            return {"status": "FAIL", "message": f"Missing agents: {list(missing)}"}
                    else:
                        return {"status": "FAIL", "message": f"Agent status check failed: {response.status}"}
            except Exception as e:
                return {"status": "FAIL", "message": f"Agent check failed: {str(e)}"}
    
    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and basic operations"""
        async with aiohttp.ClientSession() as session:
            try:
                # Test database through API endpoint
                async with session.get(f"{self.base_url}/api/health/database") as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("database_status") == "connected":
                            return {"status": "PASS", "connection_time": data.get("connection_time")}
                        else:
                            return {"status": "FAIL", "message": "Database not connected"}
                    else:
                        return {"status": "FAIL", "message": f"Database check failed: {response.status}"}
            except Exception as e:
                return {"status": "FAIL", "message": f"Database check failed: {str(e)}"}
    
    async def check_security(self) -> Dict[str, Any]:
        """Check security headers and configurations"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/health") as response:
                    headers = response.headers
                    
                    required_headers = [
                        "X-Content-Type-Options",
                        "X-Frame-Options", 
                        "X-XSS-Protection",
                        "Strict-Transport-Security"
                    ]
                    
                    missing_headers = [h for h in required_headers if h not in headers]
                    
                    if not missing_headers:
                        return {"status": "PASS", "security_headers": "All present"}
                    else:
                        return {"status": "FAIL", "message": f"Missing security headers: {missing_headers}"}
            except Exception as e:
                return {"status": "FAIL", "message": f"Security check failed: {str(e)}"}
    
    async def check_performance(self) -> Dict[str, Any]:
        """Check performance baseline"""
        async with aiohttp.ClientSession() as session:
            try:
                # Test response times for key endpoints
                endpoints = ["/health", "/api/agents/status"]
                response_times = []
                
                for endpoint in endpoints:
                    start_time = time.time()
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        end_time = time.time()
                        response_time = (end_time - start_time) * 1000  # Convert to ms
                        response_times.append(response_time)
                        
                        if response.status != 200:
                            return {"status": "FAIL", "message": f"Endpoint {endpoint} returned {response.status}"}
                
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                
                if max_response_time < 2000:  # 2 seconds max
                    return {
                        "status": "PASS", 
                        "avg_response_time": f"{avg_response_time:.2f}ms",
                        "max_response_time": f"{max_response_time:.2f}ms"
                    }
                else:
                    return {"status": "FAIL", "message": f"Response time too high: {max_response_time:.2f}ms"}
                    
            except Exception as e:
                return {"status": "FAIL", "message": f"Performance check failed: {str(e)}"}
    
    async def check_error_handling(self) -> Dict[str, Any]:
        """Check error handling and graceful degradation"""
        async with aiohttp.ClientSession() as session:
            try:
                # Test 404 handling
                async with session.get(f"{self.base_url}/nonexistent-endpoint") as response:
                    if response.status == 404:
                        error_data = await response.json()
                        if "detail" in error_data:
                            return {"status": "PASS", "error_handling": "Proper 404 responses"}
                        else:
                            return {"status": "FAIL", "message": "404 responses lack proper error format"}
                    else:
                        return {"status": "FAIL", "message": f"Expected 404, got {response.status}"}
            except Exception as e:
                return {"status": "FAIL", "message": f"Error handling check failed: {str(e)}"}
    
    async def check_load_capacity(self) -> Dict[str, Any]:
        """Check load capacity with concurrent requests"""
        async with aiohttp.ClientSession() as session:
            try:
                # Send 20 concurrent requests
                tasks = []
                for _ in range(20):
                    task = session.get(f"{self.base_url}/health")
                    tasks.append(task)
                
                start_time = time.time()
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                end_time = time.time()
                
                # Check results
                successful_responses = 0
                for response in responses:
                    if not isinstance(response, Exception) and response.status == 200:
                        successful_responses += 1
                    if hasattr(response, 'close'):
                        response.close()
                
                success_rate = (successful_responses / len(tasks)) * 100
                total_time = end_time - start_time
                
                if success_rate >= 95 and total_time < 10:
                    return {
                        "status": "PASS",
                        "success_rate": f"{success_rate:.1f}%",
                        "total_time": f"{total_time:.2f}s"
                    }
                else:
                    return {
                        "status": "FAIL", 
                        "message": f"Load test failed: {success_rate:.1f}% success in {total_time:.2f}s"
                    }
                    
            except Exception as e:
                return {"status": "FAIL", "message": f"Load capacity check failed: {str(e)}"}
    
    async def check_integrations(self) -> Dict[str, Any]:
        """Check external integrations"""
        async with aiohttp.ClientSession() as session:
            try:
                # Test agent demo endpoints to verify integrations
                test_cases = [
                    ("/api/agents/marketing/demo", {"campaign_type": "test"}),
                    ("/api/agents/finance/demo", {"action": "test"}),
                    ("/api/agents/boss/demo", {"task": "test"})
                ]
                
                for endpoint, payload in test_cases:
                    async with session.post(f"{self.base_url}{endpoint}", json=payload) as response:
                        if response.status != 200:
                            return {"status": "FAIL", "message": f"Integration test failed for {endpoint}"}
                        
                        data = await response.json()
                        if data.get("status") != "success":
                            return {"status": "FAIL", "message": f"Integration response failed for {endpoint}"}
                
                return {"status": "PASS", "integrations": "All agent integrations working"}
                
            except Exception as e:
                return {"status": "FAIL", "message": f"Integration check failed: {str(e)}"}
    
    async def check_monitoring(self) -> Dict[str, Any]:
        """Check monitoring systems availability"""
        try:
            # Check if monitoring endpoints are accessible
            monitoring_checks = []
            
            # Check metrics endpoint
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(f"{self.base_url}/metrics", timeout=5) as response:
                        if response.status == 200:
                            monitoring_checks.append("Metrics endpoint available")
                        else:
                            monitoring_checks.append(f"Metrics endpoint returned {response.status}")
                except:
                    monitoring_checks.append("Metrics endpoint not accessible")
            
            # Check if log files are being written
            log_files = ["logs/app.log", "logs/agents.log", "logs/errors.log"]
            for log_file in log_files:
                if os.path.exists(log_file):
                    # Check if file was modified recently (within last hour)
                    mod_time = os.path.getmtime(log_file)
                    current_time = time.time()
                    if (current_time - mod_time) < 3600:  # 1 hour
                        monitoring_checks.append(f"{log_file} is being updated")
                    else:
                        monitoring_checks.append(f"{log_file} is stale")
                else:
                    monitoring_checks.append(f"{log_file} does not exist")
            
            if len(monitoring_checks) >= 3:  # At least 3 monitoring aspects working
                return {"status": "PASS", "monitoring_status": monitoring_checks}
            else:
                return {"status": "FAIL", "message": "Insufficient monitoring coverage"}
                
        except Exception as e:
            return {"status": "FAIL", "message": f"Monitoring check failed: {str(e)}"}
    
    async def check_documentation(self) -> Dict[str, Any]:
        """Check documentation completeness"""
        try:
            required_docs = [
                "README.md",
                "CHANGELOG.md", 
                "docs/API.md",
                "docs/DEPLOYMENT.md",
                "requirements.txt"
            ]
            
            missing_docs = []
            for doc in required_docs:
                if not os.path.exists(doc):
                    missing_docs.append(doc)
            
            if not missing_docs:
                return {"status": "PASS", "documentation": "All required docs present"}
            else:
                return {"status": "FAIL", "message": f"Missing documentation: {missing_docs}"}
                
        except Exception as e:
            return {"status": "FAIL", "message": f"Documentation check failed: {str(e)}"}
    
    async def generate_recommendations(self):
        """Generate launch recommendations based on check results"""
        recommendations = []
        
        for check_name, result in self.results["checks"].items():
            if result["status"] == "FAIL":
                if "agent" in check_name.lower():
                    recommendations.append(f"🔧 Fix {check_name}: Restart agent services and verify configuration")
                elif "database" in check_name.lower():
                    recommendations.append(f"🗄️ Fix {check_name}: Check database connection and run migrations")
                elif "security" in check_name.lower():
                    recommendations.append(f"🔒 Fix {check_name}: Add missing security headers to web server config")
                elif "performance" in check_name.lower():
                    recommendations.append(f"⚡ Fix {check_name}: Optimize slow endpoints and add caching")
                else:
                    recommendations.append(f"⚠️ Fix {check_name}: {result.get('message', 'Unknown issue')}")
        
        # General recommendations based on overall status
        if self.results["overall_status"] == "NO GO":
            recommendations.extend([
                "🛑 CRITICAL: Do not launch until all major issues are resolved",
                "📋 Review failed checks and create action plan",
                "🧪 Run additional testing after fixes"
            ])
        elif self.results["overall_status"] == "CONDITIONAL GO":
            recommendations.extend([
                "⚠️ CAUTION: Launch with monitoring and rollback plan ready",
                "📊 Monitor key metrics closely during launch",
                "🚨 Have incident response team on standby"
            ])
        else:
            recommendations.extend([
                "🚀 READY: All systems go for launch!",
                "📈 Continue monitoring post-launch metrics",
                "🎉 Celebrate successful deployment preparation"
            ])
        
        self.results["recommendations"] = recommendations
    
    def save_report(self, filename: str = None):
        """Save launch readiness report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"launch_readiness_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Report saved to: {filename}")
        return filename

async def main():
    """Main function to run launch readiness check"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ButterflyBlue Launch Readiness Checker")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL to test")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--slack-webhook", help="Slack webhook URL for notifications")
    
    args = parser.parse_args()
    
    checker = LaunchReadinessChecker(args.url)
    results = await checker.run_all_checks()
    
    # Save report
    report_file = checker.save_report(args.output)
    
    # Send Slack notification if webhook provided
    if args.slack_webhook:
        await send_slack_notification(args.slack_webhook, results)
    
    # Print summary
    print("\n" + "="*60)
    print("🦋 BUTTERFLYBLUE LAUNCH READINESS SUMMARY")
    print("="*60)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Success Rate: {results['summary']['success_rate']:.1f}%")
    print(f"Checks Passed: {results['summary']['passed']}/{results['summary']['total_checks']}")
    
    if results["recommendations"]:
        print("\n📋 RECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"  {rec}")
    
    # Exit with appropriate code
    if results["overall_status"] == "GO":
        sys.exit(0)
    elif results["overall_status"] == "CONDITIONAL GO":
        sys.exit(1)
    else:
        sys.exit(2)

async def send_slack_notification(webhook_url: str, results: Dict[str, Any]):
    """Send launch readiness results to Slack"""
    status_emoji = {
        "GO": "🚀",
        "CONDITIONAL GO": "⚠️",
        "NO GO": "🛑"
    }
    
    status = results["overall_status"]
    emoji = status_emoji.get(status, "❓")
    
    message = {
        "text": f"{emoji} ButterflyBlue Launch Readiness Check",
        "attachments": [
            {
                "color": "good" if status == "GO" else "warning" if status == "CONDITIONAL GO" else "danger",
                "fields": [
                    {
                        "title": "Overall Status",
                        "value": status,
                        "short": True
                    },
                    {
                        "title": "Success Rate", 
                        "value": f"{results['summary']['success_rate']:.1f}%",
                        "short": True
                    },
                    {
                        "title": "Checks Passed",
                        "value": f"{results['summary']['passed']}/{results['summary']['total_checks']}",
                        "short": True
                    }
                ]
            }
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=message) as response:
            if response.status == 200:
                print("✅ Slack notification sent successfully")
            else:
                print(f"❌ Failed to send Slack notification: {response.status}")

if __name__ == "__main__":
    asyncio.run(main())