"""Modelo independente do hardware para estados de tela variável."""
from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayState:
    width_px: int
    height_px: int
    expansion: float
    mode: str
    columns: int


class RollDisplay:
    def __init__(self, compact_width: int = 1080, expanded_width: int = 2160, height: int = 2400, expanded_threshold: float = 0.68) -> None:
        if compact_width <= 0 or expanded_width < compact_width or height <= 0:
            raise ValueError("Dimensões de tela inválidas.")
        if not 0 < expanded_threshold <= 1:
            raise ValueError("O limite de expansão deve estar entre 0 e 1.")
        self.compact_width = compact_width
        self.expanded_width = expanded_width
        self.height = height
        self.expanded_threshold = expanded_threshold

    def state_for(self, expansion: float) -> DisplayState:
        """Retorna dimensões e grade simuladas; não aciona painel físico."""
        value = min(1.0, max(0.0, float(expansion)))
        width = round(self.compact_width + (self.expanded_width - self.compact_width) * value)
        expanded = value >= self.expanded_threshold
        return DisplayState(width, self.height, value, "expanded" if expanded else "compact", 2 if expanded else 1)
