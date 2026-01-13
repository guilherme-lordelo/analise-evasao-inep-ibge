import streamlit as st
from ui.yaml_io import save_yaml
from ui.modules.base import ConfigModule

from ui.sections.charts.linha_temporal.section import LinhaTemporalSection
from ui.sections.charts.scatter.section import ScatterSection


class ChartsModule(ConfigModule):
	key = "charts"
	label = "Charts"

	SECTIONS = [
		LinhaTemporalSection(),
		ScatterSection(),
	]

	def render_sidebar(self):
		labels = [s.label for s in self.SECTIONS]
		keys = [s.key for s in self.SECTIONS]

		if "charts_section" not in st.session_state:
			st.session_state.charts_section = keys[0]

		st.session_state.charts_section = st.sidebar.radio(
			"Configurações de Gráficos",
			keys,
			format_func=dict(zip(keys, labels)).get,
		)

	def render_main(self):
		doc = st.session_state.doc_charts

		section = next(
			s for s in self.SECTIONS
			if s.key == st.session_state.charts_section
		)

		section.render(doc)

	def validate(self) -> list[str]:
		doc = st.session_state.doc_charts
		erros = []

		for s in self.SECTIONS:
			erros.extend(s.validate(doc) or [])

		return erros

	def save(self):
		save_yaml(
			st.session_state.doc_charts,
			"config/charts.yml",
		)
