import pandas as pd
from utils.paths import INTERIM_INEP, PROCESSED_INEP
from utils.io import read_csv, write_csv

from .agregacao import agrega_com_sufixo
from .calculo import calcular_formulas
from inep.config import VARIAVEIS_QUANTITATIVAS


def calcular_evasao(ano_base: str, ano_seguinte: str):
    arquivo_base = INTERIM_INEP / f"inep_reduzido_{ano_base}.csv"
    arquivo_seguinte = INTERIM_INEP / f"inep_reduzido_{ano_seguinte}.csv"
    arquivo_saida = PROCESSED_INEP / f"evasao_{ano_base}_{ano_seguinte}.csv"

    if not arquivo_base.exists() or not arquivo_seguinte.exists():
        raise FileNotFoundError(
            f"Arquivos reduzidos não encontrados:\n- {arquivo_base}\n- {arquivo_seguinte}"
        )

    print(f"Lendo {arquivo_base}...")
    df_base = read_csv(arquivo_base)

    print(f"Lendo {arquivo_seguinte}...")
    df_seg = read_csv(arquivo_seguinte)

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

    print("Calculando fórmulas definidas no YAML...")
    df_merged = calcular_formulas(df_merged, ano_base, ano_seguinte)

    print("Removendo colunas quantitativas...")
    quant_cols_to_drop = []
    for base_col in VARIAVEIS_QUANTITATIVAS:
        quant_cols_to_drop.append(f"{base_col}_{ano_base}")
        quant_cols_to_drop.append(f"{base_col}_{ano_seguinte}")

    cols_existentes = [c for c in quant_cols_to_drop if c in df_merged.columns]
    df_merged = df_merged.drop(columns=cols_existentes)

    print(f"Salvando arquivo final em {arquivo_saida}...")
    write_csv(df_merged, arquivo_saida)

    print(f"Registros: {len(df_merged):,}")
