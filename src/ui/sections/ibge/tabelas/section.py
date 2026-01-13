import streamlit as st
from .render_tabela import render_tabela
from .validacao import validate_tabelas

def _init_state():
	st.session_state.setdefault("criando_tabela", False)
	st.session_state.setdefault("novo_nome_tabela", "")
	st.session_state.setdefault("merges_colunas", [])

class IBGETabelasSection:
	key = "tabelas"
	label = "Tabelas IBGE"

	def render(self, doc: dict):
		tabelas = doc.setdefault("tabelas", {})
		_init_state()

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
			st.session_state.criando_tabela = True
			st.session_state.novo_nome_tabela = ""

		if st.session_state.criando_tabela:
			st.markdown("### Nova tabela")

			nome = st.text_input(
				"Deve corresponder ao nome do arquivo 'xls' a ser extraído, não incluindo a extensão.",
				key="novo_nome_tabela",
				placeholder="ex: tab1"
			)

			col1, col2 = st.columns(2)

			with col1:
				if st.button("Criar"):
					if not nome:
						st.error("Informe um nome para a tabela.")
					elif nome in tabelas:
						st.error("Já existe uma tabela com esse nome.")
					else:
						tabelas[nome] = {
							"descricao_tabela": "",
							"sheets": []
						}
						st.session_state.criando_tabela = False
						st.rerun()

			with col2:
				if st.button("Cancelar"):
					st.session_state.criando_tabela = False
					st.rerun()


	def validate(self, doc: dict) -> list[str]:
		return validate_tabelas(doc)
