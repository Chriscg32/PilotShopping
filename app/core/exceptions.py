from typing import Optional, Any

class AppException(Exception):
    """Base application exception."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class ValidationException(AppException):
    """Validation error exception."""
    pass

class ConfigurationException(AppException):
    """Configuration error exception."""
    pass

class AgentException(AppException):
    """Agent-related exception."""
    pass