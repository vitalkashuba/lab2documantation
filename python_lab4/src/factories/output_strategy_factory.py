
from src.config.app_config import AppConfig
from src.interfaces.interfaces import IOutputStrategy
from src.strategies.strategies import (
    ConsoleOutputStrategy,
    FileOutputStrategy,
    KafkaOutputStrategy,
    RedisOutputStrategy,
)

DataRecord = dict[str, object]


class OutputStrategyFactory:
    """GoF Factory — створює стратегію виводу за значенням config.output.strategy."""

    @staticmethod
    def create(config: AppConfig) -> IOutputStrategy[DataRecord]:
        strategy = config.output.strategy

        if strategy == "console":
            return ConsoleOutputStrategy(pretty=config.output.console.pretty)

        if strategy == "file":
            return FileOutputStrategy(output_path=config.output.file.output_path)

        if strategy == "kafka":
            return KafkaOutputStrategy(
                brokers=config.output.kafka.brokers,
                client_id=config.output.kafka.client_id,
                topic=config.output.kafka.topic,
            )

        if strategy == "redis":
            return RedisOutputStrategy(
                url=config.output.redis.url,
                key=config.output.redis.key,
            )

        raise ValueError(f"Unsupported output strategy: '{strategy}'")
