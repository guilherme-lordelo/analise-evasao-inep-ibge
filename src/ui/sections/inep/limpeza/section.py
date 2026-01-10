import streamlit as st

class LimpezaSection:
	key = "limpeza"
	label = "Limpeza de Dados"

	def render(self, doc: dict):
		cfg = doc.setdefault("limpeza", {})

		st.subheader("Limpeza")

		cfg["comportamento_sem_municipio"] = st.selectbox(
			"Comportamento sem município",
			["descartar", "atribuir"],
			index=["descartar", "atribuir"].index(
				cfg.get("comportamento_sem_municipio", "atribuir")
			),
		)

		valores = cfg.setdefault("valor_padrao_sem_municipio", {})

		st.markdown("### Valores padrão sem município")

		for k in list(valores.keys()):
			valores[k] = st.text_input(
				k,
				value=str(valores[k]),
				key=f"limp_{k}",
			)

	def validate(self, doc: dict):
		pass
