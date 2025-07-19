import io
import os
import pickle
import faiss
import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

class AzureBlobManager:
    """A manager for handling blob operations with Azure Storage."""

    def __init__(self, connection_string: str, container_name: str):
        if not connection_string:
            raise ValueError("Azure Storage connection string is not set.")
        
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self._create_container_if_not_exists()

    def _create_container_if_not_exists(self):
        """Creates the container, ignoring errors if it already exists."""
        try:
            self.container_client.create_container()
            print(f"Container '{self.container_client.container_name}' created.")
        except ResourceExistsError:
            print(f"Container '{self.container_client.container_name}' already exists.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def save_faiss_index_in_memory(self, index, docstore, index_to_docstore_id: dict,faiss_index_blob_name="index.faiss",datastore_blob_name ="index.pkl"):
        """Saves the FAISS index and docstore to Azure from in-memory buffers."""
        print("Saving index to Azure...")
        try:
            # Save index to an in-memory bytes buffer
            index_bytes = faiss.write_index_to_buffer(index)
            self.container_client.upload_blob(
                name=faiss_index_blob_name, 
                data=index_bytes, 
                overwrite=True
            )

            # Save docstore to an in-memory bytes buffer
            docstore_bytes = pickle.dumps((docstore, index_to_docstore_id))
            self.container_client.upload_blob(
                name=datastore_blob_name, 
                data=docstore_bytes, 
                overwrite=True
            )
            print("Successfully saved index to Azure.")
        except Exception as e:
            print(f"Failed to save index to Azure: {e}")
            raise
    
    def download_faiss_to_local(self, local_folder_path: str):
        """Downloads all blobs from the container to a local folder."""
        print(f"Downloading index files to '{local_folder_path}'...")
        os.makedirs(local_folder_path, exist_ok=True)
        
        for blob in self.container_client.list_blobs():
            blob_client = self.container_client.get_blob_client(blob.name)
            download_file_path = os.path.join(local_folder_path, blob.name)
            
            print(f"Downloading {blob.name}...")
            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
        print("Download complete.")
    
    def load_csv_as_dataframe(self, blob_name: str) -> pd.DataFrame | None:
        """Downloads a CSV from Azure and loads it directly into a pandas DataFrame."""
        print(f"Loading '{blob_name}' from Azure...")
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            if not blob_client.exists():
                print(f"Error: Blob '{blob_name}' not found.")
                return None
            
            # Read the download stream directly into pandas for memory efficiency
            stream = io.BytesIO(blob_client.download_blob().readall())
            df = pd.read_csv(stream)
            
            print(f"Successfully loaded '{blob_name}'.")
            return df
        except Exception as e:
            print(f"Error loading CSV from Azure: {e}")
            return None