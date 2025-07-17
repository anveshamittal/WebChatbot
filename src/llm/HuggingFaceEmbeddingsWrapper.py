from langchain_huggingface import HuggingFaceEmbeddings
from src.llm.BaseAIWrapper import BaseEmbeddingsWrapper

class HuggingFaceEmbeddingsWrapper(BaseEmbeddingsWrapper):
    """
    Wrapper for HuggingFaceEmbeddings.
    Configures and returns a HuggingFaceEmbeddings instance.
    """
    def __init__(self, model_name: str):
        super().__init__(model_name)

    def get_embeddings_instance(self):
        """
        Returns an initialized HuggingFaceEmbeddings instance.
        """
        return HuggingFaceEmbeddings(
            model_name=self.model_name,
        )