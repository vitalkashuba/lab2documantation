import csv
from typing import List, Dict
from src.dal.interfaces.i_csv_reader import ICsvReader


class CsvReader(ICsvReader):
    """Зчитує CSV файл та повертає рядки як список словників."""

    def read_csv(self, file_path: str) -> List[Dict[str, str]]:
        rows = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows
