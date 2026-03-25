from abc import ABC, abstractmethod
from typing import List, Dict


class ICsvReader(ABC):
    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict[str, str]]:
        """Зчитує CSV файл і повертає список рядків як словники."""
        pass
