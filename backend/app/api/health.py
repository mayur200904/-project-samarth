"""
Health check endpoint
"""
from fastapi import APIRouter, Request
from datetime import datetime
import time

from app.models.schemas import HealthResponse

router = APIRouter()

# Track startup time
startup_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Health check endpoint"""
    
    services = {
        "api": "healthy",
        "llm": "unknown",
        "rag": "unknown",
        "data_fetcher": "unknown"
    }
    
    # Check if services are initialized
    if hasattr(request.app.state, "rag_service"):
        services["rag"] = "healthy"
    
    if hasattr(request.app.state, "data_fetcher"):
        services["data_fetcher"] = "healthy"
    
    uptime = time.time() - startup_time
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime=uptime,
        services=services
    )
