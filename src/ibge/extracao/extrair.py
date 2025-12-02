# src/ibge/extracao/extrair.py

import pandas as pd
from pathlib import Path

from utils.paths import RAW_IBGE, INTERIM_IBGE
from utils.io import write_csv
from ibge.config import SHEETS_IBGE


def extrair_ibge():
    """
    Etapa de EXTRAÇÃO do IBGE.

    Para cada tabela (tabX) definida em ibge.yml:
    - Lê o arquivo RAW correspondente (tabX.xls)
    - Extrai as sheets NA ORDEM definida em ibge.yml
    - Salva cada sheet em CSV usando o nome especificado no YAML
    - Não aplica nenhuma limpeza
    """

    for tabela_id, tabela_info in SHEETS_IBGE.items():
        arquivo_xls = tabela_info["arquivo_xls"]
        sheets = tabela_info["sheets"]

        path_xls = Path(RAW_IBGE) / arquivo_xls

        if not path_xls.exists():
            print(f"Arquivo XLS não encontrado: {path_xls}")
            continue

        print(f"\n=== Extraindo {arquivo_xls} ===")

        try:
            xls = pd.ExcelFile(path_xls)
        except Exception as e:
            print(f"Erro ao abrir {arquivo_xls}: {e}")
            continue

        for idx, sheet_info in enumerate(sheets):
            nome_csv = sheet_info["arquivo"]

            # sheet_name = índice da ordem do YAML
            sheet_name = idx

            try:
                df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            except Exception as e:
                print(f"Falha ao ler sheet de índice {sheet_name} ({arquivo_xls}): {e}")
                continue

            out_path = Path(INTERIM_IBGE) / nome_csv

            write_csv(df, out_path)

            print(f"{nome_csv} salvo ({len(df)} linhas).")
