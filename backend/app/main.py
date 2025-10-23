"""
FastAPI Backend for Project Samarth
Intelligent Q&A System for Agricultural & Climate Data
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from app.core.config import settings
from app.api import chat, data, health
from app.services.data_fetcher import DataFetcher
from app.services.rag_service import RAGService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting Project Samarth Backend...")
    
    # Initialize services
    try:
        # Initialize data fetcher
        data_fetcher = DataFetcher()
        app.state.data_fetcher = data_fetcher
        logger.info("✅ Data fetcher initialized")
        
        # Initialize RAG service
        rag_service = RAGService()
        await rag_service.initialize()
        app.state.rag_service = rag_service
        logger.info("✅ RAG service initialized")
        
        # Load initial datasets
        logger.info("📊 Loading initial datasets...")
        await data_fetcher.load_initial_datasets()
        logger.info("✅ Initial datasets loaded")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down Project Samarth Backend...")


# Create FastAPI app
app = FastAPI(
    title="Project Samarth API",
    description="Intelligent Q&A System for Agricultural & Climate Data from data.gov.in",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(data.router, prefix="/api/v1", tags=["Data"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint"""
    return {
        "message": "Project Samarth API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
