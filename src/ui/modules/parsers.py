from ui.sections.ibge.tabelas.models import ColunaEditavel, FormaColuna


def parse_coluna_yaml(col) -> ColunaEditavel:
	if isinstance(col, str):
		return ColunaEditavel(
			nome=col,
			forma=FormaColuna.CRUA
		)

	if isinstance(col, dict):
		nome = next(iter(col.keys()))
		valor = col[nome]

		if isinstance(valor, str):
			return ColunaEditavel(
				nome=nome,
				formato=valor,
				forma=FormaColuna.SIMPLES
			)

		if isinstance(valor, dict):
			return ColunaEditavel(
				nome=nome,
				formato=valor.get("formato", "CONTAGEM"),
				coluna_peso=valor.get("coluna_peso"),
				forma=FormaColuna.COMPLETA
			)

	raise ValueError(f"Coluna inválida: {col}")
