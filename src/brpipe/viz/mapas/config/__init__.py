from .loader import carregar_dados, carregar_colunas, carregar_modelo, carregar_plot, carregar_municipios, carregar_uf
from.inep import VARIAVEIS, FORMULAS

DADOS = carregar_dados()
MODELO = carregar_modelo()
COLUNAS = carregar_colunas()
PLOT = carregar_plot()
MUNICIPIOS = carregar_municipios()
UF = carregar_uf()

__all__ = [
    "DADOS",
    "MODELO",
    "COLUNAS",
    "PLOT",
    "MUNICIPIOS",
    "UF",
    "VARIAVEIS",
    "FORMULAS",
]