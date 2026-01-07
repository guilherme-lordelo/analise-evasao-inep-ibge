from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.models import ColunaIBGEConfig


def parse_colunas(colunas_cfg: list, ctx: str) -> list[ColunaIBGEConfig]:
	colunas: list[ColunaIBGEConfig] = []

	for c in colunas_cfg:
		if isinstance(c, str):
			colunas.append(
				ColunaIBGEConfig(nome=c, tipo=None)
			)

		elif isinstance(c, dict):
			if len(c) != 1:
				raise ValueError(f"{ctx} Coluna inválida: {c}")

			nome, tipo_raw = next(iter(c.items()))

			try:
				tipo = ResultadoTipo[tipo_raw]
			except KeyError:
				raise ValueError(
					f"{ctx} Tipo de coluna inválido '{tipo_raw}' para '{nome}'"
				)

			colunas.append(
				ColunaIBGEConfig(nome=nome, tipo=tipo)
			)

		else:
			raise TypeError(f"{ctx} Formato inválido de coluna: {c}")

	return colunas