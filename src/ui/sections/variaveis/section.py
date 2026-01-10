import streamlit as st
from ui.sections.variaveis.temporais import render_temporais
from ui.sections.variaveis.categoricas import render_categoricas
from ui.sections.variaveis.quantitativas import render_quantitativas

class VariaveisSection:
	key = "variaveis"
	label = "Variáveis"

	def render(self, doc: dict):
		vars = doc.setdefault("variaveis", {})

		tab1, tab2, tab3 = st.tabs([
			"Temporais",
			"Categóricas",
			"Quantitativas",
		])

		with tab1:
			render_temporais(vars.setdefault("temporais", {}))

		with tab2:
			render_categoricas(vars.setdefault("categoricas", {}))

		with tab3:
			render_quantitativas(vars.setdefault("quantitativas", {}))

	def validate(self, doc: dict) -> list[str]:
		erros = []

		variaveis = doc.get("variaveis", {})
		quantitativas = variaveis.get("quantitativas", {})

		quantitativas = {str(k): str(v) for k, v in quantitativas.items()}

		colunas_quantitativas = set(quantitativas.keys())

		mapeamento = doc.get("mapeamento_colunas", {})
		mapeamento = {str(k): str(v) for k, v in mapeamento.items()}

		for origem, destino in mapeamento.items():
			if destino not in colunas_quantitativas:
				erros.append(
					f"Coluna '{destino}' não está definida como variável quantitativa."
				)

		return erros
