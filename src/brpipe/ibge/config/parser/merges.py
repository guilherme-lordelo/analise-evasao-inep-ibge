from brpipe.ibge.config.models import ColunaIBGEConfig, MergeColunasConfig


_METODOS_MERGE_SUPORTADOS = {"soma", "media"}

def parse_merges(
	merges_cfg: list[dict],
	colunas_cfg: list[ColunaIBGEConfig],
	remover_colunas: list[str],
	ctx: str,
):
	destinos_merge = set()
	fontes_merge = set()
	merges = []
	colunas = [coluna_cfg.nome for coluna_cfg in colunas_cfg]

	for m in merges_cfg:
		destino = m["destino"]
		fontes = m["fontes"]
		metodo = m.get("metodo", "soma")

		if metodo not in _METODOS_MERGE_SUPORTADOS:
			raise ValueError(f"{ctx} Método de merge não suportado: '{metodo}'")

		if destino in colunas:
			raise ValueError(f"{ctx} Destino de merge já existe como coluna: '{destino}'")

		if destino in destinos_merge:
			raise ValueError(f"{ctx} Destino de merge duplicado: '{destino}'")

		if len(fontes) < 2:
			raise ValueError(f"{ctx} Merge '{destino}' deve ter ao menos 2 colunas fonte")

		for f in fontes:
			if f not in colunas:
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
