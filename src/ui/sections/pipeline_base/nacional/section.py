import streamlit as st
from ui.sections.base_section import Section


class NacionalSection(Section):
	key = "nacional"
	label = "Nacional"

	def render(self, doc: dict):
		cfg = doc.setdefault("nacional", {})

		st.subheader("Configuração Nacional")

		cfg["coluna"] = st.text_input(
			"Coluna para agregação nacional",
			value=cfg.get("coluna", ""),
			help="Nome simbólico usado para representar o nível nacional",
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("nacional", {})

		if not cfg.get("coluna"):
			erros.append("Nacional: coluna de agregação não informada.")

		return erros
