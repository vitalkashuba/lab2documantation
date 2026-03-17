"""from .repository_interface import RestaurantRepositoryInterface

class RestaurantRepository(RestaurantRepositoryInterface):

    def __init__(self, session):
        self.session = session

    def add_restaurant(self, restaurant):
        self.session.add(restaurant)

    def save(self):
        self.session.commit()"""