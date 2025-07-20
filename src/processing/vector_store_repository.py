import faiss
import pickle
import logging
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from src.config import app_config
import numpy as np
from src.cloud_connectors.azure_storage import AzureBlobManager

logger = logging.getLogger(__name__)

class VectorStoreRepository:
    """Handles the saving and loading of the FAISS vector store to/from a persistent location."""

    def __init__(self, azure_manager: AzureBlobManager, embedding_dimension: int):
        self.azure_manager = azure_manager
        self.embedding_dimension = embedding_dimension

    def load(self, embeddings: Embeddings) -> FAISS:
        """Loads the vector store from Azure, or creates a new empty one."""
        logger.info("Attempting to load vector store from Azure...")
        
        index_bytes = self.azure_manager.download_blob_as_bytes(app_config.files['faiss_index_blob_name'])
        docstore_bytes = self.azure_manager.download_blob_as_bytes(app_config.files['datastore_blob_name'])

        if index_bytes and docstore_bytes:
            logger.info("Found existing index in Azure. Loading into memory.")
            # Convert the bytes object to a NumPy uint8 array
            index_as_array = np.frombuffer(index_bytes, dtype=np.uint8)
            index = faiss.deserialize_index(index_as_array)
            docstore, index_to_docstore_id = pickle.loads(docstore_bytes)
        else:
            logger.warning("No existing index found in Azure. Creating a new, empty vector store.")
            index = faiss.IndexFlatL2(self.embedding_dimension)
            docstore = InMemoryDocstore({})
            index_to_docstore_id = {}
        
        return FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id
        )

    def save(self, vector_store: FAISS):
        """Saves the current state of the vector store to Azure."""
        self.azure_manager.save_faiss_index_in_memory(
            index=vector_store.index,
            docstore=vector_store.docstore,
            index_to_docstore_id=vector_store.index_to_docstore_id
        )