from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def save(self, data):
        """Save data to the storage backend."""
        pass

    @abstractmethod
    def load(self):
        """Load data from the storage backend."""
        pass
