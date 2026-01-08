from copy import deepcopy
from brpipe.ibge.config.models import ColunaIBGEConfig, SheetIBGEConfig
from brpipe.ibge.config.parser.colunas import parse_colunas
from brpipe.ibge.config.parser.merges import parse_merges
from brpipe.ibge.config.parser.validacoes import validar_remocao_colunas
from brpipe.ibge.config.runtime import COLUNAS_PESO, TIPO_DEFAULT_IBGE


def to_zero_based(indices: list[int] | set[int], *, ctx: str) -> set[int]:
	zero = set()

	for idx in indices:
		if idx <= 0:
			raise ValueError(f"{ctx}: indices must start at 1, got {idx}")
		zero.add(idx - 1)

	return zero

def aplicar_template_colunas(
	template: list[ColunaIBGEConfig],
	colunas_sheet: list[ColunaIBGEConfig],
	ctx: str,
) -> list[ColunaIBGEConfig]:

	if len(template) != len(colunas_sheet):
		raise ValueError(
			f"{ctx} Quantidade de colunas difere do template "
			f"({len(colunas_sheet)} != {len(template)})"
		)

	colunas = []

	for base, atual in zip(template, colunas_sheet):
		colunas.append(
			ColunaIBGEConfig(
				nome=atual.nome,  # nome real do sheet
				tipo_dado=base.tipo_dado,
				tipo_agregacao=base.tipo_agregacao,
				tipo_visualizacao=base.tipo_visualizacao,
			)
		)

	return colunas


def parse_sheets(
	tabela_id: str,
	sheets_cfg: list[dict],
) -> list[SheetIBGEConfig]:

	sheets = []

	template_colunas = None
	base_remover_idx = None
	base_merges = None

	for sheet in sheets_cfg:
		ctx = f"[IBGE][{tabela_id}][{sheet['arquivo']}]"

		colunas_raw = parse_colunas(
			sheet["colunas"],
			tipo_default=TIPO_DEFAULT_IBGE,
			colunas_peso=COLUNAS_PESO,
			ctx=ctx,
		)

		if template_colunas is None:
			colunas = colunas_raw
			template_colunas = colunas_raw
		else:
			colunas = aplicar_template_colunas(
				template_colunas,
				colunas_raw,
				ctx=ctx,
			)

		qtd_colunas = len(colunas)

		if "remover_colunas_idx" in sheet:
			remover_idx_raw = sheet["remover_colunas_idx"]
			validar_remocao_colunas(qtd_colunas, remover_idx_raw, ctx)
			remover_idx = to_zero_based(remover_idx_raw, ctx=ctx)
			base_remover_idx = remover_idx
		else:
			remover_idx = deepcopy(base_remover_idx) or set()

		for i in remover_idx:
			if i < 0 or i >= qtd_colunas:
				raise ValueError(
					f"{ctx} Índice herdado para remoção inválido: {i + 1} "
					f"(sheet possui {qtd_colunas} colunas)"
				)


		remover_nomes = [colunas[i].nome for i in remover_idx]

		if "merges_colunas" in sheet:
			merges = parse_merges(
				sheet["merges_colunas"],
				colunas=colunas,
				colunas_peso=COLUNAS_PESO,
				remover_idx=remover_idx,
				ctx=ctx,
			)
			base_merges = merges
		else:
			merges = deepcopy(base_merges)


		sheets.append(
			SheetIBGEConfig(
				sheet_id=sheet.get("sheet_id"),
				descricao=sheet.get("descricao_sheet", ""),
				arquivo=sheet["arquivo"],
				colunas_especificas=colunas,
				remover_colunas=remover_nomes or None,
				merges_colunas=merges or None,
			)
		)

	return sheets
