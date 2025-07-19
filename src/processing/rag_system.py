from langchain_community.docstore import InMemoryDocstore
import faiss
from langchain_community.vectorstores import FAISS
import os
from  src.cloud_connectors import azure_storage
from src.config import app_config
# from langchain_community.vectorstores import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGSystem:
    def __init__(self, container_client, embeddings):
        self.container_client = container_client
        self.embeddings = embeddings
        self._load_vector_store()

    def _load_vector_store(self):
        """Loads the vector store from Azure or creates a new one."""
        index, docstore, mapping = azure_storage.load_index_from_azure(
            self.container_client,
            app_config.files['faiss_index_blob_name'],
            app_config.files['datastore_blob_name']
        )
        if index is not None and docstore is not None and mapping is not None:
            self.vector_store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=docstore,
                index_to_docstore_id=mapping
            )
        else:
            print("Creating a new vector store.")
            index = faiss.IndexFlatL2(app_config.embedding['embedding_dimension'])
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
        azure_storage.save_index_to_azure(
            self.container_client,
            self.vector_store.index,
            self.vector_store.docstore,
            self.vector_store.index_to_docstore_id,
            app_config.files['faiss_index_blob_name'],
            app_config.files['datastore_blob_name']
        )

    # def add_documents(self, documents, text_splitter):
    #     """Chunks and adds new documents to the vector store using a provided splitter."""
    #     if not documents:
    #         return
    #     # Use the splitter that was passed into the method
    #     chunks = text_splitter.split_documents(documents)
    #     ids = [f"{doc.metadata['id']}-{i}" for i, doc in enumerate(chunks)]
    #     self.vector_store.add_documents(chunks, ids=ids)
    #     print(f"Added {len(chunks)} new chunks.")
    def add_documents(self, documents, text_splitter):
        """Chunks and adds new documents to the vector store using a provided splitter."""
        if not documents:
            return
    
        chunks = text_splitter.split_documents(documents)
    
        # --- FIX: Filter out empty chunks before processing ---
        valid_chunks = [chunk for chunk in chunks if chunk.page_content and chunk.page_content.strip()]
    
        if not valid_chunks:
            print("Warning: No valid, non-empty chunks were created. Nothing to add.")
            return
        # --- End of Fix ---
    
        # Now, use 'valid_chunks' for all subsequent operations
        ids = [f"{doc.metadata['id']}-{i}" for i, doc in enumerate(valid_chunks)]
        # IMPORTANT: The 'ids' parameter is not officially supported and should be removed.
        # See note below.
        self.vector_store.add_documents(valid_chunks) 
        print(f"Added {len(valid_chunks)} new chunks.")

    def delete_documents(self, doc_ids_to_delete):
        """Deletes all chunks associated with a list of document IDs."""
        if not doc_ids_to_delete:
            return

        # 1. Convert the list of IDs to a set for efficient O(1) lookups.
        #    This is much faster than checking against a list or map inside a loop.
        target_id_set = {str(doc_id) for doc_id in doc_ids_to_delete}
        
        # 2. Collect the actual docstore IDs (UUIDs) that need to be deleted.
        docstore_ids_to_delete = []
        
        # Iterate directly through the items in the docstore.
        for docstore_id, doc in self.vector_store.docstore._dict.items():
            # Check if the document's source ID is in our target set.
            if doc.metadata and str(doc.metadata.get('id')) in target_id_set:
                docstore_ids_to_delete.append(docstore_id)

        if not docstore_ids_to_delete:
            print("No matching chunks found to delete.")
            return

        # 3. Call delete with the correct list of docstore string IDs.
        self.vector_store.delete(docstore_ids_to_delete)
        print(f"Successfully deleted {len(docstore_ids_to_delete)} chunks.")

    def search(self, query, k=5):
        """Performs a similarity search."""
        return self.vector_store.similarity_search(query, k=k)