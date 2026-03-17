from data_access.models.place import Place


class PlaceRepository:

    def __init__(self, session):
        self.session = session

    def create_place(self, name, address, category):
        place = Place(
            name=name,
            address=address,
            category=category
        )
        self.session.add(place)
        self.session.flush()
        return place

    def add_specialized(self, specialized_place):
        self.session.add(specialized_place)
        self.session.flush()