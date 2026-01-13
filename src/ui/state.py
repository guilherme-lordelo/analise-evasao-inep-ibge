import streamlit as st
from ui.yaml_io import load_yaml

INEP_CONFIG_PATH = "config/inep.yml"
IBGE_CONFIG_PATH = "config/ibge.yml"
BASE_CONFIG_PATH = "config/base.yml"
CHART_CONFIG_PATH = "config/charts.yml"

def init_state():
	if "doc_inep" not in st.session_state:
		st.session_state.doc_inep = load_yaml(INEP_CONFIG_PATH)

	if "doc_ibge" not in st.session_state:
		st.session_state.doc_ibge = load_yaml(IBGE_CONFIG_PATH)

	if "doc_pipeline_base" not in st.session_state:
		st.session_state.doc_pipeline_base = load_yaml(BASE_CONFIG_PATH)

	if "doc_chart" not in st.session_state:
		st.session_state.doc_charts = load_yaml(CHART_CONFIG_PATH)

	if "view" not in st.session_state:
		st.session_state.view = "lista"

	if "formula_atual" not in st.session_state:
		st.session_state.formula_atual = None
