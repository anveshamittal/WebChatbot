from abc import ABC, abstractmethod
class EmbeddingModelProvider(ABC):
    """
    Abstract Base Class for all embedding model wrappers.
    Defines the contract for how to get an embedding instance.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def get_embeddings_instance(self):
        """
        Abstract method to be implemented by concrete classes.
        Must return an instance of the specific embedding model.
        """
        pass