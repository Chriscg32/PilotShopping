import os
from typing import Dict, Any

# Agent-specific configurations
AGENT_CONFIGS = {
    "data_agent": {
        "max_dataset_size": os.getenv("DATA_AGENT_MAX_SIZE", "100MB"),
        "supported_formats": ["csv", "json", "parquet", "xlsx"],
        "cache_results": os.getenv("DATA_AGENT_CACHE", "true").lower() == "true",
        "cache_ttl": int(os.getenv("DATA_AGENT_CACHE_TTL", "3600")),
        "visualization_backend": os.getenv("VIZ_BACKEND", "matplotlib"),
        "max_concurrent_analyses": int(os.getenv("DATA_AGENT_MAX_CONCURRENT", "3"))
    },
    "security_agent": {
        "token_expiry_hours": int(os.getenv("TOKEN_EXPIRY_HOURS", "24")),
        "encryption_algorithm": os.getenv("ENCRYPTION_ALGO", "Fernet"),
        "audit_log_retention": int(os.getenv("AUDIT_RETENTION_DAYS", "90")),
        "vulnerability_scan_frequency": os.getenv("VULN_SCAN_FREQ", "daily"),
        "max_token_length": int(os.getenv("MAX_TOKEN_LENGTH", "1024")),
        "security_level": os.getenv("SECURITY_LEVEL", "high")
    },
    "devops_agent": {
        "supported_platforms": os.getenv("DEVOPS_PLATFORMS", "docker,kubernetes,aws").split(","),
        "deployment_timeout": int(os.getenv("DEPLOYMENT_TIMEOUT", "600")),
        "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
        "backup_retention": int(os.getenv("BACKUP_RETENTION_DAYS", "30")),
        "max_concurrent_deployments": int(os.getenv("MAX_CONCURRENT_DEPLOYMENTS", "2")),
        "docker_registry": os.getenv("DOCKER_REGISTRY", "docker.io")
    },
    "aiml_agent": {
        "model_storage_path": os.getenv("MODEL_STORAGE_PATH", "./models"),
        "max_training_time": int(os.getenv("MAX_TRAINING_TIME", "3600")),
        "supported_algorithms": os.getenv("ML_ALGORITHMS", "rf,lr,svm,nn").split(","),
        "auto_hyperparameter_tuning": os.getenv("AUTO_HYPERPARAMS", "true").lower() == "true",
        "max_model_size": os.getenv("MAX_MODEL_SIZE", "500MB"),
        "gpu_enabled": os.getenv("GPU_ENABLED", "false").lower() == "true"
    }
}

# Global system configuration
SYSTEM_CONFIG = {
    "mqtt_broker": os.getenv("MQTT_BROKER", "localhost"),
    "mqtt_port": int(os.getenv("MQTT_PORT", "1883")),
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379"),
    "database_url": os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/landing_copy_generator"),
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "environment": os.getenv("ENVIRONMENT", "development"),
    "max_task_queue_size": int(os.getenv("MAX_TASK_QUEUE_SIZE", "1000")),
    "task_timeout": int(os.getenv("TASK_TIMEOUT", "300"))
}

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for specific agent"""
    return AGENT_CONFIGS.get(agent_name, {})

def get_system_config() -> Dict[str, Any]:
    """Get system-wide configuration"""
    return SYSTEM_CONFIG