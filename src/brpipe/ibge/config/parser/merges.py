from brpipe.ibge.config.models import ColunaIBGEConfig, MergeColunasConfig

_METODOS_MERGE_SUPORTADOS = {
	"soma",
	"media_ponderada",
}

def parse_merges(
	merges_cfg: list[dict],
	colunas: list[ColunaIBGEConfig],
	colunas_peso: dict[str, str],
	remover_idx: set[int],
	ctx: str,
) -> list[MergeColunasConfig]:

	qtd_colunas = len(colunas)
	merges: list[MergeColunasConfig] = []
	fontes_usadas: set[int] = set()

	for m in merges_cfg:
		destino = m["destino"]
		fontes_idx = m["fontes_idx"]
		metodo = m.get("metodo", "soma").lower()
		coluna_peso_alias = m.get("coluna_peso")
		peso_merge = m.get("peso_merge")

		if metodo not in _METODOS_MERGE_SUPORTADOS:
			raise ValueError(
				f"{ctx} Método de merge não suportado: '{metodo}'"
			)

		if metodo == "media_ponderada":
			if peso_merge is None:
				raise ValueError(
					f"{ctx} Merge '{destino}' exige peso_merge"
				)

			if not isinstance(peso_merge, list):
				raise ValueError(
					f"{ctx} peso_merge deve ser lista em '{destino}'"
				)

			if coluna_peso_alias:
				if coluna_peso_alias not in colunas_peso:
					raise ValueError(
						f"{ctx} Merge '{destino}' usa coluna_peso desconhecida: {coluna_peso_alias}"
					)

		fontes_nomes: list[str] = []

		for idx in fontes_idx:
			if idx <= 0 or idx > qtd_colunas:
				raise ValueError(
					f"{ctx} Fonte inválida no merge: {idx}"
				)

			zidx = idx - 1

			if zidx in remover_idx:
				raise ValueError(
					f"{ctx} Fonte removida semanticamente no merge: {idx}"
				)

			if zidx in fontes_usadas:
				raise ValueError(
					f"{ctx} Fonte usada em mais de um merge: {idx}"
				)

			fontes_nomes.append(colunas[zidx].nome)
			fontes_usadas.add(zidx)

		if metodo == "media_ponderada" and len(peso_merge) != len(fontes_nomes):
			raise ValueError(
				f"{ctx} Merge '{destino}': peso_merge e fontes têm tamanhos diferentes"
			)

		merges.append(
			MergeColunasConfig(
				destino=destino,
				fontes=fontes_nomes,
				metodo=metodo,
				coluna_peso=(
					colunas_peso.get(coluna_peso_alias)
					if coluna_peso_alias else None
				),
				peso_merge=peso_merge,
			)
		)

	return merges
