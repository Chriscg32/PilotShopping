import pytest
import asyncio
from agents import DataAgent, SecurityAgent, DevOpsAgent, AIMLAgent

class TestNewAgents:
    @pytest.mark.asyncio
    async def test_data_agent_analysis(self):
        agent = DataAgent()
        task = {
            "type": "analyze_data",
            "data": {"test": [1, 2, 3, 4, 5]},
            "analysis_type": "descriptive"
        }
        result = await agent.process_task(task)
        assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_security_agent_token_generation(self):
        agent = SecurityAgent()
        task = {
            "type": "generate_token",
            "payload": {"user_id": "123"},
            "expiry": 24
        }
        result = await agent.process_task(task)
        assert result["status"] == "success"
        assert "token" in result