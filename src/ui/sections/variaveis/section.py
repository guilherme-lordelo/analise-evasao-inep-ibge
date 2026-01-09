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

	def validate(self, doc: dict):
		pass
