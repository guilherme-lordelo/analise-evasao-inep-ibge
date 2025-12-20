# src/inep/config.py

from utils.config import load_config
from .variaveis_config import carregar_variaveis
from inep.io_config import carregar_io
from inep.arquivos_config import carregar_arquivos
from inep.mapeamento_config import carregar_mapeamento
from inep.formulas_config import carregar_formulas

_cfg = load_config("inep")

IO_CONFIG = carregar_io(_cfg)
ARQUIVOS_CONFIG = carregar_arquivos(_cfg)
MAPEAMENTO_CONFIG = carregar_mapeamento(_cfg)
VARIAVEIS_CONFIG = carregar_variaveis(_cfg)
LIMPEZA_CFG = _cfg.get("limpeza", {})

FORMULAS_CONFIG = carregar_formulas(_cfg)

# Anos
anos_cfg = _cfg.get("anos", {})
ANO_INICIO = int(anos_cfg["inicio"])
ANO_FIM = int(anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
