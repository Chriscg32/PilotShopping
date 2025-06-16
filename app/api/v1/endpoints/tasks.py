from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.core.dependencies import get_agent_service
from app.services.agent_service import AgentService

router = APIRouter()

@router.post("/execute")
async def execute_task(
    task: Dict[str, Any],
    agent_service: AgentService = Depends(get_agent_service)
):
    """Execute a task using appropriate agent."""
    try:
        if not task.get("capability"):
            raise HTTPException(status_code=400, detail="Task must specify required capability")
        
        result = await agent_service.execute_task(task)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Task executed successfully",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")

@router.post("/delegate")
async def delegate_task(
    task: Dict[str, Any],
    agent_service: AgentService = Depends(get_agent_service)
):
    """Delegate complex task to boss agent."""
    try:
        # Add delegation type to task
        task["type"] = "delegate"
        
        result = await agent_service.delegate_to_boss(task)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Task delegated successfully",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task delegation failed: {str(e)}")

@router.get("/examples")
async def get_task_examples():
    """Get example tasks for different capabilities."""
    examples = {
        "marketing": {
            "landing_page_copy": {
                "type": "generate_landing_copy",
                "capability": "landing_page_copy",
                "business_type": "SaaS",
                "target_audience": "small businesses",
                "tone": "professional",
                "key_features": ["automation", "analytics", "integration"]
            },
            "social_media_content": {
                "type": "create_social_content",
                "capability": "social_media_content",
                "platform": "twitter",
                "message": "Launch announcement for new product"
            }
        },
        "design": {
            "ui_design": {
                "type": "create_design",
                "capability": "ui_design",
                "design_type": "landing_page",
                "style": "professional"
            },
            "color_palette": {
                "type": "generate_palette",
                "capability": "color_palette",
                "theme": "professional"
            }
        },
        "engineering": {
            "code_generation": {
                "type": "generate_code",
                "capability": "code_generation",
                "component_type": "component",
                "framework": "react"
            },
            "api_development": {
                "type": "create_api",
                "capability": "api_development",
                "api_name": "user_api",
                "endpoints": ["users", "auth"]
            }
        },
        "finance": {
            "payment_processing": {
                "type": "process_payment",
                "capability": "payment_processing",
                "payment": {
                    "amount": 100.00,
                    "currency": "USD",
                    "method": "card"
                }
            },
            "invoice_generation": {
                "type": "generate_invoice",
                "capability": "invoice_generation",
                "invoice": {
                    "customer": {"name": "John Doe", "email": "john@example.com"},
                    "items": [{"name": "Service", "price": 100, "quantity": 1}]
                }
            }
        },
        "customer_service": {
            "ticket_management": {
                "type": "handle_ticket",
                "capability": "ticket_management",
                "ticket": {
                    "message": "I need help with billing",
                    "priority": "normal",
                    "category": "billing"
                }
            }
        }
    }
    
    return {
        "examples": examples,
        "usage": "Use these examples as templates for your tasks"
    }