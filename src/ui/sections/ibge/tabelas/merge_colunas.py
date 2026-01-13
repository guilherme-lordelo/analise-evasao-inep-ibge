from ui.sections.ibge.tabelas.constantes import FORMATOS, METODOS_MERGE
import streamlit as st


def render_merge_coluna(
	merge: dict,
	key_prefix: str,
	pesos: list[str],
	on_remove,
):
	with st.container(border=True):

		merge["destino"] = st.text_input(
			"Coluna de destino",
			merge.get("destino", ""),
			key=f"{key_prefix}_destino"
		)

		merge["fontes_idx"] = st.text_input(
			"Índices das colunas fonte (ex: 2,3,4)",
			", ".join(map(str, merge.get("fontes_idx", []))),
			key=f"{key_prefix}_fontes"
		)

		try:
			merge["fontes_idx"] = [
				int(i.strip())
				for i in merge["fontes_idx"].split(",")
				if i.strip()
			]
		except ValueError:
			st.error("Os índices das fontes devem ser inteiros.")

		col1, col2 = st.columns([6, 1])

		with col1:
			merge["metodo"] = st.selectbox(
				"Método de merge",
				METODOS_MERGE,
				index=METODOS_MERGE.index(
					merge.get("metodo", METODOS_MERGE[0])
				),
				key=f"{key_prefix}_metodo"
			)

			merge["formato"] = st.selectbox(
				"Formato do resultado",
				FORMATOS,
				index=FORMATOS.index(
					merge.get("formato", FORMATOS[0])
				),
				key=f"{key_prefix}_formato"
			)

			if merge["metodo"] == "MEDIA_PONDERADA":
				merge["peso_merge"] = st.text_input(
					"Pesos do merge (ex: 2.5,10,19.5)",
					", ".join(map(str, merge.get("peso_merge", []))),
					key=f"{key_prefix}_peso_merge"
				)

				try:
					merge["peso_merge"] = [
						float(i.strip())
						for i in merge["peso_merge"].split(",")
						if i.strip()
					]
				except ValueError:
					st.error("Os pesos devem ser numéricos.")

				merge["coluna_peso"] = st.selectbox(
					"Coluna de peso",
					pesos,
					index=(
						pesos.index(merge.get("coluna_peso"))
						if merge.get("coluna_peso") in pesos
						else 0
					),
					key=f"{key_prefix}_coluna_peso"
				)
			else:
				merge["peso_merge"] = None
				merge["coluna_peso"] = None

		with col2:
			st.markdown("##")
			if st.button("Remover", key=f"{key_prefix}_del"):
				on_remove()
