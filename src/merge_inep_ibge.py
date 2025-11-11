import os
import pandas as pd
from functools import reduce

# Diretórios
BASE_DIR = os.path.join("data", "processed")
IBGE_DIR = os.path.join(BASE_DIR, "ibge_csv_final")
EVASAO_DIR = BASE_DIR

# === 1. LER RESULTADOS DA ETAPA ANTERIOR ===
validos_path = os.path.join(BASE_DIR, "municipios_evasao_valida_2020_2024.csv")
invalidos_path = os.path.join(BASE_DIR, "municipios_evasao_invalida_2020_2024.csv")

if not os.path.exists(validos_path) or not os.path.exists(invalidos_path):
	raise FileNotFoundError("Arquivos de evasão da etapa anterior não encontrados. Execute o script de evasão primeiro.")

evasao_validos = pd.read_csv(validos_path, sep=";", encoding="utf-8", low_memory=False)
evasao_invalidos = pd.read_csv(invalidos_path, sep=";", encoding="utf-8", low_memory=False)

# === 2. LER E MERGEAR DADOS IBGE ===
from ibge_colunas import COLUNAS_POR_TABELA

ibge_dfs = []
for f_name, cols in COLUNAS_POR_TABELA.items():
	path = os.path.join(IBGE_DIR, f_name.replace(".csv", "_final.csv"))
	if os.path.exists(path):
		df = pd.read_csv(path, sep=";", usecols=cols, encoding="utf-8", low_memory=False)
		# Remove colunas redundantes, se existirem
		for col in ["SG_UF", "NO_MUNICIPIO_OU_CLASSE"]:
			if col in df.columns:
				df.drop(columns=col, inplace=True)
		ibge_dfs.append(df)
	else:
		print(f"Aviso: arquivo IBGE não encontrado: {path}")

if not ibge_dfs:
	raise FileNotFoundError("Nenhum arquivo IBGE encontrado em ibge_csv_final/.")

# Merge sequencial dos dados IBGE por CO_MUNICIPIO
ibge_all = reduce(lambda left, right: pd.merge(left, right, on="CO_MUNICIPIO", how="outer"), ibge_dfs)

# === 3. ADICIONAR SG_UF E NO_MUNICIPIO (garantindo correspondência) ===
# Pegamos esses dados do último par de evasão já processado
ult_ano_df = pd.read_csv(os.path.join(EVASAO_DIR, "evasao_2023_2024.csv"),
						 sep=";", encoding="utf-8", low_memory=False)
cols_info = ["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"]
if all(col in ult_ano_df.columns for col in cols_info):
	info_df = ult_ano_df[cols_info].drop_duplicates(subset="CO_MUNICIPIO")
	ibge_all = pd.merge(info_df, ibge_all, on="CO_MUNICIPIO", how="left")

# === 4. MERGE FINAL COM EVASÃO (válidos e inválidos) ===
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

# === 5. SALVAR RESULTADOS FINAIS ===
df_final_validos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_valida_ibge_2020_2024.csv"),
						sep=";", index=False, encoding="utf-8")
df_final_invalidos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_invalida_ibge_2020_2024.csv"),
						  sep=";", index=False, encoding="utf-8")

print("Merge com IBGE concluído!")
print(f"  - Municípios válidos (com IBGE): {len(df_final_validos)}")
print(f"  - Municípios inválidos (com IBGE): {len(df_final_invalidos)}")
