import streamlit as st
from ui.sections.formulas.view_lista import render_lista
from ui.sections.formulas.view_editor import render_editor

class FormulasSection:
	key = "formulas"
	label = "Fórmulas"

	def render(self, doc: dict):
		formulas = doc.setdefault("formulas", {})

		if "view" not in st.session_state:
			st.session_state.view = "lista"

		if st.session_state.view == "lista":
			render_lista(formulas)

		elif st.session_state.view == "editor":
			render_editor(formulas, st.session_state.formula_atual)

	def validate(self, doc: dict):
		from brpipe.inep.config.formulas import carregar_formulas
		carregar_formulas(doc)
