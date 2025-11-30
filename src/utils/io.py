import pandas as pd
from pathlib import Path

from inep.config import (
    ENCODING_IN, SEP_IN, CHUNKSIZE,
    ENCODING_OUT, SEP_OUT, COMPRESS, COLUMNS_ORDER
)
from utils.paths import AGREGACOES


# ---------------------------------------------------
# Determina se path é saída final
# ---------------------------------------------------
def _is_final_output(path: Path) -> bool:
    """
    Retorna True se o arquivo pertence ao diretório AGREGACOES,
    o que significa uso das configurações de saída.
    """
    try:
        return AGREGACOES in Path(path).resolve().parents
    except RuntimeError:
        return False


# ---------------------------------------------------
# Leitura CSV
# ---------------------------------------------------
def read_csv(path, **kwargs):
    kwargs.setdefault("sep", SEP_IN)
    kwargs.setdefault("encoding", ENCODING_IN)
    kwargs.setdefault("low_memory", False)

    return pd.read_csv(path, **kwargs)


# ---------------------------------------------------
# Leitura CSV em chunks
# ---------------------------------------------------
def read_csv_chunks(path, **kwargs):
    kwargs.setdefault("sep", SEP_IN)
    kwargs.setdefault("encoding", ENCODING_IN)
    kwargs.setdefault("low_memory", False)
    kwargs.setdefault("chunksize", CHUNKSIZE)

    return pd.read_csv(path, **kwargs)


# ---------------------------------------------------
# Leitura de header
# ---------------------------------------------------
def read_header(path, sep=SEP_IN, encoding=ENCODING_IN):
    with open(path, "r", encoding=encoding) as f:
        return f.readline().rstrip("\n").split(sep)


# ---------------------------------------------------
# Escrita CSV
# ---------------------------------------------------
def write_csv(df, path, **kwargs):
    path = Path(path)

    # Cria diretório automaticamente
    path.parent.mkdir(parents=True, exist_ok=True)

    # Determina se deve usar configs de saída
    is_final = _is_final_output(path)

    if is_final:
        # --- Saída final (aggregations) ---
        kwargs.setdefault("sep", SEP_OUT)
        kwargs.setdefault("encoding", ENCODING_OUT)
        kwargs.setdefault("index", False)

        # Ordenar colunas, se configurado
        if COLUMNS_ORDER:
            cols = [c for c in COLUMNS_ORDER if c in df.columns]
            df = df[cols]

        # Compressão opcional
        if COMPRESS:
            path = path.with_suffix(path.suffix + ".gz")
            kwargs.setdefault("compression", "gzip")

    else:
        # --- Escrita intermediária ---
        kwargs.setdefault("index", False)
        kwargs.setdefault("sep", SEP_IN)
        kwargs.setdefault("encoding", ENCODING_IN)

    df.to_csv(path, **kwargs)
