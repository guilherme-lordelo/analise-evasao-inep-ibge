import pandas as pd
import os
import re

RAW_DIR = "data/raw/ibge_xls"
OUTPUT_DIR = "data/interim/ibge_csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def limpar_header(df):
	# Remove linhas vazias iniciais
	df = df.dropna(how='all').reset_index(drop=True)
	
	# Detecta onde está o cabeçalho (linha com "Código" ou "Município")
	header_candidates = df[df.iloc[:, 0].astype(str).str.contains("Código", case=False, na=False)].index
	if len(header_candidates) == 0:
		raise ValueError("Não foi encontrada linha de cabeçalho ('Código do Município').")
	
	header_row = header_candidates[0]
	df.columns = df.iloc[header_row]
	df = df.iloc[header_row + 1:].reset_index(drop=True)
	
	return df

def padronizar_colunas(df):
	df.columns = (
		df.columns.astype(str)
		.str.strip()
		.str.replace(r"\s+", "_", regex=True)
		.str.replace("Código_do_município", "CO_MUNICIPIO", case=False)
		.str.replace("Código_do_Município", "CO_MUNICIPIO", case=False)
		.str.replace("Sigla_da_Unidade_da_Federação", "SG_UF", case=False)
	)
	return df

def limpar_linhas(df):
	# Remove linhas agregadas ("Brasil", "Região", "Total", etc.)
	if "CO_MUNICIPIO" in df.columns:
		df = df[~df["CO_MUNICIPIO"].astype(str).str.contains("Brasil|Região|Total", case=False, na=False)]
	return df

def processar_tabela(path, sheet_name):
	df = pd.read_excel(path, sheet_name=sheet_name, header=None)
	df = limpar_header(df)
	df = padronizar_colunas(df)
	df = limpar_linhas(df)
	return df

def main():
	for file in sorted(os.listdir(RAW_DIR)):
		if not file.endswith(".xls"):
			continue

		path = os.path.join(RAW_DIR, file)
		try:
			print(f"Lendo {file} ...")
			xls = pd.ExcelFile(path)
			
			for sheet_name in xls.sheet_names:
				print(f"  Extraindo sheet: {sheet_name}")
				df = processar_tabela(path, sheet_name)
				
				# Usa o nome do sheet diretamente
				out_name = f"{sheet_name}.csv"
				out_path = os.path.join(OUTPUT_DIR, out_name)
				
				df.to_csv(out_path, index=False, sep=";")
				print(f"    {out_name} salvo com {len(df)} linhas.")
				
		except Exception as e:
			print(f"Erro em {file}: {e}")

if __name__ == "__main__":
	main()
