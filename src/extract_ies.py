# src/extract_ies.py
"""
Extrai colunas relevantes da base INEP de IES (Instituições de Ensino Superior)
para posterior cruzamento com os cursos.
Entrada: data/raw/MICRODADOS_CADASTRO_IES_2024.CSV
Saída:   data/processed/ies_reduzido.csv
"""

import pandas as pd
from pathlib import Path

# Caminhos
INPUT_FILE = Path("data/raw/MICRODADOS_ED_SUP_IES_2024.CSV")
OUTPUT_FILE = Path("data/processed/ies_reduzido.csv")

# Colunas de interesse
COLS_TO_KEEP = [
    "NU_ANO_CENSO",
    "CO_IES",
    "NO_IES",
    "SG_IES",
    "CO_MANTENEDORA",
    "NO_MANTENEDORA",
    "NO_REGIAO_IES",
    "CO_REGIAO_IES",
    "NO_UF_IES",
    "SG_UF_IES",
    "CO_UF_IES",
    "NO_MUNICIPIO_IES",
    "CO_MUNICIPIO_IES",
    "IN_CAPITAL_IES",
]

def main():
    print(f"Lendo IES CSV: {INPUT_FILE}")

    # Leitura em chunks para economizar memória
    chunks = pd.read_csv(
        INPUT_FILE,
        sep=";",
        usecols=COLS_TO_KEEP,
        dtype=str,
        encoding="latin1",
        chunksize=50_000
    )

    # Concatenar todos os chunks
    df = pd.concat(chunks, ignore_index=True)

    print(f"Linhas carregadas: {len(df)}")

    # Salvar versão reduzida
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8-sig")

    print(f"Arquivo salvo em: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
