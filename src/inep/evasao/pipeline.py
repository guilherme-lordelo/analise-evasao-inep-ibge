import pandas as pd
from utils.paths import DATA_INTERIM, DATA_PROCESSED
from utils.io import read_csv, write_csv
from pathlib import Path

from .agregacao import agrega_com_sufixo
from .validacao import validar_linhas
from .calculo import calcular_taxa_evasao


def calcular_evasao(ano_base: str, ano_seguinte: str):
    arquivo_base = DATA_INTERIM / f"inep_reduzido_{ano_base}.csv"
    arquivo_seguinte = DATA_INTERIM / f"inep_reduzido_{ano_seguinte}.csv"
    arquivo_saida = DATA_PROCESSED / f"evasao_{ano_base}_{ano_seguinte}.csv"

    if not arquivo_base.exists() or not arquivo_seguinte.exists():
        raise FileNotFoundError(
            f"Arquivos reduzidos não encontrados:\n- {arquivo_base}\n- {arquivo_seguinte}"
        )

    print(f"Lendo {arquivo_base}...")
    df_base = read_csv(arquivo_base, sep=";", encoding="utf-8", low_memory=False)

    print(f"Lendo {arquivo_seguinte}...")
    df_seg = read_csv(arquivo_seguinte, sep=";", encoding="utf-8", low_memory=False)

    print("Agregando dados por município...")
    agg_base = agrega_com_sufixo(df_base, ano_base)
    agg_seg = agrega_com_sufixo(df_seg, ano_seguinte)

    print("Realizando merge dos anos...")
    df_merged = pd.merge(
        agg_base,
        agg_seg,
        on=["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
        how="outer"
    )

    print("Preenchendo valores ausentes...")
    num_cols = [c for c in df_merged.columns if c.startswith("QT_")]
    df_merged[num_cols] = df_merged[num_cols].fillna(0).astype(float)

    print("Validando regras de evasão...")
    df_merged = validar_linhas(df_merged, ano_base, ano_seguinte)

    print("Calculando taxa de evasão...")
    df_merged = calcular_taxa_evasao(df_merged, ano_base, ano_seguinte)

    print(f"Salvando arquivo final em {arquivo_saida}...")
    write_csv(df_merged, arquivo_saida, sep=";")

    print(f"Processamento concluído!")
    print(f"Registros: {len(df_merged):,}")
    print(f"Válidos: {df_merged[f'EVASAO_VALIDO_{ano_base}_{ano_seguinte}'].sum():,}")
    print(f"Inválidos: {len(df_merged) - df_merged[f'EVASAO_VALIDO_{ano_base}_{ano_seguinte}'].sum():,}")
    