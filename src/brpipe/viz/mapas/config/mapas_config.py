from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class MapaConfig:
    figsize: Tuple[int, int]
    legend_label: str
