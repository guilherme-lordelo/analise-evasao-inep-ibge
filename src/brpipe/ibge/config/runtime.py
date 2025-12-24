from brpipe.utils.config import load_config
from brpipe.utils.colunas_base import get_colunas_municipio
from brpipe.ibge.config.parser import parse_tabelas
from brpipe.ibge.config.models import TabelaIBGEConfig

_cfg = load_config("ibge")

COLUNAS_BASE_IBGE = get_colunas_municipio(include_nome=True)
TABELAS_IBGE: dict[str, TabelaIBGEConfig] = parse_tabelas(_cfg)
