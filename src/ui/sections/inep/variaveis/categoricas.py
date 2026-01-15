import streamlit as st

def render_categoricas(categoricas: dict):
	for nome in list(categoricas.keys()):
		with st.expander(nome, expanded=False):
			cfg = categoricas[nome]

			cfg["descricao"] = st.text_input(
				"Descrição",
				value=cfg.get("descricao", ""),
				key=f"desc_{nome}",
			)

			valores = cfg.setdefault("valores", {})

			for k in list(valores.keys()):
				col1, col2 = st.columns([2, 6])
				with col1:
					novo_k = st.text_input(
						"Código",
						value=str(k),
						key=f"k_{nome}_{k}",
					)
				with col2:
					valores[k] = st.text_input(
						"Descrição",
						value=valores[k],
						key=f"v_{nome}_{k}",
					)

			if st.button("Adicionar valor", key=f"add_val_{nome}"):
				valores[max(valores.keys(), default=0) + 1] = ""
				st.rerun()

			if valores:
				opcoes = list(valores.keys())

				filtro_atual = cfg.get("filtro_excluir", [])

				selecionados = st.multiselect(
					"Excluir valores",
					options=opcoes,
					default=filtro_atual,
					format_func=lambda k: f"{k} - {valores.get(k, '')}",
					key=f"filtro_excluir_{nome}",
				)

				if selecionados:
					cfg["filtro_excluir"] = selecionados
				else:
					cfg.pop("filtro_excluir", None)
