"""
Chat API endpoint
"""
from fastapi import APIRouter, HTTPException, Request
import logging

from app.models.schemas import ChatMessage, ChatResponse
from app.services.query_engine import QueryEngine
from app.services.llm_service import LLMService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, request: Request):
    """
    Process a chat message and return an answer with citations
    """
    try:
        # Get services from app state
        rag_service = request.app.state.rag_service
        data_fetcher = request.app.state.data_fetcher
        
        # Create LLM service (can be per-request or cached)
        llm_service = LLMService()
        
        # Create query engine
        query_engine = QueryEngine(
            llm_service=llm_service,
            rag_service=rag_service,
            data_fetcher=data_fetcher
        )
        
        # Process query
        response = await query_engine.process_query(
            user_query=message.message,
            conversation_id=message.conversation_id
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history (TODO: implement persistence)"""
    # This would retrieve conversation history from a database
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "status": "not_implemented"
    }
