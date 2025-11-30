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

# ============================
# Variáveis
# ============================
from utils.config import load_config

_cfg = load_config("inep")

variaveis_cfg = _cfg.get("variaveis", {})

# Lista completa de variáveis do dataset
VARIAVEIS = []
for categoria, campos in variaveis_cfg.items():
    VARIAVEIS.extend(list(campos.keys()))

# Variáveis por tipo
VARIAVEIS_CHAVES = list(variaveis_cfg.get("chaves", {}).keys())
VARIAVEIS_TEMPORAIS = list(variaveis_cfg.get("temporais", {}).keys())
VARIAVEIS_DESCRITIVAS = list(variaveis_cfg.get("descritivas", {}).keys())
VARIAVEIS_CATEGORICAS = list(variaveis_cfg.get("categoricas", {}).keys())
VARIAVEIS_QUANTITATIVAS = list(variaveis_cfg.get("quantitativas", {}).keys())

# Mapeamento de sinônimos para colunas
COL_MAPPINGS = _cfg.get("mapeamento_colunas", {})

# Configurações de limpeza
LIMPEZA_CFG = _cfg.get("limpeza", {})

# -----------------------
# Fórmulas
# -----------------------
formulas_cfg = _cfg.get("formulas", {})

FORMULAS = {}
for nome, info in formulas_cfg.items():
    FORMULAS[nome] = {
        "descricao": info.get("descricao", ""),
        "expressao": info.get("expressao"),
        "validacao": info.get("validacao", {}).get("regras", []),
    }

# -----------------------
# Limites de validação
# -----------------------
validacao_cfg = _cfg.get("validacao_limites", {})
LIMITES = validacao_cfg

# -----------------------
# Anos e pares
# -----------------------
anos_cfg = _cfg.get("anos", {})
ANO_INICIO = int(anos_cfg["inicio"])
ANO_FIM = int(anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
PARES = [f"{ano}_{ano+1}" for ano in range(ANO_INICIO, ANO_FIM)]
