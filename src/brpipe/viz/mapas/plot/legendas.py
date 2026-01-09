from matplotlib.patches import Patch

LEGENDA_SITUACAO_MUNICIPIOS = [
	Patch(
		facecolor="#9e9e9e",
		edgecolor="#636363",
		label="Fora do INEP",
	),
	Patch(
		facecolor="#eeeeee",
		edgecolor="#bdbdbd",
		label="Sem dados no ano",
	),
	Patch(
		facecolor="#c6dbef",
		edgecolor="#6baed6",
		label="Sem métrica no ano",
	),
]
