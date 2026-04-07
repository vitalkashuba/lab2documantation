
import json
import os

from src.interfaces.interfaces import IOutputStrategy

DataRecord = dict[str, object]


# ── ConsoleOutputStrategy ─────────────────────────────────────────────────────
class ConsoleOutputStrategy(IOutputStrategy[DataRecord]):
    """Виводить записи у консоль у форматі JSON."""

    def __init__(self, pretty: bool = True):
        self._pretty = pretty

    def write(self, records: list[DataRecord]) -> None:
        for record in records:
            if self._pretty:
                print(json.dumps(record, ensure_ascii=False, indent=2))
            else:
                print(json.dumps(record, ensure_ascii=False))


# ── FileOutputStrategy ────────────────────────────────────────────────────────
class FileOutputStrategy(IOutputStrategy[DataRecord]):
    """Записує записи у JSONL-файл (один JSON на рядок)."""

    def __init__(self, output_path: str):
        self._output_path = output_path

    def write(self, records: list[DataRecord]) -> None:
        abs_path = os.path.abspath(self._output_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        with open(abs_path, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"Saved {len(records)} records to {abs_path}")


# ── KafkaOutputStrategy ───────────────────────────────────────────────────────
class KafkaOutputStrategy(IOutputStrategy[DataRecord]):
    """Публікує записи у Kafka-топік через kafka-python."""

    def __init__(self, brokers: list[str], client_id: str, topic: str):
        self._brokers   = brokers
        self._client_id = client_id
        self._topic     = topic

    def write(self, records: list[DataRecord]) -> None:
        # Імпортуємо тут, щоб не падати при запуску без kafka-python
        try:
            from kafka import KafkaProducer  # type: ignore
        except ImportError:
            raise ImportError("Встановіть kafka-python: pip install kafka-python")

        producer = KafkaProducer(
            bootstrap_servers=self._brokers,
            client_id=self._client_id,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
        )

        try:
            for record in records:
                producer.send(self._topic, value=record)
            producer.flush()
            print(f"Published {len(records)} records to Kafka topic '{self._topic}'")
        finally:
            producer.close()


# ── RedisOutputStrategy ───────────────────────────────────────────────────────
class RedisOutputStrategy(IOutputStrategy[DataRecord]):
    """Пушить записи у Redis List через бібліотеку redis-py."""

    def __init__(self, url: str, key: str):
        self._url = url
        self._key = key

    def write(self, records: list[DataRecord]) -> None:
        try:
            import redis as redis_lib  # type: ignore
        except ImportError:
            raise ImportError("Встановіть redis: pip install redis")

        client = redis_lib.from_url(self._url, decode_responses=True)

        try:
            if records:
                values = [json.dumps(r, ensure_ascii=False) for r in records]
                client.rpush(self._key, *values)
            print(f"Pushed {len(records)} records to Redis list '{self._key}'")
        finally:
            client.close()
