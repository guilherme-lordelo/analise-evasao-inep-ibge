# src/inep/config.py

from utils.config import load_config
from utils.colunas_base import NOME_MUNICIPIO, get_colunas_municipio

_cfg = load_config("inep")

# -----------------------
# Arquivos
# -----------------------
arq_cfg = _cfg.get("arquivos", {})

# Extração
extracao_cfg = arq_cfg.get("extracao", {})
EXTRACAO_PREFIXO_IN   = extracao_cfg["prefixo_input"]
EXTRACAO_EXT_IN       = extracao_cfg["extensao_input"]
EXTRACAO_PREFIXO_OUT  = extracao_cfg["prefixo_output"]
EXTRACAO_EXT_OUT      = extracao_cfg["extensao_output"]

# Evasão
evasao_cfg = arq_cfg.get("evasao", {})
EVASAO_PREFIXO_OUT = evasao_cfg["prefixo_output"]
EVASAO_EXT_OUT     = evasao_cfg["extensao_output"]

# União
uniao_cfg = arq_cfg.get("uniao", {})
UNIAO_ARQ_MUNICIPIOS = uniao_cfg["output_municipios"]
UNIAO_ARQ_ESTADOS    = uniao_cfg["output_estados"]
UNIAO_ARQ_BRASIL     = uniao_cfg["output_nacional"]

# -----------------------
# Extração
# -----------------------
extracao = _cfg.get("extracao", {})
ENCODING_IN = extracao.get("encoding", "latin1")
SEP_IN = extracao.get("sep", ";")
CHUNKSIZE = extracao.get("chunksize", 100000)

# -----------------------
# Saída
# -----------------------
saida_cfg = _cfg.get("saida", {})
ENCODING_OUT = saida_cfg.get("encoding", "utf-8")
SEP_OUT = saida_cfg.get("sep", ";")
COMPRESS = saida_cfg.get("compress", False)
COLUMNS_ORDER = saida_cfg.get("columns_order", None)

# ============================
# Variáveis
# ============================
variaveis_cfg = _cfg.get("variaveis", {})
    
# Campos padrão

def get_campos_municipio(df=None):
    return get_colunas_municipio(include_nome=(df is None or NOME_MUNICIPIO in df.columns))



# Todas as variaveis

VARIAVEIS = []

for campo in get_campos_municipio():
    VARIAVEIS.append(campo)

for categoria, campos in variaveis_cfg.items():
    VARIAVEIS.extend(list(campos.keys()))

# Variáveis por categoria ou função

VARIAVEIS_TEMPORAIS = list(variaveis_cfg.get("temporais", {}).keys())
VARIAVEIS_CATEGORICAS = list(variaveis_cfg.get("categoricas", {}).keys())
VARIAVEIS_QUANTITATIVAS = list(variaveis_cfg.get("quantitativas", {}).keys())

# -----------------------
# Mapeamento de sinônimos para colunas
# -----------------------
COL_MAPPINGS = _cfg.get("mapeamento_colunas", {})

# ============================
# Configurações de limpeza
# ============================
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
        "agregacao": info.get("agregacao", "soma"),
        "validacao": info.get("validacao", {}).get("regras", []),
    }

COLUNA_PESO = _cfg.get("coluna_peso_inep", "QT_MAT_TOTAL")

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
