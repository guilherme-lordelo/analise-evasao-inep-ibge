import streamlit as st

class AnosSection:
	key = "anos"
	label = "Período de Análise"

	def render(self, doc: dict):
		anos = doc.setdefault("anos", {})

		st.subheader("Período de Análise")

		anos["inicio"] = st.number_input(
			"Ano inicial",
			value=int(anos.get("inicio", 0)),
			step=1,
		)

		anos["fim"] = st.number_input(
			"Ano final",
			value=int(anos.get("fim", 0)),
			step=1,
		)

	def validate(self, doc: dict):
		anos = doc.get("anos", {})
		if anos["inicio"] > anos["fim"]:
			raise ValueError("Ano inicial não pode ser maior que o ano final")
