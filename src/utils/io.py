import pandas as pd
from pathlib import Path

from inep.config import (
    ENCODING_IN, SEP_IN, CHUNKSIZE,
)


# Leitura CSV
def read_csv(path, **kwargs):
    kwargs.setdefault("sep", SEP_IN)
    kwargs.setdefault("encoding", ENCODING_IN)
    kwargs.setdefault("low_memory", False)

    return pd.read_csv(path, **kwargs)


# Leitura CSV em chunks
def read_csv_chunks(path, **kwargs):
    kwargs.setdefault("sep", SEP_IN)
    kwargs.setdefault("encoding", ENCODING_IN)
    kwargs.setdefault("low_memory", False)
    kwargs.setdefault("chunksize", CHUNKSIZE)

    return pd.read_csv(path, **kwargs)


# Leitura do cabeçalho
def read_header(path, sep=SEP_IN, encoding=ENCODING_IN):
    with open(path, "r", encoding=encoding) as f:
        return f.readline().rstrip("\n").split(sep)


# Escrita CSV
def write_csv(df: pd.DataFrame, path, **kwargs):
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    kwargs.setdefault("index", False)
    kwargs.setdefault("sep", SEP_IN)
    kwargs.setdefault("encoding", ENCODING_IN)

    df.to_csv(path, **kwargs)
