import streamlit as st
from ui.modules.parsers import parse_coluna_yaml


def sheet_state_key(tab_key: str, idx: int) -> str:
	return f"sheet_edit_{tab_key}_{idx}"


def init_sheet_state(tab_key: str, idx: int, sheet: dict):
	key = sheet_state_key(tab_key, idx)

	if key in st.session_state:
		return

	st.session_state[key] = {
		"descricao_sheet": sheet.get("descricao_sheet", ""),
		"arquivo": sheet.get("arquivo", ""),
		"remover_colunas_idx": list(sheet.get("remover_colunas_idx", [])),
		"colunas": [
			parse_coluna_yaml(c)
			for c in sheet.get("colunas", [])
		],
	}
