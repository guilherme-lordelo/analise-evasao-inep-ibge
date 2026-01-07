from brpipe.bridge.ibge.contexto import IbgeContext
from brpipe.bridge.ibge.variaveis import VariaveisIBGE
from brpipe.ibge.config import (
	TABELAS_IBGE,
)

def carregar_contexto_ibge() -> IbgeContext:
	return IbgeContext(variaveis=VariaveisIBGE(tabelas_cfg=TABELAS_IBGE))

CONTEXTO = carregar_contexto_ibge()
