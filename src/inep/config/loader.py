# src/inep/config.py

from utils.config import load_config
from inep.config.variaveis import carregar_variaveis
from inep.config.io import carregar_io
from inep.config.arquivos import carregar_arquivos
from inep.config.mapeamentos import carregar_mapeamento
from inep.config.formulas import carregar_formulas

_cfg = load_config("inep")

IO = carregar_io(_cfg)
ARQUIVOS = carregar_arquivos(_cfg)
MAPEAMENTOS = carregar_mapeamento(_cfg)
VARIAVEIS_YAML = carregar_variaveis(_cfg)
LIMPEZA = _cfg.get("limpeza", {})
FORMULAS_CONFIG = carregar_formulas(_cfg)

_anos_cfg = _cfg.get("anos", {})
ANO_INICIO = int(_anos_cfg["inicio"])
ANO_FIM = int(_anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
