# src/brpipe/viz/mapas/config/loader.py

from brpipe.utils.config import load_config
from brpipe.utils.config import load_config
from .malha import MalhaConfig
from .plot_config import PlotConfig

_CFG = load_config("mapas")

def carregar_malha() -> MalhaConfig:
    malha = _CFG["malha"]
    return MalhaConfig(
        municipio=malha["municipio"],
        uf = malha["uf"],
    )

def carregar_plot() -> PlotConfig:
    plot = _CFG["plot"]

    return PlotConfig(
        cmap=plot["cmap"],
        legend_shrink=plot["legend_shrink"],
        figsize=tuple(plot["figsize"]),
    )
