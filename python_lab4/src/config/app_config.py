
import json
import os
from dataclasses import dataclass, field
from typing import Literal

OutputStrategyName = Literal["console", "file", "kafka", "redis"]


@dataclass
class ConsoleConfig:
    pretty: bool = True


@dataclass
class FileConfig:
    output_path: str = "./output/parking-violations.jsonl"


@dataclass
class KafkaConfig:
    brokers: list[str] = field(default_factory=lambda: ["localhost:9092"])
    client_id: str = "lab-4-producer"
    topic: str = "parking-violations"


@dataclass
class RedisConfig:
    url: str = "redis://localhost:6379"
    key: str = "parking:violations"


@dataclass
class InputConfig:
    type: str = "xlsx"
    file_path: str = "./ParkingViolationCodes_March_2024.xlsx"


@dataclass
class OutputConfig:
    strategy: OutputStrategyName = "console"
    console: ConsoleConfig = field(default_factory=ConsoleConfig)
    file: FileConfig = field(default_factory=FileConfig)
    kafka: KafkaConfig = field(default_factory=KafkaConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)


@dataclass
class AppConfig:
    input: InputConfig = field(default_factory=InputConfig)
    output: OutputConfig = field(default_factory=OutputConfig)


def load_config(config_path: str | None = None) -> AppConfig:

    default_path = os.path.join(os.path.dirname(__file__), "../../config/app.config.json")
    resolved = os.path.abspath(config_path or default_path)

    with open(resolved, encoding="utf-8") as f:
        raw: dict = json.load(f)

    inp = raw.get("input", {})
    out = raw.get("output", {})

    console_cfg = out.get("console", {})
    file_cfg    = out.get("file", {})
    kafka_cfg   = out.get("kafka", {})
    redis_cfg   = out.get("redis", {})

    return AppConfig(
        input=InputConfig(
            type=inp.get("type", "xlsx"),
            file_path=inp.get("filePath", "./ParkingViolationCodes_March_2024.xlsx"),
        ),
        output=OutputConfig(
            strategy=out.get("strategy", "console"),
            console=ConsoleConfig(pretty=console_cfg.get("pretty", True)),
            file=FileConfig(output_path=file_cfg.get("outputPath", "./output/parking-violations.jsonl")),
            kafka=KafkaConfig(
                brokers=kafka_cfg.get("brokers", ["localhost:9092"]),
                client_id=kafka_cfg.get("clientId", "lab-4-producer"),
                topic=kafka_cfg.get("topic", "parking-violations"),
            ),
            redis=RedisConfig(
                url=redis_cfg.get("url", "redis://localhost:6379"),
                key=redis_cfg.get("key", "parking:violations"),
            ),
        ),
    )
