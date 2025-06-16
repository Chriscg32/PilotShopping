from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.dependencies import get_agent_service
from app.services.agent_service import AgentService

router = APIRouter()

@router.get("/")
async def list_agents(agent_service: AgentService = Depends(get_agent_service)):
    """List all available agents and their status."""
    try:
        return agent_service.get_all_agents_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agents: {str(e)}")

@router.get("/capabilities")
async def list_capabilities(agent_service: AgentService = Depends(get_agent_service)):
    """List all available capabilities."""
    try:
        capabilities = agent_service.get_available_capabilities()
        return {
            "capabilities": capabilities,
            "total_count": len(capabilities)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {str(e)}")

@router.get("/{agent_name}")
async def get_agent_details(
    agent_name: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Get details of a specific agent."""
    try:
        agent = agent_service.get_agent_by_name(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        return agent.get_status()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent details: {str(e)}")

@router.get("/{agent_name}/capabilities")
async def get_agent_capabilities(
    agent_name: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Get capabilities of a specific agent."""
    try:
        agent = agent_service.get_agent_by_name(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        capabilities = await agent.get_capabilities()
        return {
            "agent_name": agent_name,
            "capabilities": capabilities,
            "capability_count": len(capabilities)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent capabilities: {str(e)}")