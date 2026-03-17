import csv
import random
from datetime import datetime, timedelta

with open("tripadvisor_data.csv", "w", newline='', encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "user_name",
        "email",
        "place_name",
        "address",
        "category",
        "type",
        "menu",
        "stars",
        "place_rating",
        "review_text",
        "review_rating",
        "date"
    ])

    for i in range(1000):

        user_name = f"User_{random.randint(1,200)}"
        email = f"user{random.randint(1,200)}@mail.com"

        place_name = f"Place_{random.randint(1,300)}"
        address = f"Street_{random.randint(1,50)}"

        place_type = random.choice(["restaurant", "hotel"])

        category = place_type

        if place_type == "restaurant":
            menu = "pizza;pasta;salad"
            stars = ""
        else:
            menu = ""
            stars = random.randint(3,5)

        place_rating = random.randint(1,5)

        review_text = random.choice([
            "Great place",
            "Nice service",
            "Good food",
            "Average",
            "Amazing experience"
        ])

        review_rating = random.randint(1,5)

        date = datetime.now() - timedelta(days=random.randint(1,365))

        writer.writerow([
            user_name,
            email,
            place_name,
            address,
            category,
            place_type,
            menu,
            stars,
            place_rating,
            review_text,
            review_rating,
            date.strftime("%Y-%m-%d")
        ])

print("CSV generated")