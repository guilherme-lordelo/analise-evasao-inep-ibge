import streamlit as st

class ColunaPesoSection:
	key = "coluna_peso_inep"
	label = "Coluna de Peso"

	def render(self, doc: dict):
		doc["coluna_peso_inep"] = st.text_input(
			"Coluna usada como peso na agregação",
			value=doc.get("coluna_peso_inep", ""),
		)

	def validate(self, doc: dict):
		if not doc.get("coluna_peso_inep"):
			raise ValueError("coluna_peso_inep não pode ser vazia")
