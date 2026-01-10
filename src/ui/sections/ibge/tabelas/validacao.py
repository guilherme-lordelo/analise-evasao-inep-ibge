import streamlit as st
from ui.modules.estado_ibge import sheet_state_key
from ui.sections.ibge.tabelas.constantes import FORMATOS


def validate_tabelas(doc: dict) -> list[str]:
	erros = []
	pesos = doc.get("colunas_peso", {})
	tabelas = doc.get("tabelas", {})

	for tab_key, tabela in tabelas.items():
		sheets = tabela.get("sheets", [])

		if not sheets:
			erros.append(f"{tab_key}: deve possuir ao menos uma sheet")

		for idx, sheet in enumerate(sheets):
			ctx = f"{tab_key} / sheet {idx + 1}"
			state_key = sheet_state_key(tab_key, idx)

			if state_key not in st.session_state:
				continue

			state = st.session_state[state_key]

			if not state["descricao_sheet"]:
				erros.append(f"{ctx}: descrição obrigatória")

			if not state["arquivo"]:
				erros.append(f"{ctx}: arquivo obrigatório")

			colunas = state["colunas"]
			if not colunas:
				erros.append(f"{ctx}: deve possuir colunas")

			qtd_colunas = len(colunas)
			for i in state.get("remover_colunas_idx", []):
				if i < 1 or i > qtd_colunas:
					erros.append(
						f"{ctx}: índice inválido em remover_colunas_idx ({i})"
					)

			for col in colunas:
				if not col.nome:
					erros.append(f"{ctx}: coluna sem nome")

				if col.formato not in FORMATOS:
					erros.append(
						f"{ctx}: formato inválido ({col.formato})"
					)

				if col.formato != "CONTAGEM":
					if col.coluna_peso not in pesos:
						erros.append(
							f"{ctx}: coluna {col.nome} "
							"usa coluna_peso inválida"
						)

	return erros
