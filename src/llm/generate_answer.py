
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config_loader import AppConfig
from src.processing import document_processor
from src.cloud_connectors import azure_handler
load_dotenv()
app_config = AppConfig()
def setup_qa_chain():
    """
    Loads all necessary components and creates the QA chain.
    This function should be called only ONCE.
    """
    print("Loading models and FAISS index...") # Added for clarity
    embeddings = document_processor.initialize_embedding_model("huggingface",app_config.embedding['embedding_model'])
    # Load the index from disk
    index_folder = "data/faiss_index" 
    base_directory = os.path.dirname(index_folder) # e.g., 'data'
    faiss_file = os.path.join(base_directory, app_config.files['faiss_index_blob_name'])
    datastore_file = os.path.join(base_directory, app_config.files['datastore_blob_name'])

    if not os.path.exists(faiss_file) or not os.path.exists(datastore_file):
        azure_handler.download_faiss_index()

    index = FAISS.load_local(
        index_folder, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    llm = ChatOpenAI(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        default_query={"api-version": "preview"}
    )
    
    parser = StrOutputParser()
    
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant for tietoevry company. if you do not know the answer say i don't know the answer please contact us on https://www.tietoevry.com/en/contact-tietoevry/

        Data:
        {context}

        Question: {input}
        Answer:"""
    )
    
    # Create the chain that combines documents
    doc_chain = create_stuff_documents_chain(llm, prompt, output_parser=parser)
    
    # Create the final retrieval chain
    retrieval_chain = create_retrieval_chain(index.as_retriever(), doc_chain)
    
    print("QA chain is ready.")
    return retrieval_chain

# --- Main execution part ---

# 1. Load the chain only once when your application starts.
qa_chain = setup_qa_chain()

def ask_question(query):
    """
    Asks a question using the pre-loaded QA chain.
    """
    # 2. Reuse the chain for every question.
    result = qa_chain.invoke({"input": query})
    return {'answer' : result["answer"], 'Sources':{doc.metadata['source'] for doc in result['context']}}