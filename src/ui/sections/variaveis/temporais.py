import streamlit as st

def render_temporais(temporais: dict):
	st.markdown("### Variável Temporal")

	if not temporais:
		temporais["NU_ANO_CENSO"] = "Ano de referência dos dados"

	nome = next(iter(temporais.keys()))

	col1, col2 = st.columns([3, 7])

	with col1:
		novo_nome = st.text_input(
			"Código",
			value=nome,
			key="temp_nome",
		)

	with col2:
		temporais[nome] = st.text_input(
			"Descrição",
			value=temporais[nome],
			key="temp_desc",
		)

	if novo_nome != nome and novo_nome.strip():
		temporais[novo_nome] = temporais.pop(nome)
		st.rerun()
