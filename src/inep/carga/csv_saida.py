
from inep.config import (
    SEP_OUT, ENCODING_OUT,
    COMPRESS, ORDEM_COLUNAS
)


def csv_kwargs_saida(df):
    kwargs = {
        "sep": SEP_OUT,
        "encoding": ENCODING_OUT,
        "index": False,
    }

    if ORDEM_COLUNAS:
        cols = [c for c in ORDEM_COLUNAS if c in df.columns]
        df = df[cols]

    if COMPRESS:
        kwargs["compression"] = "gzip"

    return df, kwargs
