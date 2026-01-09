import streamlit as st

class ValidacaoLimitesSection:
	key = "validacao_limites"
	label = "Limites de Validação"

	def render(self, doc: dict):
		limites = doc.setdefault("validacao_limites", {})

		st.subheader("Limites de Validação")

		for nome in list(limites.keys()):
			col1, col2, col3 = st.columns([4, 4, 1])

			with col1:
				novo_nome = st.text_input(
					"Nome do limite",
					value=nome,
					key=f"lim_nome_{nome}",
				)

			with col2:
				limites[nome] = st.number_input(
					"Valor",
					value=int(limites[nome]),
					step=1,
					key=f"lim_val_{nome}",
				)

			with col3:
				if st.button("🗑", key=f"lim_del_{nome}"):
					del limites[nome]
					st.rerun()

			if novo_nome != nome and novo_nome.strip() and novo_nome not in limites:
				limites[novo_nome] = limites.pop(nome)
				st.rerun()

		if st.button("Adicionar limite"):
			limites["novo_limite"] = 0
			st.rerun()

	def validate(self, doc: dict):
		pass
