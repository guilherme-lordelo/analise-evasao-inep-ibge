import os
import pandas as pd
from functools import reduce

# Diretórios
BASE_DIR = os.path.join("data", "processed")
EVASAO_DIR = BASE_DIR

# Pares de anos
pares = ["2020_2021", "2021_2022", "2022_2023", "2023_2024"]

# === 1. LER ARQUIVOS DE EVASÃO (com pesos) ===
evasao_dfs = []
for p in pares:
	arquivo = os.path.join(EVASAO_DIR, f"evasao_{p}.csv")
	if not os.path.exists(arquivo):
		raise FileNotFoundError(f"Arquivo de evasão não encontrado: {arquivo}")
	df = pd.read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)
	df = df[
		["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO", 
		 f"TAXA_EVASAO_{p}", f"EVASAO_VALIDO_{p}", f"QT_ESTUDANTES_TOTAL_{p}"]
	]
	evasao_dfs.append(df)

# Merge sequencial por CO_MUNICIPIO
evasao_all = reduce(
	lambda left, right: pd.merge(left, right, on=["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"], how="outer"),
	evasao_dfs
)

# === 2. FILTRAR MUNICÍPIOS VÁLIDOS PARA TODOS OS PARES ===
valid_cols = [f"EVASAO_VALIDO_{p}" for p in pares]
evasao_all["todos_validos"] = evasao_all[valid_cols].all(axis=1)

evasao_validos = evasao_all[evasao_all["todos_validos"]].copy()
evasao_invalidos = evasao_all[~evasao_all["todos_validos"]].copy()

# === 3. CÁLCULO PONDERADO ===
evasao_cols = [f"TAXA_EVASAO_{p}" for p in pares]
peso_cols = [f"QT_ESTUDANTES_TOTAL_{p}" for p in pares]

evasao_validos[evasao_cols + peso_cols] = evasao_validos[evasao_cols + peso_cols].fillna(0)

# Média ponderada (para todos os períodos combinados)
evasao_validos["EVASAO_MEDIA_PONDERADA_2020_2024"] = (
	(evasao_validos[evasao_cols].values * evasao_validos[peso_cols].values).sum(axis=1)
	/ evasao_validos[peso_cols].sum(axis=1)
)

# Evasão acumulada ponderada
def evasao_acumulada_ponderada(row):
	prod = 1.0
	total_peso = row[peso_cols].sum()
	if total_peso == 0:
		return float('nan')
	for e_col, w_col in zip(evasao_cols, peso_cols):
		evasao = row[e_col]
		peso = row[w_col]
		if peso > 0 and not pd.isna(evasao):
			prod *= (1 - evasao) ** (peso / total_peso)
	return 1 - prod

evasao_validos["EVASAO_ACUMULADA_PONDERADA_2020_2024"] = evasao_validos.apply(
	evasao_acumulada_ponderada, axis=1
)

# === 4. AGREGAÇÃO POR ESTADO E PAÍS ===

def agrega_evasao(df, grupo):
	resultados = []
	for nivel, grupo_df in df.groupby(grupo):
		linha = {"NIVEL": nivel if grupo == "SG_UF" else "BRASIL"}
		for p in pares:
			tx_col = f"TAXA_EVASAO_{p}"
			peso_col = f"QT_ESTUDANTES_TOTAL_{p}"
			total_peso = grupo_df[peso_col].sum()
			if total_peso == 0:
				linha[f"TAXA_EVASAO_{p}"] = float('nan')
			else:
				linha[f"TAXA_EVASAO_{p}"] = (grupo_df[tx_col] * grupo_df[peso_col]).sum() / total_peso
			linha[peso_col] = total_peso
		# Evasão média e acumulada ponderada
		taxas = [linha[f"TAXA_EVASAO_{p}"] for p in pares]
		pesos = [linha[f"QT_ESTUDANTES_TOTAL_{p}"] for p in pares]
		total_peso = sum(pesos)
		if total_peso > 0:
			linha["EVASAO_MEDIA_PONDERADA_2020_2024"] = sum(t * w for t, w in zip(taxas, pesos)) / total_peso
			prod = 1
			for t, w in zip(taxas, pesos):
				prod *= (1 - t) ** (w / total_peso)
			linha["EVASAO_ACUMULADA_PONDERADA_2020_2024"] = 1 - prod
		else:
			linha["EVASAO_MEDIA_PONDERADA_2020_2024"] = float('nan')
			linha["EVASAO_ACUMULADA_PONDERADA_2020_2024"] = float('nan')
		resultados.append(linha)
	return pd.DataFrame(resultados)

# Agregado por UF
evasao_uf = agrega_evasao(evasao_validos, "SG_UF")

# Agregado Brasil (sem grupo, um único total)
evasao_brasil = agrega_evasao(evasao_validos.assign(NIVEL="BRASIL"), "NIVEL")

# Combinar UF + Brasil
evasao_agregada = pd.concat([evasao_uf, evasao_brasil], ignore_index=True)

# === 5. SALVAR RESULTADOS ===
evasao_validos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_valida_2020_2024.csv"),
					  sep=";", index=False, encoding="utf-8")
evasao_invalidos.to_csv(os.path.join(BASE_DIR, "municipios_evasao_invalida_2020_2024.csv"),
						sep=";", index=False, encoding="utf-8")
evasao_agregada.to_csv(os.path.join(BASE_DIR, "evasao_uf_e_brasil_2020_2024.csv"),
					   sep=";", index=False, encoding="utf-8")

print("Arquivos salvos:")
print(f"  - Municípios válidos: {len(evasao_validos)}")
print(f"  - Municípios inválidos: {len(evasao_invalidos)}")
print(f"  - Agregado UF + Brasil: {len(evasao_agregada)} linhas")
