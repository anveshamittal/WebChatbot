import faiss
import numpy as np
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(__file__,'...','...')))
from  cloud_connectors import azure_handler
import config

class RAGSystem:
    def __init__(self, container_client, embeddings):
        self.container_client = container_client
        self.embeddings = embeddings
        self._load_vector_store()

    def _load_vector_store(self):
        """Loads the vector store from Azure or creates a new one."""
        index, docstore, mapping = azure_handler.load_index_from_azure(
            self.container_client,
            config.FAISS_INDEX_BLOB_NAME,
            config.DOCSTORE_BLOB_NAME
        )
        if index and docstore and mapping is not None:
            self.vector_store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=docstore,
                index_to_docstore_id=mapping
            )
        else:
            print("Creating a new vector store.")
            index = faiss.IndexFlatL2(config.EMBEDDING_DIMENSION)
            docstore = InMemoryDocstore({})
            mapping = {}
            self.vector_store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=docstore,
                index_to_docstore_id=mapping
            )

    def save(self):
        """Saves the current vector store state to Azure."""
        azure_handler.save_index_to_azure(
            self.container_client,
            self.vector_store.index,
            self.vector_store.docstore,
            self.vector_store.index_to_docstore_id,
            config.FAISS_INDEX_BLOB_NAME,
            config.DOCSTORE_BLOB_NAME
        )

    def add_documents(self, documents, text_splitter):
        """Chunks and adds new documents to the vector store."""
        if not documents:
            return
        chunks = text_splitter.split_documents(documents)
        ids = [f"{doc.metadata['id']}-{i}" for i, doc in enumerate(chunks)]
        self.vector_store.add_documents(chunks, ids=ids)
        print(f"Added {len(chunks)} new chunks.")

    def delete_documents(self, doc_ids_to_delete):
        """Deletes all chunks associated with a list of document IDs."""
        if not doc_ids_to_delete:
            return
        
        ids_to_remove = []
        if self.vector_store.index_to_docstore_id:
            all_docstore_ids = list(self.vector_store.index_to_docstore_id.values())
            for docstore_id in all_docstore_ids:
                doc = self.vector_store.docstore.search(docstore_id)
                if doc and str(doc.metadata.get('id')) in map(str, doc_ids_to_delete):
                    faiss_index_keys = [k for k, v in self.vector_store.index_to_docstore_id.items() if v == docstore_id]
                    ids_to_remove.extend(faiss_index_keys)

        if not ids_to_remove:
            print("No matching chunks found to delete.")
            return

        self.vector_store.delete([str(i) for i in ids_to_remove])
        print(f"Successfully deleted {len(ids_to_remove)} chunks.")

    def search(self, query, k=5):
        """Performs a similarity search."""
        return self.vector_store.similarity_search(query, k=k)