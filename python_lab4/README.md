# Лабораторна 4 (Python) — GoF Strategy для виводу даних

Читає датасет `ParkingViolationCodes_March_2024.xlsx` та виводить записи у вибране сховище через патерн **Strategy**.  


---

## Технічний стек

| Python              |
|---------------------|
| `openpyxl`          |
| `kafka-python`      |
| `redis`             |
| `ABC`               | 
| `dataclass`         | 

---

## Структура проекту

```
python_lab4/
├── main.py                              ← точка входу 
├── config/
│   └── app.config.json                 ← конфігурація стратегії
├── output/
│   └── parking-violations.jsonl        ← вихідний файл (file-стратегія)
├── ParkingViolationCodes_March_2024.xlsx
└── src/
    ├── interfaces/interfaces.py         ← IDataReader, IOutputStrategy (ABC)
    ├── config/app_config.py            ← AppConfig + load_config()
    ├── readers/excel_data_reader.py    ← ExcelDataReader (openpyxl)
    ├── strategies/strategies.py        ← 4 стратегії виводу
    └── factories/output_strategy_factory.py ← OutputStrategyFactory
```

---

## Встановлення та запуск

```bash
# 1. Встановити залежності
pip install openpyxl kafka-python redis

# 2. Запустити (використовує config/app.config.json)
python main.py

# 3. Або вказати свій конфіг
python main.py config/app.config.json
```

---

## Перемикання стратегії

Змініть `"strategy"` у `config/app.config.json`:

```json
{
  "output": {
    "strategy": "file"
  }
}
```

| Значення    | Що робить                                   |
|-------------|---------------------------------------------|
| `"console"` | Виводить JSON у термінал                    |
| `"file"`    | Зберігає JSONL у `output/parking-violations.jsonl` |
| `"kafka"`   | Публікує у Kafka topic (потрібен Docker)    |
| `"redis"`   | Пушить у Redis List (потрібен Docker)       |

---

## Kafka та Redis через Docker

```bash
docker compose -f docker-compose.yml up -d
```

Зупинити:
```bash
docker compose -f docker-compose.yml down
```

---

## Відповідність TypeScript → Python

| TypeScript                      | Python                              |
|---------------------------------|-------------------------------------|
| `interface IDataReader<T>`      | `class IDataReader(ABC, Generic[T])`|
| `interface IOutputStrategy<T>`  | `class IOutputStrategy(ABC, Generic[T])` |
| `class ExcelDataReader`         | `class ExcelDataReader`             |
| `ConsoleOutputStrategy`         | `ConsoleOutputStrategy`             |
| `FileOutputStrategy`            | `FileOutputStrategy`                |
| `KafkaOutputStrategy`           | `KafkaOutputStrategy`               |
| `RedisOutputStrategy`           | `RedisOutputStrategy`               |
| `OutputStrategyFactory.create()`| `OutputStrategyFactory.create()`    |
| `loadConfig()`                  | `load_config()`                     |
