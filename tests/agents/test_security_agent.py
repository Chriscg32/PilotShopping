import pytest
import jwt
from agents.security_agent import SecurityAgent

class TestSecurityAgent:
    @pytest.fixture
    def security_agent(self):
        return SecurityAgent()
    
    @pytest.mark.asyncio
    async def test_generate_secure_token(self, security_agent):
        task = {
            "type": "generate_token",
            "payload": {"user_id": "123", "role": "admin"},
            "expiry": 24
        }
        
        result = await security_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "token" in result
        assert "expires_at" in result
        assert "token_id" in result
    
    @pytest.mark.asyncio
    async def test_encrypt_data(self, security_agent):
        test_data = {"sensitive": "information", "user_id": 123}
        
        task = {
            "type": "encrypt_data",
            "data": test_data
        }
        
        result = await security_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "encrypted_data" in result
        assert "encryption_method" in result
        assert result["encryption_method"] == "Fernet"
    
    @pytest.mark.asyncio
    async def test_vulnerability_scan_web(self, security_agent):
        task = {
            "type": "vulnerability_scan",
            "target": {
                "type": "web_application",
                "url": "https://example.com",
                "endpoints": ["/api/users", "/login"]
            }
        }
        
        result = await security_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "scan_results" in result
        assert "vulnerabilities" in result["scan_results"]
        assert "risk_score" in result["scan_results"]
        assert "recommendations" in result["scan_results"]
    
    @pytest.mark.asyncio
    async def test_audit_check(self, security_agent):
        task = {
            "type": "audit_check",
            "system": {
                "name": "user_management",
                "components": ["authentication", "authorization", "logging"]
            }
        }
        
        result = await security_agent.process_task(task)
        
        assert result["status"] == "success"