"""Serviços de base do protótipo RollOS (user space)."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


@dataclass
class RollConfig:
    product_name: str = "RollOS"
    build: str = "0.2.0-dev"
    interface_language: str = "pt-BR"
    ai_provider: str = "nvidia-nim"
    telemetry_enabled: bool = False


class RollCore:
    """Configuração local e registro simples de eventos do protótipo."""

    def __init__(self, data_dir: str | Path = "~/.rollos") -> None:
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.data_dir / "config.json"
        self.events_path = self.data_dir / "events.jsonl"
        self.config = self._load_config()

    def _load_config(self) -> RollConfig:
        if not self.config_path.exists():
            config = RollConfig()
            self.save_config(config)
            return config
        try:
            data: dict[str, Any] = json.loads(self.config_path.read_text(encoding="utf-8"))
            allowed = RollConfig.__dataclass_fields__.keys()
            return RollConfig(**{key: value for key, value in data.items() if key in allowed})
        except (OSError, ValueError, TypeError):
            return RollConfig()

    def save_config(self, config: RollConfig | None = None) -> None:
        if config is not None:
            self.config = config
        temp = self.config_path.with_suffix(".tmp")
        temp.write_text(json.dumps(asdict(self.config), ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.config_path)

    def log_event(self, name: str, details: dict[str, Any] | None = None) -> None:
        if not name.strip():
            raise ValueError("O nome do evento não pode ficar vazio.")
        event = {"time": datetime.now(timezone.utc).isoformat(), "name": name, "details": details or {}}
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\\n")
