import streamlit as st
from ui.yaml_io import save_yaml
from ui.sections.inep.formulas.section import FormulasSection
from ui.sections.inep.variaveis.section import VariaveisSection
from ui.sections.inep.mapeamento_colunas.section import MapeamentoColunasSection
from ui.sections.inep.coluna_peso.section import ColunaPesoSection
from ui.sections.inep.arquivos.section import ArquivosSection
from ui.sections.inep.anos.section import AnosSection
from ui.sections.inep.extracao.section import ExtracaoSection
from ui.sections.inep.validacao_limites.section import ValidacaoLimitesSection
from ui.sections.inep.limpeza.section import LimpezaSection

from ui.modules.base import ConfigModule


class INEPModule(ConfigModule):
	key = "inep"
	label = "INEP"

	SECTIONS = [
		FormulasSection(),
		VariaveisSection(),
		MapeamentoColunasSection(),
		ColunaPesoSection(),
		ArquivosSection(),
		AnosSection(),
		ExtracaoSection(),
		ValidacaoLimitesSection(),
		LimpezaSection(),
	]

	def render_sidebar(self):
		labels = [s.label for s in self.SECTIONS]
		keys = [s.key for s in self.SECTIONS]

		if "inep_section" not in st.session_state:
			st.session_state.inep_section = keys[0]

		st.session_state.inep_section = st.sidebar.radio(
			"Configurações INEP",
			keys,
			format_func=dict(zip(keys, labels)).get
		)

	def render_main(self):
		doc = st.session_state.doc_inep

		section = next(
			s for s in self.SECTIONS
			if s.key == st.session_state.inep_section
		)
		section.render(doc)

	def validate(self) -> list[str]:
		doc = st.session_state.doc_inep
		erros = []
		for s in self.SECTIONS:
			erros.extend(s.validate(doc) or [])
		return erros
	
	def save(self):
		save_yaml(
			st.session_state.doc_inep,
			"config/inep.yml"
		)