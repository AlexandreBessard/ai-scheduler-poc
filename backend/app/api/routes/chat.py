from fastapi import APIRouter
from app.models.appointment import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest) -> ChatResponse:
    # Placeholder: LangGraph agent will replace this response.
    # The thread_id is already being received and will be used as the
    # LangGraph checkpoint key once the agent is wired up.
    return ChatResponse(
        message="Hello! I'm your scheduling assistant. How can I help you book an appointment today?",
        thread_id=body.thread_id,
    )
