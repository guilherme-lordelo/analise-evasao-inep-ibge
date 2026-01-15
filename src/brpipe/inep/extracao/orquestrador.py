from pathlib import Path
from brpipe.inep.extracao.filtro_categorico import filtrar_variaveis_categoricas
import pandas as pd

from brpipe.inep.extracao.header import (
	ler_header,
	resolver_schema_entrada,
)
from brpipe.inep.extracao.leitura_chunks import ler_em_chunks
from brpipe.inep.extracao.limpeza import limpar_municipios


def orquestrar_extracao(
	*,
	ano: int,
	input_path: Path,
) -> pd.DataFrame:
	"""
	Executa a extração de um único ano INEP.

	Contrato:
	- resolve schema a partir do header
	- lê apenas colunas físicas existentes
	- normaliza nomes para o esquema lógico
	- retorna DataFrame já limpo
	"""

	print(f"Lendo cabeçalho de {input_path.name}...")
	header = ler_header(input_path)

	colunas_fisicas, mapeamento, faltantes = resolver_schema_entrada(header)

	if not colunas_fisicas:
		raise RuntimeError("Nenhuma coluna válida encontrada para leitura")

	if mapeamento:
		print(f"Mapeamentos aplicados: {mapeamento}")

	if faltantes:
		print(f"Atenção: colunas não encontradas: {faltantes}")

	print(f"Lendo arquivo de {ano} em chunks...")
	df = ler_em_chunks(input_path, colunas_fisicas)

	if mapeamento:
		df = df.rename(columns=mapeamento)
	
	df = filtrar_variaveis_categoricas(df)

	print("Aplicando limpeza de municípios...")
	df = limpar_municipios(df)

	return df
