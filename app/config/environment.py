import os
import sys
import platform
from typing import Dict, Any
from app.config.settings import settings

def get_environment_info() -> Dict[str, Any]:
    """Get comprehensive environment information."""
    return {
        "app": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "debug": settings.debug,
        },
        "system": {
            "platform": platform.platform(),
            "python_version": sys.version,
            "architecture": platform.architecture()[0],
        },
        "api_keys": {
            "openai_configured": bool(settings.openai_api_key),
            "paystack_configured": bool(settings.paystack_secret_key),
            "paypal_configured": bool(settings.paypal_client_id and settings.paypal_client_secret),
        },
        "services": {
            "mqtt_configured": bool(settings.mqtt_broker_host),
            "database_configured": bool(settings.database_url),
        }
    }

def validate_environment() -> Dict[str, bool]:
    """Validate that required environment variables are set."""
    validations = {
        "basic_config": True,  # Always true for basic setup
        "openai_ready": bool(settings.openai_api_key),
        "payment_ready": bool(settings.paystack_secret_key or (settings.paypal_client_id and settings.paypal_client_secret)),
        "mqtt_ready": bool(settings.mqtt_broker_host),
    }
    
    return validations