#!/usr/bin/env python3
"""
ButterflyBlue Security & Authentication
JWT tokens, API keys, rate limiting, and security headers
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import redis
import hashlib
import secrets
from functools import wraps
import time

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Redis for rate limiting and session management
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

security = HTTPBearer()

class SecurityManager:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def generate_api_key(self, user_id: str) -> str:
        """Generate API key for user"""
        random_part = secrets.token_urlsafe(32)
        user_part = hashlib.sha256(user_id.encode()).hexdigest()[:8]
        api_key = f"bb_{user_part}_{random_part}"
        
        # Store API key in Redis with user mapping
        redis_client.setex(f"api_key:{api_key}", 86400 * 365, user_id)  # 1 year expiry
        
        return api_key
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """Verify API key and return user ID"""
        user_id = redis_client.get(f"api_key:{api_key}")
        return user_id

# Rate limiting decorator
def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Get client IP
            client_ip = request.client.host
            
            # Create rate limit key
            current_window = int(time.time() // window_seconds)
            rate_limit_key = f"rate_limit:{client_ip}:{current_window}"
            
            # Check current request count
            current_requests = redis_client.get(rate_limit_key)
            if current_requests is None:
                current_requests = 0
            else:
                current_requests = int(current_requests)
            
            if current_requests >= max_requests:
                raise HTTPException(
                    status_code=429, 
                    detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds"
                )
            
            # Increment request count
            redis_client.incr(rate_limit_key)
            redis_client.expire(rate_limit_key, window_seconds)
            
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    token = credentials.credentials
    
    # Check if it's an API key
    if token.startswith("bb_"):
        security_manager = SecurityManager()
        user_id = security_manager.verify_api_key(token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return {"user_id": user_id, "auth_type": "api_key"}
    
    # Otherwise, treat as JWT token
    security_manager = SecurityManager()
    payload = security_manager.verify_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    return {"user_id": payload.get("sub"), "auth_type": "jwt"}

# Security headers middleware
def add_security_headers(response):
    """Add security headers to response"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Initialize security manager
security_manager = SecurityManager()