def obter_colunas_peso(doc: dict) -> dict[str, str]:
	return doc.get("colunas_peso", {})
