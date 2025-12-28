from dataclasses import dataclass

@dataclass(frozen=True)
class PlotConfig:
    cmap: str
    legend_shrink: float
