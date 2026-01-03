import matplotlib.pyplot as plt

from brpipe.viz.config.metadados import MetaVisual

def plot_linha_temporal(
	df,
	coluna_ano: str,
	coluna_valor: str,
	meta: MetaVisual,
	titulo: str | None = None,
	figsize=(8, 4),
):
	fig, ax = plt.subplots(figsize=figsize)

	ax.plot(
		df[coluna_ano],
		df[coluna_valor],
		marker="o",
	)

	ax.set_xlabel("Ano")
	ax.set_ylabel(meta.y_label)

	if meta.y_min is not None or meta.y_max is not None:
		ax.set_ylim(meta.y_min, meta.y_max)

	if titulo:
		ax.set_title(titulo)

	ax.grid(True, alpha=0.3)

	return fig, ax
