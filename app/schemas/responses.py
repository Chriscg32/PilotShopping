from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List

class BaseResponse(BaseModel):
    """Base response schema."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")

class GenerateResponse(BaseResponse):
    """Response schema for content generation."""
    data: Dict[str, Any] = Field(default={}, description="Generated content data")

class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Service status")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment")

class AgentStatusResponse(BaseModel):
    """Agent status response schema."""
    agent_id: str = Field(..., description="Agent ID")
    name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Agent status")
    capabilities: List[str] = Field(..., description="Agent capabilities")
    tasks_completed: int = Field(..., description="Number of completed tasks")

class TaskResponse(BaseResponse):
    """Task execution response schema."""
    task_id: Optional[str] = Field(None, description="Task ID")
    result: Dict[str, Any] = Field(default={}, description="Task result")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")