import streamlit as st
from ui.sections.formulas.validacao import validar_expressao
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

	def validate(self, doc: dict) -> list[str]:
		erros = []

		formulas = doc.get("formulas", {})
		quantitativas = set(
			doc.get("variaveis", {})
			   .get("quantitativas", {})
			   .keys()
		)
		limites = set(
			doc.get("validacao_limites", {}).keys()
		)

		for nome, formula in formulas.items():
			expr = formula.get("expressao", "")

			erros.extend(
				validar_expressao(
					expr,
					quantitativas,
					limites,
					ctx=f"Fórmula '{nome}' (expressão)",
				)
			)

			regras = (
				formula.get("validacao", {})
					   .get("regras", [])
			)

			for i, regra in enumerate(regras):
				erros.extend(
					validar_expressao(
						regra,
						quantitativas,
						limites,
						ctx=f"Fórmula '{nome}' (regra {i+1})",
					)
				)

		return erros