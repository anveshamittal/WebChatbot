from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from src.utils.file_utils import delete_index_files
from src.processing.batch_processor import run_batch_ingestion_logic
from src.llm.embedding_providers import EmbeddingModelFactory
from fastapi import APIRouter, Depends, Request

router = APIRouter(prefix="/admin", tags=["Admin"])

# This dependency provider gets the factory that was created in the lifespan manager
def get_embedding_factory(request: Request) -> EmbeddingModelFactory:
    return request.app.state.embedding_factory

@router.post("/run-ingestion")
async def trigger_ingestion_process(
    # 1. Inject the shared factory instance into the route
    factory: EmbeddingModelFactory = Depends(get_embedding_factory)
):
    """Triggers the batch ingestion process using the shared embedding factory."""
    
    # 2. Pass the factory as an argument to the function being run in the thread pool
    result = await run_in_threadpool(run_batch_ingestion_logic, factory)
    
    return result

@router.post("/delete-local-index")
async def trigger_delete_local_index():
    """Deletes all local index files in a non-blocking way."""
    result = await run_in_threadpool(delete_index_files)
    return result