from brpipe.ibge.config.models import ColunaIBGEConfig


def validar_remocao_colunas(
	colunas: list[ColunaIBGEConfig],
	remover_colunas: list[str],
	ctx: str,
):
	nomes = [coluna.nome for coluna in colunas]
	for col in remover_colunas:
		if col not in nomes:
			raise ValueError(
				f"{ctx} Coluna para remoção inexistente: '{col}'"
			)