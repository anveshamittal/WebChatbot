"""
This module provides utility functions for loading, parsing, and processing
web content for use in a RAG (Retrieval-Augmented Generation) pipeline.
"""

# Standard library imports
import re
from typing import Optional

# Third-party imports
from bs4 import SoupStrainer
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Local application imports
from src.llm.get_ai_model import get_embeddings_wrapper


def _clean_text(text: str) -> str:
    """
    Cleans extracted text by removing excessive whitespace and newlines.

    This helper function performs the following operations:
    1.  Collapses multiple consecutive newlines into a single newline.
    2.  Strips leading/trailing whitespace from each individual line.
    3.  Collapses multiple consecutive spaces into a single space.
    4.  Removes any leading/trailing whitespace from the entire text block.

    Args:
        text: The raw string content to be cleaned.

    Returns:
        The cleaned text as a string.
    """
    # Collapse 2 or more newlines into a single one
    text = re.sub(r'\n{2,}', '\n', text)
    # Remove leading/trailing whitespace from each line for consistent formatting
    text = '\n'.join([line.strip() for line in text.split('\n')])
    # Collapse 2 or more spaces into a single one
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def load_and_parse_url(url: str, doc_id: str) -> Optional[Document]:
    """
    Loads content from a URL, parses it, and returns a LangChain Document.

    This function uses WebBaseLoader to fetch a webpage. It specifically
    parses only the <main> and <head> HTML tags for content, which helps
    in excluding irrelevant boilerplate like navbars and footers. The
    extracted text is then cleaned and packaged into a LangChain Document
    with custom metadata.

    Args:
        url: The URL of the webpage to load.
        doc_id: A unique identifier to assign to the document's metadata.

    Returns:
        A LangChain Document object containing the cleaned page content
        and metadata, or None if an error occurs.
    """
    try:
        # Use SoupStrainer to focus parsing on the most relevant HTML tags.
        # This improves speed and reduces noise from irrelevant content.
        strainer = SoupStrainer(["main", "head"])
        loader = WebBaseLoader(
            web_paths=[url],
            bs_kwargs={"parse_only": strainer}
        )

        # Load the document from the specified URL
        documents = loader.load()
        if not documents:
            print(f"Warning: No documents were loaded from URL {url}.")
            return None

        # Clean the extracted page content using the helper function
        cleaned_content = _clean_text(documents[0].page_content)

        # Structure the metadata for the document
        metadata = {'source': url, 'id': doc_id}

        # Create and return a new Document object
        return Document(page_content=cleaned_content, metadata=metadata,ID=doc_id)

    except Exception as e:
        # Log any exceptions that occur during the process
        print(f"Error: Failed to load or parse URL '{url}'. Reason: {e}")
        return None


def create_text_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> RecursiveCharacterTextSplitter:
    """
    Creates and configures a text splitter instance.

    This factory function initializes a `RecursiveCharacterTextSplitter`,
    which is effective for splitting text for language models. It tries to
    keep related pieces of text together by splitting on a hierarchy of
    separators (e.g., "\\n\\n", "\\n", " ", "").

    Args:
        chunk_size: The maximum number of characters in each chunk.
        chunk_overlap: The number of characters to overlap between adjacent
                       chunks to preserve context.

    Returns:
        An instance of RecursiveCharacterTextSplitter.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )