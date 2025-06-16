from typing import Dict, Any, List, Optional
from app.agents import (
    BossAgent, MarketingAgent, CustomerServiceAgent, 
    FinanceAgent, DesignAgent, EngineeringAgent
)
from app.core.logger import get_logger
from app.core.exceptions import AgentException

class AgentService:
    """Service for managing and coordinating agents."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.agents = {}
        self.boss_agent = None
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agents."""
        try:
            # Initialize boss agent
            self.boss_agent = BossAgent()
            self.agents[self.boss_agent.id] = self.boss_agent
            
            # Initialize specialized agents
            agents_to_create = [
                MarketingAgent(),
                CustomerServiceAgent(),
                FinanceAgent(),
                DesignAgent(),
                EngineeringAgent()
            ]
            
            for agent in agents_to_create:
                self.agents[agent.id] = agent
                self.boss_agent.register_agent(agent)
                self.logger.info(f"Initialized {agent.name} agent")
            
            self.logger.info(f"Successfully initialized {len(self.agents)} agents")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {str(e)}")
            raise AgentException(f"Agent initialization failed: {str(e)}")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using appropriate agent."""
        try:
            capability_required = task.get("capability")
            
            if not capability_required:
                return {"error": "No capability specified in task"}
            
            # Find agent with required capability
            suitable_agent = self._find_agent_by_capability(capability_required)
            
            if not suitable_agent:
                return {"error": f"No agent found for capability: {capability_required}"}
            
            # Execute task
            result = await suitable_agent.execute_task(task)
            
            self.logger.info(f"Task executed successfully by {suitable_agent.name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            return {"error": f"Task execution failed: {str(e)}"}
    
    async def delegate_to_boss(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate complex task to boss agent for coordination."""
        if not self.boss_agent:
            return {"error": "Boss agent not available"}
        
        try:
            result = await self.boss_agent.execute_task(task)
            return result
        except Exception as e:
            self.logger.error(f"Boss delegation failed: {str(e)}")
            return {"error": f"Boss delegation failed: {str(e)}"}
    
    def _find_agent_by_capability(self, capability: str) -> Optional[Any]:
        """Find agent that has the required capability."""
        for agent in self.agents.values():
            if capability in agent.capabilities:
                return agent
        return None
    
    def get_all_agents_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return {
            "total_agents": len(self.agents),
            "agents": [agent.get_status() for agent in self.agents.values()],
            "boss_agent_summary": self.boss_agent.get_agent_status_summary() if self.boss_agent else None
        }
    
    def get_agent_by_name(self, name: str) -> Optional[Any]:
        """Get agent by name."""
        for agent in self.agents.values():
            if agent.name == name:
                return agent
        return None
    
    def get_available_capabilities(self) -> List[str]:
        """Get list of all available capabilities."""
        capabilities = set()
        for agent in self.agents.values():
            capabilities.update(agent.capabilities)
        return list(capabilities)