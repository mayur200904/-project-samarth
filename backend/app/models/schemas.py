"""
Data models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    """Types of queries supported"""
    COMPARISON = "comparison"
    TREND_ANALYSIS = "trend_analysis"
    CORRELATION = "correlation"
    RANKING = "ranking"
    RECOMMENDATION = "recommendation"
    GENERAL = "general"


class DataSource(BaseModel):
    """Information about a data source"""
    dataset_id: str
    dataset_name: str
    organization: str
    url: str
    last_updated: Optional[str] = None
    description: Optional[str] = None


class Citation(BaseModel):
    """Citation for a claim in the answer"""
    claim: str
    sources: List[DataSource]
    confidence: float = Field(ge=0.0, le=1.0)


class ChatMessage(BaseModel):
    """Chat message from user"""
    message: str
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response to a chat query"""
    answer: str
    citations: List[Citation]
    query_type: QueryType
    sub_queries: List[str]
    data_sources_used: List[DataSource]
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time: float
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    visualizations: Optional[List[Dict[str, Any]]] = None


class DatasetInfo(BaseModel):
    """Information about available datasets"""
    dataset_id: str
    name: str
    description: str
    organization: str
    category: str  # agriculture, climate, etc.
    format: str  # csv, json, xls, api
    fields: List[str]
    row_count: Optional[int] = None
    last_updated: str
    url: str
    tags: List[str] = []


class DataQuery(BaseModel):
    """Request to query specific dataset"""
    dataset_id: str
    filters: Optional[Dict[str, Any]] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)


class DataQueryResponse(BaseModel):
    """Response from data query"""
    dataset_id: str
    data: List[Dict[str, Any]]
    total_count: int
    returned_count: int
    metadata: DatasetInfo


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    uptime: float
    services: Dict[str, str]  # service_name -> status
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
