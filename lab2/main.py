import sys
import os
from src.config.container import container


def main() -> None:
    print("=== IoT Lab 2: Data Import Application (Python + SQLAlchemy) ===\n")

    # Ініціалізація DI-контейнера (створює БД + реєструє залежності)
    container.configure()

    # Отримуємо сервіс через інтерфейс IDataImportService
    service = container.resolve()

    # Шлях до CSV файлу з аргументу або за замовчуванням
    csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "reviews.csv")

    print(f"\nImporting data from: {csv_path}\n")
    service.import_from_csv(csv_path)
    print("\n=== Import completed successfully! ===")


if __name__ == "__main__":
    main()
