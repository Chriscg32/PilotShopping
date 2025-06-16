from functools import lru_cache
from app.services.agent_service import AgentService
from app.services.communication_service import CommunicationService

# Global service instances
_agent_service = None
_communication_service = None

@lru_cache()
def get_agent_service() -> AgentService:
    """Get agent service instance."""
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service

@lru_cache()
def get_communication_service() -> CommunicationService:
    """Get communication service instance."""
    global _communication_service
    if _communication_service is None:
        _communication_service = CommunicationService()
    return _communication_service

async def startup_services():
    """Initialize services on startup."""
    # Initialize agent service
    agent_service = get_agent_service()
    
    # Initialize and start communication service
    comm_service = get_communication_service()
    await comm_service.start()

async def shutdown_services():
    """Cleanup services on shutdown."""
    comm_service = get_communication_service()
    await comm_service.stop()