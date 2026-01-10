import streamlit as st
from .render_sheet import render_sheet

def render_tabela(tab_key: str, tabela: dict, doc: dict):
	tabela["descricao_tabela"] = st.text_input(
		"Descrição da tabela",
		value=tabela.get("descricao_tabela", ""),
		key=f"{tab_key}_desc"
	)

	sheets = tabela.setdefault("sheets", [])

	for i, sheet in enumerate(sheets):
		with st.expander(f"Sheet {i+1}", expanded=i == 0):
			render_sheet(tab_key, i, sheet, doc)

	if st.button("Adicionar sheet", key=f"{tab_key}_add_sheet"):
		sheets.append({
			"descricao_sheet": "",
			"arquivo": "",
			"colunas": [],
			"remover_colunas_idx": []
		})
