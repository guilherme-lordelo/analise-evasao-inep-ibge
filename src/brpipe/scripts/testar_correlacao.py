import pandas as pd

from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.inep.config.formulas import FormulasConfig
from brpipe.utils.paths import INEP_TRANSFORMACOES, inep_municipal, ibge_municipio
from brpipe.utils.io import read_csv
from brpipe.utils.colunas_base import get_colunas_municipio
from brpipe.inep.config import FORMULAS_CONFIG

COLUNAS_BASE = get_colunas_municipio()

def selecionar_variaveis_ibge(df_ibge: pd.DataFrame, colunas_base: list[str]) -> list[str]:
	"""
	Seleciona apenas colunas IBGE numéricas que não fazem parte da chave.
	"""
	variaveis = []

	for col in df_ibge.columns:
		if col in colunas_base:
			continue
		if pd.api.types.is_numeric_dtype(df_ibge[col]):
			variaveis.append(col)

	return variaveis


def listar_metricas_proporcao(formulas_cfg: FormulasConfig) -> list[str]:
	metricas = []

	for nome, cfg in formulas_cfg.formulas.items():
		formato = cfg.formato or ResultadoTipo.PROPORCAO
		if formato == ResultadoTipo.PROPORCAO:
			metricas.append(nome.upper())

	return metricas

def correlacionar_inep_ibge(
	df_inep: pd.DataFrame,
	df_ibge: pd.DataFrame,
	colunas_base: list[str],
	metricas_inep: list[str],
):
	resultados = []

	df = df_inep.merge(
		df_ibge,
		on=colunas_base,
		how="inner",
	)

	variaveis_ibge = selecionar_variaveis_ibge(df_ibge, colunas_base)

	for metrica in metricas_inep:
		if metrica not in df.columns:
			continue

		for var in variaveis_ibge:
			serie_x = df[metrica]
			serie_y = df[var]

			mask = serie_x.notna() & serie_y.notna()
			if mask.sum() < 3:
				continue

			corr = serie_x[mask].corr(serie_y[mask])

			if pd.notna(corr):
				resultados.append({
					"metrica": metrica,
					"variavel_ibge": var,
					"correlacao": corr,
				})

	return (
		pd.DataFrame(resultados)
		.sort_values("correlacao", key=lambda s: s.abs(), ascending=False)
	)

def main():
	INEP_MUNICIPAL = INEP_TRANSFORMACOES / inep_municipal
	IBGE_MUNICIPIO = INEP_TRANSFORMACOES / ibge_municipio
	df_ibge = read_csv(IBGE_MUNICIPIO)


	df_inep = read_csv(INEP_MUNICIPAL)

	metricas = listar_metricas_proporcao(FORMULAS_CONFIG)

	df_corr = correlacionar_inep_ibge(
		df_inep=df_inep,
		df_ibge=df_ibge,
		colunas_base=COLUNAS_BASE,
		metricas_inep=metricas,
	)

	print(df_corr)


if __name__ == "__main__":
	main()
