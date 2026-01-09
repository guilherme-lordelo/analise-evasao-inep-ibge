from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.models import SheetIBGEConfig


def coletar_resultados(
	tabela,
	sheet: SheetIBGEConfig,
) -> list[tuple[str, ResultadoTipo]]:

	resultado: list[tuple[str, ResultadoTipo]] = []

	for col in sheet.colunas_especificas:
		resultado.append(
			(col.nome, col.tipo_visualizacao)
		)

	return resultado

def coletar_resultados_merges(
	tabela,
	sheet: SheetIBGEConfig,
) -> tuple[list[tuple[str, ResultadoTipo]], list[str]] | None:

	if not sheet.merges_colunas:
		return None

	resultados: list[tuple[str, ResultadoTipo]] = []
	fontes_remover: list[str] = []

	for merge in sheet.merges_colunas:
		col = merge.coluna

		resultados.append(
			(merge.destino, col.tipo_visualizacao)
		)

		fontes_remover.extend(merge.fontes)

	return resultados, fontes_remover
