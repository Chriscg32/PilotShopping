from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import GenerateRequest
from app.schemas.responses import GenerateResponse
from app.core.dependencies import get_agent_service
from app.services.agent_service import AgentService

router = APIRouter()

@router.post("/landing-copy", response_model=GenerateResponse)
async def generate_landing_copy(
    request: GenerateRequest,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Generate landing page copy using marketing agent."""
    try:
        # Prepare task for marketing agent
        task = {
            "type": "generate_landing_copy",
            "capability": "landing_page_copy",
            "business_type": request.business_type,
            "target_audience": request.target_audience,
            "tone": request.tone,
            "key_features": request.key_features
        }
        
        # Execute task
        result = await agent_service.execute_task(task)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GenerateResponse(
            success=True,
            message="Landing copy generated successfully",
            data=result.get("result", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/social-content")
async def generate_social_content(
    platform: str,
    message: str,
    agent_service: AgentService = Depends(get_agent_service)
):
    """Generate social media content."""
    try:
        task = {
            "type": "create_social_content",
            "capability": "social_media_content",
            "platform": platform,
            "message": message
        }
        
        result = await agent_service.execute_task(task)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GenerateResponse(
            success=True,
            message="Social content generated successfully",
            data=result.get("result", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/design")
async def generate_design(
    design_type: str,
    style: str = "professional",
    agent_service: AgentService = Depends(get_agent_service)
):
    """Generate design specifications."""
    try:
        task = {
            "type": "create_design",
            "capability": "ui_design",
            "design_type": design_type,
            "style": style
        }
        
        result = await agent_service.execute_task(task)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GenerateResponse(
            success=True,
            message="Design generated successfully",
            data=result.get("result", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Design generation failed: {str(e)}")