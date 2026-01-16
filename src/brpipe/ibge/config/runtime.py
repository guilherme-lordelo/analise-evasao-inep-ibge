from brpipe.utils.config import load_config
from brpipe.utils.colunas_base import get_colunas_municipio

_cfg_ibge = load_config("ibge")
_cfg_base = load_config("base")

COLUNAS_PESO = _cfg_ibge.get("colunas_peso")
TIPO_DEFAULT_IBGE = "CONTAGEM"
COLUNAS_BASE_IBGE = get_colunas_municipio(include_nome=True)
SAIDA_IBGE = _cfg_base.get("saida")
NOME_FINAL_MUNICIPIOS = _cfg_ibge.get("arquivo_final_municipios", "ibge_final_municipios.csv")
NOME_FINAL_ESTADOS = _cfg_ibge.get("arquivo_final_estados", "ibge_final_estados.csv")
NOME_FINAL_NACIONAL = _cfg_ibge.get("arquivo_final_nacional", "ibge_final_nacional.csv")
