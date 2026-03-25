from abc import ABC, abstractmethod


class IDataImportService(ABC):
    @abstractmethod
    def import_from_csv(self, file_path: str) -> None:
        """Імпортує дані з CSV файлу до бази даних."""
        pass
