from brpipe.bridge.inep.variaveis import VariaveisINEP


class TerritoriosINEP:
	def __init__(self, variaveis: VariaveisINEP):
		self._territoriais = variaveis.territoriais

	def coluna(self, nivel: str, chave: str) -> str:
		if nivel == "estadual" and chave == "ufs":
			return self._territoriais["uf"]

		if nivel == "municipal" and chave == "municipio":
			return self._territoriais["municipio"]

		raise KeyError(
			f"Território inválido: nivel={nivel}, chave={chave}"
		)
