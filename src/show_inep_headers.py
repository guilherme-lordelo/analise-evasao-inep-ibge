import pandas as pd
from pathlib import Path

INPUT_FILE = Path("C:/Users/guilh/OneDrive/Desktop/IFBA/TCC/microdados_censo_da_educacao_superior_2024/dados/MICRODADOS_CADASTRO_CURSOS_2024.CSV")

# Ler só a primeira linha para ver os headers
df_header = pd.read_csv(INPUT_FILE, sep=";", nrows=0, encoding="latin1")
print(df_header.columns.tolist())
