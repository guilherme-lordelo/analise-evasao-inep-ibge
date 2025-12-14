# src/inep/config.py

from utils.config import load_config
from utils.colunas_base import get_colunas_municipio

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

# Transformação
transformacao_cfg = arq_cfg.get("transformacao", {})
TRANSFORMACAO_PREFIXO_OUT = transformacao_cfg["prefixo_output"]
TRANSFORMACAO_EXT_OUT     = transformacao_cfg["extensao_output"]
TRANSFORMACAO_NIVEIS      = transformacao_cfg.get("niveis", ["municipios", "estados", "nacional"])

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
ORDEM_COLUNAS = saida_cfg.get("ordem_colunas", None)

# ============================
# Variáveis
# ============================
variaveis_cfg = _cfg.get("variaveis", {})
    
# Campos padrão

CAMPOS_PADRAO = get_colunas_municipio()

# Todas as variaveis

VARIAVEIS = []

for campo in CAMPOS_PADRAO:
    VARIAVEIS.append(campo)

for categoria, campos in variaveis_cfg.items():
    VARIAVEIS.extend(list(campos.keys()))

# Variáveis por categoria ou função

VARIAVEIS_TEMPORAIS = list(variaveis_cfg.get("temporais", {}).keys())
VARIAVEIS_CATEGORICAS = list(variaveis_cfg.get("categoricas", {}).keys())
VARIAVEIS_QUANTITATIVAS = list(variaveis_cfg.get("quantitativas", {}).keys())

VALORES_CATEGORICOS = {
    var: set(props["valores"].keys())
    for var, props in variaveis_cfg.get("categoricas", {}).items()
}

COLUNA_ANO = VARIAVEIS_TEMPORAIS[0]

COLUNA_COD_MUNICIPIO = CAMPOS_PADRAO[0]
COLUNA_UF = CAMPOS_PADRAO[1]
COLUNA_NOME_MUNICIPIO = CAMPOS_PADRAO[2] if len(CAMPOS_PADRAO) > 2 else None

COLUNA_PESO = _cfg.get("coluna_peso_inep", "QT_MAT_TOTAL")


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
