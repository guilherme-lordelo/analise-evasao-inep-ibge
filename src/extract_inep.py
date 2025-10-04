import os
import pandas as pd

# Arquivos
INPUT_FILE = os.path.join("data", "raw", "MICRODADOS_CADASTRO_CURSOS_2024.CSV")
OUTPUT_FILE = os.path.join("data", "processed", "inep_reduzido.csv")

# Colunas de interesse (baseado no dicionário + primeira linha do CSV)
COLS = [
    "NU_ANO_CENSO",
    "NO_REGIAO",
    "CO_REGIAO",
    "NO_UF",
    "SG_UF",
    "CO_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "IN_CAPITAL",
    "TP_ORGANIZACAO_ACADEMICA",
    "TP_REDE",
    "TP_CATEGORIA_ADMINISTRATIVA",
    "IN_COMUNITARIA",
    "IN_CONFESSIONAL",
    "CO_IES",
    "NO_CURSO",
    "QT_CURSO",
    "QT_INSCRITO_TOTAL",
    "QT_MAT",
    "QT_DOC_TOTAL"
]

CHUNK_SIZE = 100000  # ajusta se quiser menor/grande

def main():
    print(f"Reading INEP CSV in chunks: {INPUT_FILE}")

    dfs = []
    for i, chunk in enumerate(pd.read_csv(
        INPUT_FILE,
        sep=";",              # CSV do INEP usa ";"
        encoding="latin1",    # encoding comum nos microdados
        chunksize=CHUNK_SIZE,
        low_memory=False
    )):
        # Remove espaços extras nos nomes das colunas
        chunk.columns = chunk.columns.str.strip()

        # Seleciona só colunas que realmente existem no CSV
        cols_existing = [c for c in COLS if c in chunk.columns]
        df_chunk = chunk[cols_existing]

        dfs.append(df_chunk)
        print(f"Chunk {i+1} processed ({len(df_chunk)} rows).")

    # Concatena tudo em um dataframe final
    df_final = pd.concat(dfs, ignore_index=True)

    # Salva em CSV reduzido
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False, sep=";", encoding="utf-8-sig")

    print(f"Done! Reduced file saved at: {OUTPUT_FILE}")
    print(f"Final shape: {df_final.shape}")

if __name__ == "__main__":
    main()
