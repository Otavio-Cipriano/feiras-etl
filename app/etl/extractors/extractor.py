from abc import ABC, abstractmethod


class Extractor(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract(self, data):
        raise NotImplementedError("Extractor must implement the extract method")

    @abstractmethod
    def validate(self):
        """Validate extracted data."""
        return len(self.data) > 0

    @abstractmethod
    def get_data(self):
        """Return extracted data."""
        return self.data
