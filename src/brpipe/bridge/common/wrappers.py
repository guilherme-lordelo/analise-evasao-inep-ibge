from dataclasses import dataclass
from pandas import Series
from typing import Protocol
from matplotlib.axes import Axes


class Renderizavel(Protocol):
    def aplicar_formatter(self, ax: Axes) -> None:
        ...

@dataclass(frozen=True)
class SerieFormatada:
    serie: Series
    resultado: Renderizavel
