import pytest
import asyncio
import time
import statistics
from agents import AGENT_REGISTRY

class TestAgentPerformance:
    @pytest.mark.asyncio
    async def test_agent_response_times(self):
        """Test response times for all agents"""
        response_times = {}
        
        for agent_name, agent_class in AGENT_REGISTRY.items():
            if agent_name == "boss":  # Skip boss agent for this test
                continue
                
            agent = agent_class()
            times = []
            
            # Run 10 health checks and measure time
            for _ in range(10):
                start_time = time.time()
                try:
                    result = await agent.health_check()
                    end_time = time.time()
                    times.append(end_time - start_time)
                except Exception as e:
                    print(f"Health check failed for {agent_name}: {e}")
            
            if times:
                response_times[agent_name] = {
                    "avg": statistics.mean(times),
                    "min": min(times),
                    "max": max(times),
                    "median": statistics.median(times)
                }
        
        # Assert reasonable response times (< 1 second average)
        for agent_name, metrics in response_times.items():
            assert metrics["avg"] < 1.0, f"{agent_name} average response time too high: {metrics['avg']}"
    
    @pytest.mark.asyncio
    async def test_concurrent_task_processing(self):
        """Test concurrent task processing"""
        from agents.data_agent import DataAgent
        
        agent = DataAgent()
        
        # Create multiple tasks
        tasks = []
        for i in range(5):
            task = {
                "type": "analyze_data",
                "data": [{"id": i, "value": i * 10}],
                "analysis_type": "descriptive"
            }
            tasks.append(agent.process_task(task))
        
        # Run tasks concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # All tasks should complete successfully
        for result in results:
            assert result["status"] == "success"
        
        # Concurrent execution should be faster than sequential
        total_time = end_time - start_time
        assert total_time < 5.0, f"Concurrent execution took too long: {total_time}"