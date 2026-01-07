from brpipe.bridge.common.tipos import resolver_resultado_tipo
from brpipe.bridge.ibge.contexto import IbgeContext
from brpipe.bridge.ibge.variaveis import VariaveisIBGE
from brpipe.ibge.config import (
	TABELAS_IBGE,
)
from brpipe.ibge.config.runtime import TIPO_DEFAULT_IBGE

def carregar_contexto_ibge() -> IbgeContext:
	return IbgeContext(
		variaveis=VariaveisIBGE(
			tabelas_cfg=TABELAS_IBGE,
			tipo_default=resolver_resultado_tipo(
				TIPO_DEFAULT_IBGE,
				padrao=None,
				ctx="Campo formato_padrao: "
				),
		)
	)

CONTEXTO = carregar_contexto_ibge()
