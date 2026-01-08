def validar_remocao_colunas(
	qtd_colunas: int,
	remover_idx: list[int],
	ctx: str,
):
	for idx in remover_idx:
		if idx < 1 or idx >= qtd_colunas + 1:
			raise ValueError(
				f"{ctx} Índice inválido para remoção de coluna: {idx}"
			)
