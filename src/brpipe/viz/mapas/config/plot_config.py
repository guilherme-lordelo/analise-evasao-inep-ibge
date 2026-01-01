from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class PlotConfig:
    cmap: str
    legend_shrink: float
    figsize: Tuple[int, int]
