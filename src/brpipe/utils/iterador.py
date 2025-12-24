from typing import Callable

def iterar_sheets_ibge(
	tabelas: dict,
	fn: Callable,
	*,
	incluir_idx: bool = False,
):
	"""
	Itera por todas as tabelas e sheets IBGE
	aplicando uma função de callback.
	"""
	for tabela in tabelas.values():
		for idx, sheet in enumerate(tabela.sheets):
			if incluir_idx:
				fn(tabela, sheet, idx)
			else:
				fn(tabela, sheet)
