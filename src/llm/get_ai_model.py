from src.llm import HuggingFaceEmbeddingsWrapper, OpenAIEmbeddingsWrapper
from src.llm.BaseAIWrapper import BaseEmbeddingsWrapper


def get_embeddings_wrapper(model_type: str, model_name: str) -> BaseEmbeddingsWrapper:
    """
    Factory function to get the appropriate embedding wrapper.

    Args:
        model_type (str): The type of the embedding model (e.g., "openai", "huggingface").
        model_name (str): The specific name of the model (e.g., "text-embedding-ada-002", "sentence-transformers/all-MiniLM-L6-v2").

    Returns:
        BaseEmbeddingsWrapper: An instance of the concrete embedding wrapper.

    Raises:
        ValueError: If an unsupported model_type is provided.
    """
    if model_type.lower() == "openai":
        return OpenAIEmbeddingsWrapper(model_name)
    elif model_type.lower() == "huggingface":
        return HuggingFaceEmbeddingsWrapper(model_name)
    else:
        raise ValueError(f"Unsupported ai model type: {model_type}")
