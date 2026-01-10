import streamlit as st
from .render_tabela import render_tabela
from .validacao import validate_tabelas

class IBGETabelasSection:
	key = "tabelas"
	label = "Tabelas IBGE"

	def render(self, doc: dict):
		tabelas = doc.setdefault("tabelas", {})

		st.subheader(self.label)

		for tab_key in list(tabelas.keys()):
			with st.expander(f"Tabela {tab_key}", expanded=False):
				col1, col2 = st.columns([0.85, 0.15])

				with col1:
					render_tabela(tab_key, tabelas[tab_key], doc)

				with col2:
					if st.button("Remover", key=f"{tab_key}_remove"):
						del tabelas[tab_key]
						st.rerun()

		if st.button("Adicionar tabela"):
			n = len(tabelas) + 1
			tabelas[f"tab{n}"] = {
				"descricao_tabela": "",
				"sheets": []
			}

	def validate(self, doc: dict) -> list[str]:
		return validate_tabelas(doc)
