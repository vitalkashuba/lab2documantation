
import openpyxl
from src.interfaces.interfaces import IDataReader

DataRecord = dict[str, object]


class ExcelDataReader(IDataReader[DataRecord]):
    """Читає XLSX і повертає список рядків як словників {колонка: значення}."""

    def read(self, file_path: str) -> list[DataRecord]:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)

        sheet_name = wb.sheetnames[0]
        if not sheet_name:
            raise ValueError("XLSX file does not contain any sheets.")

        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))

        if not rows:
            return []

        # Перший рядок — заголовки
        headers = [str(h) if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]

        records: list[DataRecord] = []
        for row in rows[1:]:
            record: DataRecord = {}
            for header, value in zip(headers, row):
                # Конвертуємо значення у рядок (як raw: false у xlsx npm)
                record[header] = str(value) if value is not None else None
            records.append(record)

        wb.close()
        return records
