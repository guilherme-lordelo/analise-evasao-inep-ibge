from dataclasses import dataclass
from typing import List

from brpipe.utils.config import load_config


_CFG = load_config("charts")


@dataclass(frozen=True)
class LinhaTemporalPlotConfig:
    figsize: tuple[int, int]
    mostrar_titulo: bool
    grid: bool


@dataclass(frozen=True)
class LinhaTemporalConfig:
    plot: LinhaTemporalPlotConfig
    variaveis: List[str]
    formato_saida: str
    dpi: int


def carregar_linha_temporal() -> LinhaTemporalConfig:
    cfg = _CFG["linha_temporal"]

    plot = cfg["plot"]

    return LinhaTemporalConfig(
        plot=LinhaTemporalPlotConfig(
            figsize=tuple(plot["figsize"]),
            mostrar_titulo=plot["mostrar_titulo"],
            grid=plot["grid"],
        ),
        variaveis=cfg["variaveis"],
        formato_saida=cfg["saida"]["formato"],
        dpi=cfg["saida"]["dpi"],
    )
