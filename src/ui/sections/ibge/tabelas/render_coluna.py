import streamlit as st

from ui.sections.ibge.tabelas.models import ColunaEditavel
from .constantes import FORMATOS

def render_coluna(col: ColunaEditavel, key_prefix: str, pesos: list[str]):
	col.nome = st.text_input("Nome", col.nome, key=f"{key_prefix}_nome")

	col.formato = st.selectbox(
		"Formato",
		FORMATOS,
		index=FORMATOS.index(col.formato),
		key=f"{key_prefix}_formato"
	)

	if col.formato != "CONTAGEM":
		col.coluna_peso = st.selectbox(
			"Coluna de peso",
			pesos,
			index=pesos.index(col.coluna_peso)
			if col.coluna_peso in pesos else 0,
			key=f"{key_prefix}_peso"
		)
	else:
		col.coluna_peso = None
