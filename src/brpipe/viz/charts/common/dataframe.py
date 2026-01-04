from brpipe.viz.charts.common import PlotSpecBase
from brpipe.utils.paths import (
	arquivo_nacional,
	arquivo_estadual,
	arquivo_municipal,
)
from brpipe.utils.io import read_csv


def carregar_dataframe_por_plot(
	plot_spec: PlotSpecBase,
	variaveis,
):
	if plot_spec.nivel == "nacional":
		df = read_csv(arquivo_nacional)

	elif plot_spec.nivel == "estadual":
		df = read_csv(arquivo_estadual)

		if plot_spec.territorio_chave == "ufs":
			col = variaveis.territoriais["uf"]
			df = df[df[col] == plot_spec.territorio_valor]

	elif plot_spec.nivel == "municipal":
		df = read_csv(arquivo_municipal)

		if plot_spec.territorio_chave == "municipios":
			col = variaveis.territoriais["municipio"]
			df = df[df[col] == plot_spec.territorio_valor]

	else:
		raise ValueError(f"Nível desconhecido: {plot_spec.nivel}")

	return df
