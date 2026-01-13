import streamlit as st
from ui.sections.base_section import Section


class MunicipioSection(Section):
	key = "municipio"
	label = "Município"

	def render(self, doc: dict):
		cfg = doc.setdefault("municipio", {})

		st.subheader("Configuração de Município")

		cfg["codigo"] = st.text_input(
			"Código do município",
			value=cfg.get("codigo", ""),
		)

		cfg["nome"] = st.text_input(
			"Nome do município",
			value=cfg.get("nome", ""),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("municipio", {})

		if not cfg.get("codigo"):
			erros.append("Município: coluna de código não informada.")

		if not cfg.get("nome"):
			erros.append("Município: coluna de nome não informada.")

		return erros
