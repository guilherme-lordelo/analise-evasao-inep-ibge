from pandas import DataFrame
from brpipe.viz.charts.common.consumiveis import Consumiveis
from brpipe.viz.charts.common.plot_spec import PlotSpecBase


def _exige_drop(itens) -> int:
    lags = [
        getattr(item, "lag", 0)
        for item in itens
    ]
    return max(lags, default=0)

def filtrar_ano_inicial(
    df: DataFrame,
    *,
    consumiveis: Consumiveis,
    coluna_ano: str,
    plot_spec: PlotSpecBase,
) -> DataFrame:

    itens = [consumiveis.get(nome) for nome in plot_spec.variaveis]
    lag = _exige_drop(itens)
    if lag > 0:
        min_year = df[coluna_ano].min()
        df = df[df[coluna_ano] > min_year]
    return df