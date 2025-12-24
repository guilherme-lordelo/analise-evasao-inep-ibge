def validar_remocao_colunas(
	colunas_especificas: list[str],
	remover_colunas: list[str],
	ctx: str,
):
	for col in remover_colunas:
		if col not in colunas_especificas:
			raise ValueError(
				f"{ctx} Coluna para remoção inexistente: '{col}'"
			)