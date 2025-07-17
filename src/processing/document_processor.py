from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def load_and_parse_url(url, doc_id):
    """Loads and parses a URL into a LangChain Document."""
    try:
        loader = WebBaseLoader(url)
        data = loader.load()
        soup = BeautifulSoup(data[0].page_content, "html.parser")

        head_content = soup.head or soup.new_tag('head')
        metadata = {
            'source': url,
            'id': doc_id,
            'title': soup.title.string if soup.title else "No title",
            'meta': {
                tag['name']: tag['content']
                for tag in head_content.find_all('meta')
                if tag.get('name') and tag.get('content')
            }
        }
        body_content = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
        return Document(page_content=body_content, metadata=metadata)
    except Exception as e:
        print(f"Error loading or parsing URL {url}: {e}")
        return None

def get_text_splitter(chunk_size, chunk_overlap):
    """Initializes and returns the text splitter."""
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

def get_embeddings(model_name):
    # return OpenAIEmbeddings(
    # model=model_name,
    # base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    # api_key=os.getenv("AZURE_EMBEDDING_KEY"),
    # default_query={"api-version":"preview"}
    # )
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
