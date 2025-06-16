import asyncio
import json
import logging
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
import aioredis
import smtplib
from email.mime.text import MIMEText

@dataclass
class AgentMetrics:
    agent_name: str
    status: str
    last_check: datetime
    task_count: int
    error_count: int
    response_time: float
    memory_usage: float
    cpu_usage: float

class AgentMonitor:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis_client = None
        self.metrics_history: Dict[str, List[AgentMetrics]] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
        
        # Alert thresholds
        self.thresholds = {
            "response_time": 5.0,  # seconds
            "error_rate": 0.1,     # 10%
            "memory_usage": 0.8,   # 80%
            "cpu_usage": 0.9       # 90%
        }
    
    async def start(self):
        """Start the monitoring system"""
        self.redis_client = await aioredis.from_url(self.redis_url)
        self.logger.info("Agent monitor started")
    
    async def monitor_agents(self, agents: Dict[str, Any]):
        """Main monitoring loop"""
        while True:
            try:
                for agent_name, agent in agents.items():
                    metrics = await self._collect_agent_metrics(agent_name, agent)
                    await self._store_metrics(metrics)
                    await self._check_alerts(metrics)
                
                # Clean old metrics
                await self._cleanup_old_metrics()
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
            
            await asyncio.sleep(30)  # Check every 30 seconds
    
    async def _collect_agent_metrics(self, agent_name: str, agent: Any) -> AgentMetrics:
        """Collect metrics from an agent"""
        start_time = datetime.now()
        
        try:
            # Get health status
            health = await agent.health_check()
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Get system metrics
            memory_usage = await self._get_memory_usage(agent_name)
            cpu_usage = await self._get_cpu_usage(agent_name)
            
            metrics = AgentMetrics(
                agent_name=agent_name,
                status=health.get("status", "unknown"),
                last_check=datetime.now(),
                task_count=health.get("task_count", 0),
                error_count=health.get("error_count", 0),
                response_time=response_time,
                memory_usage=memory_usage,
                cpu_usage=cpu_usage
            )
            
        except Exception as e:
            self.logger.error(f"Failed to collect metrics for {agent_name}: {e}")
            metrics = AgentMetrics(
                agent_name=agent_name,
                status="error",
                last_check=datetime.now(),
                task_count=0,
                error_count=1,
                response_time=0.0,
                memory_usage=0.0,
                cpu_usage=0.0
            )
        
        return metrics
    
    async def _get_memory_usage(self, agent_name: str) -> float:
        """Get memory usage for agent process"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_percent() / 100.0
        except:
            return 0.0
    
    async def _get_cpu_usage(self, agent_name: str) -> float:
        """Get CPU usage for agent process"""
        try:
            process = psutil.Process(os.getpid())
            return process.cpu_percent() / 100.0
        except:
            return 0.0
    
    async def _store_metrics(self, metrics: AgentMetrics):
        """Store metrics in Redis"""
        if self.redis_client:
            key = f"agent_metrics:{metrics.agent_name}"
            value = json.dumps(asdict(metrics), default=str)
            await self.redis_client.lpush(key, value)
            await self.redis_client.ltrim(key, 0, 100)  # Keep last 100 entries
    
    async def _check_alerts(self, metrics: AgentMetrics):
        """Check if metrics exceed thresholds and generate alerts"""
        alerts = []
        
        if metrics.response_time > self.thresholds["response_time"]:
            alerts.append({
                "type": "high_response_time",
                "agent": metrics.agent_name,
                "value": metrics.response_time,
                "threshold": self.thresholds["response_time"],
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics.memory_usage > self.thresholds["memory_usage"]:
            alerts.append({
                "type": "high_memory_usage",
                "agent": metrics.agent_name,
                "value": metrics.memory_usage,
                "threshold": self.thresholds["memory_usage"],
                "timestamp": datetime.now().isoformat()
            })
        
        if metrics.status != "healthy":
            alerts.append({
                "type": "unhealthy_status",
                "agent": metrics.agent_name,
                "status": metrics.status,
                "timestamp": datetime.now().isoformat()
            })
        
        for alert in alerts:
            await self._send_alert(alert)
    
    async def _send_alert(self, alert: Dict[str, Any]):
        """Send alert notification"""
        self.alerts.append(alert)
        self.logger.warning(f"ALERT: {alert}")
        
        # Send email notification (if configured)
        await self._send_email_alert(alert)
    
    async def _send_email_alert(self, alert: Dict[str, Any]):
        """Send email alert notification"""
        # Implementation would depend on email configuration
        pass
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        status = {}
        
        if self.redis_client:
            for agent_name in ["data", "security", "devops", "aiml", "finance", "design", "engineering", "customer_service", "marketing"]:
                key = f"agent_metrics:{agent_name}"
                latest = await self.redis_client.lindex(key, 0)
                if latest:
                    metrics = json.loads(latest)
                    status[agent_name] = metrics
        
        return status