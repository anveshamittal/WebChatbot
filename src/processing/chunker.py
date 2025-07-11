from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.extract_data import docs  # now this works


# def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     chunks = []
#     for doc in docs:
#         for chunk in splitter.split_text(doc["body"]):
#             chunks.append({
#                 "text": chunk,
#                 "url": doc["url"],
#                 "title": doc["title"]
#             })
#     return chunks
def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in docs:
        body = doc.get("body", "")
        # force conversion to string in case it's decimal, None, etc.
        if not isinstance(body, str):
            body = str(body)
        for chunk in splitter.split_text(body):
            chunks.append({
                "text": chunk,
                "url": doc.get("url", ""),
                "title": doc.get("title", "")
            })
    return chunks


chunks=chunk_documents(docs)