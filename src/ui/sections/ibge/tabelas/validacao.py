from .constantes import FORMATOS

def validate_tabelas(doc: dict) -> list[str]:
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

			colunas = sheet.get("colunas", [])
			if not colunas:
				erros.append(f"{ctx}: deve possuir colunas")

			qtd_colunas = len(colunas)
			for idx in sheet.get("remover_colunas_idx", []):
				if idx < 1 or idx > qtd_colunas:
					erros.append(
						f"{ctx}: índice inválido em remover_colunas_idx ({idx})"
					)

			for c in colunas:
				if not c.get("nome"):
					erros.append(f"{ctx}: coluna sem nome")

				formato = c.get("formato", "CONTAGEM")
				if formato not in FORMATOS:
					erros.append(f"{ctx}: formato inválido ({formato})")

				if formato != "CONTAGEM":
					if c.get("coluna_peso") not in pesos:
						erros.append(
							f"{ctx}: coluna {c.get('nome')} "
							"usa coluna_peso inválida"
						)

	return erros
