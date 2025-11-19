import pandas as pd
from inep.extracao.config import SEP, ENCODING, CHUNKSIZE


def ler_em_chunks(path, colunas):
    chunks = pd.read_csv(
        path,
        sep=SEP,
        usecols=colunas,
        encoding=ENCODING,
        low_memory=False,
        chunksize=CHUNKSIZE,
    )

    df_list = []
    total = 0

    for i, chunk in enumerate(chunks, start=1):
        df_list.append(chunk)
        total += len(chunk)
        print(f"  → Chunk {i} lido ({len(chunk):,} linhas, total: {total:,})")

    return pd.concat(df_list, ignore_index=True)
