from fastapi import APIRouter, Depends, Request
from src.llm.chatbot import ChatBot
from src.api.schemas import QuestionRequest, QAResponse

# Create a new router instance
router = APIRouter()

def get_chatbot(request: Request) -> ChatBot:
    return request.app.state.chatbot

@router.post("/question", response_model=QAResponse)
async def ask(
    request_data: QuestionRequest,
    chatbot: ChatBot = Depends(get_chatbot)
):
    """Endpoint to ask a question using the injected chatbot instance."""
    return await chatbot.aask_question(request_data.question)