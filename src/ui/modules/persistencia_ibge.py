
from .estado_ibge import sheet_state_key
from ui.sections.ibge.tabelas.serializacao import serializar_coluna


import streamlit as st
from ui.modules.estado_ibge import sheet_state_key
from ui.sections.ibge.tabelas.serializacao import serializar_coluna


def commit_ibge_edicao(doc: dict):
	tabelas = doc.get("tabelas", {})

	for tab_key, tabela in tabelas.items():
		sheets_yaml = []

		for sheet in tabela.get("sheets", []):
			uid = sheet.get("_ui_uid")
			if not uid:
				continue

			state_key = sheet_state_key(tab_key, uid)
			if state_key not in st.session_state:
				continue

			state = st.session_state[state_key]

			sheets_yaml.append({
				"descricao_sheet": state["descricao_sheet"],
				"arquivo": state["arquivo"],
				"colunas": [
					serializar_coluna(c)
					for c in state["colunas"]
				],
				**(
					{"remover_colunas_idx": state["remover_colunas_idx"]}
					if state["remover_colunas_idx"]
					else {}
				),
				**(
					{"merges_colunas": state["merges_colunas"]}
					if state.get("merges_colunas")
					else {}
				),
			})


		tabela["sheets"] = sheets_yaml



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

	if state.get("merges_colunas"):
		sheet["merges_colunas"] = state["merges_colunas"]
	else:
		sheet.pop("merges_colunas", None)
