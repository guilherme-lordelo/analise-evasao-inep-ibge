import streamlit as st
from ui.sections.base_section import Section


class EstadoSection(Section):
	key = "estado"
	label = "Estado"

	def render(self, doc: dict):
		cfg = doc.setdefault("estado", {})

		st.subheader("Configuração de Estado")

		cfg["sigla"] = st.text_input(
			"Sigla do estado (UF)",
			value=cfg.get("sigla", ""),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("estado", {})

		if not cfg.get("sigla"):
			erros.append("Estado: coluna de sigla não informada.")

		return erros
