import streamlit as st

def render_quantitativas(quantitativas: dict):
	st.markdown("### Variáveis Quantitativas")

	for nome in list(quantitativas.keys()):
		col1, col2, col3 = st.columns([3, 6, 1])

		with col1:
			novo_nome = st.text_input(
				"Código",
				value=nome,
				key=f"qt_nome_{nome}",
			)

		with col2:
			quantitativas[nome] = st.text_input(
				"Descrição",
				value=quantitativas[nome],
				key=f"qt_desc_{nome}",
			)

		with col3:
			if st.button("Remover", key=f"qt_del_{nome}"):
				del quantitativas[nome]
				st.rerun()

		if novo_nome != nome and novo_nome.strip() and novo_nome not in quantitativas:
			quantitativas[novo_nome] = quantitativas.pop(nome)
			st.rerun()

	st.divider()

	if st.button("Adicionar variável quantitativa"):
		base = "QT_NOVA"
		i = 1
		nome = base
		while nome in quantitativas:
			nome = f"{base}_{i}"
			i += 1

		quantitativas[nome] = ""
		st.rerun()
