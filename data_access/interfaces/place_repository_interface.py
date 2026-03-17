from abc import ABC, abstractmethod

class PlaceRepositoryInterface(ABC):

    @abstractmethod
    def create_place(self, name, address, category):
        pass