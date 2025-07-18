from langchain_openai import OpenAIEmbeddings
from src.llm.BaseAIWrapper import BaseAIWrapper

import os

class OpenAIEmbeddingsWrapper(BaseAIWrapper):
    """
    Wrapper for OpenAIEmbeddings.
    Configures and returns an OpenAIEmbeddings instance.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)

    def get_embeddings_instance(self):
        """
        Returns an initialized OpenAIEmbeddings instance.
        """
        return OpenAIEmbeddings(
         model=self.model_name,
         base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
         api_key=os.getenv("AZURE_EMBEDDING_KEY"),
         default_query={"api-version":"preview"}
    )