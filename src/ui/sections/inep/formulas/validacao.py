import re

RE_QUANT = re.compile(r"([A-Z0-9_]+)_\{([pn])\}")
RE_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def extrair_quantitativas(expr: str) -> list[tuple[str, str]]:
	return RE_QUANT.findall(expr)

def validar_quantitativas(expr, quantitativas, ctx):
	erros = []

	for base, sufixo in extrair_quantitativas(expr):
		if base not in quantitativas:
			erros.append(
				f"{ctx}: variável quantitativa '{base}' não existe"
			)

	return erros

def remover_quantitativas(expr: str) -> str:
	return RE_QUANT.sub("0", expr)

def extrair_identificadores(expr: str) -> set[str]:
	return set(RE_IDENT.findall(expr))

def validar_expressao(expr, quantitativas, limites, ctx):
	erros = []

	if not expr.strip():
		return erros

	erros.extend(validar_quantitativas(expr, quantitativas, ctx))

	expr_limpa = remover_quantitativas(expr)

	ids = extrair_identificadores(expr_limpa)

	for ident in ids:
		if ident in limites:
			continue

		erros.append(
			f"{ctx}: identificador desconhecido '{ident}'"
		)

	return erros
