from abc import ABC, abstractmethod

class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_or_create(self, name, email):
        pass