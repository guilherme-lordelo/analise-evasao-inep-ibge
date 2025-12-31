from dataclasses import dataclass
from brpipe.bridge.inep.formulas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisParaMapas

@dataclass(frozen=True)
class InepContext:
	variaveis: VariaveisParaMapas
	formulas: FormulasParaMetricas
