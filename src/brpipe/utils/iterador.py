from typing import Callable, TypeVar, Optional, List

T = TypeVar("T")


def iterar_sheets_ibge(
	tabelas: dict,
	fn: Callable[..., Optional[T]],
	*,
	incluir_idx: bool = False,
) -> Optional[List[T]]:
	"""
	Itera por todas as tabelas e sheets IBGE aplicando uma função de callback.

	- Se a função retornar valores diferentes de None,
	  eles são coletados e retornados em uma lista.
	- Se todos os retornos forem None, retorna None.
	"""

	resultados: List[T] = []

	for tabela in tabelas.values():
		for idx, sheet in enumerate(tabela.sheets):
			if incluir_idx:
				resultado = fn(tabela, sheet, idx)
			else:
				resultado = fn(tabela, sheet)

			if resultado is not None:
				resultados.append(resultado)

	return resultados or None
