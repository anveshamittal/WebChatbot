from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.schema import Document

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.config import embedding_config

embedding_config = embedding_config()

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)
import pickle
CHUNKS_INPUT_PATH = 'chunks.pkl'
FAISS_STORE_PATH = 'faiss_vector_store' 

def build_index_from_chunks():
    with open(CHUNKS_INPUT_PATH, 'rb') as f:
        all_chunked_docs = pickle.load(f)

    if not all_chunked_docs:
        print("The chunks file is empty. No new documents to add.")
        return

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = None
    if os.path.exists(FAISS_STORE_PATH):
        vector_store = FAISS.load_local(
            FAISS_STORE_PATH, 
            embedding_model,
            allow_dangerous_deserialization=True 
        )
        vector_store.add_documents(all_chunked_docs)

    else:
        print("No existing store found. Creating a new one from documents...")
        vector_store = FAISS.from_documents(
            documents=all_chunked_docs,
            embedding=embedding_model
        )
    vector_store.save_local(FAISS_STORE_PATH)
