import logging
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from typing import List

# Import the classes it depends on for type hinting
from src.cloud_connectors.azure_storage import AzureBlobManager
from src.llm.embedding_providers import EmbeddingModelFactory
from src.processing.document_processor import WebPageProcessor
from src.processing.rag_system import RAGSystem
from src.processing.vector_store_repository import VectorStoreRepository
from src.config import app_config

logger = logging.getLogger(__name__)

class BatchIngestionService:
    """
    Orchestrates the batch processing of documents based on a CSV instruction file.
    """
    def __init__(
        self,
        azure_manager: AzureBlobManager,
        page_processor: WebPageProcessor,
        rag_system: RAGSystem,
        instruction_blob_name: str
    ):
        """Initializes the service with all required dependencies."""
        self.azure_manager = azure_manager
        self.page_processor = page_processor
        self.rag_system = rag_system
        self.instruction_blob_name = instruction_blob_name
        self.changes_made = False
    
    def _load_instruction_file(self) -> pd.DataFrame | None:
        """Loads and validates the CSV instruction file from Azure."""
        logger.info(f"Loading instruction file: {self.instruction_blob_name}")
        df = self.azure_manager.load_csv_as_dataframe(self.instruction_blob_name)
        if df is None:
            logger.error("Exiting: Could not load CSV instruction file.")
            return None
        if not all(col in df.columns for col in ['type', 'url', 'id']):
            logger.error("Instruction file is missing required columns: 'type', 'url', 'id'.")
            return None
        return df
    
    def _process_additions(self, dataframe: pd.DataFrame):
        """Processes all 'add' instructions from the dataframe."""
        add_files = dataframe[dataframe['type'].str.lower() == 'add']
        if add_files.empty:
            return

        logger.info(f"Found {len(add_files)} document(s) to add.")
        docs_to_process = []
        for _, row in add_files.iterrows():
            doc = self.page_processor.process_url(row['url'], row['id'])
            if doc:
                docs_to_process.append(doc)

        if docs_to_process:
            chunks = []
            for doc in docs_to_process:
                chunks.extend(self.page_processor.split_document(doc))
            
            self.rag_system.add_documents(chunks)
            self.changes_made = True

    def _process_deletions(self, dataframe: pd.DataFrame):
        """Processes all 'delete' instructions from the dataframe."""
        ids_to_delete = dataframe[dataframe['type'].str.lower() == 'delete']['id'].tolist()
        if not ids_to_delete:
            return

        logger.info(f"Found {len(ids_to_delete)} document(s) to delete.")
        self.rag_system.delete_documents(ids_to_delete)
        self.changes_made = True

    def run(self, repository: VectorStoreRepository):
        """Executes the full batch ingestion process."""
        instruction_df = self._load_instruction_file()
        if instruction_df is None:
            return {"status": "failed", "reason": "Could not load instruction file."}

        self._process_additions(instruction_df)
        self._process_deletions(instruction_df)

        # if self.changes_made:
        #     logger.info("Saving updated index to Azure...")
        #     self.rag_system.save()
        #     return {"status": "success", "message": "Index updated and saved."}
        if self.changes_made:
            logger.info("Saving updated index via repository...")
        # Now we use the repository that was passed directly into this method
            repository.save(self.rag_system.vector_store)
            return {"status": "success", "message": "Index updated and saved."}
        else:
            logger.info("No changes to add or delete. Index is up to date.")
            return {"status": "success", "message": "No changes needed."}
        
# This is the main entry point function for the batch process
def run_batch_ingestion_logic(embedding_factory: EmbeddingModelFactory):
    """Initializes all services and runs the batch ingestion process."""
    logger.info("Starting batch ingestion process...")
    azure_manager = AzureBlobManager(
        connection_string=os.getenv('AZURE_STORAGE_CONNECTION_STRING'),
        container_name=app_config.azure['container_name']
    )
    
    embedding_provider = embedding_factory.create(
        app_config.embedding['model_provider'],
        app_config.embedding['embedding_model']
    )
    embedding_model = embedding_provider.get_instance()

    repository = VectorStoreRepository(
        azure_manager,
        app_config.embedding['embedding_dimension']
    )

    vector_store_instance = repository.load(embeddings=embedding_model)
    rag_system = RAGSystem(vector_store=vector_store_instance)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=app_config.chunking['chunk_size'],
        chunk_overlap=app_config.chunking['chunk_overlap']
    )
    page_processor = WebPageProcessor(text_splitter=text_splitter)

    service = BatchIngestionService(
        azure_manager=azure_manager,
        page_processor=page_processor,
        rag_system=rag_system,
        instruction_blob_name=app_config.files['csv_blob_name']
    )
    
    result = service.run(repository=repository)
    logger.info(f"Batch ingestion process finished with status: {result.get('status')}")
    return result