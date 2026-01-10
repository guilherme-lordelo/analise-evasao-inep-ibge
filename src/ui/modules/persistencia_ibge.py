
from .estado_ibge import sheet_state_key
from ui.sections.ibge.tabelas.serializacao import serializar_coluna


def commit_ibge_edicao(doc: dict):
	tabelas = doc.get("tabelas", {})

	for tab_key, tabela in tabelas.items():
		sheets = tabela.get("sheets", [])

		for idx, sheet in enumerate(sheets):
			state_key = sheet_state_key(tab_key, idx)

			if state_key not in __import__("streamlit").session_state:
				continue

			state = __import__("streamlit").session_state[state_key]

			_aplicar_sheet_state(sheet, state)


def _aplicar_sheet_state(sheet: dict, state: dict):
	sheet["descricao_sheet"] = state["descricao_sheet"]
	sheet["arquivo"] = state["arquivo"]

	sheet["colunas"] = [
		serializar_coluna(c)
		for c in state["colunas"]
	]

	if state["remover_colunas_idx"]:
		sheet["remover_colunas_idx"] = state["remover_colunas_idx"]
	else:
		sheet.pop("remover_colunas_idx", None)
