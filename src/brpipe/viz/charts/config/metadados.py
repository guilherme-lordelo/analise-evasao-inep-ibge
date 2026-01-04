from dataclasses import dataclass

from brpipe.bridge.inep.tipos import ResultadoTipo
from brpipe.bridge.inep.variaveis import VariavelINEP

@dataclass(frozen=True)
class MetaVisual:
	y_label: str
	y_min: float | None = None
	y_max: float | None = None
	y_fmt: str | None = None

def meta_para_linha(var: VariavelINEP) -> MetaVisual:
	if var.resultado == ResultadoTipo.PERCENT_0_100:
		return MetaVisual(
			y_label="Percentual (%)",
			y_min=0,
			y_max=100,
		)

	if var.resultado == ResultadoTipo.PROPORTION:
		return MetaVisual(
			y_label="Proporção",
			y_min=0,
			y_max=1,
		)

	return MetaVisual(y_label=var.nome)

