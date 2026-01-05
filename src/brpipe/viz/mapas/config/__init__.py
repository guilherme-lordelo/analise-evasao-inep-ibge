from .loader import carregar_malha, carregar_plot
from.inep import VARIAVEIS, METRICAS, ANOS

MALHA = carregar_malha()
PLOT = carregar_plot()

__all__ = [
    "MALHA"
    "PLOT",
    "VARIAVEIS",
    "METRICAS",
    "ANOS",
]