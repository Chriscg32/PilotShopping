-- Initialize ButterflyBlue Database
-- This script runs automatically when the container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'offline',
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tasks_completed INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id),
    task_type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    result JSONB
);

-- Insert default agents
INSERT INTO agents (name, type, status) VALUES
    ('boss', 'coordinator', 'online'),
    ('marketing', 'marketing', 'online'),
    ('finance', 'finance', 'online'),
    ('customer-service', 'support', 'online'),
    ('engineering', 'development', 'online'),
    ('design', 'creative', 'online')
ON CONFLICT DO NOTHING;

-- Create a demo user (password: demo123)
INSERT INTO users (email, username, password_hash) VALUES
    ('demo@butterflyblue.co.za', 'demo', crypt('demo123', gen_salt('bf')))
ON CONFLICT DO NOTHING;

-- Grant all permissions to the application user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO butterflyblue_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO butterflyblue_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO butterflyblue_user;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(type);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
