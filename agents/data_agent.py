import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import sqlite3
import json
from datetime import datetime, timedelta
import asyncio
from .base_agent import BaseAgent

class DataAgent(BaseAgent):
    """Advanced data processing and analytics agent"""
    
    def __init__(self, agent_id: str = "data_agent"):
        super().__init__(agent_id)
        self.capabilities = [
            "data_processing",
            "analytics",
            "data_visualization",
            "etl_operations",
            "data_quality_checks",
            "reporting"
        ]
        self.db_connections = {}
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process data-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "analyze_data":
                return await self._analyze_data(task.get("data"), task.get("analysis_type"))
            elif task_type == "generate_report":
                return await self._generate_report(task.get("data_source"), task.get("report_config"))
            elif task_type == "data_quality_check":
                return await self._check_data_quality(task.get("dataset"))
            elif task_type == "etl_process":
                return await self._run_etl_process(task.get("source"), task.get("destination"), task.get("transformations"))
            elif task_type == "create_visualization":
                return await self._create_visualization(task.get("data"), task.get("chart_type"))
            else:
                return {"status": "error", "message": f"Unknown task type: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Error processing data task: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _analyze_data(self, data: Any, analysis_type: str) -> Dict[str, Any]:
        """Perform data analysis"""
        if isinstance(data, str):
            # Assume it's a file path or SQL query
            df = pd.read_csv(data) if data.endswith('.csv') else pd.read_sql(data, self.db_connections.get('default'))
        else:
            df = pd.DataFrame(data)
        
        results = {}
        
        if analysis_type == "descriptive":
            results = {
                "summary_stats": df.describe().to_dict(),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "shape": df.shape
            }
        elif analysis_type == "correlation":
            numeric_df = df.select_dtypes(include=[np.number])
            results = {"correlation_matrix": numeric_df.corr().to_dict()}
        elif analysis_type == "trend":
            # Assuming time series data
            results = await self._analyze_trends(df)
        
        return {"status": "success", "analysis": results}
    
    async def _generate_report(self, data_source: str, config: Dict) -> Dict[str, Any]:
        """Generate analytical reports"""
        report = {
            "title": config.get("title", "Data Analysis Report"),
            "generated_at": datetime.now().isoformat(),
            "sections": []
        }
        
        # Add different sections based on config
        for section in config.get("sections", []):
            if section["type"] == "summary":
                report["sections"].append(await self._create_summary_section(data_source))
            elif section["type"] == "charts":
                report["sections"].append(await self._create_charts_section(data_source, section.get("charts", [])))
        
        return {"status": "success", "report": report}
    
    async def _check_data_quality(self, dataset: Any) -> Dict[str, Any]:
        """Perform data quality checks"""
        df = pd.DataFrame(dataset) if not isinstance(dataset, pd.DataFrame) else dataset
        
        quality_report = {
            "completeness": (1 - df.isnull().sum() / len(df)).to_dict(),
            "duplicates": df.duplicated().sum(),
            "data_types_consistency": self._check_data_types(df),
            "outliers": self._detect_outliers(df),
            "quality_score": 0.0
        }
        
        # Calculate overall quality score
        completeness_avg = np.mean(list(quality_report["completeness"].values()))
        duplicate_penalty = min(quality_report["duplicates"] / len(df), 0.2)
        quality_report["quality_score"] = max(0, completeness_avg - duplicate_penalty)
        
        return {"status": "success", "quality_report": quality_report}
    
    def _check_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data type consistency"""
        issues = {}
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if numeric data is stored as string
                try:
                    pd.to_numeric(df[col].dropna())
                    issues[col] = "numeric_as_string"
                except:
                    pass
        return issues
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, List]:
        """Detect outliers using IQR method"""
        outliers = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_indices = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
            if outlier_indices:
                outliers[col] = outlier_indices
        
        return outliers