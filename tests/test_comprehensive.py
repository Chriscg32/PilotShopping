#!/usr/bin/env python3
"""
ButterflyBlue Comprehensive Test Suite
Unit, Integration, and E2E tests for all components
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json
from datetime import datetime

# Import our application
from main import app
from agents.finance_agent import FinanceAgent
from database.models import DatabaseManager
from auth.security import SecurityManager

# Test client
client = TestClient(app)

class TestFinanceAgent:
    """Test Finance Agent functionality"""
    
    @pytest.fixture
    def finance_agent(self):
        return FinanceAgent()
    
    @pytest.mark.asyncio
    async def test_payment_processing(self, finance_agent):
        """Test payment processing"""
        payment_data = {
            "gateway": "paystack",
            "amount": 100.00,
            "currency": "ZAR",
            "customer_email": "test@example.com"
        }
        
        result = await finance_agent.process_payment(payment_data)
        
        assert result["status"] == "success"
        assert result["gateway"] == "paystack"
        assert result["amount"] == 100.00
        assert "payment_id" in result
        assert "invoice" in result
    
    @pytest.mark.asyncio
    async def test_invoice_generation(self, finance_agent):
        """Test invoice generation"""
        invoice_data = {
            "amount": 100.00,
            "currency": "ZAR",
            "customer_email": "test@example.com",
            "payment_id": "test_payment_123"
        }
        
        result = await finance_agent.generate_invoice(invoice_data)
        
        assert result["status"] == "success"
        invoice = result["invoice"]
        assert "invoice_id" in invoice
        assert invoice["financial_summary"]["total_amount"] == 115.00  # Including 15% VAT
    
    @pytest.mark.asyncio
    async def test_financial_analysis(self, finance_agent):
        """Test financial analysis"""
        analysis_request = {
            "type": "monthly_summary",
            "date_range": 30
        }
        
        result = await finance_agent.financial_analysis(analysis_request)
        
        assert result["status"] == "success"
        analysis = result["analysis"]
        assert "revenue" in analysis
        assert "profit_margin" in analysis
        assert "recommendations" in analysis

class TestSecurity:
    """Test Security and Authentication"""
    
    @pytest.fixture
    def security_manager(self):
        return SecurityManager()
    
    def test_password_hashing(self, security_manager):
        """Test password hashing and verification"""
        password = "test_password_123"
        hashed = security_manager.hash_password(password)
        
        assert security_manager.verify_password(password, hashed)
        assert not security_manager.verify_password("wrong_password", hashed)
    
    def test_jwt_token_creation(self, security_manager):
        """Test JWT token creation and verification"""
        user_data = {"sub": "user123", "email": "test@example.com"}
        
        # Create tokens
        access_token = security_manager.create_access_token(user_data)
        refresh_token = security_manager.create_refresh_token(user_data)
        
        # Verify tokens
        access_payload = security_manager.verify_token(access_token)
        refresh_payload = security_manager.verify_token(refresh_token)
        
        assert access_payload["sub"] == "user123"
        assert access_payload["type"] == "access"
        assert refresh_payload["type"] == "refresh"
    
    def test_api_key_generation(self, security_manager):
        """Test API key generation and verification"""
        user_id = "user123"
        api_key = security_manager.generate_api_key(user_id)
        
        assert api_key.startswith("bb_")
        # Note: Redis verification would need Redis running for full test

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agents" in data
    
    def test_agent_status(self):
        """Test agent status endpoint"""
        response = client.get("/api/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 6  # All 6 agents
    
    def test_boss_agent_demo(self):
        """Test Boss Agent demo endpoint"""
        response = client.post("/api/agents/boss/demo", json={
            "task": "coordinate marketing campaign"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "boss"
        assert "result" in data
    
    def test_marketing_agent_demo(self):
        """Test Marketing Agent demo endpoint"""
        response = client.post("/api/agents/marketing/demo", json={
            "campaign_type": "social_media",
            "target_audience": "small businesses"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "marketing"
        assert "campaign_strategy" in data["result"]
    
    def test_finance_agent_demo(self):
        """Test Finance Agent demo endpoint"""
        response = client.post("/api/agents/finance/demo", json={
            "action": "generate_invoice",
            "amount": 100.00
        })
        assert response.status_code == 200
        data = response.json()
        assert data["agent"] == "finance"
        assert "invoice" in data["result"]

class TestIntegration:
    """Integration tests for multi-agent workflows"""
    
    def test_complete_business_workflow(self):
        """Test complete business automation workflow"""
        # 1. Boss Agent coordinates task
        boss_response = client.post("/api/agents/boss/demo", json={
            "task": "launch product campaign"
        })
        assert boss_response.status_code == 200
        
        # 2. Marketing Agent creates campaign
        marketing_response = client.post("/api/agents/marketing/demo", json={
            "campaign_type": "product_launch",
            "product": "AI automation tool"
        })
        assert marketing_response.status_code == 200
        
        # 3. Finance Agent processes payment
        finance_response = client.post("/api/agents/finance/demo", json={
            "action": "process_payment",
            "amount": 299.00
        })
        assert finance_response.status_code == 200
        
        # Verify all agents responded successfully
        assert all([
            boss_response.json()["status"] == "success",
            marketing_response.json()["status"] == "success", 
            finance_response.json()["status"] == "success"
        ])

class TestPerformance:
    """Performance and load tests"""
    
    def test_concurrent_requests(self):
        """Test handling concurrent requests"""
        import concurrent.futures
        import time
        
        def make_request():
            return client.get("/health")
        
        start_time = time.time()
        
        # Make 50 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            responses = [future.result() for future in futures]
        
        end_time = time.time()
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in responses)
        
        # Should complete within reasonable time (5 seconds)
        assert (end_time - start_time) < 5.0
    
    def test_large_payload_handling(self):
        """Test handling of large payloads"""
        large_data = {
            "campaign_data": ["item_" + str(i) for i in range(1000)],
            "description": "x" * 10000  # 10KB string
        }
        
        response = client.post("/api/agents/marketing/demo", json=large_data)
        assert response.status_code == 200

# Pytest configuration and fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Test data fixtures
@pytest.fixture
def sample_user_data():
    return {
        "email": "test@butterflyblue.co.za",
        "name": "Test User",
        "subscription_tier": "premium"
    }

@pytest.fixture
def sample_payment_data():
    return {
        "amount": 299.00,
        "currency": "ZAR",
        "gateway": "paystack",
        "customer_email": "customer@example.com"
    }

# Custom test markers
pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.integration
]

if __name__ == "__main__":
    # Run tests with coverage
    pytest.main([
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v",
        __file__
    ])