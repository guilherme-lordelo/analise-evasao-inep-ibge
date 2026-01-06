from dataclasses import dataclass

from brpipe.bridge.common.tipos import ResultadoTipo

@dataclass(frozen=True)
class MetaVisual:
    x_label: str | None = None
    y_label: str | None = None
    x_min: float | None = None
    x_max: float | None = None
    y_min: float | None = None
    y_max: float | None = None
    x_fmt: str | None = None
    y_fmt: str | None = None


def _limites_por_resultado(item):
    if item.resultado == ResultadoTipo.PERCENT_0_100:
        return 0, 100

    if item.resultado == ResultadoTipo.PROPORTION:
        return 0, 1

    return None, None

def meta_para_linha(item) -> MetaVisual:
    label = item.nome.replace("_", " ").title()
    ymin, ymax = _limites_por_resultado(item)

    return MetaVisual(
        y_label=label,
        y_min=ymin,
        y_max=ymax,
    )

def meta_para_scatter(item) -> MetaVisual:
    label = item.nome.replace("_", " ").title()

    return MetaVisual(
        x_label=label,
        y_label=label,
    )
