from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
from langchain.docstore.document import Document
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.extract_data import fetch_data
from src.config_loader import chunking_config

def chunk_documents(docs, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks= splitter.split_text(docs)
     
    return chunks

CHUNKS_OUTPUT_PATH = 'chunks.pkl' # The output of this script

def create_chunks():
    """
    Main function for this module. Fetches data using the extractor,
    splits it into chunks based on the loaded configuration, 
    and saves the chunks to a file.
    """
    # Step 1: Fetch the initial documents using the dedicated extractor
    initial_docs = fetch_data()
    if not initial_docs:
        print("No documents were fetched. Exiting.")
        return

    # Step 2: Load chunking configuration
    config = chunking_config()
    # print(f"\nUsing chunking config: size={config['chunk_size']}, overlap={config['chunk_overlap']}")

    # Step 3: Initialize the text splitter with parameters from the config
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config['chunk_size'], 
        chunk_overlap=config['chunk_overlap'],
        length_function=len
    )
    
    all_chunked_docs = []
    # print("\nChunking documents...")
    for doc in initial_docs:
        # Split the main text into smaller chunks
        chunks = text_splitter.split_text(doc["page_content"])
        
        # Create a LangChain Document for each chunk with metadata
        for i, chunk_text in enumerate(chunks):
            chunk_doc = Document(
                page_content=chunk_text, 
                metadata={
                    'source': doc["url"],
                    'original_id': doc["id"],
                    'chunk_id': i 
                }
            )
            all_chunked_docs.append(chunk_doc)
    
    # if not all_chunked_docs:
    #     print("No chunks were created. Exiting.")
    #     return
    
    # print(f"Total chunks created: {len(all_chunked_docs)}")

    # Step 4: Save the chunked documents to a file
    print(f"Saving chunked documents to '{CHUNKS_OUTPUT_PATH}'...")
    with open(CHUNKS_OUTPUT_PATH, 'wb') as f:
        pickle.dump(all_chunked_docs, f)
        
    # print("\nChunking process complete!")

if __name__ == '__main__':
    # This allows the script to be run directly if needed
    create_chunks()
