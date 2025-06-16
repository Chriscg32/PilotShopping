import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union
import joblib
import json
from datetime import datetime
import asyncio
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
from .base_agent import BaseAgent

class AIMLAgent(BaseAgent):
    """Machine learning model training and deployment agent"""
    
    def __init__(self, agent_id: str = "aiml_agent"):
        super().__init__(agent_id)
        self.capabilities = [
            "model_training",
            "model_deployment",
            "prediction_service",
            "model_evaluation",
            "data_preprocessing",
            "feature_engineering"
        ]
        self.models = {}
        self.model_registry = {}
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process AI/ML-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "train_model":
                return await self._train_model(task.get("data"), task.get("config"))
            elif task_type == "make_prediction":
                return await self._make_prediction(task.get("model_id"), task.get("input_data"))
            elif task_type == "evaluate_model":
                return await self._evaluate_model(task.get("model_id"), task.get("test_data"))
            elif task_type == "deploy_model":
                return await self._deploy_model(task.get("model_id"), task.get("deployment_config"))
            elif task_type == "preprocess_data":
                return await self._preprocess_data(task.get("data"), task.get("preprocessing_config"))
            elif task_type == "feature_engineering":
                return await self._feature_engineering(task.get("data"), task.get("feature_config"))
            else:
                return {"status": "error", "message": f"Unknown AI/ML task: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"AI/ML task error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _train_model(self, data: Union[str, Dict], config: Dict) -> Dict[str, Any]:
        """Train machine learning model"""
        # Load data
        if isinstance(data, str):
            df = pd.read_csv(data)
        else:
            df = pd.DataFrame(data)
        
        # Prepare features and target
        target_column = config.get("target_column")
        feature_columns = config.get("feature_columns", [col for col in df.columns if col != target_column])
        
        X = df[feature_columns]
        y = df[target_column]
        
        # Split data
        test_size = config.get("test_size", 0.2)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        
        # Select and train model
        model_type = config.get("model_type", "random_forest")
        model = self._get_model(model_type, config.get("model_params", {}))
        
        model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        # Generate model ID and save
        model_id = f"{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.models[model_id] = model
        
        # Save model metadata
        self.model_registry[model_id] = {
            "model_type": model_type,
            "feature_columns": feature_columns,
            "target_column": target_column,
            "train_score": train_score,
            "test_score": test_score,
            "created_at": datetime.now().isoformat(),
            "config": config
        }
        
        # Save model to disk
        model_path = f"models/{model_id}.joblib"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, model_path)
        
        return {
            "status": "success",
            "model_training": {
                "model_id": model_id,
                "model_type": model_type,
                "train_score": train_score,
                "test_score": test_score,
                "model_path": model_path,
                "feature_columns": feature_columns
            }
        }
    
    def _get_model(self, model_type: str, params: Dict) -> Any:
        """Get model instance based on type"""
        if model_type == "random_forest_classifier":
            return RandomForestClassifier(**params)
        elif model_type == "random_forest_regressor":
            return RandomForestRegressor(**params)
        elif model_type == "linear_regression":
            return LinearRegression(**params)
        elif model_type == "logistic_regression":
            return LogisticRegression(**params)
        else:
            return RandomForestClassifier(**params)  # Default
    
    async def _make_prediction(self, model_id: str, input_data: Union[Dict, List]) -> Dict[str, Any]:
        """Make predictions using trained model"""
        if model_id not in self.models:
            # Try to load from disk
            try:
                model_path = f"models/{model_id}.joblib"
                self.models[model_id] = joblib.load(model_path)
            except:
                return {"status": "error", "message": f"Model {model_id} not found"}
        
        model = self.models[model_id]
        model_info = self.model_registry.get(model_id, {})
        
        # Prepare input data
        if isinstance(input_data, dict):
            input_df = pd.DataFrame([input_data])
        else:
            input_df = pd.DataFrame(input_data)
        
        # Ensure correct feature order
        feature_columns = model_info.get("feature_columns", input_df.columns.tolist())
        input_df = input_df[feature_columns]
        
        # Make prediction
        predictions = model.predict(input_df)
        
        # Get prediction probabilities if available
        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df).tolist()
        
        return {
            "status": "success",
            "predictions": {
                "model_id": model_id,
                "predictions": predictions.tolist(),
                "probabilities": probabilities,
                "prediction_timestamp": datetime.now().isoformat()
            }
        }