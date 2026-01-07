from brpipe.bridge.common.tipos import resolver_resultado_tipo
from brpipe.ibge.config.models import ColunaIBGEConfig


def parse_colunas(
	colunas_cfg: list,
	*,
	tipo_default: str,
	ctx: str
) -> list[ColunaIBGEConfig]:

	colunas: list[ColunaIBGEConfig] = []

	for c in colunas_cfg:
		if isinstance(c, str):
			tipo = resolver_resultado_tipo(
				valor=None,
				padrao=resolver_resultado_tipo(
					tipo_default,
					padrao=None,
					ctx=f"{ctx}[TIPO_DEFAULT_IBGE]"
				),
				ctx=f"{ctx}[{c}]",
			)

			colunas.append(
				ColunaIBGEConfig(nome=c, tipo=tipo)
			)

		elif isinstance(c, dict):
			if len(c) != 1:
				raise ValueError(f"{ctx} Coluna inválida: {c}")

			nome, tipo_raw = next(iter(c.items()))

			tipo = resolver_resultado_tipo(
				tipo_raw,
				padrao=None,
				ctx=f"{ctx}[{nome}]",
			)

			colunas.append(
				ColunaIBGEConfig(nome=nome, tipo=tipo)
			)

		else:
			raise TypeError(f"{ctx} Formato inválido de coluna: {c}")

	return colunas