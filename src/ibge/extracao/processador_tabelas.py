import pandas as pd

def limpar_header(df):
	df = df.dropna(how='all').reset_index(drop=True)

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
	if "CO_MUNICIPIO" in df.columns:
		df = df[~df["CO_MUNICIPIO"].astype(str).str.contains("Brasil|Região|Total", case=False, na=False)]
	return df

def processar_tabela(path, sheet_name):
	df = pd.read_excel(path, sheet_name=sheet_name, header=None)
	df = limpar_header(df)
	df = padronizar_colunas(df)
	df = limpar_linhas(df)
	return df
