from ui.sections.ibge.tabelas.models import ColunaEditavel, FormaColuna


def serializar_coluna(col: ColunaEditavel):
	if col.forma == FormaColuna.CRUA and col.formato == "CONTAGEM":
		return col.nome

	if col.forma == FormaColuna.SIMPLES and col.formato == "CONTAGEM":
		return {col.nome: "CONTAGEM"}

	if col.coluna_peso:
		return {
			col.nome: {
				"formato": col.formato,
				"coluna_peso": col.coluna_peso
			}
		}

	return {col.nome: col.formato}
