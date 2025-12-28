from brpipe.utils.config import load_config

_CFG = load_config("mapas")

def coluna_evasao() -> str:
    return _CFG["metricas"]["evasao"]["padrao"]

def plot_cfg() -> dict:
    return _CFG["plot"]

def municipios_cfg() -> dict:
    return _CFG["municipios"]

def uf_cfg() -> dict:
    return _CFG["uf"]

def arquivo_evasao() -> str:
    return _CFG["dados"]["evasao"]["arquivo"]

def sep_evasao() -> str:
    return _CFG["dados"]["evasao"]["separador"]

def colunas_municipio() -> dict:
    return _CFG["colunas"]["territoriais"]["municipio"]
