import csv
from datetime import datetime
from data_access.models.user import User
from data_access.models.review import Review
from data_access.models.place import Place
from data_access.models.restaurant import  Restaurant
from data_access.models.hotel import  Hotel
from .service_interface import TripServiceInterface


class TripService(TripServiceInterface):

    def __init__(self, user_repo, place_repo, review_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = review_repo

    def load_csv(self, path):

        with open(path, newline='', encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:


                user = self.user_repo.get_or_create(
                    name=row["user_name"],
                    email=row["email"]
                )


                place = self.place_repo.create_place(
                    name=row["place_name"],
                    address=row["address"],
                    category=row["category"]
                )



                if row["type"] == "restaurant":

                    restaurant = Restaurant(
                        id=place.id,
                        menu=row["menu"],
                        rating=int(row["place_rating"])
                    )

                    self.place_repo.add_specialized(restaurant)

                elif row["type"] == "hotel":

                    hotel = Hotel(
                        id=place.id,
                        stars=int(row["stars"]),
                        user_rating=int(row["place_rating"])
                    )

                    self.place_repo.add_specialized(hotel)


                review = Review(
                    text=row["review_text"],
                    rating=int(row["review_rating"]),
                    date=datetime.strptime(row["date"], "%Y-%m-%d"),
                    user_id=user.id,
                    place_id=place.id
                )

                self.review_repo.add_review(review)

        self.review_repo.save()