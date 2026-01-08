from brpipe.ibge.config.models import TransformacaoColunaConfig

_METODOS_TRANSFORMACAO_SUPORTADOS = {"logit"}

def parse_transformacoes(
	transformacoes_cfg: list[dict],
	qtd_colunas: int,
	destinos_merge: set[int],
	remover_idx: list[int],
	ctx: str,
):
	destinos_transformacao = set()
	transformacoes = []

	for t in transformacoes_cfg:
		fonte_idx = t["fonte_idx"]
		destino = t["destino"]
		tipo = t["tipo"]
		escala = t.get("escala_origem")

		if tipo not in _METODOS_TRANSFORMACAO_SUPORTADOS:
			raise ValueError(f"{ctx} Tipo de transformação não suportado: '{tipo}'")

		if fonte_idx < 0 or fonte_idx >= qtd_colunas:
			raise ValueError(f"{ctx} Índice de fonte inválido: {fonte_idx}")

		if fonte_idx in remover_idx:
			raise ValueError(
				f"{ctx} Fonte da transformação removida: índice {fonte_idx}"
			)

		if destino < qtd_colunas:
			raise ValueError(
				f"{ctx} Índice de destino já existe como coluna: {destino}"
			)

		if destino in destinos_merge:
			raise ValueError(
				f"{ctx} Destino de transformação conflita com merge: {destino}"
			)

		if destino in destinos_transformacao:
			raise ValueError(
				f"{ctx} Destino de transformação duplicado: {destino}"
			)

		destinos_transformacao.add(destino)

		transformacoes.append(
			TransformacaoColunaConfig(
				fonte=fonte_idx,
				destino=destino,
				tipo=tipo,
				escala_origem=escala,
			)
		)

	return transformacoes
