import pandas as pd
from pathlib import Path

from utils.paths import RAW_IBGE, IBGE_REDUZIDO
from utils.io import write_csv

from ibge.config import TABELAS_IBGE


def extrair_ibge():
    """
    Extrai arquivos XLS do IBGE
    """

    for tabela in TABELAS_IBGE.values():

        path_xls = Path(RAW_IBGE) / tabela.arquivo_xls

        if not path_xls.exists():
            print(f"Arquivo XLS não encontrado: {path_xls}")
            continue

        print(f"\n=== Extraindo {tabela.arquivo_xls} ===")

        try:
            xls = pd.ExcelFile(path_xls)
        except Exception as e:
            print(f"Erro ao abrir {tabela.arquivo_xls}: {e}")
            continue

        for idx, sheet in enumerate(tabela.sheets):

            nome_csv_interim = sheet.arquivo.replace(".csv", "_interim.csv")
            out_path = Path(IBGE_REDUZIDO) / nome_csv_interim

            sheet_name = idx

            try:
                df = pd.read_excel(
                    xls,
                    sheet_name=sheet_name,
                    header=None
                )
            except Exception as e:
                print(
                    f"Falha ao ler sheet '{sheet.sheet_id}' "
                    f"(índice {sheet_name}) em {tabela.arquivo_xls}: {e}"
                )
                continue

            write_csv(df, out_path)

            print(
                f"{nome_csv_interim} salvo "
                f"({len(df)} linhas)."
            )
