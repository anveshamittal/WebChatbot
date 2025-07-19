from abc import ABC, abstractmethod
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

# 1. The Abstract Base Class (The "Product" Interface)
# Renamed for clarity
class EmbeddingModelProvider(ABC):
    """Abstract base class for all embedding model providers."""
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs

    @abstractmethod
    def get_instance(self):
        """Returns an instance of the specific embedding model."""
        pass

# 2. Concrete Implementations (The "Concrete Products")
class HuggingFaceProvider(EmbeddingModelProvider):
    """Provides a HuggingFaceEmbeddings instance."""
    def get_instance(self):
        return HuggingFaceEmbeddings(model_name=self.model_name, **self.kwargs)

class OpenAIProvider(EmbeddingModelProvider):
    """Provides an OpenAIEmbeddings instance."""
    def get_instance(self):
        # Assumes OPENAI_API_KEY is set in the environment
        return OpenAIEmbeddings(model=self.model_name, **self.kwargs)

# 3. The Factory Class
class EmbeddingModelFactory:
    """Factory for creating embedding model provider instances."""
    def __init__(self):
        self._providers = {}

    def register_provider(self, key: str, provider_class):
        """Registers a new provider class in the factory's registry."""
        self._providers[key] = provider_class

    def create(self, provider_key: str, model_name: str, **kwargs) -> EmbeddingModelProvider:
        """Creates an instance of a registered provider."""
        provider_class = self._providers.get(provider_key.lower())
        if not provider_class:
            raise ValueError(f"Unsupported provider key: {provider_key}")
        return provider_class(model_name, **kwargs)