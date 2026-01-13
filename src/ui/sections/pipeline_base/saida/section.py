import streamlit as st
from ui.sections.base_section import Section


class SaidaSection(Section):
	key = "saida"
	label = "Saída"

	def render(self, doc: dict):
		cfg = doc.setdefault("saida", {})

		st.subheader("Configuração de Saída")

		cfg["encoding"] = st.text_input(
			"Encoding",
			value=cfg.get("encoding", "utf-8"),
		)

		cfg["sep"] = st.text_input(
			"Separador",
			value=cfg.get("sep", ";"),
		)

	def validate(self, doc: dict):
		erros = []
		cfg = doc.get("saida", {})

		if not cfg.get("encoding"):
			erros.append("Saída: encoding não informado.")

		if not cfg.get("sep"):
			erros.append("Saída: separador não informado.")

		return erros
