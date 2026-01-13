import streamlit as st
from ui.yaml_io import save_yaml
from ui.modules.base import ConfigModule

from ui.sections.mapas.plot.section import PlotSection
from ui.sections.mapas.malha.section import MalhaSection


class MapasModule(ConfigModule):
	key = "mapas"
	label = "Mapas"

	SECTIONS = [
		MalhaSection(),
		PlotSection(),
	]

	def render_sidebar(self):
		labels = [s.label for s in self.SECTIONS]
		keys = [s.key for s in self.SECTIONS]

		if "mapas_section" not in st.session_state:
			st.session_state.mapas_section = keys[0]

		st.session_state.mapas_section = st.sidebar.radio(
			"Configurações de Mapas",
			keys,
			format_func=dict(zip(keys, labels)).get,
		)

	def render_main(self):
		doc = st.session_state.doc_mapas

		section = next(
			s for s in self.SECTIONS
			if s.key == st.session_state.mapas_section
		)

		section.render(doc)

	def validate(self) -> list[str]:
		doc = st.session_state.doc_mapas
		erros = []

		for s in self.SECTIONS:
			erros.extend(s.validate(doc) or [])

		return erros

	def save(self):
		save_yaml(
			st.session_state.doc_mapas,
			"config/mapas.yml",
		)
