import streamlit as st
from ui.sections.ibge.tabelas.normalizacao import normalizar_coluna

FORMATOS = [
	"CONTAGEM",
	"PORCENTAGEM",
	"PROPORCAO",
	"MEDIA",
]

class IBGETabelasSection:
	key = "tabelas"
	label = "Tabelas IBGE"

	def render(self, doc: dict):
		tabelas = doc.setdefault("tabelas", {})

		st.subheader("Tabelas IBGE")

		for tab_key in list(tabelas.keys()):
			with st.expander(f"Tabela {tab_key}", expanded=False):
				self._render_tabela(tab_key, tabelas[tab_key], doc)

		if st.button("Adicionar tabela"):
			n = len(tabelas) + 1
			tabelas[f"tab{n}"] = {
				"descricao_tabela": "",
				"sheets": []
			}

	def _render_tabela(self, tab_key: str, tabela: dict, doc: dict):
		tabela["descricao_tabela"] = st.text_input(
			"Descrição da tabela",
			value=tabela.get("descricao_tabela", ""),
			key=f"{tab_key}_desc"
		)

		sheets = tabela.setdefault("sheets", [])

		for i, sheet in enumerate(sheets):
			with st.expander(f"Sheet {i+1}", expanded=i == 0):
				self._render_sheet(tab_key, i, sheet, doc)

		if st.button("Adicionar sheet", key=f"{tab_key}_add_sheet"):
			sheets.append({
				"descricao_sheet": "",
				"arquivo": "",
				"colunas": []
			})

	def _render_sheet(self, tab_key: str, idx: int, sheet: dict, doc: dict):
		sheet["descricao_sheet"] = st.text_input(
			"Descrição da sheet",
			value=sheet.get("descricao_sheet", ""),
			key=f"{tab_key}_sheet_{idx}_desc"
		)

		sheet["arquivo"] = st.text_input(
			"Arquivo CSV",
			value=sheet.get("arquivo", ""),
			key=f"{tab_key}_sheet_{idx}_arq"
		)

		st.markdown("### Colunas")

		if not sheet.get("_normalizado"):
			sheet["colunas"] = [
				normalizar_coluna(c)
				for c in sheet.get("colunas", [])
			]
			sheet["_normalizado"] = True

		for c_idx, col in enumerate(sheet["colunas"]):
			self._render_coluna(tab_key, idx, c_idx, col, doc)

		if st.button("Adicionar coluna", key=f"{tab_key}_{idx}_add_col"):
			sheet["colunas"].append({
				"nome": "",
				"formato": "CONTAGEM",
				"coluna_peso": None,
			})

	def _render_coluna(
		self,
		tab_key: str,
		sheet_idx: int,
		col_idx: int,
		col: dict,
		doc: dict,
	):
		with st.container(border=True):
			col["nome"] = st.text_input(
				"Nome da coluna",
				value=col.get("nome", ""),
				key=f"{tab_key}_{sheet_idx}_{col_idx}_nome"
			)

			col["formato"] = st.selectbox(
				"Formato",
				options=FORMATOS,
				index=FORMATOS.index(
					col.get("formato", "CONTAGEM")
				),
				key=f"{tab_key}_{sheet_idx}_{col_idx}_formato"
			)

			if col["formato"] != "CONTAGEM":
				pesos = doc.get("colunas_peso", {})
				opcoes = list(pesos.keys())

				col["coluna_peso"] = st.selectbox(
					"Coluna de peso",
					options=opcoes,
					index=(
						opcoes.index(col["coluna_peso"])
						if col.get("coluna_peso") in opcoes
						else 0
					),
					key=f"{tab_key}_{sheet_idx}_{col_idx}_peso"
				)
			else:
				col["coluna_peso"] = None

	def validate(self, doc: dict) -> list[str]:
		erros = []
		pesos = doc.get("colunas_peso", {})
		tabelas = doc.get("tabelas", {})

		for tab_key, tabela in tabelas.items():
			if not tabela.get("sheets"):
				erros.append(f"{tab_key}: deve possuir ao menos uma sheet")

			for i, sheet in enumerate(tabela.get("sheets", [])):
				ctx = f"{tab_key} / sheet {i+1}"

				if not sheet.get("descricao_sheet"):
					erros.append(f"{ctx}: descrição obrigatória")

				if not sheet.get("arquivo"):
					erros.append(f"{ctx}: arquivo obrigatório")

				if not sheet.get("colunas"):
					erros.append(f"{ctx}: deve possuir colunas")

				for c in sheet.get("colunas", []):
					if not c.get("nome"):
						erros.append(f"{ctx}: coluna sem nome")

					formato = c.get("formato", "CONTAGEM")

					if formato not in FORMATOS:
						erros.append(
							f"{ctx}: formato inválido ({formato})"
						)

					if formato != "CONTAGEM":
						if c.get("coluna_peso") not in pesos:
							erros.append(
								f"{ctx}: coluna {c.get('nome')} "
								"usa coluna_peso inválida"
							)

		return erros
