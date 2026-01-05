from dataclasses import dataclass
from brpipe.bridge.inep.metricas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisINEP

@dataclass(frozen=True)
class InepContext:
	variaveis: VariaveisINEP
	metricas: FormulasParaMetricas
	anos: list[int]
