# TripAdvisor-like Platform — Python Version

Серверний додаток на **Python + SQLAlchemy + SQLite**, що реалізує платформу для управління готелями та відгуками.  


---

## Технічний стек

| Технологія   | Призначення                                    | Аналог (TS)     |
|--------------|------------------------------------------------|-----------------|
| Python 3.11+ | Мова програмування                             | TypeScript      |
| SQLAlchemy   | ORM для роботи з базою даних                   | TypeORM         |
| SQLite       | Вбудована реляційна база даних                 | SQLite          |
| csv (stdlib) | Парсинг CSV-файлів при імпорті даних           | csv-parser      |
| ABC          | Абстрактні класи замість інтерфейсів           | TypeScript interfaces |

---

## Архітектура (DAL → BLL → PL)

```
src/
├── domain/
│   ├── entities/models.py          # SQLAlchemy ORM-моделі (Hotel, User, Review, ReviewableEntity)
│   └── enums/review_status.py     # ReviewStatus enum (PENDING / APPROVED / REJECTED)
├── dal/
│   ├── interfaces/repositories.py # Абстрактні класи (ICsvReader, IUserRepository, ...)
│   ├── repositories/repositories.py # Реалізації репозиторіїв
│   └── data_source.py             # Конфігурація SQLAlchemy (аналог dataSource.ts)
├── bll/
│   ├── interfaces/i_data_import_service.py
│   └── services/data_import_service.py  # Бізнес-логіка імпорту
├── config/
│   └── container.py               # DI-контейнер (аналог TSyringe container.ts)
└── utils/
    └── csv_generator.py           # Генератор тестових CSV-даних
data/
└── reviews.csv                    # Тестовий набір даних
index.py                           # Точка входу (аналог src/index.ts)
```

---

## Встановлення та запуск

```bash
# 1. Встановити залежності
pip install sqlalchemy

# 2. Згенерувати тестові дані (CSV)
python src/utils/csv_generator.py

# 3. Імпортувати дані в SQLite
python index.py

# 4. Або вказати власний CSV-файл
python index.py data/my_data.csv
```

---

## Модель даних

```
ReviewableEntity (базовий клас, таблиця з discriminator-колонкою "type")
└── Hotel          (stars, reviews[])

User               (username, email, reviews[])

Review             (comment, rating, date, status, FK→User, FK→Hotel)
```

### Відповідність TypeScript → Python

| TypeScript (TypeORM)          | Python (SQLAlchemy)                        |
|-------------------------------|--------------------------------------------|
| `@Entity() @TableInheritance` | `DeclarativeBase` + `__mapper_args__`      |
| `@ChildEntity()`              | `polymorphic_identity`                     |
| `@PrimaryGeneratedColumn()`   | `Column(Integer, primary_key=True)`        |
| `@OneToMany / @ManyToOne`     | `relationship()` + `ForeignKey`            |
| `@injectable()` TSyringe      | `Container` клас із ручною реєстрацією     |
| `interface I...`              | `ABC` абстрактні класи                     |
| `enum ReviewStatus`           | `class ReviewStatus(str, Enum)`            |

---

## CSV формат

```csv
username,userEmail,entityType,entityName,entityAddress,stars,comment,rating,date,status
olena_mand,olena@example.com,hotel,Grand Palace Hotel,"вул. Хрещатик, 1, Київ",5,Чудовий готель!,5,2023-06-15,APPROVED
```
