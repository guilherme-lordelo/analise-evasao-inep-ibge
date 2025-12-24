from typing import Dict
from brpipe.ibge.config.models import TabelaIBGEConfig
from brpipe.ibge.config.parser.sheets import parse_sheets


def parse_tabelas(_cfg: dict) -> Dict[str, TabelaIBGEConfig]:

	tabelas: Dict[str, TabelaIBGEConfig] = {}
	sheet_count = 0

	for tabela_id, info in _cfg.get("tabelas", {}).items():

		sheets_cfg = info.get("sheets", [])
		sheets = parse_sheets(tabela_id, sheets_cfg)
		sheet_count += len(sheets)

		tabelas[tabela_id] = TabelaIBGEConfig(
			tabela_id=tabela_id,
			descricao=info.get("descricao_tabela", ""),
			arquivo_xls=f"{tabela_id}.xls",
			sheets=sheets,
		)

	print(
		f"Encontradas {len(tabelas)} tabelas e "
		f"{sheet_count} sheets IBGE na configuração."
	)

	return tabelas
