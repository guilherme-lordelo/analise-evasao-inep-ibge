from dataclasses import dataclass

from brpipe.bridge.inep.tipos import ResultadoTipo

@dataclass(frozen=True)
class MetaVisual:
	y_label: str
	y_min: float | None = None
	y_max: float | None = None
	y_fmt: str | None = None

def meta_para_linha(item) -> MetaVisual:
    y_label = item.nome.replace("_", " ").title()
    if item.resultado == ResultadoTipo.PERCENT_0_100:
        return MetaVisual(
            y_label=y_label,
            y_min=0,
            y_max=100,
        )

    if item.resultado == ResultadoTipo.PROPORTION:
        return MetaVisual(
            y_label=y_label,
            y_min=0,
            y_max=1,
        )

    return MetaVisual(y_label=y_label)


