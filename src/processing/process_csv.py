from src.processing import document_processor
from src.processing.rag_system import RAGSystem
from src.config import app_config
from src.cloud_connectors  import azure_storage
import os
from dotenv import load_dotenv
load_dotenv()

def process_csv():
    """Main function to run the RAG system update process."""
    # --- 1. Initialization ---
    container_client = azure_storage.get_container_client(
        os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        app_config.azure['container_name']
    )

 # --- 2. Load Instructions and Initialize RAG System ---
    file = azure_storage.load_csv_from_azure(container_client, app_config.files['csv_blob_name'])
    if file is None:
        print("Exiting: Could not load CSV instruction file.")
        return

    embeddings = document_processor.initialize_embedding_model("huggingface",app_config.embedding['embedding_model'])

    text_splitter = document_processor.create_text_splitter(
        app_config.chunking['chunk_size'],
        app_config.chunking['chunk_overlap']
    )

    rag = RAGSystem(container_client, embeddings, app_config)

    # --- 3. Process Documents for Addition ---
    docs_to_add = []
    add_files = file[file['type'].str.lower() == 'add']
    for _, row in add_files.iterrows():
        doc = document_processor.load_and_parse_url(row['url'], row['id'])
        if doc:
            docs_to_add.append(doc)
    
    if docs_to_add:
        print(f"\nAdding {len(docs_to_add)} new document(s)...")
        rag.add_documents(docs_to_add, text_splitter)

    # --- 4. Process Documents for Deletion ---
    ids_to_delete = file[file['type'].str.lower() == 'delete']['id'].tolist()
    if ids_to_delete:
        print(f"\nDeleting document(s) with IDs: {ids_to_delete}...")
        rag.delete_documents(ids_to_delete)

    # --- 5. Save the final state ---

    if docs_to_add or ids_to_delete:
        rag.save()
        print("\nSaving updated index to Azure...")
    else:
        print("\nNo changes to add or delete. Index is up to date.")

    return 'csv processed successfully!'

    # # --- 6. Perform a test search ---
    # print("\n--- Performing a test search ---")
    # search_query = "What are the benefits of SWIFT for corporates?"
    # results = rag.search(search_query)

    # if results:
    #     print(f"Found {len(results)} results for '{search_query}':")
    #     for i, res in enumerate(results):
    #         print(f"\nResult {i+1}:")
    #         print(f"  Source: {res.metadata.get('source', 'N/A')}")
    #         print(f"  ID: {res.metadata.get('id', 'N/A')}")
    #         print(f"  Content: {res.page_content[:200]}...")
    # else:
    #     print("No results found.")