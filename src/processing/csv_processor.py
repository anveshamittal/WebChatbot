
from src.cloud_connectors.azure_storage import AzureBlobManager
from src.processing.document_processor import WebPageProcessor
from src.processing.rag_system import RAGSystem
from src.processing.vector_store_repository import VectorStoreRepository
from src.llm.embedding_providers import EmbeddingModelFactory
from src.processing.batch_processor import BatchIngestionService
from src.config import app_config
import os
from dotenv import load_dotenv
load_dotenv()

azure_manager = AzureBlobManager(connection_string=os.getenv('AZURE_STORAGE_CONNECTION_STRING'),container_name=app_config.azure['container_name'])
embedding_model = EmbeddingModelFactory().create(app_config.embedding['model_provider'],app_config.embedding['embedding_model'])
repository = VectorStoreRepository(azure_manager, app_config.embedding['embedding_dimension'])

vector_store_instance = repository.load(embeddings=embedding_model)

rag_system = RAGSystem(vector_store=vector_store_instance)

BatchIngestionService(azure_manager=azure_manager,
                      page_processor=WebPageProcessor(),rag_system=rag_system,instruction_blob_name=app_config.files['csv_blob_name']).run()