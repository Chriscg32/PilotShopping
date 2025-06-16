import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock
from agents.aiml_agent import AIMLAgent

class TestAIMLAgent:
    @pytest.fixture
    def aiml_agent(self):
        return AIMLAgent()
    
    @pytest.fixture
    def training_data(self):
        # Create sample training data
        np.random.seed(42)
        data = {
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100),
            'target': np.random.randint(0, 2, 100)
        }
        return pd.DataFrame(data)
    
    @pytest.mark.asyncio
    async def test_train_model(self, aiml_agent, training_data):
        with patch('os.makedirs'), patch('joblib.dump'):
            task = {
                "type": "train_model",
                "data": training_data.to_dict('records'),
                "config": {
                    "target_column": "target",
                    "feature_columns": ["feature1", "feature2", "feature3"],
                    "model_type": "random_forest_classifier",
                    "test_size": 0.2,
                    "model_params": {"n_estimators": 10, "random_state": 42}
                }
            }
            
            result = await aiml_agent.process_task(task)
            
            assert result["status"] == "success"
            assert "model_training" in result
            assert "model_id" in result["model_training"]
            assert "train_score" in result["model_training"]
            assert "test_score" in result["model_training"]
    
    @pytest.mark.asyncio
    async def test_make_prediction(self, aiml_agent, training_data):
        # First train a model
        model_id = "test_model_123"
        from sklearn.ensemble import RandomForestClassifier
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        X = training_data[["feature1", "feature2", "feature3"]]
        y = training_data["target"]
        model.fit(X, y)
        
        aiml_agent.models[model_id] = model
        aiml_agent.model_registry[model_id] = {
            "feature_columns": ["feature1", "feature2", "feature3"]
        }
        
        # Test prediction
        task = {
            "type": "make_prediction",
            "model_id": model_id,
            "input_data": {
                "feature1": 0.5,
                "feature2": -0.3,
                "feature3": 1.2
            }
        }
        
        result = await aiml_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "predictions" in result
        assert "predictions" in result["predictions"]
        assert "probabilities" in result["predictions"]
    
    @pytest.mark.asyncio
    async def test_preprocess_data(self, aiml_agent, training_data):
        # Add some missing values and outliers
        data_with_issues = training_data.copy()
        data_with_issues.loc[0, 'feature1'] = None
        data_with_issues.loc[1, 'feature2'] = 100  # Outlier
        
        task = {
            "type": "preprocess_data",
            "data": data_with_issues.to_dict('records'),
            "preprocessing_config": {
                "handle_missing": "mean",
                "handle_outliers": "clip",
                "normalize": True
            }
        }
        
        result = await aiml_agent.process_task(task)
        
        assert result["status"] == "success"