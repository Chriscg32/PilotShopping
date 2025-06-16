import logging
import sys
from typing import Optional
from app.config.settings import settings

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        # Create handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(settings.log_format)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    return logger

# Create default logger
logger = get_logger("app")