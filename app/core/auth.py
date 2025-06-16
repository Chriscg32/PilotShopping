from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import redis
from typing import Optional

class AuthManager:
    """Comprehensive authentication and authorization system."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
        self.SECRET_KEY = "your-secret-key"  # Use environment variable
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create refresh token and store in Redis."""
        token_data = {"user_id": user_id, "type": "refresh"}
        expire = timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        token = self.create_access_token(token_data, expire)
        
        # Store in Redis with expiration
        self.redis_client.setex(
            f"refresh_token:{user_id}", 
            int(expire.total_seconds()), 
            token
        )
        return token
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Get current authenticated user."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(credentials.credentials, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        # Check if token is blacklisted
        if self.redis_client.get(f"blacklist:{credentials.credentials}"):
            raise credentials_exception
        
        return user_id
    
    def blacklist_token(self, token: str):
        """Blacklist a token (for logout)."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            exp = payload.get("exp")
            if exp:
                ttl = exp - datetime.utcnow().timestamp()
                if ttl > 0:
                    self.redis_client.setex(f"blacklist:{token}", int(ttl), "true")
        except JWTError:
            pass  # Invalid token, no need to blacklist

# Global auth manager
auth_manager = AuthManager()