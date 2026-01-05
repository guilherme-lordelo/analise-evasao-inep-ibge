from pandas import DataFrame
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common import PlotSpecBase
from brpipe.utils.paths import (
	arquivo_nacional,
	arquivo_estadual,
	arquivo_municipal,
)
from brpipe.utils.io import read_csv


def carregar_dataframe_por_plot(
	plot_spec: PlotSpecBase,
) -> DataFrame:

	if plot_spec.nivel == "nacional":
		df = read_csv(arquivo_nacional)

	elif plot_spec.nivel == "estadual":
		df = read_csv(arquivo_estadual)

	elif plot_spec.nivel == "municipal":
		df = read_csv(arquivo_municipal)

	else:
		raise ValueError(f"Nível desconhecido: {plot_spec.nivel}")

	if plot_spec.coluna_territorial:
		df = df[
			df[plot_spec.coluna_territorial]
			== plot_spec.valor_territorial
		]

	return df
