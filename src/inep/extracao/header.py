from utils.io import read_header
from inep.config import VARIAVEIS_YAML, MAPEAMENTOS


def ler_header(path):
	return read_header(path)


from inep.config import VARIAVEIS_YAML, MAPEAMENTOS


def resolver_schema_entrada(header: list[str]):
	"""
	Resolve o schema de entrada do CSV INEP.

	Retorna:
	- colunas_fisicas: colunas reais a serem lidas do arquivo
	- mapeamento: colunas a serem renomeadas (fisico -> logico)
	- faltantes: variáveis esperadas não encontradas
	"""

	colunas_fisicas = []
	mapeamento = {}
	faltantes = set()

	variaveis_esperadas = VARIAVEIS_YAML.variaveis
	map_dict = MAPEAMENTOS.map_dict

	for var in variaveis_esperadas:
		# Caso 1: variável lógica existe fisicamente
		if var in header:
			colunas_fisicas.append(var)
			continue

		# Caso 2: procurar coluna alternativa
		encontrado = False
		for alternativo, destino in map_dict.items():
			if destino == var and alternativo in header:
				colunas_fisicas.append(alternativo)
				mapeamento[alternativo] = var
				encontrado = True
				break

		if not encontrado:
			faltantes.add(var)

	return colunas_fisicas, mapeamento, faltantes


def identificar_faltantes(colunas_existentes, mapeamento):
	normalizadas = {
		mapeamento.get(coluna, coluna)
		for coluna in colunas_existentes
	}

	return set(VARIAVEIS_YAML.variaveis) - normalizadas
