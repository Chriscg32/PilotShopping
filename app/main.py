from fastapi import FastAPI
from app.routers import auth, items, users, monitoring
from app.core.config import settings

app = FastAPI(title="Landing Copy Generator API")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])

@app.get("/")
async def root():
    return {"message": "Landing Copy Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}