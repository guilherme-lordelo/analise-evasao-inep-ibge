import pandas as pd
from pathlib import Path

from brpipe.inep.config import IO


# Leitura CSV
def read_csv(path, **kwargs):
	kwargs.setdefault("sep", IO.sep_in)
	kwargs.setdefault("encoding", IO.encoding_in)
	kwargs.setdefault("low_memory", False)

	return pd.read_csv(path, **kwargs)


# Leitura CSV em chunks
def read_csv_chunks(path, **kwargs):
	kwargs.setdefault("sep", IO.sep_in)
	kwargs.setdefault("encoding", IO.encoding_in)
	kwargs.setdefault("low_memory", False)
	kwargs.setdefault("chunksize", IO.chunksize)

	return pd.read_csv(path, **kwargs)


# Leitura do cabeçalho
def read_header(path, sep=None, encoding=None):
	sep = sep or IO.sep_in
	encoding = encoding or IO.encoding_in

	with open(path, "r", encoding=encoding) as f:
		return f.readline().rstrip("\n").split(sep)


# Escrita CSV
def write_csv(df: pd.DataFrame, path, **kwargs):
	path = Path(path)
	path.parent.mkdir(parents=True, exist_ok=True)

	kwargs.setdefault("index", False)
	kwargs.setdefault("sep", IO.sep_out)
	kwargs.setdefault("encoding", IO.encoding_out)

	df.to_csv(path, **kwargs)
