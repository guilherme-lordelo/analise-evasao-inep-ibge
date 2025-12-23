from pandas import DataFrame
from brpipe.ibge.config.models import SheetIBGEConfig


def remover_colunas(
	df: DataFrame,
	sheet_cfg: SheetIBGEConfig
) -> DataFrame:
	"""
	Remove colunas declaradas em remover_colunas na configuração da sheet.
	"""

	if not sheet_cfg.remover_colunas:
		return df

	colunas_a_remover = [
		c for c in sheet_cfg.remover_colunas if c in df.columns
	]

	return df.drop(columns=colunas_a_remover)
