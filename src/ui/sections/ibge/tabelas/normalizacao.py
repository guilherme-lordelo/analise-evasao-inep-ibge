def normalizar_coluna(col):
	if isinstance(col, str):
		return {
			"nome": col,
			"formato": "CONTAGEM",
			"coluna_peso": None,
		}

	if isinstance(col, dict):
		nome = next(iter(col.keys()))
		valor = col[nome]

		if isinstance(valor, str):
			return {
				"nome": nome,
				"formato": valor,
				"coluna_peso": None,
			}

		if isinstance(valor, dict):
			return {
				"nome": nome,
				"formato": valor.get("formato", "CONTAGEM"),
				"coluna_peso": valor.get("coluna_peso"),
			}

	raise ValueError(f"Formato de coluna inválido: {col}")
