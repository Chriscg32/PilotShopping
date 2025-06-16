from fastapi import HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
from typing import Dict, Any

class SmartRateLimiter:
    """Intelligent rate limiting based on user tier and usage patterns."""
    
    def __init__(self):
        self.redis_client = redis.Redis(host="localhost", port=6379, db=1)
        self.limiter = Limiter(key_func=get_remote_address)
        
        # Rate limits by subscription tier
        self.tier_limits = {
            "free": {"requests": 100, "ai_calls": 50, "period": "hour"},
            "starter": {"requests": 1000, "ai_calls": 500, "period": "hour"},
            "professional": {"requests": 10000, "ai_calls": 5000, "period": "hour"},
            "enterprise": {"requests": 100000, "ai_calls": 50000, "period": "hour"}
        }
    
    def get_user_limits(self, user_tier: str) -> Dict[str, Any]:
        """Get rate limits for user tier."""
        return self.tier_limits.get(user_tier, self.tier_limits["free"])
    
    async def check_rate_limit(self, user_id: str, user_tier: str, request_type: str = "requests"):
        """Check if user has exceeded rate limits."""
        limits = self.get_user_limits(user_tier)
        key = f"rate_limit:{user_id}:{request_type}:{limits['period']}"
        
        current_count = self.redis_client.get(key)
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)
        
        limit = limits.get(request_type, limits["requests"])
        
        if current_count >= limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. {limit} {request_type} per {limits['period']} allowed for {user_tier} tier."
            )
        
        # Increment counter
        pipe = self.redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, 3600 if limits['period'] == 'hour' else 86400)  # 1 hour or 1 day
        pipe.execute()
        
        return {
            "current_usage": current_count + 1,
            "limit": limit,
            "remaining": limit - current_count - 1
        }

# Global rate limiter
rate_limiter = SmartRateLimiter()