"""
index.py — точка входу для імпорту даних.


Запуск:
    python index.py                     # використовує data/reviews.csv за замовчуванням
    python index.py data/my_data.csv    # вказати інший файл
"""
import sys
from pathlib import Path

# Щоб імпорти src.* працювали при запуску з кореневої папки
sys.path.insert(0, str(Path(__file__).parent))

from src.config.container import container


def main() -> None:
    print("=== IoT Lab 3: Data Import Application (Python) ===\n")

    # Ініціалізація DI-контейнера та БД
    container.initialize()

    # Сервіс імпорту даних
    import_service = container.data_import_service()

    # Шлях до CSV (перший аргумент або за замовчуванням)
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/reviews.csv"

    print(f"\nImporting data from: {csv_path}\n")

    try:
        import_service.import_from_csv(csv_path)
        container.commit()
        print("\n=== Import completed successfully! ===")
    except Exception as e:
        print(f"\nError during data import: {e}")
        raise
    finally:
        container.close()


if __name__ == "__main__":
    main()
