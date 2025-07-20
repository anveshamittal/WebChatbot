
import re
import logging
from typing import List
from bs4 import SoupStrainer
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class WebPageProcessor:
    """
    Handles loading, parsing, cleaning, and splitting content from web pages.
    """
    def __init__(self, text_splitter: RecursiveCharacterTextSplitter):
        """
        Initializes the processor with a configured text splitter.

        Args:
            text_splitter: An instance of a LangChain text splitter.
        """
        self.text_splitter = text_splitter
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Cleans extracted text by removing excessive whitespace and newlines.
        """
        text = re.sub(r'\n{2,}', '\n', text)
        text = '\n'.join([line.strip() for line in text.split('\n')])
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()
    
    def process_url(self, url: str, doc_id: str) -> Document | None:
        """
        Loads, parses, and cleans content from a URL into a single Document.
        """
        logger.info(f"Processing URL: {url}")
        try:
            strainer = SoupStrainer(["main", "head"])
            loader = WebBaseLoader(
                web_paths=[url],
                bs_kwargs={"parse_only": strainer}
            )
            documents = loader.load()
            if not documents:
                logger.warning(f"No documents were loaded from URL {url}.")
                return None

            cleaned_content = self._clean_text(documents[0].page_content)
            
            # The document ID should be part of the metadata dictionary
            metadata = {'source': url, 'id': doc_id}

            return Document(page_content=cleaned_content, metadata=metadata)

        except Exception:
            logger.exception(f"Failed to load or parse URL '{url}'.")
            return None
        
    def split_document(self, document: Document) -> List[Document]:
        """Splits a single large Document into smaller chunks."""
        if not document:
            return []
        logger.info(f"Splitting document from source: {document.metadata.get('source')}")
        return self.text_splitter.split_documents([document])