import pandas as pd
from pathlib import Path
import re

from utils.paths import IBGE_REDUZIDO, PROCESSED_IBGE
from utils.io import read_csv, write_csv
from ibge.config import SHEETS_IBGE, COLUNAS_BASE_IBGE


def is_codigo_municipio(value):
    """Retorna True para valores de 7 dígitos (ex: '4316477')."""
    if not isinstance(value, str):
        value = str(value)
    return bool(re.fullmatch(r"\d{7}", value.strip()))


def limpar_ibge():
    """
    Processa os arquivos IBGE extraídos.
    """

    PROCESSED_IBGE.mkdir(parents=True, exist_ok=True)

    for tabela_id, tabela_info in SHEETS_IBGE.items():

        for idx, sheet_info in enumerate(tabela_info["sheets"]):

            nome_final = sheet_info["arquivo"]                           # ex: tab12_rendimento_total.csv
            nome_interim = nome_final.replace(".csv", "_interim.csv")    # ex: tab12_rendimento_total_interim.csv

            path_in = Path(IBGE_REDUZIDO) / nome_interim
            path_out = Path(PROCESSED_IBGE) / nome_final

            if not path_in.exists():
                print(f"Arquivo intermediário não encontrado: {path_in}")
                continue

            print(f"\n=== Limpando {nome_interim} ===")

            df = read_csv(path_in, header=None, dtype=str)

            # ----------------------------
            # 1. Filtrar apenas municípios
            # ----------------------------
            mask_validas = df.iloc[:, 0].apply(is_codigo_municipio)
            df = df[mask_validas].copy()

            print(f"Linhas municipais: {len(df)}")

            # ----------------------------
            # 2. Construção do cabeçalho
            # ----------------------------
            colunas_sheet = sheet_info["colunas"]

            colunas_finais = COLUNAS_BASE_IBGE + colunas_sheet

            n = len(colunas_finais)

            # Reduz o DF ao número esperado de colunas
            df = df.iloc[:, :n]

            df.columns = colunas_finais

            # Remover espaços e normalizar strings
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # ----------------------------
            # 3. Salvar arquivo
            # ----------------------------
            write_csv(df, path_out)

            print(f"{path_out.name} ({len(df)} linhas)")
