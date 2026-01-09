import streamlit as st

class MapeamentoColunasSection:
	key = "mapeamento_colunas"
	label = "Mapeamento de Colunas"

	def render(self, doc: dict):
		mapeamentos = doc.setdefault("mapeamento_colunas", {})

		st.subheader("Mapeamento de Colunas")
		st.markdown("Colunas divergentes encontradas nos dados INEP")

		for origem in list(mapeamentos.keys()):
			col1, col2, col3 = st.columns([4, 4, 1])

			with col1:
				nova_origem = st.text_input(
					"Coluna origem",
					value=origem,
					key=f"map_src_{origem}",
				)

			with col2:
				mapeamentos[origem] = st.text_input(
					"Coluna destino",
					value=mapeamentos[origem],
					key=f"map_dst_{origem}",
				)

			with col3:
				if st.button("🗑", key=f"map_del_{origem}"):
					del mapeamentos[origem]
					st.rerun()

			if nova_origem != origem and nova_origem.strip() and nova_origem not in mapeamentos:
				mapeamentos[nova_origem] = mapeamentos.pop(origem)
				st.rerun()

		st.divider()

		if st.button("Adicionar mapeamento"):
			base = "COL_ORIGEM"
			i = 1
			nome = base
			while nome in mapeamentos:
				nome = f"{base}_{i}"
				i += 1

			mapeamentos[nome] = ""
			st.rerun()

	def validate(self, doc: dict):
		mapeamentos = doc.get("mapeamento_colunas", {})

		for k, v in mapeamentos.items():
			if not k or not v:
				raise ValueError("Mapeamento de colunas não pode ter chave ou valor vazio")
