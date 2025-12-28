from .loader import carregar_dados, carregar_colunas, carregar_plot, carregar_municipios, carregar_uf

DADOS = carregar_dados()
COLUNAS = carregar_colunas()
PLOT = carregar_plot()
MUNICIPIOS = carregar_municipios()
UF = carregar_uf()

__all__ = [
    "DADOS",
    "COLUNAS",
    "PLOT",
    "MUNICIPIOS",
    "UF",
]