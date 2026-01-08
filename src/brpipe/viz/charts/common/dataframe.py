import os
from pandas import DataFrame
from brpipe.utils.colunas_base import COL_NACIONAL, get_colunas_municipio
from brpipe.viz.charts.common import PlotSpecBase
from brpipe.utils.paths import (
	inep_nacional,
	inep_estadual,
	inep_municipal,
	ibge_municipio,
)
from brpipe.utils.io import read_csv

def carregar_df_inep(plot_spec: PlotSpecBase) -> DataFrame:
	if plot_spec.nivel == "nacional":
		return read_csv(inep_nacional)

	if plot_spec.nivel == "estadual":
		return read_csv(inep_estadual)

	if plot_spec.nivel == "municipal":
		return read_csv(inep_municipal)

	raise ValueError(f"Nível desconhecido: {plot_spec.nivel}")

def carregar_df_ibge() -> DataFrame | None:
	if os.path.exists(ibge_municipio):
		return read_csv(ibge_municipio)

def aplicar_filtro_territorial(
	df: DataFrame,
	plot_spec: PlotSpecBase,
) -> DataFrame:
	if not plot_spec.coluna_territorial:
		return df

	return df[
		df[plot_spec.coluna_territorial]
		== plot_spec.valor_territorial
	]

def unir_inep_ibge(
	df_inep: DataFrame,
	df_ibge: DataFrame,
	plot_spec: PlotSpecBase,
) -> DataFrame:

	chaves = get_colunas_municipio()

	if plot_spec.nivel == "nacional":
		chaves = [COL_NACIONAL]

	if plot_spec.nivel == "estadual":
		chaves = [chaves["UF"]]

	return df_inep.merge(
		df_ibge,
		on=chaves,
		how="left",
		validate="many_to_one",
	)


def carregar_dataframe_por_plot(
	plot_spec: PlotSpecBase,
) -> DataFrame:

	df_inep = carregar_df_inep(plot_spec)
	df_inep = aplicar_filtro_territorial(df_inep, plot_spec)

	df_ibge = carregar_df_ibge()
	if df_ibge is None:
		return df_inep

	df_ibge = aplicar_filtro_territorial(df_ibge, plot_spec)

	return unir_inep_ibge(df_inep, df_ibge, plot_spec)
