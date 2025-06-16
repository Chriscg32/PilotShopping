#!/usr/bin/env python3
"""
ButterflyBlue Creations - Main Application Entry Point
Multi-Agent AI Business Automation Platform
"""

import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime
from typing import Dict, Any
import json

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/butterflyblue.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import agent classes
from agents.finance_agent import FinanceAgent # Assuming full FinanceAgent should be used
from agents.data_agent import DataAgent
from agents.security_agent import SecurityAgent
from agents.devops_agent import DevOpsAgent
from agents.aiml_agent import AIMLAgent
# Simple Agent Base Class
class SimpleAgent:
    def __init__(self, name: str):
        self.name = name
        self.capabilities = []
        self.logger = logging.getLogger(f"agent.{name}")
    
    async def initialize(self):
        self.logger.info(f"🤖 {self.name.title()} Agent initializing...")
        await asyncio.sleep(0.1)  # Simulate initialization
        self.logger.info(f"✅ {self.name.title()} Agent ready!")
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"📋 Processing task: {task_data.get('type', 'unknown')}")
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        return {
            "task_id": f"{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "agent": self.name,
            "result": f"Task processed successfully by {self.name} agent",
            "timestamp": datetime.now().isoformat()
        }
    
    async def cleanup(self):
        self.logger.info(f"🧹 {self.name.title()} Agent cleaning up...")

# Initialize agents
boss_agent = SimpleAgent("boss")
marketing_agent = SimpleAgent("marketing")
# finance_agent = SimpleAgent("finance") # Using full FinanceAgent below
finance_agent = FinanceAgent() # Instantiate the full FinanceAgent
engineering_agent = SimpleAgent("engineering")
design_agent = SimpleAgent("design")
customer_service_agent = SimpleAgent("customer_service")

# Initialize new agents
data_agent = DataAgent(agent_id="data")
security_agent = SecurityAgent(agent_id="security")
devops_agent = DevOpsAgent(agent_id="devops")
aiml_agent = AIMLAgent(agent_id="aiml")
# Set capabilities
marketing_agent.capabilities = ["campaign_creation", "social_media", "email_marketing", "analytics"]
finance_agent.capabilities = ["payment_processing", "invoicing", "financial_analysis", "reporting"]
engineering_agent.capabilities = ["code_generation", "api_development", "testing", "deployment"]
design_agent.capabilities = ["ui_design", "branding", "logo_creation", "responsive_design"]
customer_service_agent.capabilities = ["ticket_management", "chat_support", "knowledge_base", "escalation"]
boss_agent.capabilities = ["task_coordination", "agent_management", "workflow_optimization"]
# New agent capabilities are set within their class definitions.
# data_agent.capabilities = [...] # Already set in DataAgent class
# security_agent.capabilities = [...] # Already set in SecurityAgent class
# devops_agent.capabilities = [...] # Already set in DevOpsAgent class
# aiml_agent.capabilities = [...] # Already set in AIMLAgent class

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("🦋 ButterflyBlue Creations - Starting up...")
    
    # Initialize all agents
    agents = [
        boss_agent, marketing_agent, finance_agent, engineering_agent, design_agent, customer_service_agent,
        data_agent, security_agent, devops_agent, aiml_agent
    ]
    
    for agent in agents:
        try:
            await agent.initialize()
        except Exception as e:
            logger.error(f"❌ Failed to initialize {agent.name} agent: {e}")
    
    logger.info("🚀 ButterflyBlue Creations is ready!")
    
    yield
    
    # Shutdown
    logger.info("🦋 ButterflyBlue Creations - Shutting down...")
    
    # Cleanup agents
    for agent in agents:
        try:
            await agent.cleanup()
        except Exception as e:
            logger.error(f"Error cleaning up {agent.name} agent: {e}")
    
    logger.info("👋 ButterflyBlue Creations - Shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="ButterflyBlue Creations",
    description="AI-Powered Multi-Agent Business Automation Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directory and mount static files
os.makedirs('static', exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ButterflyBlue Creations",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with welcome message."""
    return {
        "message": "🦋 Welcome to ButterflyBlue Creations!",
        "description": "AI-Powered Multi-Agent Business Automation Platform",
        "version": "1.0.0",
        "agents": {
            "boss": "Central coordination and task management",
            "marketing": "Digital marketing automation",
            "finance": "Payment processing and financial analysis", 
            "engineering": "Full-stack development automation",
            "design": "UI/UX design and branding",
            "customer_service": "Automated customer support",
            "data": "Advanced data processing and analytics",
            "security": "Security monitoring and compliance",
            "devops": "Infrastructure management and CI/CD",
            "aiml": "Machine learning model training and deployment"
        },
        "endpoints": {
            "health": "/health",
            "agents": "/api/agents/",
            "tasks": "/api/tasks/",
            "web_app": "/app",
            "documentation": "/docs"
        }
    }

# Web app endpoint
@app.get("/app")
async def web_app():
    """Serve the web application."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🦋 ButterflyBlue Creations</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 40px; }
        .header h1 { font-size: 3rem; margin-bottom: 10px; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .agents-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px; margin-bottom: 40px;
        }
        .agent-card {
            background: white; border-radius: 15px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease;
        }
        .agent-card:hover { transform: translateY(-5px); }
        .agent-card h3 { color: #667eea; margin-bottom: 15px; font-size: 1.5rem; }
        .agent-card p { color: #666; margin-bottom: 15px; line-height: 1.6; }
        .capabilities { display: flex; flex-wrap: wrap; gap: 8px; }
        .capability {
            background: #f0f2ff; color: #667eea; padding: 5px 12px;
            border-radius: 20px; font-size: 0.9rem;
        }
        .demo-section {
            background: white; border-radius: 15px; padding: 30px; margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .demo-buttons {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px; margin-top: 20px;
        }
        .demo-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; padding: 15px 25px; border-radius: 10px;
            font-size: 1rem; cursor: pointer; transition: all 0.3s ease;
        }
        .demo-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .result-area {
            background: #f8f9ff; border-radius: 10px; padding: 20px; margin-top: 20px;
            min-height: 100px; font-family: 'Courier New', monospace; white-space: pre-wrap;
            overflow-x: auto; max-height: 400px; overflow-y: auto;
        }
        .loading { text-align: center; color: #667eea; font-style: italic; }
        .footer { text-align: center; color: white; margin-top: 40px; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦋 ButterflyBlue Creations</h1>
            <p>AI-Powered Multi-Agent Business Automation Platform</p>
        </div>
        <div class="agents-grid" id="agentsGrid"></div>
        <div class="demo-section">
            <h2>🚀 Try Our AI Agents</h2>
            <p>Click the buttons below to see our AI agents in action!</p>
            <div class="demo-buttons">
                <button class="demo-btn" onclick="runDemo('marketing')">📈 Create Marketing Campaign</button>
                <button class="demo-btn" onclick="runDemo('design')">🎨 Design Website</button>
                <button class="demo-btn" onclick="runDemo('finance')">💰 Financial Analysis</button>
                <button class="demo-btn" onclick="runDemo('engineering')">⚙️ Engineering Task</button>
            </div>
            <div class="result-area" id="resultArea">Click a button above to see AI magic happen! ✨</div>
        </div>
        <div class="footer">
            <p>🦋 Transforming businesses with AI-powered automation</p>
            <p>Built with FastAPI • Powered by AI • Made with ❤️</p>
        </div>
    </div>
    <script>
        window.onload = function() { loadAgents(); };
        async function loadAgents() {
            try {
                const response = await fetch('/api/agents');
                const agents = await response.json();
                const agentsGrid = document.getElementById('agentsGrid');
                agentsGrid.innerHTML = '';
                const agentDescriptions = {
                    boss: 'Central coordination and task management across all agents',
                    marketing: 'Digital marketing automation, campaigns, and analytics',
                    finance: 'Payment processing, invoicing, and financial analysis',
                    engineering: 'Full-stack development, APIs, and deployment automation',
                    design: 'UI/UX design, branding, and creative asset generation',
                    customer_service: 'Automated customer support and ticket management',
                    data: 'Advanced data processing, analytics, and reporting',
                    security: 'Vulnerability scanning, encryption, and compliance checks',
                    devops: 'Container management, CI/CD pipelines, and infrastructure automation',
                    aiml: 'Model training, prediction services, and AI/ML workflows'
                };
                for (const [name, info] of Object.entries(agents)) {
                    const agentCard = document.createElement('div');
                    agentCard.className = 'agent-card';                    
                    const capabilities = info.capabilities.map(cap => 
                        `<span class="capability">${cap.replace(/_/g, ' ')}</span>`
                    ).join('');
                    agentCard.innerHTML = `
                        <h3>🤖 ${name.charAt(0).toUpperCase() + name.slice(1).replace('_', ' ')} Agent</h3>
                        <p>${agentDescriptions[name] || 'Specialized AI agent for business automation'}</p>
                        <div class="capabilities">${capabilities}</div>
                    `;
                    agentsGrid.appendChild(agentCard);
                }
            } catch (error) { console.error('Error loading agents:', error); }
        }
        async function runDemo(type) {
            const resultArea = document.getElementById('resultArea');
            resultArea.innerHTML = '<div class="loading">🤖 AI Agent working... Please wait...</div>';
            try {
                let endpoint;
                switch(type) {
                    case 'marketing': endpoint = '/api/demo/marketing-campaign'; break;
                    case 'design': endpoint = '/api/demo/website-design'; break;
                    case 'finance': endpoint = '/api/demo/financial-analysis'; break;
                    case 'engineering': endpoint = '/api/agents/engineering/task'; break;
                    // Add demo cases for new agents if specific demo endpoints are created
                    // For now, they can be tested via the generic /api/agents/{agent_name}/task
                    default: resultArea.innerHTML = `ℹ️ Demo for ${type} agent not yet implemented in this UI.`; return;
                }
                const response = await fetch(endpoint, { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' },
                    body: type === 'engineering' ? JSON.stringify({type: 'code_generation'}) : undefined
                });
                const result = await response.json();
                resultArea.innerHTML = `✅ Success!\\n\\n${JSON.stringify(result, null, 2)}`;
            } catch (error) {
                resultArea.innerHTML = `❌ Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)

# Endpoint to get list of agents and their capabilities
@app.get("/api/agents")
async def get_agents_list():
    """Get a list of all available agents and their capabilities."""
    all_agents_instances = [
        boss_agent, marketing_agent, finance_agent, engineering_agent, design_agent, 
        customer_service_agent, data_agent, security_agent, devops_agent, aiml_agent
    ]
    agents_info = {}
    for agent_instance in all_agents_instances:
        # Ensure agent_instance.name is the short key like "boss", "data"
        # SimpleAgent uses 'name', new agents use 'agent_id' which becomes 'name' via BaseAgent (assumed)
        # or we directly use the agent_id if it's set as the .name attribute.
        # For consistency, let's assume agent_instance.name holds the correct key.
        # If agent_id is "data_agent", we might want the key to be "data".
        # The current SimpleAgent("boss") has agent_instance.name = "boss".
        # The new agents DataAgent(agent_id="data") should also have agent_instance.name = "data".
        agents_info[agent_instance.name] = {
            "capabilities": agent_instance.capabilities
        }
    return agents_info

# Agent endpoints
@app.post("/api/agents/{agent_name}/task")
async def create_agent_task(agent_name: str, task_data: dict):
    """Create a task for a specific agent."""
    agents_map = {
        "boss": boss_agent, "marketing": marketing_agent, "finance": finance_agent,
        "engineering": engineering_agent, "design": design_agent, "customer_service": customer_service_agent,
        "data": data_agent, "security": security_agent, "devops": devops_agent, "aiml": aiml_agent
    }
    if agent_name not in agents_map:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
