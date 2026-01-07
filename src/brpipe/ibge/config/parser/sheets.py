from brpipe.ibge.config.parser.colunas import parse_colunas
from brpipe.ibge.config.parser.validacoes import validar_remocao_colunas
from brpipe.ibge.config.parser.merges import parse_merges
from brpipe.ibge.config.parser.transformacoes import parse_transformacoes
from brpipe.ibge.config.models import SheetIBGEConfig
from brpipe.ibge.config.runtime import TIPO_DEFAULT_IBGE


def parse_sheets(
	tabela_id: str,
	sheets_cfg: list[dict],
) -> list[SheetIBGEConfig]:

	sheets: list[SheetIBGEConfig] = []

	for sheet in sheets_cfg:
		ctx = f"[IBGE][{tabela_id}][{sheet['arquivo']}]"

		colunas_cfg  = sheet.get("colunas", [])
		colunas = parse_colunas(colunas_cfg, tipo_default=TIPO_DEFAULT_IBGE, ctx=ctx)
		remover = sheet.get("remover_colunas", [])

		validar_remocao_colunas(colunas, remover, ctx)

		merges, destinos_merge = parse_merges(
			sheet.get("merges_colunas", []),
			colunas,
			remover,
			ctx,
		)

		transformacoes = parse_transformacoes(
			sheet.get("transformacoes_colunas", []),
			colunas,
			destinos_merge,
			remover,
			ctx,
		)

		sheets.append(
			SheetIBGEConfig(
				sheet_id=sheet.get("sheet_id"),
				descricao=sheet.get("descricao_sheet", ""),
				arquivo=sheet["arquivo"],
				colunas_especificas=colunas,
				merges_colunas=merges or None,
				transformacoes_colunas=transformacoes or None,
				remover_colunas=remover or None,
			)
		)

	return sheets
