from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.schema import Document

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.processing.chunker import chunks
from src.config_loader import embedding_config

embedding_config = embedding_config()

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)


def embed_chunks(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index = FAISS.from_texts(chunks, embeddings)
    faiss_index.save_local("data/faiss_index")
    return faiss_index


embeddings=embed_chunks(chunks)