from brpipe.utils.config import load_config
from brpipe.utils.colunas_base import get_colunas_municipio

from brpipe.ibge.config.tabelas import TabelaIBGEConfig, carregar_tabelas_ibge

_cfg = load_config("ibge")

COLUNAS_BASE_IBGE = get_colunas_municipio(include_nome=True)
TABELAS_IBGE: dict[str, TabelaIBGEConfig] = carregar_tabelas_ibge(_cfg)
