from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.llm.chatbot import ChatBot # <-- Utilizing code from another file

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown events.
    """
    # --- Startup Logic ---
    print("Lifespan: Startup event. Initializing chatbot...")
    
    # Create and set up the chatbot instance
    chatbot_instance = ChatBot()
    chatbot_instance.setup_qa_chain()
    
    # Store the single, ready-to-use instance in the application's state
    app.state.chatbot = chatbot_instance
    
    yield
    
    # --- Shutdown Logic ---
    print("Lifespan: Shutdown event. Cleaning up resources.")
    app.state.chatbot = None