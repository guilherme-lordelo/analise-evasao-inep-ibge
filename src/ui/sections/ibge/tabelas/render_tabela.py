import streamlit as st

from ui.modules.estado_ibge import sheet_state_key
from ui.modules.uid import get_sheet_uid
from .render_sheet import render_sheet


def render_tabela(tab_key: str, tabela: dict, doc: dict):
	tabela["descricao_tabela"] = st.text_input(
		"Descrição da tabela",
		value=tabela.get("descricao_tabela", ""),
		key=f"{tab_key}_desc",
	)

	sheets = tabela.setdefault("sheets", [])

	def remove_sheet(uid: str):
		state_key = sheet_state_key(tab_key, uid)

		if state_key in st.session_state:
			del st.session_state[state_key]

		sheets[:] = [
			s for s in sheets
			if s.get("_ui_uid") != uid
		]

		st.rerun()
	idx = 0

	for sheet in sheets:
		idx = idx + 1
		uid = get_sheet_uid(sheet)

		with st.expander(f"Planilha {idx}", expanded=False):
			render_sheet(
				tab_key=tab_key,
				sheet_uid=uid,
				sheet=sheet,
				doc=doc,
				on_remove_sheet=lambda u=uid: remove_sheet(u),
			)

	if st.button("Adicionar Planilha", key=f"{tab_key}_add_sheet"):
		sheet = {
			"descricao_sheet": "",
			"arquivo": "",
			"colunas": [],
			"remover_colunas_idx": [],
			"merges_colunas": [],
		}

		get_sheet_uid(sheet)
		sheets.append(sheet)

		st.rerun()
