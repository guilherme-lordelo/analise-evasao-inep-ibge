from brpipe.ibge.config import TABELAS_IBGE
from brpipe.utils.iterador import iterar_sheets_ibge
from pandas import DataFrame
from brpipe.ibge.config import COLUNAS_BASE_IBGE
from brpipe.ibge.config.models import SheetIBGEConfig
from brpipe.ibge.transformacao.limpar_linhas import limpar
from brpipe.ibge.transformacao.aplicar_schema import aplicar_schema_ibge
from brpipe.ibge.transformacao.remocao_colunas import remover_colunas
from brpipe.ibge.transformacao.merge_colunas import aplicar_merges_colunas
from brpipe.ibge.checkpoints import carregar_checkpoint
from brpipe.utils.paths import IBGE_REDUZIDO


def _transformar_sheet(
	tabela: None,
	sheet: SheetIBGEConfig
) -> DataFrame | None:
	"""
	Transforma um sheet IBGE a partir do CSV interim e
	retorna o DataFrame transformado.
	"""

	nome_interim = sheet.arquivo.replace(".csv", "_interim.csv")
	path_in = IBGE_REDUZIDO / nome_interim
	colunas = [coluna.nome for coluna in sheet.colunas_especificas]

	if not path_in.exists():
		return None

	df = carregar_checkpoint(path_in)

	if df.empty:
		return None
	df = limpar(df)
	df = aplicar_schema_ibge(
		df,
		COLUNAS_BASE_IBGE,
		colunas,
	)
	df = aplicar_merges_colunas(df, sheet)
	df = remover_colunas(df, sheet)

	return df

def transformar_ibge():
	return iterar_sheets_ibge(TABELAS_IBGE, _transformar_sheet)
