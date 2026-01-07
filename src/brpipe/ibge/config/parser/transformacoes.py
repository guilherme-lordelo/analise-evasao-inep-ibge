from brpipe.ibge.config.models import ColunaIBGEConfig, TransformacaoColunaConfig

_METODOS_TRANSFORMACAO_SUPORTADOS = {"logit"}

def parse_transformacoes(
	transformacoes_cfg: list[dict],
	colunas_cfg: list[ColunaIBGEConfig],
	destinos_merge: set[str],
	remover_colunas: list[str],
	ctx: str,
):
	colunas = [coluna_cfg.nome for coluna_cfg in colunas_cfg]
	colunas_disponiveis = set(colunas) | destinos_merge

	destinos_transformacao = set()
	transformacoes = []

	for t in transformacoes_cfg:
		fonte = t["fonte"]
		destino = t["destino"]
		tipo = t["tipo"]
		escala = t.get("escala_origem")

		if tipo not in _METODOS_TRANSFORMACAO_SUPORTADOS:
			raise ValueError(f"{ctx} Tipo de transformação não suportado: '{tipo}'")

		if fonte not in colunas_disponiveis:
			raise ValueError(f"{ctx} Coluna fonte da transformação inexistente: '{fonte}'")

		if fonte in remover_colunas:
			raise ValueError(
				f"{ctx} Coluna fonte '{fonte}' da transformação não pode ser removida"
			)

		if destino in colunas:
			raise ValueError(
				f"{ctx} Destino de transformação já existe como coluna: '{destino}'"
			)

		if destino in destinos_merge:
			raise ValueError(
				f"{ctx} Destino de transformação conflita com destino de merge: '{destino}'"
			)

		if destino in destinos_transformacao:
			raise ValueError(
				f"{ctx} Destino de transformação duplicado: '{destino}'"
			)

		destinos_transformacao.add(destino)

		transformacoes.append(
			TransformacaoColunaConfig(
				fonte=fonte,
				destino=destino,
				tipo=tipo,
				escala_origem=escala,
			)
		)

	return transformacoes
