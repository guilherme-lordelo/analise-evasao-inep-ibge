import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from brpipe.ibge.config.models import SheetIBGEConfig, TransformacaoColunaConfig


def aplicar_transformacoes_colunas(
	df: DataFrame,
	sheet_cfg: SheetIBGEConfig
) -> DataFrame:

	if not sheet_cfg.transformacoes_colunas:
		return df

	fontes_a_remover: set[str] = set()

	for transf in sheet_cfg.transformacoes_colunas:
		df = _aplicar_transformacao(df, transf)

		# registra fonte para remoção posterior
		fontes_a_remover.add(transf.fonte)

	# remove colunas fonte após todas as transformações
	fontes_validas = [c for c in fontes_a_remover if c in df.columns]

	if fontes_validas:
		df = df.drop(columns=fontes_validas)

	return df

def _aplicar_transformacao(
	df: DataFrame,
	transf: TransformacaoColunaConfig
) -> DataFrame:

	if transf.fonte not in df.columns:
		print(f"Aviso: coluna fonte '{transf.fonte}' não encontrada")
		print(f"para transformação '{transf.destino}'. Pulando.")
		return df

	serie = pd.to_numeric(df[transf.fonte], errors="coerce")

	if transf.tipo == "logit":
		df[transf.destino] = _logit(
			serie,
			escala_origem=transf.escala_origem
		)

	return df

def _logit(
	serie: Series,
	escala_origem: str | None = None,
	epsilon: float = 1e-6
) -> Series:

	p = serie.astype(float)

	if escala_origem == "0-100":
		p = p / 100.0

	p = p.clip(epsilon, 1 - epsilon)

	return pd.Series(
		np.log(p / (1 - p)),
		index=p.index,
		name=serie.name
	)