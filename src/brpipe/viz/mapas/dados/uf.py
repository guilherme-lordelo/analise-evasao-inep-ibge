import pandas as pd

from brpipe.utils.paths import INEP_TRANSFORMACOES
from brpipe.viz.mapas.config import DADOS, COLUNAS


def _carregar_csv() -> pd.DataFrame:
	path = INEP_TRANSFORMACOES / DADOS.arquivos.uf
	return pd.read_csv(path, sep=DADOS.separador)


def _metrica_wide(df: pd.DataFrame) -> pd.DataFrame:
	cols = COLUNAS.territoriais.uf
	cfg = DADOS.metrica_principal.wide

	if cfg is None:
		raise ValueError("Configuração wide não definida para a métrica principal (UF)")

	return (
		df[
			[
				cols.tabela,
				cfg.coluna_valor,
			]
		]
		.rename(
			columns={cfg.coluna_valor: DADOS.metrica_principal.coluna_mapa}
		)
	)


def _metrica_long(df: pd.DataFrame) -> pd.DataFrame:
	cols = COLUNAS.territoriais.uf
	cfg = DADOS.metrica_principal.long

	if cfg is None:
		raise ValueError("Configuração long não definida para a métrica principal (UF)")

	df = df.copy()

	if cfg.anos is not None:
		df = df[df[cfg.coluna_ano].isin(cfg.anos)]

	return (
		df
		.groupby(
			cols.tabela,
			as_index=False
		)
		.agg({cfg.coluna_valor: cfg.agregacao})
		.rename(
			columns={cfg.coluna_valor: DADOS.metrica_principal.coluna_mapa}
		)
	)


def carregar_metrica_uf() -> pd.DataFrame:
	df = _carregar_csv()

	if DADOS.formato == "wide":
		return _metrica_wide(df)

	if DADOS.formato == "long":
		return _metrica_long(df)

	raise ValueError(f"Formato de dados desconhecido: {DADOS.formato}")
