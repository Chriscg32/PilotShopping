from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateRequest(BaseModel):
    """Request schema for content generation."""
    business_type: str = Field(..., description="Type of business")
    target_audience: str = Field(..., description="Target audience description")
    tone: str = Field(default="professional", description="Tone of the content")
    key_features: List[str] = Field(default=[], description="Key features to highlight")

class TaskRequest(BaseModel):
    """Request schema for task execution."""
    capability: str = Field(..., description="Required capability")
    task_type: str = Field(..., description="Type of task")
    parameters: dict = Field(default={}, description="Task parameters")

class AgentTaskRequest(BaseModel):
    """Request schema for agent-specific tasks."""
    agent_name: str = Field(..., description="Target agent name")
    task: dict = Field(..., description="Task details")