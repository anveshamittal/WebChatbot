from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from bs4 import  SoupStrainer
import os
from dotenv import load_dotenv
import re

load_dotenv()

def load_and_parse_url(url, doc_id):
    """Loads and parses a URL into a LangChain Document."""
    try:
        loader = WebBaseLoader(
                web_paths=[url],
                bs_kwargs={
                    "parse_only": SoupStrainer(["main","head"])})
        
        document = loader.load()
        body_content = _clean_text(document[0].page_content)

        metadata = {
            'source': url,
            'id': doc_id
            }
        return Document(page_content=body_content, metadata=metadata)
    except Exception as e:
        print(f"Error loading or parsing URL {url}: {e}")
        return None

def get_text_splitter(chunk_size, chunk_overlap):
    """Initializes and returns the text splitter."""
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

def _clean_text(text):
    text = re.sub(r'\n{2,}', '\n', text)
    text = '\n'.join([line.strip() for line in text.split('\n')])
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def get_embeddings(model_name):
    # return OpenAIEmbeddings(
    # model=model_name,
    # base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    # api_key=os.getenv("AZURE_EMBEDDING_KEY"),
    # default_query={"api-version":"preview"}
    # )
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
