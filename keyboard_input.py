
from abc import ABC, abstractmethod

class KeyBoardInput(ABC):
    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def is_key_pressed(self, key: str) -> bool:
        pass

    @abstractmethod
    def read_key(self) -> str:
        pass