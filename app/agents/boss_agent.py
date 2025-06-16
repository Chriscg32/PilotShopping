from typing import Dict, Any, List
from app.agents.base import BaseAgent
from app.core.logger import get_logger

class BossAgent(BaseAgent):
    """Boss agent responsible for task coordination and delegation."""
    
    def __init__(self):
        super().__init__(
            name="boss",
            capabilities=[
                "task_delegation",
                "agent_coordination", 
                "workflow_management",
                "result_aggregation"
            ]
        )
        self.subordinate_agents = {}
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process coordination tasks."""
        task_type = task.get("type")
        
        if task_type == "delegate":
            return await self._delegate_task(task)
        elif task_type == "coordinate":
            return await self._coordinate_agents(task)
        elif task_type == "aggregate":
            return await self._aggregate_results(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
    
    async def get_capabilities(self) -> List[str]:
        """Get boss agent capabilities."""
        return self.capabilities
    
    async def _delegate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate task to appropriate agent."""
        target_capability = task.get("capability")
        task_data = task.get("data", {})
        
        # Find appropriate agent
        suitable_agents = [
            agent for agent in self.subordinate_agents.values()
            if target_capability in agent.capabilities
        ]
        
        if not suitable_agents:
            return {"error": f"No agent available for capability: {target_capability}"}
        
        # Select first available agent (can be improved with load balancing)
        selected_agent = suitable_agents[0]
        
        try:
            result = await selected_agent.execute_task(task_data)
            return {
                "delegated_to": selected_agent.name,
                "result": result
            }
        except Exception as e:
            return {"error": f"Delegation failed: {str(e)}"}
    
    async def _coordinate_agents(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate multiple agents for complex tasks."""
        workflow = task.get("workflow", [])
        results = []
        
        for step in workflow:
            step_result = await self._delegate_task(step)
            results.append(step_result)
            
            # If any step fails, stop the workflow
            if "error" in step_result:
                break
        
        return {
            "workflow_completed": len(results) == len(workflow),
            "steps_completed": len(results),
            "results": results
        }
    
    async def _aggregate_results(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results from multiple agents."""
        results = task.get("results", [])
        
        # Simple aggregation - can be enhanced based on needs
        successful_results = [r for r in results if r.get("success", False)]
        failed_results = [r for r in results if not r.get("success", False)]
        
        return {
            "total_results": len(results),
            "successful": len(successful_results),
            "failed": len(failed_results),
            "success_rate": len(successful_results) / len(results) if results else 0,
            "aggregated_data": successful_results
        }
    
    def register_agent(self, agent: BaseAgent):
        """Register a subordinate agent."""
        self.subordinate_agents[agent.id] = agent
        self.logger.info(f"Registered agent: {agent.name} ({agent.id})")
    
    def get_agent_status_summary(self) -> Dict[str, Any]:
        """Get status summary of all registered agents."""
        return {
            "total_agents": len(self.subordinate_agents),
            "agents": [agent.get_status() for agent in self.subordinate_agents.values()]
        }