from brpipe.ibge.config.models import ColunaIBGEConfig
from brpipe.ibge.config.tipos import TipoDado, TipoAgregacao
from brpipe.bridge.common.tipos import ResultadoTipo

MAPA_TIPO_DADO = {
	TipoDado.COUNT: (TipoAgregacao.SOMA, ResultadoTipo.COUNT),
	TipoDado.PERCENT: (TipoAgregacao.MEDIA_PONDERADA, ResultadoTipo.PERCENT_0_100),
	TipoDado.MEDIA: (TipoAgregacao.MEDIA_PONDERADA, ResultadoTipo.VALUE),
	TipoDado.RATIO: (TipoAgregacao.MEDIA_PONDERADA, ResultadoTipo.RATIO),
}


def build_coluna_config(
	*,
	nome: str,
	formato: str,
	coluna_peso_alias: str | None,
	colunas_peso: dict[str, str],
	ctx: str,
) -> ColunaIBGEConfig:

	tipo_dado = TipoDado.from_str(formato, ctx)

	coluna_peso_resolvida = None
	if coluna_peso_alias:
		if coluna_peso_alias not in colunas_peso:
			raise ValueError(
				f"{ctx} Coluna '{nome}' usa coluna_peso desconhecida: {coluna_peso_alias}"
			)
		coluna_peso_resolvida = colunas_peso[coluna_peso_alias]

	agreg, viz = MAPA_TIPO_DADO[tipo_dado]

	return ColunaIBGEConfig(
		nome=nome,
		tipo_dado=tipo_dado,
		tipo_agregacao=agreg,
		tipo_visualizacao=viz,
		coluna_peso=coluna_peso_resolvida,
	)


def parse_colunas(
	colunas_cfg: list,
	*,
	tipo_default: str,
	colunas_peso: dict[str, str],
	ctx: str,
) -> list[ColunaIBGEConfig]:

	colunas: list[ColunaIBGEConfig] = []

	for c in colunas_cfg:
		coluna_peso_alias = None

		if isinstance(c, str):
			nome = c
			tipo_dado = TipoDado.from_str(tipo_default, ctx)

		elif isinstance(c, dict):
			if len(c) != 1:
				raise ValueError(f"{ctx} Coluna inválida: {c}")

			nome, raw = next(iter(c.items()))

			if isinstance(raw, dict):
				formato = raw.get("formato")
				coluna_peso_alias = raw.get("coluna_peso")

				if not formato:
					raise ValueError(f"{ctx} Coluna '{nome}' sem formato")

				tipo_dado = TipoDado.from_str(formato, ctx)

				if tipo_dado not in {TipoDado.RATIO, TipoDado.MEDIA}:
					raise ValueError(
						f"{ctx} Coluna '{nome}' só pode usar formato expandido para RATIO ou MEDIA"
					)

				if not coluna_peso_alias:
					raise ValueError(
						f"{ctx} Coluna '{nome}' exige coluna_peso"
					)

				if coluna_peso_alias not in colunas_peso:
					raise ValueError(
						f"{ctx} Coluna '{nome}' usa coluna_peso desconhecida: {coluna_peso_alias}"
					)

			else:
				tipo_dado = TipoDado.from_str(raw, ctx)

		else:
			raise TypeError(f"{ctx} Formato inválido de coluna: {c}")

		colunas.append(
			build_coluna_config(
				nome=nome,
				formato=tipo_dado.name,
				coluna_peso_alias=None if not coluna_peso_alias else coluna_peso_alias,
				colunas_peso=colunas_peso,
				ctx=ctx,
			)
		)

	return colunas
