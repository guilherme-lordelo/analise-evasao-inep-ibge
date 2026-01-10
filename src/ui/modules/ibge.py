import streamlit as st
from ui.yaml_io import save_yaml

from ui.sections.ibge.colunas_peso.section import ColunasPesoSection
from ui.sections.ibge.tabelas.section import IBGETabelasSection
from ui.modules.base import ConfigModule


class IBGEModule(ConfigModule):
	key = "ibge"
	label = "IBGE"

	SECTIONS = [
		ColunasPesoSection(),
		IBGETabelasSection(),
	]

	def render_sidebar(self):
		labels = [s.label for s in self.SECTIONS]
		keys = [s.key for s in self.SECTIONS]

		if "ibge_section" not in st.session_state:
			st.session_state.ibge_section = keys[0]

		st.session_state.ibge_section = st.sidebar.radio(
			"Configurações IBGE",
			keys,
			format_func=dict(zip(keys, labels)).get
		)

	def render_main(self):
		doc = st.session_state.doc_ibge

		section = next(
			s for s in self.SECTIONS
			if s.key == st.session_state.ibge_section
		)
		section.render(doc)

	def validate(self) -> list[str]:
		doc = st.session_state.doc_ibge
		erros = []

		for s in self.SECTIONS:
			erros.extend(s.validate(doc) or [])

		return erros

	def save(self):
		save_yaml(
			st.session_state.doc_ibge,
			"config/ibge.yml"
		)
