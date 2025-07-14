from src.db.extract_data import docs
from src.processing.chunker import chunk_documents,chunks
from src.processing.embedder import embed_chunks

def run_indexing():
    chunks = chunk_documents(docs)
    embed_chunks(chunks)

if __name__ == "__main__":
    run_indexing()
