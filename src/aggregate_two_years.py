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

# === AGREGAÇÃO POR MUNICÍPIO ===
def agrega(df):
	return df.groupby(["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"], as_index=False).agg({
		"QT_ING_TOTAL": "sum",
		"QT_MAT_TOTAL": "sum",
		"QT_CONC_TOTAL": "sum"
	})

print("Agregando dados por município...")
agg_base = agrega(df_base).rename(columns={
	"QT_ING_TOTAL": f"QT_ING_TOTAL_{ano_base}",
	"QT_MAT_TOTAL": f"QT_MAT_TOTAL_{ano_base}",
	"QT_CONC_TOTAL": f"QT_CONC_TOTAL_{ano_base}"
})

agg_seguinte = agrega(df_seguinte).rename(columns={
	"QT_ING_TOTAL": f"QT_ING_TOTAL_{ano_seguinte}",
	"QT_MAT_TOTAL": f"QT_MAT_TOTAL_{ano_seguinte}",
	"QT_CONC_TOTAL": f"QT_CONC_TOTAL_{ano_seguinte}"
})

# === JUNÇÃO ENTRE ANOS ===
print("Unindo dados dos dois anos...")
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

# === COMPONENTES DA FÓRMULA ===
M_n = df_merged[col_M_n]
I_n = df_merged[col_I_n]
M_prev = df_merged[col_M_prev]
C_prev = df_merged[col_C_prev]

num = M_n - I_n
den = M_prev - C_prev

# === PARÂMETROS DE RELEVÂNCIA ===
MIN_M_PREV = 10     # matrículas mínimas no ano base
MIN_M_N = 5         # matrículas mínimas no ano seguinte
MIN_I_N = 1         # ingressantes mínimos
MIN_C_PREV = 1      # concluintes mínimos

# === VALIDAÇÕES ===
motivo_invalidez = []

for i in range(len(df_merged)):
	motivo = []

	# === Checagem de significância mínima ===
	if M_prev[i] < MIN_M_PREV:
		motivo.append(f"M(n-1) < {MIN_M_PREV}")
	if M_n[i] < MIN_M_N:
		motivo.append(f"M(n) < {MIN_M_N}")
	if I_n[i] < MIN_I_N:
		motivo.append(f"I(n) < {MIN_I_N}")
	if C_prev[i] < MIN_C_PREV:
		motivo.append(f"C(n-1) < {MIN_C_PREV}")

	# === Checagens lógicas ===
	if not (M_n[i] - I_n[i] > 0):
		motivo.append("M(n)-I(n) <= 0")
	if not (M_prev[i] - C_prev[i] > 0):
		motivo.append("M(n-1)-C(n-1) <= 0")
	if not ((M_n[i] - I_n[i]) <= (M_prev[i] - C_prev[i])):
		motivo.append("M(n)-I(n) > M(n-1)-C(n-1)")

	# === Resultado final ===
	if not motivo:
		motivo_invalidez.append("válido")
	else:
		motivo_invalidez.append("; ".join(motivo))

df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] = motivo_invalidez

# === CÁLCULO DA EVASÃO ===
evasao = pd.Series(np.nan, index=df_merged.index, dtype="float64")
validos = df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] == "válido"

evasao.loc[validos] = 1.0 - ((M_n.loc[validos] - I_n.loc[validos]) / (M_prev.loc[validos] - C_prev.loc[validos]))

df_merged[f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = evasao.round(4)
df_merged[f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}"] = validos

# === SALVAR RESULTADO ===
df_merged.to_csv(arquivo_saida, sep=";", index=False, encoding="utf-8")
print(f"Arquivo final salvo em: {arquivo_saida}")
print(f"Total de municípios processados: {len(df_merged):,}")
print(f"Total de evasões válidas: {validos.sum():,}")
print(f"Total de evasões inválidas: {(~validos).sum():,}")
