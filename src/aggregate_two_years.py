import os
import pandas as pd
import numpy as np

# === ENTRADA DOS ANOS ===
ano_base = input("Digite o ANO BASE (ex: 2022): ").strip()
ano_seguinte = input("Digite o ANO SEGUINTE (ex: 2023): ").strip()

# === CAMINHOS ===
INTERIM_DIR = os.path.join("data", "interim")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

arquivo_base = os.path.join(INTERIM_DIR, f"inep_reduzido_{ano_base}.csv")
arquivo_seguinte = os.path.join(INTERIM_DIR, f"inep_reduzido_{ano_seguinte}.csv")
arquivo_saida = os.path.join(PROCESSED_DIR, f"evasao_{ano_base}_{ano_seguinte}.csv")

# === VERIFICAÇÕES ===
for arq in [arquivo_base, arquivo_seguinte]:
	if not os.path.exists(arq):
		print(f"Arquivo não encontrado: {arq}")
		print("Certifique-se de executar antes o script de redução para ambos os anos.")
		exit(1)

# === LEITURA ===
print(f"Lendo {arquivo_base} ...")
df_base = pd.read_csv(arquivo_base, sep=";", encoding="utf-8", low_memory=False)

print(f"Lendo {arquivo_seguinte} ...")
df_seguinte = pd.read_csv(arquivo_seguinte, sep=";", encoding="utf-8", low_memory=False)

# === AGREGAÇÃO (nível município) ===
def agrega_por_municipio(df):
	return df.groupby(
		["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
		as_index=False
	).agg({
		"QT_ING_TOTAL": "sum",
		"QT_MAT_TOTAL": "sum",
		"QT_CONC_TOTAL": "sum"
	})

print("Agregando dados...")
agg_base = agrega_por_municipio(df_base).rename(columns={
	"QT_ING_TOTAL": f"QT_ING_TOTAL_{ano_base}",
	"QT_MAT_TOTAL": f"QT_MAT_TOTAL_{ano_base}",
	"QT_CONC_TOTAL": f"QT_CONC_TOTAL_{ano_base}"
})

agg_seguinte = agrega_por_municipio(df_seguinte).rename(columns={
	"QT_ING_TOTAL": f"QT_ING_TOTAL_{ano_seguinte}",
	"QT_MAT_TOTAL": f"QT_MAT_TOTAL_{ano_seguinte}",
	"QT_CONC_TOTAL": f"QT_CONC_TOTAL_{ano_seguinte}"
})

# === JUNÇÃO ENTRE ANOS ===
df_merged = pd.merge(
	agg_base,
	agg_seguinte,
	on=["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
	how="outer"
)

# === TRATAMENTO DE VALORES ===
num_cols = [c for c in df_merged.columns if c.startswith("QT_")]
df_merged[num_cols] = df_merged[num_cols].fillna(0).astype(float)

# === NOMES DAS COLUNAS ===
col_M_n = f"QT_MAT_TOTAL_{ano_seguinte}"
col_I_n = f"QT_ING_TOTAL_{ano_seguinte}"
col_M_prev = f"QT_MAT_TOTAL_{ano_base}"
col_C_prev = f"QT_CONC_TOTAL_{ano_base}"

# === PARÂMETROS DE RELEVÂNCIA ===
MIN_M_PREV = 10
MIN_M_N = 5
MIN_I_N = 1
MIN_C_PREV = 1

# === VALIDAÇÕES (após merge, nível agregado) ===
motivo_invalidez = []

for i in range(len(df_merged)):
	motivo = []

	M_prev = df_merged.at[i, col_M_prev]
	M_n = df_merged.at[i, col_M_n]
	I_n = df_merged.at[i, col_I_n]
	C_prev = df_merged.at[i, col_C_prev]

	if M_prev < MIN_M_PREV:
		motivo.append(f"M(n-1) < {MIN_M_PREV}")
	if M_n < MIN_M_N:
		motivo.append(f"M(n) < {MIN_M_N}")
	if I_n < MIN_I_N:
		motivo.append(f"I(n) < {MIN_I_N}")
	if C_prev < MIN_C_PREV:
		motivo.append(f"C(n-1) < {MIN_C_PREV}")

	if not (M_n - I_n > 0):
		motivo.append("M(n)-I(n) <= 0")
	if not (M_prev - C_prev > 0):
		motivo.append("M(n-1)-C(n-1) <= 0")
	if not ((M_n - I_n) <= (M_prev - C_prev)):
		motivo.append("M(n)-I(n) > M(n-1)-C(n-1)")

	if not motivo:
		motivo_invalidez.append("válido")
	else:
		motivo_invalidez.append("; ".join(motivo))

df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] = motivo_invalidez

# === CÁLCULO DA EVASÃO ===
evasao = pd.Series(np.nan, index=df_merged.index, dtype="float64")
validos = df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] == "válido"

M_n = df_merged[col_M_n]
I_n = df_merged[col_I_n]
M_prev = df_merged[col_M_prev]
C_prev = df_merged[col_C_prev]

evasao.loc[validos] = 1.0 - ((M_n.loc[validos] - I_n.loc[validos]) / (M_prev.loc[validos] - C_prev.loc[validos]))
df_merged[f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = evasao.round(4)
df_merged[f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}"] = validos

# === NÚMERO TOTAL DE ESTUDANTES (para uso futuro como peso) ===
df_merged[f"QT_ESTUDANTES_TOTAL_{ano_base}_{ano_seguinte}"] = (
	df_merged[col_M_prev] + df_merged[col_I_n]
)

# === SALVAR RESULTADO ===
df_merged.to_csv(arquivo_saida, sep=";", index=False, encoding="utf-8")
print(f"Arquivo final salvo em: {arquivo_saida}")
print(f"Total de registros processados: {len(df_merged):,}")
print(f"Total de evasões válidas: {validos.sum():,}")
print(f"Total de evasões inválidas: {(~validos).sum():,}")
