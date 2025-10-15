import os
import pandas as pd

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
print(f" Lendo {arquivo_base} ...")
df_base = pd.read_csv(arquivo_base, sep=";", encoding="utf-8", low_memory=False)

print(f" Lendo {arquivo_seguinte} ...")
df_seguinte = pd.read_csv(arquivo_seguinte, sep=";", encoding="utf-8", low_memory=False)

# === AGREGAÇÃO POR MUNICÍPIO ===
def agrega(df):
	return df.groupby(["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"], as_index=False).agg({
		"QT_ING_TOTAL": "sum",
		"QT_MAT_TOTAL": "sum",
		"QT_CONC_TOTAL": "sum"
	})

print(" Agregando dados por município...")
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
print(" Unindo dados dos dois anos...")
df_merged = pd.merge(
	agg_base,
	agg_seguinte,
	on=["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
	how="outer"
).fillna(0)

# === CÁLCULO DA EVASÃO ===
# Fórmula: evasão = (ingressantes_base - (matriculados_seguinte + concluintes_seguinte)) / ingressantes_base
# Obs: se ingressantes_base for zero, resultado será zero para evitar divisão por zero

print(" Calculando taxa de evasão...")
ing = df_merged[f"QT_ING_TOTAL_{ano_base}"]
mat_next = df_merged[f"QT_MAT_TOTAL_{ano_seguinte}"]
conc_next = df_merged[f"QT_CONC_TOTAL_{ano_seguinte}"]

df_merged[f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = (
	(ing - (mat_next + conc_next)) / ing.replace(0, 1)
).round(4)

# Opcional: definir evasão como 0 se não houve ingressantes
df_merged.loc[ing == 0, f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = 0

# === SALVAR RESULTADO ===
df_merged.to_csv(arquivo_saida, sep=";", index=False, encoding="utf-8")
print(f" Arquivo final salvo em: {arquivo_saida}")
print(f" Total de municípios processados: {len(df_merged):,}")
