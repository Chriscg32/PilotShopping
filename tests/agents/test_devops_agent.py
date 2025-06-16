import pytest
from unittest.mock import Mock, patch
from agents.devops_agent import DevOpsAgent

class TestDevOpsAgent:
    @pytest.fixture
    def devops_agent(self):
        agent = DevOpsAgent()
        # Mock Docker client for testing
        agent.docker_client = Mock()
        return agent
    
    @pytest.mark.asyncio
    async def test_docker_deployment(self, devops_agent):
        # Mock Docker operations
        mock_container = Mock()
        mock_container.id = "container123"
        mock_container.name = "test-app"
        mock_container.status = "running"
        
        devops_agent.docker_client.containers.run.return_value = mock_container
        
        task = {
            "type": "deploy_application",
            "config": {
                "strategy": "docker",
                "image_name": "test-app:latest",
                "ports": {"80/tcp": 8080},
                "environment": {"ENV": "production"}
            }
        }
        
        result = await devops_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "deployment" in result
        assert result["deployment"]["container_id"] == "container123"
    
    @pytest.mark.asyncio
    async def test_setup_github_actions_pipeline(self, devops_agent):
        task = {
            "type": "setup_ci_cd",
            "repository": "user/repo",
            "config": {
                "type": "github_actions",
                "name": "CI/CD Pipeline",
                "branches": ["main", "develop"],
                "node_version": "18",
                "deploy": True,
                "deploy_command": "npm run deploy"
            }
        }
        
        with patch('os.makedirs'), patch('builtins.open'), patch('yaml.dump'):
            result = await devops_agent.process_task(task)
        
        assert result["status"] == "success"
        assert "pipeline" in result
        assert result["pipeline"]["type"] == "github_actions"
    
    @pytest.mark.asyncio
    async def test_manage_containers(self, devops_agent):
        mock_container = Mock()
        mock_container.name = "test-container"
        mock_container.status = "running"
        
        devops_agent.docker_client.containers.list.return_value = [mock_container]
        
        task = {
            "type": "manage_containers",
            "action": "list",
            "containers": ["test-container"]
        }
        
        result = await devops_agent.process_task(task)
        
        assert result["status"] == "success"