"""
Configuration settings for Project Samarth
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    DEBUG: bool = True
    LOG_LEVEL: str = "info"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai, anthropic, google, ollama
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    MODEL_NAME: str = "gpt-4-turbo-preview"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"
    
    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Data.gov.in
    DATA_GOV_API_KEY: str = ""
    DATA_GOV_BASE_URL: str = "https://api.data.gov.in/resource"
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
    # Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 86400  # 24 hours
    USE_CACHE: bool = True
    
    # Data
    DATA_DIRECTORY: str = "./data"
    MAX_DATASET_SIZE_MB: int = 100
    AUTO_UPDATE_INTERVAL: int = 3600
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = 10
    QUERY_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        Path(self.DATA_DIRECTORY).mkdir(parents=True, exist_ok=True)
        Path(self.CHROMA_PERSIST_DIRECTORY).mkdir(parents=True, exist_ok=True)


settings = Settings()
