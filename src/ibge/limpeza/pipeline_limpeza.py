import os
import pandas as pd
from utils.io import write_csv
from utils.paths import DATA_INTERIM, DATA_PROCESSED
from ibge.limpeza.processadores import limpar_linhas, renomear_colunas

INPUT_DIR = DATA_INTERIM / "ibge_csv"
OUTPUT_DIR = DATA_PROCESSED / "ibge_csv_final"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def processar_arquivo(nome_arquivo, colunas):
    """Executa o pipeline completo para um arquivo específico."""
    input_path = INPUT_DIR / nome_arquivo
    output_path = OUTPUT_DIR / nome_arquivo.replace(".csv", "_final.csv")

    print(f"\nProcessando {nome_arquivo} ...")

    if not input_path.exists():
        print(f"Arquivo não encontrado: {input_path}")
        return

    df = pd.read_csv(input_path, sep=";", dtype=str)

    # Limpeza
    df = limpar_linhas(df)

    # Renomeia colunas
    df = renomear_colunas(df, colunas)

    # Normalização de strings
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    write_csv(df, output_path, sep=";")
    print(f"{nome_arquivo} salvo ({len(df)} linhas válidas).")


def processar_varias_tabelas(lista_arquivos, colunas_por_tabela):
    """Processa vários arquivos de acordo com o dicionário COLUNAS_POR_TABELA."""
    for arquivo in lista_arquivos:
        processar_arquivo(arquivo, colunas_por_tabela[arquivo])
