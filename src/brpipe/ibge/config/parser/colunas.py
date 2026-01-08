from brpipe.ibge.config.models import ColunaIBGEConfig
from brpipe.ibge.config.tipos import TipoDado
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.tipos import TipoAgregacao

MAPA_TIPO_DADO = {
	TipoDado.COUNT: (TipoAgregacao.SOMA, ResultadoTipo.COUNT),
	TipoDado.PERCENT: (TipoAgregacao.MEDIA_PONDERADA, ResultadoTipo.PERCENT_0_100),
	TipoDado.MEDIA: (TipoAgregacao.MEDIA_PONDERADA, ResultadoTipo.VALUE),
	TipoDado.RATIO: (TipoAgregacao.RATIO_RECALCULADO, ResultadoTipo.RATIO),
	TipoDado.PESO: (TipoAgregacao.SOMA, ResultadoTipo.COUNT),
}


def parse_colunas(
	colunas_cfg: list,
	*,
	tipo_default: str,
	colunas_peso: dict[str, str],
	ctx: str,
) -> list[ColunaIBGEConfig]:

	colunas: list[ColunaIBGEConfig] = []

	for c in colunas_cfg:
		coluna_peso_resolvida = None

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

				# 🔑 resolve alias → real column name
				coluna_peso_resolvida = colunas_peso[coluna_peso_alias]

			# formato antigo
			else:
				tipo_dado = TipoDado.from_str(raw, ctx)

		else:
			raise TypeError(f"{ctx} Formato inválido de coluna: {c}")

		agreg, viz = MAPA_TIPO_DADO[tipo_dado]

		colunas.append(
			ColunaIBGEConfig(
				nome=nome,
				tipo_dado=tipo_dado,
				tipo_agregacao=agreg,
				tipo_visualizacao=viz,
				coluna_peso=coluna_peso_resolvida,
			)
		)

	return colunas
