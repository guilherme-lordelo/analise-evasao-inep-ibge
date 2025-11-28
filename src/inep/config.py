# src/inep/config.py

from utils.config import load_config

_cfg = load_config("inep")

# -----------------------
# Extração
# -----------------------
extracao = _cfg.get("extracao", {})
ENCODING = extracao.get("encoding", "latin1")
SEP = extracao.get("sep", ";")
CHUNKSIZE = extracao.get("chunksize", 100000)
COLUNAS_SELECIONADAS = extracao.get("colunas_selecionadas", [])

# -----------------------
# Anos e pares
# -----------------------
anos_cfg = _cfg.get("anos", {})
ANO_INICIO = int(anos_cfg["inicio"])
ANO_FIM = int(anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
PARES = [f"{ano}_{ano+1}" for ano in range(ANO_INICIO, ANO_FIM)]
