from utils.paths import DATA_PROCESSED
from utils.io import read_csv, write_csv

from ibge.leitura_tabelas_finais import ler_tabelas_ibge
import pandas as pd

BASE_DIR = DATA_PROCESSED
EVASAO_DIR = DATA_PROCESSED

# 1. LER EVASÃO
validos = read_csv(BASE_DIR / "municipios_evasao_valida_2020_2024.csv", sep=";")
invalidos = read_csv(BASE_DIR / "municipios_evasao_invalida_2020_2024.csv", sep=";")

# 2. LER IBGE
ibge_all = ler_tabelas_ibge()

# 3. LER INFORMAÇÕES DO ÚLTIMO ANO
ult_df = read_csv(EVASAO_DIR / "evasao_2023_2024.csv", sep=";")
info_df = ult_df[["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"]].drop_duplicates()

ibge_all = pd.merge(info_df, ibge_all, on="CO_MUNICIPIO", how="left")

# 4. MERGE FINAL
final_validos = pd.merge(validos, ibge_all, on="CO_MUNICIPIO", how="left")
final_invalidos = pd.merge(invalidos, ibge_all, on="CO_MUNICIPIO", how="left")

# 5. SALVAR
write_csv(final_validos, BASE_DIR / "municipios_evasao_valida_ibge_2020_2024.csv", sep=";")
write_csv(final_invalidos, BASE_DIR / "municipios_evasao_invalida_ibge_2020_2024.csv", sep=";")

print("Merge com IBGE concluído")
