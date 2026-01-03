# brpipe/domain/inep/bootstrap.py

from brpipe.bridge.inep.contexto import InepContext
from brpipe.bridge.inep.formulas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.inep.config import VARIAVEIS_YAML, FORMULAS_CONFIG, ANOS

def carregar_contexto_inep() -> InepContext:

	return InepContext(
		variaveis=VariaveisINEP(VARIAVEIS_YAML),
		formulas=FormulasParaMetricas(FORMULAS_CONFIG),
		anos=ANOS,
	)

CONTEXTO = carregar_contexto_inep()