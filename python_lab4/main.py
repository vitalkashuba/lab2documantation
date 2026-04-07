"""
main.py — точка входу програми.
Аналог src/main.ts:
  1. Завантажує конфіг (app.config.json)
  2. Читає XLSX через ExcelDataReader
  3. Виводить через обрану стратегію (OutputStrategyFactory)

Запуск:
    python main.py                        # використовує config/app.config.json
    python main.py config/app.config.json # явний шлях до конфігу
"""
import sys
import os

# Щоб src.* імпорти працювали при запуску з кореневої папки проекту
sys.path.insert(0, os.path.dirname(__file__))

from src.config.app_config import load_config
from src.readers.excel_data_reader import ExcelDataReader
from src.factories.output_strategy_factory import OutputStrategyFactory


def main() -> None:
    try:
        # 1. Завантажити конфіг
        config_path = sys.argv[1] if len(sys.argv) > 1 else None
        config = load_config(config_path)

        # 2. Визначити шлях до XLSX відносно розташування main.py
        base_dir   = os.path.dirname(__file__)
        input_path = os.path.abspath(os.path.join(base_dir, config.input.file_path))

        # 3. Прочитати дані
        reader  = ExcelDataReader()
        records = reader.read(input_path)
        print(f"Read {len(records)} records from {input_path}")

        # 4. Вивести через стратегію
        strategy = OutputStrategyFactory.create(config)
        strategy.write(records)

        print("Lab-4 pipeline completed successfully.")

    except Exception as e:
        print(f"Lab-4 pipeline failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
