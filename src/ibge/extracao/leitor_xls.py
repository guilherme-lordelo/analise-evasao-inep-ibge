import os
import pandas as pd
from utils.paths import RAW_IBGE_XLS, OUT_IBGE_CSV
from ibge.extracao.processador_tabelas import processar_tabela

def extrair_ibge():
	os.makedirs(OUT_IBGE_CSV, exist_ok=True)

	for file in sorted(os.listdir(RAW_IBGE_XLS)):
		if not file.endswith(".xls"):
			continue

		path = os.path.join(RAW_IBGE_XLS, file)

		try:
			print(f"Lendo {file} ...")
			xls = pd.ExcelFile(path)

			for sheet_name in xls.sheet_names:
				print(f"  Extraindo sheet: {sheet_name}")
				df = processar_tabela(path, sheet_name)

				out_name = f"{sheet_name}.csv"
				out_path = os.path.join(OUT_IBGE_CSV, out_name)

				df.to_csv(out_path, index=False, sep=";")
				print(f"    {out_name} salvo com {len(df)} linhas.")

		except Exception as e:
			print(f"Erro em {file}: {e}")
