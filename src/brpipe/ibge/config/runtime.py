from brpipe.utils.config import load_config
from brpipe.utils.colunas_base import get_colunas_municipio
from brpipe.ibge.config.parser import parse_tabelas
from brpipe.ibge.config.models import TabelaIBGEConfig

_cfg_ibge = load_config("ibge")
_cfg_base = load_config("base")

COLUNAS_BASE_IBGE = get_colunas_municipio(include_nome=True)
TABELAS_IBGE: dict[str, TabelaIBGEConfig] = parse_tabelas(_cfg_ibge)
SAIDA_IBGE = _cfg_base.get("saida")
NOME_FINAL = _cfg_ibge.get("arquivo_final", "ibge_final.csv")
TIPO_DEFAULT_IBGE = _cfg_ibge.get("formato_padrao", "COUNT")
