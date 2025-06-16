from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import logging

from agents import AGENT_REGISTRY
from monitoring.agent_monitor import AgentMonitor

app = FastAPI(
    title="Landing Copy Generator API",
    description="Multi-Agent System for Business Automation",
    version="0.4.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
agents = {}
monitor = None

class TaskRequest(BaseModel):
    agent_type: str
    task_type: str
    data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

@app.on_event("startup")
async def startup_event():
    """Initialize agents and monitoring on startup"""
    global agents, monitor
    
    # Initialize agents
    for agent_name, agent_class in AGENT_REGISTRY.items():
        try:
            agent = agent_class()
            agents[agent_name] = agent
            await agent.start()
            logging.info(f"Started {agent_name} agent")
        except Exception as e:
            logging.error(f"Failed to start {agent_name} agent: {e}")
    
    # Initialize monitoring
    monitor = AgentMonitor()
    await monitor.start()
    
    # Start monitoring in background
    asyncio.create_task(monitor.monitor_agents(agents))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Landing Copy Generator API v0.4.0",
        "agents": list(agents.keys()),
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    agent_status = {}
    
    for agent_name, agent in agents.items():
        try:
            health = await agent.health_check()
            agent_status[agent_name] = health.get("status", "unknown")
        except Exception as e:
            agent_status[agent_name] = "error"
    
    return {
        "status": "healthy" if all(status == "healthy" for status in agent_status.values()) else "degraded",
        "agents": agent_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task_request: TaskRequest, background_tasks: BackgroundTasks):
    """Create and execute a task"""
    
    # Validate agent type
    if task_request.agent_type not in agents:
        raise HTTPException(status_code=400, detail=f"Unknown agent type: {task_request.agent_type}")
    
    agent = agents[task_request.agent_type]
    
    # Create task
    task = {
        "type": task_request.task_type,
        "data": task_request.data,
        "config": task_request.config,
        "description": task_request.description
    }
    
    task_id = f"{task_request.agent_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    try:
        # Execute task
        result = await agent.process_task(task)
        
        return TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        return TaskResponse(
            task_id=task_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/agents")
async def list_agents():
    """List all available agents and their capabilities"""
    agent_info = {}
    
    for agent_name, agent in agents.items():
        agent_info[agent_name] = {
            "capabilities": getattr(agent, 'capabilities', []),
            "status": "active"
        }
    
    return agent_info

@app.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """Get status of specific agent"""
    if agent_name not in agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    agent = agents[agent_name]
    
    try:
        health = await agent.health_check()
        return health
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/monitoring/metrics")
async def get_monitoring_metrics():
    """Get monitoring metrics for all agents"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitoring not available")
    
    return await monitor.get_agent_status()

@app.get("/monitoring/alerts")
async def get_alerts():
    """Get current alerts"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitoring not available")
    
    return {"alerts": monitor.alerts}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)