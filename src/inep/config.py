# src/inep/config.py

from utils.config import load_config

_cfg = load_config("inep")

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

def _validar_unicidade(nome_cat, lista_vars, obrigatorio, max_itens=1):
    if obrigatorio and len(lista_vars) == 0:
        raise ValueError(
            f"A categoria '{nome_cat}' deve conter exatamente 1 variável obrigatória, "
            f"mas está vazia."
        )
    if len(lista_vars) > max_itens:
        raise ValueError(
            f"A categoria '{nome_cat}' deve conter no máximo {max_itens} variável(is), "
            f"mas foram encontradas: {lista_vars}"
        )

# Listão de todas as variáveis declaradas
VARIAVEIS = []
for categoria, campos in variaveis_cfg.items():
    VARIAVEIS.extend(list(campos.keys()))

# -------------------------
# Variáveis por categoria ou função
# -------------------------

VARIAVEIS_CHAVES_MUNICIPIO = list(variaveis_cfg.get("chaves_municipais", {}).keys())
VARIAVEIS_CHAVES_ESTADO = list(variaveis_cfg.get("chaves_estaduais", {}).keys())
VARIAVEIS_TEMPORAIS = list(variaveis_cfg.get("temporais", {}).keys())
VARIAVEIS_DESCRITIVAS_MUNICIPIO = list(variaveis_cfg.get("descritivas_municipais", {}).keys())
VARIAVEIS_CATEGORICAS = list(variaveis_cfg.get("categoricas", {}).keys())
VARIAVEIS_QUANTITATIVAS = list(variaveis_cfg.get("quantitativas", {}).keys())

# -------------------------
# Checks de unicidade
# -------------------------

# Código do município - obrigatório, único
_validar_unicidade(
    "chaves_municipais",
    VARIAVEIS_CHAVES_MUNICIPIO,
    obrigatorio=True,
    max_itens=1
)

# Sigla da UF - obrigatório, único
_validar_unicidade(
    "chaves_estaduais",
    VARIAVEIS_CHAVES_ESTADO,
    obrigatorio=True,
    max_itens=1
)

# Ano de referência - opcional, único
_validar_unicidade(
    "descritivas_municipais",
    VARIAVEIS_DESCRITIVAS_MUNICIPIO,
    obrigatorio=False,
    max_itens=1
)

# -----------------------
# Campos padrão
# -----------------------

CAMPO_COD_MUNICIPIO = VARIAVEIS_CHAVES_MUNICIPIO[0]
CAMPO_UF = VARIAVEIS_CHAVES_ESTADO[0]

CAMPO_NOME_MUNICIPIO = (
    VARIAVEIS_DESCRITIVAS_MUNICIPIO[0]
    if VARIAVEIS_DESCRITIVAS_MUNICIPIO
    else None
)

def get_campos_municipio(df=None):
    """
    Retorna as colunas que identificam um município:
    - código (obrigatório)
    - UF (obrigatório)
    - nome (opcional)
    
    Se `df` for fornecido, inclui o nome apenas se a coluna existir no dataframe.
    """
    cols = [CAMPO_COD_MUNICIPIO, CAMPO_UF]

    if CAMPO_NOME_MUNICIPIO is not None:
        if df is None or CAMPO_NOME_MUNICIPIO in df.columns:
            cols.append(CAMPO_NOME_MUNICIPIO)

    return cols


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
