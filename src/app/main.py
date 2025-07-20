from fastapi import FastAPI, Depends, Request
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

# Local Application Imports
from src.app_lifespan import lifespan
from src.llm.chatbot import ChatBot, QAResponse
from src.utils.file_utils import delete_index_files
from src.processing.batch_processor import run_batch_ingestion_logic

# --- App Initialization ---
app = FastAPI(lifespan=lifespan)

# --- Dependency Provider ---
def get_chatbot(request: Request) -> ChatBot:
    return request.app.state.chatbot

# --- API Models ---
class QuestionRequest(BaseModel):
    question: str

# --- API Routes ---
@app.get("/")
def get_root():
    return {"message": "Server is running."}

@app.post("/question", response_model=QAResponse)
async def ask(
    request_data: QuestionRequest,
    chatbot: ChatBot = Depends(get_chatbot)
):
    return await chatbot.aask_question(request_data.question)

@app.post("/run-ingestion")
async def trigger_ingestion_process():
    result = await run_in_threadpool(run_batch_ingestion_logic)
    return result

@app.post("/delete-local-index")
async def trigger_delete_local_index():
    result = await run_in_threadpool(delete_index_files)
    return result