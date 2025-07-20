from fastapi import FastAPI
from src.app_lifespan import lifespan
from src.api.routes import chat, ingestion # Import your new router modules

# --- App Initialization ---
# The lifespan manager is still connected here
app = FastAPI(lifespan=lifespan)

@app.get("/")
def get_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the WebChatBot API"}

# --- Include API Routers ---
# This adds all the routes from your other files to the main application
app.include_router(chat.router)
app.include_router(ingestion.router)