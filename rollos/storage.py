"""Leitura informativa de espaço em disco para o protótipo."""
from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(frozen=True)
class StorageSnapshot:
    path: str
    total_bytes: int
    used_bytes: int
    free_bytes: int

    @property
    def used_percent(self) -> float:
        return (self.used_bytes / self.total_bytes * 100) if self.total_bytes else 0.0

    @property
    def free_gb(self) -> float:
        return self.free_bytes / (1024 ** 3)


class RollStorage:
    """Consulta capacidade; não apaga nem altera arquivos do usuário."""

    def snapshot(self, path: str | Path = ".") -> StorageSnapshot:
        target = Path(path).expanduser().resolve()
        usage = shutil.disk_usage(target)
        return StorageSnapshot(str(target), usage.total, usage.used, usage.free)
