import asyncio
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.core.logger import get_logger
from app.core.exceptions import AgentException

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, capabilities: List[str]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.capabilities = capabilities
        self.status = "idle"
        self.created_at = datetime.utcnow()
        self.logger = get_logger(f"agent.{name}")
        self.tasks_completed = 0
        self.tasks_failed = 0
        
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task assigned to this agent."""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> List[str]:
        """Get list of capabilities this agent can handle."""
        pass
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task with error handling and logging."""
        task_id = task.get("id", str(uuid.uuid4()))
        self.logger.info(f"Starting task {task_id}")
        
        try:
            self.status = "working"
            result = await self.process_task(task)
            
            self.tasks_completed += 1
            self.status = "idle"
            
            self.logger.info(f"Completed task {task_id}")
            
            return {
                "success": True,
                "task_id": task_id,
                "agent_id": self.id,
                "agent_name": self.name,
                "result": result,
                "completed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.tasks_failed += 1
            self.status = "error"
            self.logger.error(f"Failed task {task_id}: {str(e)}")
            
            raise AgentException(f"Task execution failed: {str(e)}", {
                "task_id": task_id,
                "agent_id": self.id,
                "agent_name": self.name
            })
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "capabilities": self.capabilities,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "created_at": self.created_at.isoformat(),
            "uptime": (datetime.utcnow() - self.created_at).total_seconds()
        }