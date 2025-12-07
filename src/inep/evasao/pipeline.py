import pandas as pd
from utils.paths import INTERIM_INEP, PROCESSED_INEP
from utils.io import read_csv, write_csv

from .agregacao import agrega_quantitativas_com_sufixo, agrega_categoricas
from .calculo import calcular_formulas
from inep.config import (
    EXTRACAO_PREFIXO_OUT,
    EXTRACAO_EXT_OUT,
    EVASAO_PREFIXO_OUT,
    VARIAVEIS_QUANTITATIVAS,
    get_campos_municipio,
)


def calcular_evasao(ano_base: int, ano_seguinte: int):

    # ------------------
    # Definir arquivos
    # ------------------
    arquivo_base = INTERIM_INEP / f"{EXTRACAO_PREFIXO_OUT}{ano_base}{EXTRACAO_EXT_OUT}"
    arquivo_seguinte = INTERIM_INEP / f"{EXTRACAO_PREFIXO_OUT}{ano_seguinte}{EXTRACAO_EXT_OUT}"
    arquivo_saida = PROCESSED_INEP / f"{EVASAO_PREFIXO_OUT}{ano_base}_{ano_seguinte}{EXTRACAO_EXT_OUT}"

    # ------------------
    # Validação
    # ------------------
    if not arquivo_base.exists() or not arquivo_seguinte.exists():
        raise FileNotFoundError(
            f"Arquivos reduzidos não encontrados:\n- {arquivo_base}\n- {arquivo_seguinte}"
        )

    # ------------------
    # Leitura
    # ------------------
    print(f"Lendo {arquivo_base}...")
    df_base = read_csv(arquivo_base)

    print(f"Lendo {arquivo_seguinte}...")
    df_seg = read_csv(arquivo_seguinte)

    # ------------------
    # Agregação por município (quantitativas)
    # ------------------
    print("Agregando quantitativas por município...")
    agg_base = agrega_quantitativas_com_sufixo(df_base, ano_base)
    agg_seg = agrega_quantitativas_com_sufixo(df_seg, ano_seguinte)

    # ------------------
    # Merge entre anos (quantitativas)
    # ------------------
    print("Realizando merge dos anos (quantitativas)...")
    df_merged = pd.merge(
        agg_base,
        agg_seg,
        on=get_campos_municipio(agg_base),
        how="outer"
    )

    # ------------------
    # Preencher quantitativas ausentes
    # ------------------
    print("Preenchendo valores ausentes nas variáveis quantitativas...")
    variaveis_com_sufixos = (
        [f"{col}_{ano_base}" for col in VARIAVEIS_QUANTITATIVAS] +
        [f"{col}_{ano_seguinte}" for col in VARIAVEIS_QUANTITATIVAS]
    )

    existentes = [c for c in variaveis_com_sufixos if c in df_merged.columns]
    df_merged[existentes] = df_merged[existentes].fillna(0).astype(float)

    # ------------------
    # Cálculo das fórmulas
    # ------------------
    print("Calculando fórmulas definidas no YAML...")
    df_merged = calcular_formulas(df_merged, ano_base, ano_seguinte)

    # ------------------
    # Remover quantitativas usadas no cálculo
    # ------------------
    print("Removendo colunas quantitativas originais...")
    df_merged = df_merged.drop(columns=existentes, errors="ignore")

    # ============================================================
    #  AGREGAÇÃO DE CATEGÓRICAS
    # ============================================================

    print("Agregando variáveis categóricas usando ano base...")
    agg_cat = agrega_categoricas(df_base, ano_base, ano_seguinte)

    # ------------------
    # Merge final com categóricas
    # ------------------
    print("Realizando merge final com variáveis categóricas...")
    df_final = pd.merge(
        df_merged,
        agg_cat,
        on=get_campos_municipio(df_base),
        how="left"
    )

    # ------------------
    # Escrita final
    # ------------------
    print(f"Salvando arquivo final em {arquivo_saida}...")
    write_csv(df_final, arquivo_saida)

    print(f"Registros: {len(df_final):,}")
