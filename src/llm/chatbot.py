
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import app_config
from src.processing import document_processor
from src.cloud_connectors import azure_storage
load_dotenv()

class ChatBot:
    
    def __init__(self):
        self.qa_chain = None

    def setup_qa_chain(self):
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
            azure_storage.download_faiss_index()

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
        self.qa_chain  = create_retrieval_chain(index.as_retriever(), doc_chain)
        
        print("QA chain is ready.")

    def ask_question(self, query: str):
        """Asks a question using the pre-loaded QA chain."""
        
        # 3. Add a check to ensure the setup has been run.
        if self.qa_chain is None:
            raise RuntimeError("The QA chain has not been initialized. Please run setup_qa_chain() first.")
        
        # Use the module-level qa_chain variable
        result = self.qa_chain.invoke({"input": query})
        
        sources = {doc.metadata['source'] for doc in result['context']}
        return {'answer': result["answer"], 'Sources': sources}