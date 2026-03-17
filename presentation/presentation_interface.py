from abc import ABC, abstractmethod

class PresentationInterface(ABC):

    @abstractmethod
    def run(self):
        pass