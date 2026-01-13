import streamlit as st
from ui.yaml_io import save_yaml
from ui.modules.base import ConfigModule

from ui.sections.pipeline_base.saida.section import SaidaSection
from ui.sections.pipeline_base.municipio.section import MunicipioSection
from ui.sections.pipeline_base.estado.section import EstadoSection
from ui.sections.pipeline_base.nacional.section import NacionalSection


class PipelineBaseModule(ConfigModule):
	key = "base"
	label = "Base"

	SECTIONS = [
		SaidaSection(),
		MunicipioSection(),
		EstadoSection(),
		NacionalSection(),
	]

	def render_sidebar(self):
		labels = [s.label for s in self.SECTIONS]
		keys = [s.key for s in self.SECTIONS]

		if "territorio_section" not in st.session_state:
			st.session_state.territorio_section = keys[0]

		st.session_state.territorio_section = st.sidebar.radio(
			"Configurações base",
			keys,
			format_func=dict(zip(keys, labels)).get,
		)

	def render_main(self):
		doc = st.session_state.doc_pipeline_base

		section = next(
			s for s in self.SECTIONS
			if s.key == st.session_state.territorio_section
		)

		section.render(doc)

	def validate(self) -> list[str]:
		doc = st.session_state.doc_pipeline_base
		erros = []

		for s in self.SECTIONS:
			erros.extend(s.validate(doc) or [])

		return erros

	def save(self):
		save_yaml(
			st.session_state.doc_pipeline_base,
			"config/base.yml",
		)
