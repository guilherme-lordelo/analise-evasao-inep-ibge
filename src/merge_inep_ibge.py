import os
import pandas as pd
from functools import reduce

# Diretórios relativos à raiz do projeto
BASE_DIR = os.path.join("data", "processed")
IBGE_DIR = os.path.join(BASE_DIR, "ibge_csv_final")
EVASAO_DIR = BASE_DIR

# Pares de anos
pares = ["2020_2021", "2021_2022", "2022_2023", "2023_2024"]

# === 1. LER ARQUIVOS DE EVASÃO ===
evasao_dfs = []
for p in pares:
    arquivo = os.path.join(EVASAO_DIR, f"evasao_{p}.csv")
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo de evasão não encontrado: {arquivo}")
    df = pd.read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)
    df = df[["CO_MUNICIPIO", f"TAXA_EVASAO_{p}", f"EVASAO_VALIDO_{p}"]]
    evasao_dfs.append(df)

# Merge sequencial por CO_MUNICIPIO
evasao_all = reduce(lambda left, right: pd.merge(left, right, on="CO_MUNICIPIO", how="outer"), evasao_dfs)

# === 2. FILTRAR MUNICÍPIOS VÁLIDOS PARA TODOS OS PARES ===
valid_cols = [f"EVASAO_VALIDO_{p}" for p in pares]
evasao_all["todos_validos"] = evasao_all[valid_cols].all(axis=1)

# Separar válidos e inválidos
evasao_validos = evasao_all[evasao_all["todos_validos"]].copy()
evasao_invalidos = evasao_all[~evasao_all["todos_validos"]].copy()

# === 3. CALCULAR MÉDIA E ACUMULADA ===
evasao_cols = [f"TAXA_EVASAO_{p}" for p in pares]

# Média simples
evasao_validos["EVASAO_MEDIA_2020_2024"] = evasao_validos[evasao_cols].mean(axis=1)

# Acumulada
evasao_validos["EVASAO_ACUMULADA_2020_2024"] = 1 - (
    (1 - evasao_validos[evasao_cols[0]]) *
    (1 - evasao_validos[evasao_cols[1]]) *
    (1 - evasao_validos[evasao_cols[2]]) *
    (1 - evasao_validos[evasao_cols[3]])
)

# === 4. LER E MERGEAR DADOS IBGE ===
from ibge_colunas import COLUNAS_POR_TABELA

ibge_dfs = []
for f_name, cols in COLUNAS_POR_TABELA.items():
    path = os.path.join(IBGE_DIR, f_name.replace(".csv", "_final.csv"))
    if os.path.exists(path):
        df = pd.read_csv(path, sep=";", usecols=cols, encoding="utf-8", low_memory=False)
        # Remove colunas redundantes
        for col in ["SG_UF", "NO_MUNICIPIO_OU_CLASSE"]:
            if col in df.columns:
                df.drop(columns=col, inplace=True)
        ibge_dfs.append(df)
    else:
        print(f"Aviso: arquivo IBGE não encontrado: {path}")

# Merge sequencial dos dados IBGE por CO_MUNICIPIO
ibge_all = reduce(lambda left, right: pd.merge(left, right, on="CO_MUNICIPIO", how="outer"), ibge_dfs)

# === Adicionar SG_UF e NO_MUNICIPIO_OU_CLASSE de volta ===
ult_ano_df = pd.read_csv(os.path.join(EVASAO_DIR, f"evasao_{pares[-1]}.csv"),
                         sep=";", encoding="utf-8", low_memory=False)
cols_info = ["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"]
if all(col in ult_ano_df.columns for col in cols_info):
    info_df = ult_ano_df[cols_info].drop_duplicates(subset="CO_MUNICIPIO")
    ibge_all = pd.merge(info_df, ibge_all, on="CO_MUNICIPIO", how="left")

# Merge final com evasão válida
df_final_validos = pd.merge(evasao_validos, ibge_all, on="CO_MUNICIPIO", how="left")
df_final_invalidos = pd.merge(evasao_invalidos, ibge_all, on="CO_MUNICIPIO", how="left")

# Reordenar colunas: CO_MUNICIPIO, SG_UF, NO_MUNICIPIO, restante
def reorder_columns(df):
    cols = df.columns.tolist()
    for col in ["NO_MUNICIPIO", "SG_UF"]:
        if col in cols:
            cols.insert(1, cols.pop(cols.index(col)))  # Move para posição 1 e 2
    return df[cols]

df_final_validos = reorder_columns(df_final_validos)
df_final_invalidos = reorder_columns(df_final_invalidos)

# === 5. SALVAR RESULTADOS ===
df_final_validos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_valida_2020_2024.csv"),
                        sep=";", index=False, encoding="utf-8")
df_final_invalidos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_invalida_2020_2024.csv"),
                          sep=";", index=False, encoding="utf-8")

print("Arquivos salvos:")
print(f"  - Válidos: {len(df_final_validos)} municípios")
print(f"  - Inválidos: {len(df_final_invalidos)} municípios")
