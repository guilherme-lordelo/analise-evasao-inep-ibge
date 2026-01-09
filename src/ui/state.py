import streamlit as st
from ui.yaml_io import load_yaml

CONFIG_PATH = "config/inep.yml"

def init_state():
	if "doc" not in st.session_state:
		st.session_state.doc = load_yaml(CONFIG_PATH)

	if "view" not in st.session_state:
		st.session_state.view = "lista"

	if "formula_atual" not in st.session_state:
		st.session_state.formula_atual = None
