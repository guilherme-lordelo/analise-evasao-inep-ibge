# brpipe/domain/inep/bootstrap.py

from brpipe.bridge.inep.contexto import InepContext
from brpipe.bridge.inep.formulas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisParaMapas
from brpipe.inep.config import VARIAVEIS_YAML, FORMULAS_CONFIG

def carregar_contexto_inep() -> InepContext:

	return InepContext(
		variaveis=VariaveisParaMapas(VARIAVEIS_YAML),
		formulas=FormulasParaMetricas(FORMULAS_CONFIG),
	)

CONTEXTO = carregar_contexto_inep()