from brpipe.ibge.config.models import MergeColunasConfig, TransformacaoColunaConfig


_METODOS_MERGE_SUPORTADOS = {"soma", "media"}
_METODOS_TRANSFORMACAO_SUPORTADOS = {"logit"}

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

def parse_merges(
	merges_cfg: list[dict],
	colunas_especificas: list[str],
	remover_colunas: list[str],
	ctx: str,
):
	destinos_merge = set()
	fontes_merge = set()
	merges = []

	for m in merges_cfg:
		destino = m["destino"]
		fontes = m["fontes"]
		metodo = m.get("metodo", "soma")

		if metodo not in _METODOS_MERGE_SUPORTADOS:
			raise ValueError(f"{ctx} Método de merge não suportado: '{metodo}'")

		if destino in colunas_especificas:
			raise ValueError(f"{ctx} Destino de merge já existe como coluna: '{destino}'")

		if destino in destinos_merge:
			raise ValueError(f"{ctx} Destino de merge duplicado: '{destino}'")

		if len(fontes) < 2:
			raise ValueError(f"{ctx} Merge '{destino}' deve ter ao menos 2 colunas fonte")

		for f in fontes:
			if f not in colunas_especificas:
				raise ValueError(f"{ctx} Coluna fonte inexistente no merge '{destino}': '{f}'")

			if f in remover_colunas:
				raise ValueError(
					f"{ctx} Coluna fonte '{f}' do merge '{destino}' não pode ser removida"
				)

			if f in fontes_merge:
				raise ValueError(
					f"{ctx} Coluna fonte '{f}' usada em mais de um merge"
				)

		destinos_merge.add(destino)
		fontes_merge.update(fontes)

		merges.append(
			MergeColunasConfig(
				destino=destino,
				fontes=fontes,
				metodo=metodo,
			)
		)

	return merges, destinos_merge

def parse_transformacoes(
	transformacoes_cfg: list[dict],
	colunas_especificas: list[str],
	destinos_merge: set[str],
	remover_colunas: list[str],
	ctx: str,
):
	colunas_disponiveis = set(colunas_especificas) | destinos_merge

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

		if destino in colunas_especificas:
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
