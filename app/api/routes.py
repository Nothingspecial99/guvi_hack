from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent_orchestrator import AgentOrchestrator
from app.core.security import get_api_key

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, api_key: str = Depends(get_api_key)):
    """
    Main endpoint for the honeypot.
    Receives a message, processes it via the agent, and returns a reply or completion status.
    """
    try:
        response = AgentOrchestrator.process_message(
            session_id=request.sessionId,
            message=request.message,
            history=request.conversationHistory
        )
        return response
    except Exception as e:
        # Log for deploy
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
