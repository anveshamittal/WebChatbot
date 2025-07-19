# Standard Library Imports
import pathlib
# Third-Party Imports
from fastapi import FastAPI, Depends, Request
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
# Local Application Imports
from src.app_lifespan import lifespan
from src.llm.chatbot import ChatBot
from src.processing.process_csv import process_csv

# --- App Initialization ---
app = FastAPI(lifespan=lifespan)

# --- Dependency Provider ---
# This simple function gets the chatbot that the lifespan manager created
def get_chatbot(request: Request) -> ChatBot:
    return request.app.state.chatbot

# --- API Models ---
class QuestionRequest(BaseModel):
    question: str

# --- API Routes ---
@app.get("/")
def get_root():
    """An instant endpoint to check if the server is responsive."""
    return {"message": "I'm alive!"}

@app.post("/question")
def ask(
    request_data: QuestionRequest,
    chatbot: ChatBot = Depends(get_chatbot)
):
    """Endpoint to ask a question using the injected chatbot instance."""
    return chatbot.ask_question(request_data.question)

@app.get("/process_csv_file")
async def process_csv_file():
    """Processes the CSV file in a non-blocking way."""
    result = await run_in_threadpool(process_csv)
    return {"status": "processing_triggered", "result": result}

@app.get("/delete_local_index")
async def delete_local_index():
    """Deletes all local index files in a non-blocking way."""
    result = await run_in_threadpool(delete_index_files)
    return result

# --- Helper Functions for delete files ---
def delete_index_files():
    """Contains the blocking logic for deleting files."""
    index_folder_path = pathlib.Path("data/faiss_index")
    if not index_folder_path.exists():
        print(f"Directory not found: {index_folder_path}")
        return {"status": "error", "message": "Directory not found."}

    print(f"Clearing files in: {index_folder_path}")
    deleted_count = 0
    for entry in index_folder_path.iterdir():
        try:
            if entry.is_file():
                entry.unlink()
                deleted_count += 1
        except Exception as e:
            print(f"Error deleting {entry.name}: {e}")
    return {"status": "success", "files_deleted": deleted_count}