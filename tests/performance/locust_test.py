#!/usr/bin/env python3
"""
Locust Performance Testing for ButterflyBlue Creations
Advanced user behavior simulation and load testing
"""

from locust import HttpUser, task, between
import json
import random

class ButterflyBlueUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Called when a user starts"""
        # Simulate user authentication (if implemented)
        pass
    
    @task(3)
    def check_health(self):
        """Check application health - most common operation"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    response.success()
                else:
                    response.failure("Health check failed")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def get_agent_status(self):
        """Check agent status"""
        with self.client.get("/api/agents/status", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if len(data.get("agents", [])) >= 6:
                    response.success()
                else:
                    response.failure("Not all agents available")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def test_marketing_agent(self):
        """Test marketing agent with various scenarios"""
        campaigns = [
            {"campaign_type": "social_media", "target_audience": "millennials"},
            {"campaign_type": "email", "target_audience": "small businesses"},
            {"campaign_type": "content", "target_audience": "entrepreneurs"},
            {"campaign_type": "seo", "target_audience": "e-commerce"}
        ]
        
        payload = random.choice(campaigns)
        payload["budget"] = random.randint(500, 5000)
        
        with self.client.post("/api/agents/marketing/demo", 
                            json=payload, 
                            catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure("Marketing agent failed")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def test_finance_agent(self):
        """Test finance agent operations"""
        actions = [
            {"action": "generate_invoice", "amount": random.uniform(100, 1000)},
            {"action": "process_payment", "amount": random.uniform(50, 500)},
            {"action": "financial_analysis", "period": "monthly"}
        ]
        
        payload = random.choice(actions)
        payload["currency"] = random.choice(["ZAR", "USD", "EUR"])
        
        with self.client.post("/api/agents/finance/demo", 
                            json=payload, 
                            catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure("Finance agent failed")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def test_boss_agent(self):
        """Test boss agent coordination"""
        tasks = [
            {"task": "coordinate marketing campaign"},
            {"task": "analyze business performance"},
            {"task": "optimize operations"},
            {"task": "generate business report"}
        ]
        
        payload = random.choice(tasks)
        
        with self.client.post("/api/agents/boss/demo", 
                            json=payload, 
                            catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure("Boss agent failed")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def test_customer_service_agent(self):
        """Test customer service agent"""
        tickets = [
            {"type": "support", "priority": "high", "issue": "payment problem"},
            {"type": "inquiry", "priority": "medium", "issue": "feature request"},
            {"type": "complaint", "priority": "high", "issue": "service issue"},
            {"type": "feedback", "priority": "low", "issue": "general feedback"}
        ]
        
        payload = random.choice(tickets)
        
        with self.client.post("/api/agents/customer-service/demo", 
                            json=payload, 
                            catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure("Customer service agent failed")
            else:
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def test_engineering_agent(self):
        """Test engineering agent"""
        requests = [
            {"task": "generate_api", "framework": "fastapi"},
            {"task": "create_component", "type": "react"},
            {"task": "database_schema", "type": "postgresql"},
            {"task": "deploy_app", "platform": "docker"}
        ]
        
        payload = random.choice(requests)
        
        with self.client.post("/api/agents/engineering/demo", 
                            json=payload, 
                            catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    response.success()
                else:
                    response.failure("Engineering agent failed")
            else:
                response.failure(f"Got status code {response.status_code}")

class StressTestUser(HttpUser):
    """High-intensity stress testing user"""
    wait_time = between(0.1, 0.5)  # Very short wait times
    
    @task
    def rapid_fire_requests(self):
        """Rapid fire requests to test system limits"""
        endpoints = [
            "/health",
            "/api/agents/status",
            "/api/agents/boss/demo",
            "/api/agents/marketing/demo"
        ]
        
        endpoint = random.choice(endpoints)
        
        if endpoint.endswith("/demo"):
            self.client.post(endpoint, json={"test": "stress"})
        else:
            self.client.get(endpoint)

# Custom Locust events for detailed reporting
from locust import events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("🦋 ButterflyBlue Performance Test Starting...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("🦋 ButterflyBlue Performance Test Complete!")
    
    # Generate custom performance report
    stats = environment.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.num_failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"95th percentile: {stats.total.get_response_time_percentile(0.95):.2f}ms")