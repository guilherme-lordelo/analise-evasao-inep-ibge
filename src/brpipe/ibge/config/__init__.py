# src/ibge/_config/__init__.py
from brpipe.ibge.config.models import TabelaIBGEConfig
from brpipe.ibge.config.parser.tabelas import parse_tabelas
from brpipe.ibge.config.runtime import COLUNAS_BASE_IBGE,SAIDA_IBGE, NOME_FINAL_MUNICIPIOS
from brpipe.utils.config import load_config

_cfg_ibge = load_config("ibge")
TABELAS_IBGE: dict[str, TabelaIBGEConfig] = parse_tabelas(_cfg_ibge)

__all__ = [
    "COLUNAS_BASE_IBGE",
    "TABELAS_IBGE",
    "SAIDA_IBGE",
    "NOME_FINAL_MUNICIPIOS",
    "TABELAS_IBGE",
]