from brpipe.utils.iterador import iterar_sheets_ibge
import pandas as pd
from pathlib import Path

from brpipe.utils.paths import RAW_IBGE, IBGE_REDUZIDO
from brpipe.ibge.checkpoints import salvar_checkpoint

from brpipe.ibge.config import TABELAS_IBGE


def extrair_ibge():

	def _extrair_sheet(tabela, sheet, idx):
		path_xls = Path(RAW_IBGE) / tabela.arquivo_xls
		if not path_xls.exists():
			return

		try:
			xls = pd.ExcelFile(path_xls)
			df = pd.read_excel(xls, sheet_name=idx, header=None)
		except Exception:
			return

		nome_csv_interim = sheet.arquivo.replace(".csv", "_interim.csv")
		out_path = Path(IBGE_REDUZIDO) / nome_csv_interim
		salvar_checkpoint(df, output_path=out_path)

	iterar_sheets_ibge(TABELAS_IBGE, _extrair_sheet, incluir_idx=True)
