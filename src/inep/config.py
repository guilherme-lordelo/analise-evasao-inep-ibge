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
# -----------------------
# Variáveis (todas as categorias do YAML)
# -----------------------
variaveis_cfg = _cfg.get("variaveis", {})

VARIAVEIS = []
for categoria, campos in variaveis_cfg.items():
    VARIAVEIS.extend(list(campos.keys()))
# -----------------------
# Anos e pares
# -----------------------
anos_cfg = _cfg.get("anos", {})
ANO_INICIO = int(anos_cfg["inicio"])
ANO_FIM = int(anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
PARES = [f"{ano}_{ano+1}" for ano in range(ANO_INICIO, ANO_FIM)]
