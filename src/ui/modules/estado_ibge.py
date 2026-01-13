import streamlit as st
from ui.modules.parsers import parse_coluna_yaml


def sheet_state_key(tab_key: str, sheet_uid: str) -> str:
	return f"sheet_edit_{tab_key}_{sheet_uid}"


def init_sheet_state(tab_key: str, sheet_uid: str, sheet: dict):
	key = sheet_state_key(tab_key, sheet_uid)

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
		"merges_colunas": list(sheet.get("merges_colunas", [])),
	}
