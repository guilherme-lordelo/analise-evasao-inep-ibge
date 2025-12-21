from ibge.config import COLUNAS_BASE_IBGE, TABELAS_IBGE
from ibge.transformacao.limpar_linhas import limpar
from ibge.transformacao.aplicar_schema import aplicar_schema_ibge
from utils.io import read_csv, write_csv
from utils.paths import IBGE_REDUZIDO, PROCESSED_IBGE


def transformar_ibge():
    for tabela in TABELAS_IBGE.values():
        for sheet in tabela.sheets:

            nome_final = sheet.arquivo
            nome_interim = nome_final.replace(".csv", "_interim.csv")

            path_in = IBGE_REDUZIDO / nome_interim
            path_out = PROCESSED_IBGE / nome_final

            df = read_csv(path_in, header=None, dtype=str)

            df = limpar(df)
            df = aplicar_schema_ibge(
                df,
                COLUNAS_BASE_IBGE,
                sheet.colunas_especificas,
            )

            write_csv(df, path_out)
