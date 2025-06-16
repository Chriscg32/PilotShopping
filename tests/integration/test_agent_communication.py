import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from agents.boss_agent import BossAgent
from agents.data_agent import DataAgent
from agents.security_agent import SecurityAgent
from agents.devops_agent import DevOpsAgent
from agents.aiml_agent import AIMLAgent

class TestAgentIntegration:
    @pytest.fixture
    def mock_mqtt_client(self):
        mock = Mock()
        mock.publish = AsyncMock()
        mock.subscribe = AsyncMock()
        return mock
    
    @pytest.mark.asyncio
    async def test_boss_to_data_agent_workflow(self, mock_mqtt_client):
        boss = BossAgent()
        boss.mqtt_client = mock_mqtt_client
        
        # Test task delegation to data agent
        task = {
            "type": "analyze_data",
            "description": "analyze customer data for insights",
            "data": [
                {"id": 1, "name": "John", "age": 30, "purchase": 100},
                {"id": 2, "name": "Jane", "age": 25, "purchase": 150}
            ],
            "analysis_type": "descriptive"
        }
        
        # Mock the agent determination
        determined_agent = boss._determine_agent_for_task(task)
        assert determined_agent == "data"
    
    @pytest.mark.asyncio
    async def test_security_and_data_agent_workflow(self):
        """Test workflow involving multiple agents"""
        security_agent = SecurityAgent()
        data_agent = DataAgent()
        
        # Step 1: Encrypt sensitive data
        sensitive_data = {"customer_id": 123, "ssn": "123-45-6789"}
        encrypt_task = {
            "type": "encrypt_data",
            "data": sensitive_data
        }
        
        encrypt_result = await security_agent.process_task(encrypt_task)
        assert encrypt_result["status"] == "success"
        
        # Step 2: Analyze encrypted data (mock scenario)
        analysis_task = {
            "type": "data_quality_check",
            "dataset": [{"id": 1, "encrypted_field": "encrypted_data"}]
        }
        
        analysis_result = await data_agent.process_task(analysis_task)
        assert analysis_result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_ml_pipeline_workflow(self):
        """Test complete ML pipeline with multiple agents"""
        data_agent = DataAgent()
        aiml_agent = AIMLAgent()
        devops_agent = DevOpsAgent()
        
        # Step 1: Prepare data
        raw_data = [
            {"feature1": 1.0, "feature2": 2.0, "target": 0},
            {"feature1": 2.0, "feature2": 3.0, "target": 1},
            {"feature1": 3.0, "feature2": 4.0, "target": 0}
        ]
        
        preprocess_task = {
            "type": "preprocess_data",
            "data": raw_data,
            "preprocessing_config": {"normalize": True}
        }
        
        preprocess_result = await data_agent.process_task(preprocess_task)
        assert preprocess_result["status"] == "success"
        
        # Step 2: Train model
        train_task = {
            "type": "train_model",
            "data": raw_data,
            "config": {
                "target_column": "target",
                "feature_columns": ["feature1", "feature2"],
                "model_type": "random_forest_classifier"
            }
        }
        
        with patch('os.makedirs'), patch('joblib.dump'):
            train_result = await aiml_agent.process_task(train_task)
            assert train_result["status"] == "success"