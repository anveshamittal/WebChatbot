import pathlib
import logging

logger = logging.getLogger(__name__)

def delete_index_files():
    """Contains the blocking logic for deleting files in the local FAISS index directory."""
    index_folder_path = pathlib.Path("data/faiss_index")
    if not index_folder_path.exists():
        logger.info(f"Directory not found, no action taken: {index_folder_path}")
        return {"status": "no_op", "message": "Directory not found."}

    logger.info(f"Clearing all files in: {index_folder_path}")
    deleted_count = 0
    for entry in index_folder_path.iterdir():
        try:
            if entry.is_file():
                entry.unlink()
                deleted_count += 1
        except Exception as e:
            logger.error(f"Error deleting {entry.name}: {e}")
            
    logger.info(f"Successfully deleted {deleted_count} files.")
    return {"status": "success", "files_deleted": deleted_count}