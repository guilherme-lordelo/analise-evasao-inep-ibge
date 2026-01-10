import streamlit as st
from ui.sections.formulas.model import nova_formula

def render_lista(formulas: dict):
	st.subheader("Fórmulas")

	if not formulas:
		st.info("Nenhuma fórmula configurada")

	for nome in list(formulas.keys()):
		col1, col2, col3, col4 = st.columns([5, 2, 2, 1])

		with col1:
			if st.button(nome, key=f"open_{nome}"):
				st.session_state.formula_atual = nome
				st.session_state.view = "editor"
				st.rerun()

		with col2:
			novo_nome = st.text_input(
				"Renomear",
				value=nome,
				key=f"rename_{nome}",
				label_visibility="collapsed",
			)
			if novo_nome != nome and novo_nome.strip() and novo_nome not in formulas:
				formulas[novo_nome] = formulas.pop(nome)
				st.rerun()

		with col3:
			pass

		with col4:
			if st.button("Remover", key=f"del_{nome}"):
				del formulas[nome]

				if st.session_state.formula_atual == nome:
					st.session_state.formula_atual = None
					st.session_state.view = "lista"

				st.rerun()

	st.divider()

	if st.button("Adicionar nova fórmula"):
		base = "nova_formula"
		i = 1
		nome = base
		while nome in formulas:
			nome = f"{base}_{i}"
			i += 1

		formulas[nome] = nova_formula()
		st.session_state.formula_atual = nome
		st.session_state.view = "editor"
		st.rerun()
