import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re
import asyncio
from cryptography.fernet import Fernet
from .base_agent import BaseAgent

class SecurityAgent(BaseAgent):
    """Comprehensive security monitoring and compliance agent"""
    
    def __init__(self, agent_id: str = "security_agent"):
        super().__init__(agent_id)
        self.capabilities = [
            "vulnerability_scanning",
            "access_control",
            "encryption",
            "audit_logging",
            "compliance_checking",
            "threat_detection"
        ]
        self.security_rules = self._load_security_rules()
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process security-related tasks"""
        task_type = task.get("type")
        
        try:
            if task_type == "vulnerability_scan":
                return await self._vulnerability_scan(task.get("target"))
            elif task_type == "generate_token":
                return await self._generate_secure_token(task.get("payload"), task.get("expiry"))
            elif task_type == "encrypt_data":
                return await self._encrypt_data(task.get("data"))
            elif task_type == "audit_check":
                return await self._perform_audit_check(task.get("system"))
            elif task_type == "compliance_report":
                return await self._generate_compliance_report(task.get("framework"))
            elif task_type == "threat_analysis":
                return await self._analyze_threats(task.get("logs"))
            else:
                return {"status": "error", "message": f"Unknown security task: {task_type}"}
                
        except Exception as e:
            self.logger.error(f"Security task error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _vulnerability_scan(self, target: Dict[str, Any]) -> Dict[str, Any]:
        """Perform vulnerability scanning"""
        vulnerabilities = []
        
        # Check for common vulnerabilities
        if target.get("type") == "web_application":
            vulnerabilities.extend(await self._scan_web_vulnerabilities(target))
        elif target.get("type") == "api":
            vulnerabilities.extend(await self._scan_api_vulnerabilities(target))
        elif target.get("type") == "database":
            vulnerabilities.extend(await self._scan_database_vulnerabilities(target))
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(vulnerabilities)
        
        return {
            "status": "success",
            "scan_results": {
                "target": target,
                "vulnerabilities": vulnerabilities,
                "risk_score": risk_score,
                "scan_timestamp": datetime.now().isoformat(),
                "recommendations": self._generate_security_recommendations(vulnerabilities)
            }
        }
    
    async def _scan_web_vulnerabilities(self, target: Dict) -> List[Dict]:
        """Scan for web application vulnerabilities"""
        vulnerabilities = []
        url = target.get("url", "")
        
        # Check for common web vulnerabilities
        checks = [
            {"name": "SQL Injection", "pattern": r"(union|select|insert|update|delete)", "severity": "high"},
            {"name": "XSS", "pattern": r"(<script|javascript:|onload=)", "severity": "medium"},
            {"name": "CSRF", "pattern": r"(csrf|cross-site)", "severity": "medium"},
            {"name": "Insecure Headers", "check": "headers", "severity": "low"}
        ]
        
        for check in checks:
            if await self._check_vulnerability(target, check):
                vulnerabilities.append({
                    "type": check["name"],
                    "severity": check["severity"],
                    "description": f"Potential {check['name']} vulnerability detected",
                    "location": url
                })
        
        return vulnerabilities
    
    async def _generate_secure_token(self, payload: Dict, expiry_hours: int = 24) -> Dict[str, Any]:
        """Generate secure JWT tokens"""
        secret_key = secrets.token_urlsafe(32)
        
        token_payload = {
            **payload,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=expiry_hours),
            "jti": secrets.token_urlsafe(16)  # Unique token ID
        }
        
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")
        
        return {
            "status": "success",
            "token": token,
            "expires_at": token_payload["exp"].isoformat(),
            "token_id": token_payload["jti"]
        }
    
    async def _encrypt_data(self, data: Any) -> Dict[str, Any]:
        """Encrypt sensitive data"""
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        encrypted_data = self.cipher_suite.encrypt(data_str.encode())
        
        return {
            "status": "success",
            "encrypted_data": encrypted_data.decode(),
            "encryption_method": "Fernet",
            "encrypted_at": datetime.now().isoformat()
        }
    
    def _load_security_rules(self) -> Dict[str, Any]:
        """Load security rules and policies"""
        return {
            "password_policy": {
                "min_length": 12,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True
            },
            "session_policy": {
                "max_duration": 8,  # hours
                "idle_timeout": 30,  # minutes
                "require_2fa": True
            },
            "api_security": {
                "rate_limit": 1000,  # requests per hour
                "require_https": True,
                "require_auth": True
            }
        }