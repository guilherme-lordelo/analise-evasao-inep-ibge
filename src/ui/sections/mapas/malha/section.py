import streamlit as st
from ui.sections.base_section import Section


class MalhaSection(Section):
	key = "malha"
	label = "Malha Geográfica"

	def render(self, doc: dict):
		cfg = doc.setdefault("malha", {})

		st.subheader("Configuração da Malha")

		cfg["municipio"] = st.text_input(
			"Coluna de município",
			value=cfg.get("municipio", "CD_MUN"),
		)

		cfg["uf"] = st.text_input(
			"Coluna de UF",
			value=cfg.get("uf", "SIGLA_UF"),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("malha", {})

		if not cfg.get("municipio"):
			erros.append("Malha: coluna de município não informada.")

		if not cfg.get("uf"):
			erros.append("Malha: coluna de UF não informada.")

		return erros
