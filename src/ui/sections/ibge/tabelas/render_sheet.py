import streamlit as st
from ui.modules.estado_ibge import (
	sheet_state_key,
	init_sheet_state,
)
from ui.sections.ibge.tabelas.models import ColunaEditavel, FormaColuna
from .render_coluna import render_coluna


def render_sheet(
	tab_key: str,
	idx: int,
	sheet: dict,
	doc: dict,
):
	init_sheet_state(tab_key, idx, sheet)

	state_key = sheet_state_key(tab_key, idx)
	state = st.session_state[state_key]

	state["descricao_sheet"] = st.text_input(
		"Descrição da sheet",
		value=state["descricao_sheet"],
		key=f"{tab_key}_sheet_{idx}_desc"
	)

	state["arquivo"] = st.text_input(
		"Arquivo CSV",
		value=state["arquivo"],
		key=f"{tab_key}_sheet_{idx}_arq"
	)

	st.markdown("### Colunas")
	pesos = list(doc.get("colunas_peso", {}).keys())

	for col in state["colunas"]:
		def _remove(col=col):
			state["colunas"].remove(col)
			st.rerun()
		render_coluna(
			col,
			key_prefix=f"{tab_key}_{idx}_{col.uid}",
			pesos=pesos,
			on_remove=_remove,
	)

	if st.button("Adicionar coluna", key=f"{tab_key}_{idx}_add_col"):
		state["colunas"].append(
			ColunaEditavel(nome="", forma=FormaColuna.CRUA)
		)
		st.rerun()

	st.markdown("### Remoção de colunas (por índice)")

	texto = st.text_input(
		"Índices das colunas a remover (ex: 3,5,6)",
		value=", ".join(map(str, state["remover_colunas_idx"])),
		key=f"{tab_key}_{idx}_remover_idx"
	)

	if texto.strip():
		try:
			state["remover_colunas_idx"] = [
				int(i.strip())
				for i in texto.split(",")
				if i.strip()
			]
		except ValueError:
			st.error("Os índices devem ser números inteiros.")
	else:
		state["remover_colunas_idx"] = []
