from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import json
from app.core.base_agent import BaseAgent
from app.core.telemetry import TelemetryManager

class MetaAgent(BaseAgent):
    """
    Meta-Agent: Monitors, optimizes, and improves the entire multi-agent system.
    This agent watches other agents and makes system-wide improvements.
    """
    
    def __init__(self):
        super().__init__("meta")
        self.telemetry = TelemetryManager()
        self.optimization_rules = self._load_optimization_rules()
        self.performance_baselines = {}
        
    def _load_optimization_rules(self) -> Dict[str, Any]:
        """Load system optimization rules."""
        return {
            "performance_thresholds": {
                "max_response_time": 2.0,
                "min_success_rate": 99.0,
                "max_error_rate": 1.0
            },
            "resource_limits": {
                "max_cpu_usage": 80.0,
                "max_memory_usage": 85.0,
                "max_queue_size": 1000
            },
            "auto_scaling": {
                "scale_up_threshold": 75.0,
                "scale_down_threshold": 25.0,
                "min_instances": 1,
                "max_instances": 10
            }
        }
    
    async def monitor_system_health(self) -> Dict[str, Any]:
        """Continuously monitor entire system health."""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "agents": {},
            "system_metrics": {},
            "recommendations": []
        }
        
        # Monitor each agent
        agents = ["boss", "marketing", "finance", "engineering", "design", "customer_service"]
        
        for agent_name in agents:
            agent_health = await self._check_agent_health(agent_name)
            health_report["agents"][agent_name] = agent_health
            
            # Generate recommendations based on agent performance
            if agent_health["response_time"] > self.optimization_rules["performance_thresholds"]["max_response_time"]:
                health_report["recommendations"].append({
                    "type": "performance",
                    "agent": agent_name,
                    "issue": "high_response_time",
                    "current_value": agent_health["response_time"],
                    "threshold": self.optimization_rules["performance_thresholds"]["max_response_time"],
                    "suggested_action": "optimize_agent_processing"
                })
        
        # Monitor system-wide metrics
        health_report["system_metrics"] = await self._get_system_metrics()
        
        # Determine overall status
        critical_issues = [r for r in health_report["recommendations"] if r.get("severity") == "critical"]
        if critical_issues:
            health_report["overall_status"] = "critical"
        elif health_report["recommendations"]:
            health_report["overall_status"] = "warning"
        
        return health_report
    
    async def _check_agent_health(self, agent_name: str) -> Dict[str, Any]:
        """Check health of individual agent."""
        try:
            # Get agent metrics from telemetry
            metrics = await self.telemetry.get_agent_metrics(agent_name, timedelta(minutes=15))
            
            return {
                "status": "healthy" if metrics["error_rate"] < 1.0 else "unhealthy",
                "response_time": metrics.get("avg_response_time", 0),
                "success_rate": metrics.get("success_rate", 0),
                "error_rate": metrics.get("error_rate", 0),
                "request_count": metrics.get("request_count", 0),
                "last_activity": metrics.get("last_activity"),
                "resource_usage": {
                    "cpu": metrics.get("cpu_usage", 0),
                    "memory": metrics.get("memory_usage", 0),
                    "queue_size": metrics.get("queue_size", 0)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "response_time": 999,
                "success_rate": 0,
                "error_rate": 100
            }
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide performance metrics."""
        import psutil
        
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            },
            "active_connections": len(psutil.net_connections()),
            "uptime": psutil.boot_time()
        }
    
    async def auto_optimize_system(self) -> Dict[str, Any]:
        """Automatically optimize system based on current performance."""
        optimization_actions = []
        
        # Get current system health
        health_report = await self.monitor_system_health()
        
        # Apply optimization rules
        for recommendation in health_report["recommendations"]:
            action_taken = await self._apply_optimization(recommendation)
            if action_taken:
                optimization_actions.append({
                    "recommendation": recommendation,
                    "action": action_taken,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Auto-scaling decisions
        scaling_actions = await self._auto_scale_system(health_report["system_metrics"])
        optimization_actions.extend(scaling_actions)
        
        return {
            "optimization_timestamp": datetime.now().isoformat(),
            "actions_taken": optimization_actions,
            "system_status": health_report["overall_status"]
        }
    
    async def _apply_optimization(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply specific optimization based on recommendation."""
        action = None
        
        if recommendation["type"] == "performance":
            if recommendation["issue"] == "high_response_time":
                # Increase agent processing capacity
                action = await self._scale_agent_resources(
                    recommendation["agent"], 
                    "increase_workers"
                )
            elif recommendation["issue"] == "high_error_rate":
                # Restart agent or apply circuit breaker
                action = await self._restart_agent(recommendation["agent"])
        
        elif recommendation["type"] == "resource":
            if recommendation["issue"] == "high_memory_usage":
                # Clear caches or restart agent
                action = await self._clear_agent_cache(recommendation["agent"])
            elif recommendation["issue"] == "high_queue_size":
                # Scale up processing or add workers
                action = await self._scale_agent_resources(
                    recommendation["agent"], 
                    "add_workers"
                )
        
        return action
    
    async def _auto_scale_system(self, system_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Make auto-scaling decisions based on system metrics."""
        scaling_actions = []
        
        cpu_usage = system_metrics.get("cpu_usage", 0)
        memory_usage = system_metrics.get("memory_usage", 0)
        
        # Scale up if resources are high
        if cpu_usage > self.optimization_rules["auto_scaling"]["scale_up_threshold"]:
            action = await self._scale_system("up", "cpu_high")
            if action:
                scaling_actions.append(action)
        
        if memory_usage > self.optimization_rules["auto_scaling"]["scale_up_threshold"]:
            action = await self._scale_system("up", "memory_high")
            if action:
                scaling_actions.append(action)
        
        # Scale down if resources are low (and we have multiple instances)
        elif (cpu_usage < self.optimization_rules["auto_scaling"]["scale_down_threshold"] and
              memory_usage < self.optimization_rules["auto_scaling"]["scale_down_threshold"]):
            action = await self._scale_system("down", "resources_low")
            if action:
                scaling_actions.append(action)
        
        return scaling_actions
    
    async def _scale_system(self, direction: str, reason: str) -> Dict[str, Any]:
        """Scale system up or down."""
        # This would integrate with container orchestration (Docker Swarm, Kubernetes, etc.)
        try:
            if direction == "up":
                # Add more container instances
                result = await self._add_container_instance()
            else:
                # Remove container instances (if safe)
                result = await self._remove_container_instance()
            
            return {
                "action": f"scale_{direction}",
                "reason": reason,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "action": f"scale_{direction}_failed",
                "reason": reason,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def generate_improvement_suggestions(self) -> Dict[str, Any]:
        """Generate suggestions for system improvements based on historical data."""
        # Analyze performance trends over time
        performance_trends = await self._analyze_performance_trends()
        
        # Identify bottlenecks
        bottlenecks = await self._identify_bottlenecks()
        
        # Generate code optimization suggestions
        code_suggestions = await self._analyze_code_performance()
        
        # Generate infrastructure suggestions
        infra_suggestions = await self._analyze_infrastructure()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "performance_trends": performance_trends,
            "bottlenecks": bottlenecks,
            "code_optimizations": code_suggestions,
            "infrastructure_improvements": infra_suggestions,
            "priority_actions": self._prioritize_improvements([
                *bottlenecks,
                *code_suggestions,
                *infra_suggestions
            ])
        }
    
    async def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over the last 30 days."""
        # Get historical metrics
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        trends = {
            "response_time_trend": "stable",  # increasing, decreasing, stable
            "error_rate_trend": "stable",
            "throughput_trend": "increasing",
            "user_growth_trend": "increasing",
            "recommendations": []
        }
        
        # This would analyze actual historical data
        # For now, we'll simulate trend analysis
        
        if trends["response_time_trend"] == "increasing":
            trends["recommendations"].append({
                "type": "performance",
                "priority": "high",
                "suggestion": "Response times are increasing. Consider optimizing database queries and adding caching.",
                "estimated_impact": "30% response time improvement"
            })
        
        return trends
    
    async def _identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify system bottlenecks."""
        bottlenecks = []
        
        # Analyze agent performance
        agents = ["marketing", "finance", "engineering", "design", "customer_service"]
        
        for agent in agents:
            agent_metrics = await self._check_agent_health(agent)
            
            if agent_metrics["response_time"] > 3.0:
                bottlenecks.append({
                    "type": "agent_performance",
                    "agent": agent,
                    "issue": "slow_response",
                    "current_value": agent_metrics["response_time"],
                    "priority": "high",
                    "suggested_fix": f"Optimize {agent} agent processing logic"
                })
            
            if agent_metrics["error_rate"] > 2.0:
                bottlenecks.append({
                    "type": "agent_reliability",
                    "agent": agent,
                    "issue": "high_errors",
                    "current_value": agent_metrics["error_rate"],
                    "priority": "critical",
                    "suggested_fix": f"Debug and fix errors in {agent} agent"
                })
        
        return bottlenecks
    
    async def self_improve(self) -> Dict[str, Any]:
        """Meta-agent improves itself and the system."""
        improvement_log = {
            "timestamp": datetime.now().isoformat(),
            "improvements_made": [],
            "learning_updates": [],
            "system_optimizations": []
        }
        
        # 1. Analyze own performance
        meta_performance = await self._analyze_self_performance()
        
        # 2. Update optimization rules based on learning
        rule_updates = await self._update_optimization_rules()
        improvement_log["learning_updates"] = rule_updates
        
        # 3. Optimize system based on new insights
        optimizations = await self.auto_optimize_system()
        improvement_log["system_optimizations"] = optimizations["actions_taken"]
        
        # 4. Generate and apply code improvements
        code_improvements = await self._generate_code_improvements()
        improvement_log["improvements_made"] = code_improvements
        
        return improvement_log
    
    async def _update_optimization_rules(self) -> List[Dict[str, Any]]:
        """Update optimization rules based on system learning."""
        updates = []
        
        # Analyze if current thresholds are appropriate
        current_performance = await self.monitor_system_health()
        
        # Adjust thresholds based on actual system behavior
        if current_performance["overall_status"] == "healthy":
            # System is performing well, we can be more aggressive with thresholds
            if self.optimization_rules["performance_thresholds"]["max_response_time"] > 1.5:
                self.optimization_rules["performance_thresholds"]["max_response_time"] = 1.5
                updates.append({
                    "rule": "max_response_time",
                    "old_value": 2.0,
                    "new_value": 1.5,
                    "reason": "System performing well, tightening threshold"
                })
        
        return updates

# Global meta-agent instance
meta_agent = MetaAgent()