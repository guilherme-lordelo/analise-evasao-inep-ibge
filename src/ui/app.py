import streamlit as st
from ui.state import init_state
from ui.yaml_io import save_yaml
from ui.sections.formulas.section import FormulasSection
from ui.sections.variaveis.section import VariaveisSection
from ui.sections.mapeamento_colunas.section import MapeamentoColunasSection
from ui.sections.coluna_peso.section import ColunaPesoSection
from ui.sections.arquivos.section import ArquivosSection
from ui.sections.anos.section import AnosSection
from ui.sections.extracao.section import ExtracaoSection
from ui.sections.validacao_limites.section import ValidacaoLimitesSection
from ui.sections.limpeza.section import LimpezaSection


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

init_state()

doc = st.session_state.doc

st.set_page_config(page_title="Editor INEP", layout="wide")
st.title("Editor de Configuração INEP")

labels = [s.label for s in SECTIONS]
keys = [s.key for s in SECTIONS]

if "section" not in st.session_state:
	st.session_state.section = keys[0]

selected = st.sidebar.radio("Configurações", keys, format_func=dict(zip(keys, labels)).get)
st.session_state.section = selected

section = next(s for s in SECTIONS if s.key == selected)
section.render(doc)

st.divider()

col1, col2 = st.columns(2)

with col1:
	if st.button("Validar configuração"):
		erros = []

		for s in SECTIONS:
			erros.extend(s.validate(doc) or [])

		if erros:
			st.error("Foram encontrados erros na configuração:")
			for e in erros:
				st.write(f"• {e}")
		else:
			st.success("Configuração válida")

with col2:
	if st.button("Salvar arquivo"):
		save_yaml(doc, "config/inep.yml")
		st.success("Arquivo salvo")
