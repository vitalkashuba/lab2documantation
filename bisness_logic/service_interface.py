from abc import ABC, abstractmethod

class TripServiceInterface(ABC):

    @abstractmethod
    def load_csv(self, path):
        pass