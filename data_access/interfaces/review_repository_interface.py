from abc import ABC, abstractmethod

class ReviewRepositoryInterface(ABC):

    @abstractmethod
    def add_review(self, review):
        pass