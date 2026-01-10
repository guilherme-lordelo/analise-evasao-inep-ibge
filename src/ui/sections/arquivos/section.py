import streamlit as st

class ArquivosSection:
	key = "arquivos"
	label = "Arquivos"

	def render(self, doc: dict):
		cfg = doc.setdefault("arquivos", {})

		st.subheader("Arquivos")

		extracao = cfg.setdefault("extracao", {})
		transformacao = cfg.setdefault("transformacao", {})

		st.markdown("### Extração")

		extracao["prefixo_input"] = st.text_input(
			"Prefixo input",
			value=extracao.get("prefixo_input", ""),
			key="arquivos_extracao_prefixo_input",
		)

		extracao["extensao_input"] = st.text_input(
			"Extensão input",
			value=extracao.get("extensao_input", ""),
			key="arquivos_extracao_extensao_input",
		)

		extracao["prefixo_output"] = st.text_input(
			"Prefixo output",
			value=extracao.get("prefixo_output", ""),
			key="arquivos_extracao_prefixo_output",
		)

		extracao["extensao_output"] = st.text_input(
			"Extensão output",
			value=extracao.get("extensao_output", ""),
			key="arquivos_extracao_extensao_output",
		)

		st.markdown("### Transformação")

		transformacao["prefixo_output"] = st.text_input(
			"Prefixo output",
			value=transformacao.get("prefixo_output", ""),
			key="arquivos_transformacao_prefixo_output",
		)

		transformacao["extensao_output"] = st.text_input(
			"Extensão output",
			value=transformacao.get("extensao_output", ""),
			key="arquivos_transformacao_extensao_output",
		)

		niveis = transformacao.setdefault("niveis", [])

		for i, nivel in enumerate(list(niveis)):
			col1, col2 = st.columns([8, 1])

			with col1:
				niveis[i] = st.text_input(
					f"Nível {i + 1}",
					value=nivel,
					key=f"arquivos_transformacao_nivel_{i}",
				)

			with col2:
				if st.button("Remover", key=f"arquivos_transformacao_del_nivel_{i}"):
					niveis.pop(i)
					st.rerun()

	def validate(self, doc: dict):
		pass
