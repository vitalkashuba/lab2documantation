
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IDataReader(ABC, Generic[T]):
    """Читає дані з джерела і повертає список записів."""
    @abstractmethod
    def read(self, file_path: str) -> list[T]:
        ...


class IOutputStrategy(ABC, Generic[T]):
    """Виводить список записів у певне сховище (GoF Strategy)."""
    @abstractmethod
    def write(self, records: list[T]) -> None:
        ...
