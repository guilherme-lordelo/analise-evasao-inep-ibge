from dataclasses import dataclass
from brpipe.bridge.inep.formulas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisINEP

@dataclass(frozen=True)
class InepContext:
	variaveis: VariaveisINEP
	formulas: FormulasParaMetricas
	anos: list[int]
