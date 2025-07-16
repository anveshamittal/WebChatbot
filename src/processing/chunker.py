from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.extract_data import fetch_data
from src.config_loader import chunking_config

chunking_config = chunking_config()

def chunk_documents(docs, chunk_size=chunking_config['chunk_size'], chunk_overlap=chunking_config['chunk_overlap']):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks= splitter.split_text(docs)
    return chunks

docs = fetch_data()

for doc in docs:
    chunks=chunk_documents(doc)
    print(chunks)