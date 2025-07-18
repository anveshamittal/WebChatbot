import io
import pickle
import faiss
import tempfile
import os
from azure.storage.blob import BlobServiceClient
from src.config_loader import AppConfig
app_config = AppConfig()
def get_container_client(connection_string, container_name):
    """Initializes and returns a Blob Container Client."""
    if not connection_string:
        raise ValueError("Azure Storage connection string is not set.")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    try:
        container_client.create_container()
        print(f"Container '{container_name}' created.")
    except Exception as e:
        if "ContainerAlreadyExists" in str(e):
            print(f"Container '{container_name}' already exists.")
        else:
            raise e
            
    return container_client

def load_csv_from_azure(container_client, blob_name):
    """Downloads a CSV from Azure and loads it into a pandas DataFrame."""
    print(f"Attempting to load '{blob_name}' from Azure...")
    try:
        blob_client = container_client.get_blob_client(blob_name)
        if not blob_client.exists():
            print(f"Error: Blob '{blob_name}' not found in container '{container_client.container_name}'.")
            return None
        
        downloader = blob_client.download_blob()
        blob_content = downloader.readall()
        csv_file = io.StringIO(blob_content.decode('utf-8'))
        
        import pandas as pd
        df = pd.read_csv(csv_file)
        print(f"Successfully loaded '{blob_name}' from Azure.")
        return df
    except Exception as e:
        print(f"Error loading CSV from Azure: {e}")
        return None

def load_index_from_azure(container_client, index_blob_name, docstore_blob_name):
    """Downloads and loads the FAISS index and docstore from Azure."""
    print("Attempting to load index from Azure...")
    index_blob = container_client.get_blob_client(index_blob_name)
    docstore_blob = container_client.get_blob_client(docstore_blob_name)

    if not (index_blob.exists() and docstore_blob.exists()):
        return None, None, None

    print("Found existing index in Azure. Downloading...")
    with tempfile.TemporaryDirectory() as temp_dir:
        index_path = os.path.join(temp_dir, index_blob_name)
        docstore_path = os.path.join(temp_dir, docstore_blob_name)

        with open(index_path, "wb") as f:
            f.write(index_blob.download_blob().readall())
        with open(docstore_path, "wb") as f:
            f.write(docstore_blob.download_blob().readall())

        index = faiss.read_index(index_path)
        with open(docstore_path, 'rb') as f:
            docstore, index_to_docstore_id = pickle.load(f)
    
    print("Successfully loaded index from Azure.")
    return index, docstore, index_to_docstore_id

def save_index_to_azure(container_client, index, docstore, index_to_docstore_id, index_blob_name, docstore_blob_name):
    """Saves the FAISS index and docstore to Azure."""
    print("Saving index to Azure Blob Storage...")
    with tempfile.TemporaryDirectory() as temp_dir:
        index_path = os.path.join(temp_dir, index_blob_name)
        docstore_path = os.path.join(temp_dir, docstore_blob_name)

        faiss.write_index(index, index_path)
        with open(docstore_path, 'wb') as f:
            pickle.dump((docstore, index_to_docstore_id), f)

        with open(index_path, "rb") as data:
            container_client.upload_blob(name=index_blob_name, data=data, overwrite=True)
        with open(docstore_path, "rb") as data:
            container_client.upload_blob(name=docstore_blob_name, data=data, overwrite=True)
    
    print("Successfully saved index to Azure.")

def download_faiss_index():
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name =app_config.azure['container_name']
    index_folder = "data/faiss_index" # A local folder to store the index

    if not os.path.exists(index_folder):
        os.makedirs(index_folder)
        print(f"Created local directory: {index_folder}")

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        download_file_path = os.path.join(index_folder, blob.name)
        print(f"Downloading {blob.name} to {download_file_path}")
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())