import streamlit as st

class ColunaPesoSection:
	key = "coluna_peso_inep"
	label = "Coluna de Peso"

	def render(self, doc: dict):
		doc["coluna_peso_inep"] = st.text_input(
			"Coluna usada como peso na agregação",
			value=doc.get("coluna_peso_inep", ""),
		)

	def validate(self, doc: dict) -> list[str]:
		erros = []

		coluna = doc.get("coluna_peso_inep")

		if not coluna:
			erros.append("coluna_peso_inep não pode ser vazia")
			return erros

		coluna = str(coluna).strip()

		quantitativas = (
			doc.get("variaveis", {})
			   .get("quantitativas", {})
		)

		colunas_validas = {str(k) for k in quantitativas.keys()}

		if coluna not in colunas_validas:
			erros.append(
				f"coluna_peso_inep '{coluna}' não está definida como variável quantitativa"
			)

		return erros