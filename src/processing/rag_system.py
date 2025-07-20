import logging
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

class RAGSystem:
    """Manages an in-memory FAISS vector store for retrieval operations."""

    def __init__(self, vector_store: FAISS):
        """Initializes the system with a pre-loaded vector store."""
        self.vector_store = vector_store

    def add_documents(self, chunks: List[Document]):
        """Adds a list of pre-chunked documents to the vector store."""
        if not chunks:
            return
        logger.info(f"Adding {len(chunks)} new chunks to the vector store.")
        self.vector_store.add_documents(chunks)

    def delete_documents(self, doc_ids_to_delete: List[str]):
        """Deletes all chunks associated with a list of parent document IDs."""
        if not doc_ids_to_delete:
            return

        target_id_set = {str(doc_id) for doc_id in doc_ids_to_delete}
        
        # Note: This operation can be slow on large datasets.
        ids_to_remove_from_store = [
            docstore_id for docstore_id, doc in self.vector_store.docstore._dict.items()
            if str(doc.metadata.get('id')) in target_id_set
        ]

        if not ids_to_remove_from_store:
            logger.warning("No matching chunks found in vector store to delete.")
            return

        self.vector_store.delete(ids_to_remove_from_store)
        logger.info(f"Successfully deleted {len(ids_to_remove_from_store)} chunks.")

    def search(self, query: str, k: int = 5) -> List[Document]:
        """Performs a similarity search."""
        return self.vector_store.similarity_search(query, k=k)