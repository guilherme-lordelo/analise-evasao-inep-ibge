import pandas as pd
from brpipe.utils.io import read_csv_chunks

def ler_em_chunks(path, colunas):
    chunks = read_csv_chunks(path, usecols=colunas)

    df_list = []
    total = 0

    for i, chunk in enumerate(chunks, start=1):
        df_list.append(chunk)
        total += len(chunk)
        print(f"  → Chunk {i} lido ({len(chunk):,} linhas, total: {total:,})")

    return pd.concat(df_list, ignore_index=True)
