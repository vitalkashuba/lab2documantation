"""
Генератор тестових CSV даних.

Запуск:
    python src/utils/csv_generator.py              # 1000 рядків → data/reviews.csv
    python src/utils/csv_generator.py 2000         # 2000 рядків → data/reviews.csv
    python src/utils/csv_generator.py 500 out.csv  # 500 рядків → out.csv
"""
import csv
import random
import os
import sys
from datetime import datetime, timedelta


class CsvGenerator:
    """Генерує CSV файл з тестовими даними готелів та відгуків."""

    HOTEL_NAMES = [
        "Grand Hotel Imperial", "Sunset Beach Resort", "Mountain View Lodge",
        "City Center Plaza",    "Royal Palace Hotel",  "Ocean Paradise",
        "Metropolitan Inn",     "Garden Pavilion",     "Sky Tower Hotel",
        "Riverside Manor",      "Crystal Palace",      "Golden Gate Inn",
        "Emerald Resort",       "Silver Star Hotel",   "Diamond Suites",
        "Pearl Harbor Hotel",   "Sapphire Lodge",      "Ruby Tower",
        "Amber Inn",            "Jade Garden Hotel",
    ]
    STREETS = [
        "Main Street", "Oak Avenue", "Maple Drive", "Pine Street", "Cedar Lane",
        "Elm Road", "Park Boulevard", "Lake Avenue", "River Road", "Hill Street",
        "Market Square", "Church Street", "School Road", "Station Avenue", "Bridge Street",
    ]
    CITIES = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    ]
    COMMENTS = [
        "Excellent service and amazing food!",
        "Great experience, will definitely come back.",
        "Food was good but service could be better.",
        "Outstanding quality and atmosphere!",
        "Average experience, nothing special.",
        "Disappointed with the quality.",
        "Absolutely loved it! Highly recommend.",
        "Good value for money.",
        "Not what I expected, quite disappointing.",
        "Perfect place for a special occasion!",
        "Clean and comfortable, staff was friendly.",
        "Beautiful location and great amenities.",
        "Room was spacious and well-maintained.",
        "Breakfast was delicious!",
        "Wi-Fi was slow but everything else was good.",
    ]
    FIRST_NAMES = [
        "John", "Emma", "Michael", "Olivia", "William", "Ava", "James", "Sophia",
        "Robert", "Isabella", "David", "Mia", "Richard", "Charlotte", "Joseph",
        "Amelia", "Thomas", "Harper", "Daniel", "Evelyn",
    ]
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    ]
    STATUSES = ["PENDING", "APPROVED", "REJECTED"]
    DOMAINS  = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]

    # ─────────────────────────────────────────────────────────────────────────
    def _make_user(self, first: str, last: str) -> dict:
        num      = random.randint(1, 999)
        username = f"{first.lower()}.{last.lower()}{num}"
        email    = f"{first.lower()}.{last.lower()}{num}@{random.choice(self.DOMAINS)}"
        return {"username": username, "email": email}

    def _random_address(self) -> str:
        return f"{random.randint(1, 9999)} {random.choice(self.STREETS)}, {random.choice(self.CITIES)}"

    def _random_date(self) -> str:
        start = datetime(2020, 1, 1)
        delta = (datetime.now() - start).days
        return (start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d")

    # ─────────────────────────────────────────────────────────────────────────
    def generate(self, row_count: int, output_path: str) -> None:
        print(f"Generating CSV file with {row_count} rows...")

        # Унікальні користувачі (~10% від row_count, мінімум 50)
        users_count = max(50, row_count // 10)
        users = [
            self._make_user(random.choice(self.FIRST_NAMES), random.choice(self.LAST_NAMES))
            for _ in range(users_count)
        ]

        # Готелі
        hotels = [
            {"name": name, "address": self._random_address(), "stars": random.randint(1, 5)}
            for name in self.HOTEL_NAMES
        ]

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        headers = [
            "username", "userEmail", "entityType", "entityName",
            "entityAddress", "stars", "comment", "rating", "date", "status",
        ]

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(headers)
            for _ in range(row_count):
                user  = random.choice(users)
                hotel = random.choice(hotels)
                writer.writerow([
                    user["username"],
                    user["email"],
                    "hotel",
                    hotel["name"],
                    hotel["address"],
                    hotel["stars"],
                    random.choice(self.COMMENTS),
                    random.randint(1, 5),
                    self._random_date(),
                    random.choice(self.STATUSES),
                ])

        print(f"CSV file generated: {output_path}")
        print(f"Rows: {row_count} | Users: {users_count} | Hotels: {len(hotels)}")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    row_count   = int(sys.argv[1])   if len(sys.argv) > 1 else 1000
    output_path = sys.argv[2]        if len(sys.argv) > 2 else os.path.join("data", "reviews.csv")
    CsvGenerator().generate(row_count, output_path)
