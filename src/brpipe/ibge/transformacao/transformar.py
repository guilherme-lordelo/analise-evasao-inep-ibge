from brpipe.ibge.config import COLUNAS_BASE_IBGE, TABELAS_IBGE
from brpipe.ibge.transformacao.limpar_linhas import limpar
from brpipe.ibge.transformacao.aplicar_schema import aplicar_schema_ibge
from brpipe.ibge.transformacao.remocao_colunas import remover_colunas
from brpipe.ibge.transformacao.merge_colunas import aplicar_merges_colunas
from brpipe.ibge.transformacao.transformar_colunas import aplicar_transformacoes_colunas
from brpipe.utils.io import read_csv, write_csv
from brpipe.utils.paths import IBGE_REDUZIDO, PROCESSED_IBGE


def transformar_ibge():
	"""
	Transforma os arquivos IBGE reduzidos aplicando limpeza, schema,
	merges, transformações estatísticas e remoção de colunas
	conforme configuração.
	"""
	for tabela in TABELAS_IBGE.values():
		for sheet in tabela.sheets:

			nome_final = sheet.arquivo
			nome_interim = nome_final.replace(".csv", "_interim.csv")

			path_in = IBGE_REDUZIDO / nome_interim
			path_out = PROCESSED_IBGE / nome_final

			if not path_in.exists():
				continue

			df = read_csv(path_in, header=None, dtype=str)

			df = limpar(df)

			df = aplicar_schema_ibge(
				df,
				COLUNAS_BASE_IBGE,
				sheet.colunas_especificas,
			)

			df = aplicar_merges_colunas(df, sheet)

			df = aplicar_transformacoes_colunas(df, sheet)

			df = remover_colunas(df, sheet)

			write_csv(df, path_out)
