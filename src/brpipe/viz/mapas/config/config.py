from brpipe.utils.config import load_config

_CFG = load_config("mapas")

def dados_cfg() -> dict:
    return _CFG["dados"]

def evasao_cfg() -> dict:
    return _CFG["dados"]["evasao"]

def formato_dados() -> str:
    return dados_cfg().get("formato", "wide")

def arquivo_evasao() -> str:
    return dados_cfg()["evasao"]["arquivo"]

def sep_evasao() -> str:
    return dados_cfg().get("separador", ";")

def coluna_evasao() -> str:
    return _CFG["metricas"]["evasao"]["padrao"]

def colunas_municipio() -> dict:
    return _CFG["colunas"]["territoriais"]["municipio"]

def plot_cfg() -> dict:
    return _CFG["plot"]

def municipios_cfg() -> dict:
    return _CFG["municipios"]

def uf_cfg() -> dict:
    return _CFG["uf"]

def coluna_mapa() -> str:
    return evasao_cfg()["coluna_mapa"]