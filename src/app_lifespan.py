import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.logger_setup import setup_logging
from src.llm.chatbot import ChatBot # <-- Utilizing code from another file
from src.processing import document_processor
from cloud_connectors.azure_storage import AzureBlobManager
from src.config import app_config
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown events.
    """
    # --- Startup Logic ---
    
    # Configure logging as the VERY first action.
    setup_logging()
    
    # Get a logger for this module (optional, but good for logging startup itself)
    logger = logging.getLogger(__name__)

    logger.info("Application startup: Initializing resources...")

     # 1. Prepare the embedding model
    embeddings = document_processor.initialize_embedding_model(app_config.embedding['model_provider'],app_config.embedding['embedding_model'])

    # 2. Prepare the vector store (check for local files, download if needed)
    azure_manager = AzureBlobManager(os.getenv('AZURE_STORAGE_CONNECTION_STRING',app_config.azure['container_name']))

    azure_manager.download_faiss_to_local("data/faiss_index")

    vector_store = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)

      # 3. Prepare the LLM
    llm = ChatOpenAI(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            default_query={"api-version": "preview"}
        )
    
      # 4. Prepare the prompt
    parser = StrOutputParser()
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant for tietoevry company. if you do not know the answer say i don't know the answer please contact us on https://www.tietoevry.com/en/contact-tietoevry/
            Data:
            {context}
            Question: {input}
            Answer:"""
        )

    # 5. Create the ChatBot instance by injecting the prepared components
    chatbot_instance = ChatBot(llm=llm, vector_store=vector_store, prompt=prompt,parser=parser)
    
    # Store the final, ready-to-use chatbot instance in the app state
    app.state.chatbot = chatbot_instance

    logger.info("ChatBot has been initialized and stored in app state.")
    
    yield
    
    # --- Shutdown Logic ---
    logger.info("Application shutdown: Cleaning up resources.")
    app.state.chatbot = None
    logger = None