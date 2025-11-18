import pandas as pd
import numpy as np
import os
from utils.paths import DATA_INTERIM, DATA_PROCESSED
from utils.io import read_csv, write_csv
from ibge.colunas import COLUNAS_POR_TABELA

INPUT_DIR = DATA_INTERIM / "ibge_csv"
OUTPUT_DIR = DATA_PROCESSED / "ibge_csv_final"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# FUNÇÕES AUXILIARES
# -------------------------------------------------------------

def renomear_colunas(df, novos_nomes):
    """Renomeia colunas conforme lista fornecida."""
    if not novos_nomes:
        raise ValueError("Lista de novos nomes de colunas vazia.")
    if len(df.columns) != len(novos_nomes):
        print(f"Aviso: número de colunas ({len(df.columns)}) diferente da lista fornecida ({len(novos_nomes)}).")
    df.columns = novos_nomes[:len(df.columns)]
    return df


def limpar_linhas(df):
    """
    Remove:
    - Linhas com duas primeiras colunas vazias ou NaN (resquícios ';;')
    - Linhas de texto ou explicativas nas últimas 10 linhas
    - Colunas sem informação nas últimas 2 linhas
    - Última linha vazia, se existir
    - Substitui '-' por NaN
    """

    # Remove linhas com ';;'
    cond_invalidas = (
        (df.iloc[:, 0].isna() | (df.iloc[:, 0].astype(str).str.strip() == "")) &
        (df.iloc[:, 1].isna() | (df.iloc[:, 1].astype(str).str.strip() == ""))
    )
    df = df[~cond_invalidas].copy()

    # Substitui '-' por NaN
    df = df.replace("-", np.nan)

    # Detecta e remove linhas textuais nas últimas 10 linhas
    # Critério: mais de 70% dos valores não numéricos e não NaN
    ultimas_linhas = df.tail(10)
    mask_texto = ultimas_linhas.apply(
        lambda linha: (
            sum(~linha.astype(str).str.replace(r"[\d\.,\-]", "", regex=True).str.strip().eq("")) /
            len(linha)
        ) > 0.7,  # mais de 70% de texto
        axis=1
    )
    if mask_texto.any():
        df = df.drop(ultimas_linhas[mask_texto].index)

    # Remove colunas sem dados nas últimas 2 linhas (totalmente NaN ou vazias)
    ultimas_2 = df.tail(2)
    colunas_sem_info = ultimas_2.columns[
        ultimas_2.isna().all() |
        (ultimas_2.astype(str).apply(lambda s: s.str.strip() == "").all())
    ]
    df = df.drop(columns=colunas_sem_info)

    # Remove última linha se estiver completamente vazia
    if df.tail(1).isna().all(axis=1).iloc[0]:
        df = df.iloc[:-1]

    return df.reset_index(drop=True)



def processar_arquivo(nome_arquivo, colunas):
    """Executa o pipeline completo para um arquivo específico."""
    input_path = INPUT_DIR / nome_arquivo
    output_path = os.path.join(OUTPUT_DIR, nome_arquivo.replace(".csv", "_final.csv"))

    print(f"\n Processando {nome_arquivo} ...")
    if not os.path.exists(input_path):
        print(f"Arquivo não encontrado: {input_path}")
        return

    df = pd.read_csv(input_path, sep=";", dtype=str)

    # Limpeza
    df = limpar_linhas(df)

    # Renomeia colunas
    df = renomear_colunas(df, colunas)

    # Normaliza espaços
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    write_csv(df, output_path, sep=";")
    print(f"{nome_arquivo} salvo em {output_path} ({len(df)} linhas válidas).")


# -------------------------------------------------------------
# MAIN FLEXÍVEL
# -------------------------------------------------------------
def main():
    print("=== Processador de Tabelas IBGE ===")

    print("\nTabelas configuradas:")
    print(", ".join(COLUNAS_POR_TABELA.keys()))

    escolha = input(
        "\nDigite o nome das tabelas a processar (separadas por vírgula ou 'todas'): "
    ).strip()

    if escolha.lower() == "todas":
        arquivos_para_processar = list(COLUNAS_POR_TABELA.keys())
    else:
        mapa_lower = {k.lower(): k for k in COLUNAS_POR_TABELA.keys()}
        arquivos_para_processar = [
            mapa_lower[a.strip().lower()]
            for a in escolha.split(",")
            if a.strip().lower() in mapa_lower
        ]

    if not arquivos_para_processar:
        print("Nenhum arquivo válido selecionado.")
        return

    for arquivo in arquivos_para_processar:
        processar_arquivo(arquivo, COLUNAS_POR_TABELA[arquivo])


if __name__ == "__main__":
    main()
