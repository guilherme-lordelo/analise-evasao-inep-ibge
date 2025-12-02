from utils.config import load_config

_cfg = load_config("colunas_base")

# ----------- Colunas principais -----------------

COD_MUNICIPIO = _cfg["municipio"]["codigo"]
NOME_MUNICIPIO = _cfg["municipio"]["nome"]
UF = _cfg["estado"]["sigla"]

# ----------- Funções utilitárias ----------------

def get_colunas_municipio(include_nome=True):
    """Retorna as colunas principais de identificação municipal."""
    cols = [COD_MUNICIPIO, UF]
    if include_nome and NOME_MUNICIPIO:
        cols.append(NOME_MUNICIPIO)
    return cols