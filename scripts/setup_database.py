#!/usr/bin/env python3

import asyncio
import asyncpg
import logging
import os
from datetime import datetime

# Database setup script for Landing Copy Generator v0.4.0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:password@localhost:5432/landing_copy_generator"
)

async def setup_database():
    """Setup database tables and initial data"""
    
    logger.info("🗄️  Setting up database...")
    
    try:
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        logger.info("✅ Connected to database")
        
        # Create tables
        await create_tables(conn)
        
        # Insert initial data
        await insert_initial_data(conn)
        
        # Close connection
        await conn.close()
        logger.info("✅ Database setup completed")
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        raise

async def create_tables(conn):
    """Create necessary database tables"""
    
    logger.info("📋 Creating database tables...")
    
    # Agent metrics table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_metrics (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL,
            task_count INTEGER DEFAULT 0,
            error_count INTEGER DEFAULT 0,
            response_time FLOAT DEFAULT 0.0,
            memory_usage FLOAT DEFAULT 0.0,
            cpu_usage FLOAT DEFAULT 0.0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tasks table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_id VARCHAR(100) UNIQUE NOT NULL,
            agent_name VARCHAR(50) NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL,
            data JSONB,
            result JSONB,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)
    
    # Alerts table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            alert_type VARCHAR(50) NOT NULL,
            agent_name VARCHAR(50) NOT NULL,
            severity VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            data JSONB,
            resolved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP
        )
    """)
    
    # Agent configurations table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_configs (
            id SERIAL PRIMARY KEY,
            agent_name VARCHAR(50) UNIQUE NOT NULL,
            config JSONB NOT NULL,
            version VARCHAR(20) NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User sessions table (for API authentication)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100) UNIQUE NOT NULL,
            user_id VARCHAR(50) NOT NULL,
            token_hash VARCHAR(255) NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for better performance
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent_name ON agent_metrics(agent_name)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_agent_metrics_timestamp ON agent_metrics(timestamp)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_agent_name ON tasks(agent_name)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_agent_name ON alerts(agent_name)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved)")
    
    logger.info("✅ Database tables created successfully")

async def insert_initial_data(conn):
    """Insert initial configuration data"""
    
    logger.info("📝 Inserting initial data...")
    
    # Initial agent configurations
    agent_configs = [
        {
            "agent_name": "data",
            "config": {
                "max_dataset_size": "100MB",
                "supported_formats": ["csv", "json", "parquet", "xlsx"],
                "cache_results": True,
                "cache_ttl": 3600
            },
            "version": "0.4.0"
        },
        {
            "agent_name": "security",
            "config": {
                "token_expiry_hours": 24,
                "encryption_algorithm": "Fernet",
                "audit_log_retention": 90,
                "security_level": "high"
            },
            "version": "0.4.0"
        },
        {
            "agent_name": "devops",
            "config": {
                "supported_platforms": ["docker", "kubernetes", "aws"],
                "deployment_timeout": 600,
                "health_check_interval": 30,
                "backup_retention": 30
            },
            "version": "0.4.0"
        },
        {
            "agent_name": "aiml",
            "config": {
                "model_storage_path": "./models",
                "max_training_time": 3600,
                "supported_algorithms": ["rf", "lr", "svm", "nn"],
                "auto_hyperparameter_tuning": True
            },
            "version": "0.4.0"
        }
    ]
    
    for config in agent_configs:
        await conn.execute("""
            INSERT INTO agent_configs (agent_name, config, version)
            VALUES ($1, $2, $3)
            ON CONFLICT (agent_name) DO UPDATE SET
                config = EXCLUDED.config,
                version = EXCLUDED.version,
                updated_at = CURRENT_TIMESTAMP
        """, config["agent_name"], config["config"], config["version"])
    
    logger.info("✅ Initial data inserted successfully")

if __name__ == "__main__":
    asyncio.run(setup_database())