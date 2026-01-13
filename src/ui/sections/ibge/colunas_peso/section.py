import streamlit as st
from ui.sections.base_section import Section


class ColunasPesoSection(Section):
	key = "colunas_peso"
	label = "Colunas de Peso"

	def render(self, doc: dict):
		st.subheader("Colunas de Peso")
		st.caption(
			"Defina colunas que representam totais "
			"e podem ser usadas como peso em indicadores."
		)

		colunas_peso = doc.setdefault("colunas_peso", {})

		remover = []

		for nome_logico, coluna_fisica in colunas_peso.items():
			c1, c2, c3 = st.columns([3, 4, 1])

			with c1:
				novo_nome = st.text_input(
					"Identificador",
					value=nome_logico,
					key=f"peso_nome_{nome_logico}",
				)

			with c2:
				nova_coluna = st.text_input(
					"Coluna física",
					value=coluna_fisica,
					key=f"peso_coluna_{nome_logico}",
				)

			with c3:
				if st.button("Remover", key=f"peso_del_{nome_logico}"):
					remover.append(nome_logico)

			if novo_nome != nome_logico:
				colunas_peso[novo_nome] = colunas_peso.pop(nome_logico)

		for k in remover:
			colunas_peso.pop(k, None)

		st.divider()

		if st.button("Adicionar coluna de peso"):
			colunas_peso[f"peso_{len(colunas_peso)+1}"] = ""

	def validate(self, doc: dict):
		erros = []
		colunas_peso = doc.get("colunas_peso", {})

		if not colunas_peso:
			erros.append("IBGE: nenhuma coluna de peso definida.")

		for nome, coluna in colunas_peso.items():
			if not nome:
				erros.append("IBGE: identificador vazio em colunas_peso.")
			if not coluna:
				erros.append(
					f"IBGE: coluna física vazia para peso '{nome}'."
				)

		return erros
