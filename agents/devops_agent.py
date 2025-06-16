import docker
import subprocess
import yaml
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import os
from .base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    """Infrastructure management and monitoring agent"""
    
    def __init__(self, agent_id: str = "devops_agent"):
        super().__init__(agent_id)
        self.capabilities = [
            "container_management",
            "deployment_automation",
            "infrastructure_monitoring",
            "ci_cd_pipeline",
            "environment_management",
            "backup_management"
        ]
        self.docker_client = None
        self._init_docker_client()
        
    def _init_docker_client(self):
        """Initialize Docker client"""
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            self.logger.warning(f"Docker client initialization failed: {e}")
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process DevOps-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "deploy_application":
                return await self._deploy_application(task.get("config"))
            elif task_type == "manage_containers":
                return await self._manage_containers(task.get("action"), task.get("containers"))
            elif task_type == "setup_ci_cd":
                return await self._setup_ci_cd_pipeline(task.get("repository"), task.get("config"))
            elif task_type == "monitor_infrastructure":
                return await self._monitor_infrastructure(task.get("targets"))
            elif task_type == "backup_data":
                return await self._backup_data(task.get("sources"), task.get("destination"))
            elif task_type == "scale_services":
                return await self._scale_services(task.get("services"), task.get("scale_config"))
            else:
                return {"status": "error", "message": f"Unknown DevOps task: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"DevOps task error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _deploy_application(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy application using various strategies"""
        deployment_strategy = config.get("strategy", "docker")
        
        if deployment_strategy == "docker":
            return await self._docker_deployment(config)
        elif deployment_strategy == "kubernetes":
            return await self._kubernetes_deployment(config)
        elif deployment_strategy == "serverless":
            return await self._serverless_deployment(config)
        
        return {"status": "error", "message": f"Unknown deployment strategy: {deployment_strategy}"}
    
    async def _docker_deployment(self, config: Dict) -> Dict[str, Any]:
        """Deploy using Docker"""
        if not self.docker_client:
            return {"status": "error", "message": "Docker client not available"}
        
        try:
            # Build image if Dockerfile provided
            if config.get("dockerfile_path"):
                image = self.docker_client.images.build(
                    path=config.get("build_context", "."),
                    dockerfile=config.get("dockerfile_path"),
                    tag=config.get("image_name", "app:latest")
                )
                self.logger.info(f"Built image: {image[0].tags}")
            
            # Run container
            container = self.docker_client.containers.run(
                config.get("image_name", "app:latest"),
                ports=config.get("ports", {}),
                environment=config.get("environment", {}),
                detach=True,
                name=config.get("container_name", f"app-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
            )
            
            return {
                "status": "success",
                "deployment": {
                    "container_id": container.id,
                    "container_name": container.name,
                    "status": container.status,
                    "deployed_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Docker deployment failed: {str(e)}"}
    
    async def _setup_ci_cd_pipeline(self, repository: str, config: Dict) -> Dict[str, Any]:
        """Setup CI/CD pipeline"""
        pipeline_type = config.get("type", "github_actions")
        
        if pipeline_type == "github_actions":
            return await self._create_github_actions_pipeline(repository, config)
        elif pipeline_type == "gitlab_ci":
            return await self._create_gitlab_ci_pipeline(repository, config)
        
        return {"status": "error", "message": f"Unknown pipeline type: {pipeline_type}"}
    
    async def _create_github_actions_pipeline(self, repository: str, config: Dict) -> Dict[str, Any]:
        """Create GitHub Actions workflow"""
        workflow = {
            "name": config.get("name", "CI/CD Pipeline"),
            "on": {
                "push": {"branches": config.get("branches", ["main"])},
                "pull_request": {"branches": config.get("branches", ["main"])}
            },
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v3"},
                        {
                            "name": "Setup Node.js",
                            "uses": "actions/setup-node@v3",
                            "with": {"node-version": config.get("node_version", "18")}
                        },
                        {"name": "Install dependencies", "run": "npm install"},
                        {"name": "Run tests", "run": "npm test"},
                        {"name": "Build application", "run": "npm run build"}
                    ]
                }
            }
        }
        
        # Add deployment job if specified
        if config.get("deploy"):
            workflow["jobs"]["deploy"] = {
                "needs": "build",
                "runs-on": "ubuntu-latest",
                "if": "github.ref == 'refs/heads/main'",
                "steps": [
                    {"uses": "actions/checkout@v3"},
                    {"name": "Deploy to production", "run": config.get("deploy_command", "echo 'Deploy command not specified'")}
                ]
            }
        
        workflow_path = ".github/workflows/ci-cd.yml"
        os.makedirs(os.path.dirname(workflow_path), exist_ok=True)
        
        with open(workflow_path, 'w') as f:
            yaml.dump(workflow, f, default_flow_style=False)
        
        return {
            "status": "success",
            "pipeline": {
                "type": "github_actions",
                "file_path": workflow_path,
                "workflow": workflow
            }
        }