# src/inep/config/loader.py

from brpipe.utils.config import load_config
from brpipe.inep.config.variaveis import carregar_variaveis
from brpipe.inep.config.io import carregar_io
from brpipe.inep.config.arquivos import carregar_arquivos
from brpipe.inep.config.mapeamentos import carregar_mapeamento
from brpipe.inep.config.formulas import carregar_formulas

_cfg_inep = load_config("inep")
_cfg_base = load_config("base")

IO = carregar_io(cfg_inep=_cfg_inep, cfg_base=_cfg_base)
ARQUIVOS = carregar_arquivos(_cfg_inep)
MAPEAMENTOS = carregar_mapeamento(_cfg_inep)
VARIAVEIS_YAML = carregar_variaveis(_cfg_inep)
LIMPEZA = _cfg_inep.get("limpeza", {})
FORMULAS_CONFIG = carregar_formulas(_cfg_inep)

_anos_cfg = _cfg_inep.get("anos", {})
ANO_INICIO = int(_anos_cfg["inicio"])
ANO_FIM = int(_anos_cfg["fim"])

ANOS = list(range(ANO_INICIO, ANO_FIM + 1))
