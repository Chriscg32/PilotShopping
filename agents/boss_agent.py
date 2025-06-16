# Add to existing boss_agent.py

class BossAgent(BaseAgent):
    def __init__(self):
        super().__init__("boss_agent")
        self.agents = {
            "finance": "finance_agent",
            "design": "design_agent", 
            "engineering": "engineering_agent",
            "customer_service": "customer_service_agent",
            "marketing": "marketing_agent",
            # New agents for v0.4.0
            "data": "data_agent",
            "security": "security_agent", 
            "devops": "devops_agent",
            "aiml": "aiml_agent"
        }
        
    def _determine_agent_for_task(self, task: Dict[str, Any]) -> str:
        """Enhanced task routing for new agents"""
        task_type = task.get("type", "").lower()
        keywords = task.get("description", "").lower()
        
        # Data-related tasks
        if any(word in keywords for word in ["analyze", "data", "report", "analytics", "visualization"]):
            return "data"
        
        # Security-related tasks  
        if any(word in keywords for word in ["security", "encrypt", "vulnerability", "audit", "compliance"]):
            return "security"
            
        # DevOps-related tasks
        if any(word in keywords for word in ["deploy", "container", "infrastructure", "ci/c