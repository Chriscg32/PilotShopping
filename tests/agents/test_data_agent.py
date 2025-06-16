import pytest
import pandas as pd
from agents.data_agent import DataAgent

class TestDataAgent:
    @pytest.fixture
    def data_agent(self):
        return DataAgent()
    
    @pytest.mark.asyncio
    async def test_analyze_data_descriptive(self, data_agent, sample_data):
        task = {
            "type": "analyze_data",
            "data": sample_data["customers"],
            "analysis_type": "descriptive"
        }
        
        result = await data_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "analysis" in result
        assert "summary_stats" in result["analysis"]
        assert "data_types" in result["analysis"]
        assert "missing_values" in result["analysis"]
    
    @pytest.mark.asyncio
    async def test_analyze_data_correlation(self, data_agent, sample_data):
        task = {
            "type": "analyze_data",
            "data": sample_data["customers"],
            "analysis_type": "correlation"
        }
        
        result = await data_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "correlation_matrix" in result["analysis"]
    
    @pytest.mark.asyncio
    async def test_data_quality_check(self, data_agent, sample_data):
        # Add some missing values for testing
        test_data = sample_data["customers"].copy()
        test_data.append({"id": 4, "name": None, "age": 40, "purchase_amount": None})
        
        task = {
            "type": "data_quality_check",
            "dataset": test_data
        }
        
        result = await data_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "quality_report" in result
        assert "completeness" in result["quality_report"]
        assert "duplicates" in result["quality_report"]
        assert "quality_score" in result["quality_report"]
    
    @pytest.mark.asyncio
    async def test_generate_report(self, data_agent, sample_csv_file):
        task = {
            "type": "generate_report",
            "data_source": sample_csv_file,
            "report_config": {
                "title": "Customer Analysis Report",
                "sections": [
                    {"type": "summary"},
                    {"type": "charts", "charts": ["bar", "line"]}
                ]
            }
        }
        
        result = await data_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "report" in result
        assert result["report"]["title"] == "Customer Analysis Report"
    
    @pytest.mark.asyncio
    async def test_invalid_task_type(self, data_agent):
        task = {"type": "invalid_task"}
        
        result = await data_agent.process_task(task)
        
        assert result["status"] == "error"
        assert "Unknown task type" in result["message"]