from abc import ABC, abstractmethod


class IController(ABC):
    """Базовий інтерфейс контролера (презентаційний рівень)."""
    pass


class IHotelController(IController):
    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def get_by_id(self, id: int): pass


class IReviewController(IController):
    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def get_by_hotel_id(self, hotel_id: int): pass


class IDataImportController(IController):
    @abstractmethod
    def import_data(self, file_path: str): pass
