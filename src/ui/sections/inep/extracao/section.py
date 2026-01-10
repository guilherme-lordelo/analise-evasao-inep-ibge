import streamlit as st

class ExtracaoSection:
	key = "extracao"
	label = "Extração de Dados"

	def render(self, doc: dict):
		cfg = doc.setdefault("extracao", {})

		st.subheader("Configurações de Extração")

		cfg["encoding"] = st.text_input(
			"Encoding",
			value=cfg.get("encoding", ""),
		)

		cfg["sep"] = st.text_input(
			"Separador",
			value=cfg.get("sep", ""),
		)

		cfg["chunksize"] = st.number_input(
			"Chunk size",
			value=int(cfg.get("chunksize", 0)),
			step=1000,
		)

	def validate(self, doc: dict):
		pass
