from typing import Dict
from brpipe.ibge.config.parser import (
	validar_remocao_colunas,
	parse_merges,
	parse_transformacoes,
)
from brpipe.ibge.config.models import SheetIBGEConfig, TabelaIBGEConfig

def carregar_tabelas_ibge(_cfg: dict) -> Dict[str, TabelaIBGEConfig]:

	tabelas = {}
	sheet_count = 0

	for tabela_id, info in _cfg.get("tabelas", {}).items():
		sheets = []

		for sheet in info.get("sheets", []):
			sheet_count += 1

			ctx = f"[IBGE][{tabela_id}][{sheet['arquivo']}]"

			colunas = sheet.get("colunas", [])
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

		tabelas[tabela_id] = TabelaIBGEConfig(
			tabela_id=tabela_id,
			descricao=info.get("descricao_tabela", ""),
			arquivo_xls=f"{tabela_id}.xls",
			sheets=sheets,
		)

	print(f"Encontradas {len(tabelas)} tabelas e {sheet_count} sheets IBGE na configuração.")
	return tabelas