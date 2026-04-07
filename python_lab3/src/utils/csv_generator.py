"""
csvGenerator.py — генерує тестовий CSV-файл з даними.
Аналог src/utils/csvGenerator.ts з оригінального проекту.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

HOTELS = [
    ("Grand Palace Hotel",   "вул. Хрещатик, 1, Київ",      5),
    ("Lviv Classic Hotel",   "пл. Ринок, 10, Львів",         4),
    ("Odessa Pearl",         "Приморський бульвар, 5, Одеса", 4),
    ("Carpathian Resort",    "вул. Лісова, 3, Буковель",     3),
    ("Kharkiv Business Inn", "пр. Науки, 42, Харків",        3),
    ("Dnipro Riverside",     "Набережна, 7, Дніпро",         4),
    ("Kyiv Budget Stay",     "вул. Борщагівська, 22, Київ",  2),
    ("Eco Lodge Polissia",   "с. Тур'я, Волинська обл.",     3),
]

USERS = [
    ("olena_mand",  "olena@example.com"),
    ("ivan_drob",   "ivan@example.com"),
    ("sofiia_kh",   "sofiia@example.com"),
    ("mykola_b",    "mykola@example.com"),
    ("daria_pol",   "daria@example.com"),
    ("andrii_t",    "andrii@example.com"),
    ("kateryna_v",  "kateryna@example.com"),
    ("vasyl_s",     "vasyl@example.com"),
    ("oksana_l",    "oksana@example.com"),
    ("pavlo_h",     "pavlo@example.com"),
]

COMMENTS = [
    "Чудовий готель, дуже задоволений обслуговуванням!",
    "Непоганий варіант за таку ціну.",
    "Сніданок залишав бажати кращого, але номер зручний.",
    "Відмінне розташування, зручна парковка.",
    "Персонал дуже привітний, обов'язково повернуся.",
    "Трохи шумно через будівництво поруч.",
    "Бездоганна чистота, сучасний ремонт.",
    "Зручне розташування, близько до центру.",
    "Wi-Fi повільний, але загалом нормально.",
    "Перевершив усі очікування, рекомендую!",
    "Непоганий готель, але ціна завелика.",
    "Дуже зручне ліжко, добре виспався.",
]

STATUSES = ["PENDING", "APPROVED", "APPROVED", "APPROVED", "REJECTED"]


def random_date(start_year: int = 2022, end_year: int = 2024) -> str:
    start = datetime(start_year, 1, 1)
    delta = datetime(end_year, 12, 31) - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")


def generate_csv(output_path: str = "data/reviews.csv", n_rows: int = 100) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "username", "userEmail",
        "entityType", "entityName", "entityAddress", "stars",
        "comment", "rating", "date", "status",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(n_rows):
            user    = random.choice(USERS)
            hotel   = random.choice(HOTELS)
            writer.writerow({
                "username":      user[0],
                "userEmail":     user[1],
                "entityType":    "hotel",
                "entityName":    hotel[0],
                "entityAddress": hotel[1],
                "stars":         hotel[2],
                "comment":       random.choice(COMMENTS),
                "rating":        random.randint(1, 5),
                "date":          random_date(),
                "status":        random.choice(STATUSES),
            })

    print(f"Generated {n_rows} rows → {output_path}")


if __name__ == "__main__":
    generate_csv()
