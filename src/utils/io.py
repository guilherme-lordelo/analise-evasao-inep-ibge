import pandas as pd
from pathlib import Path

from inep.config import IO_CONFIG


# Leitura CSV
def read_csv(path, **kwargs):
	kwargs.setdefault("sep", IO_CONFIG.sep_in)
	kwargs.setdefault("encoding", IO_CONFIG.encoding_in)
	kwargs.setdefault("low_memory", False)

	return pd.read_csv(path, **kwargs)


# Leitura CSV em chunks
def read_csv_chunks(path, **kwargs):
	kwargs.setdefault("sep", IO_CONFIG.sep_in)
	kwargs.setdefault("encoding", IO_CONFIG.encoding_in)
	kwargs.setdefault("low_memory", False)
	kwargs.setdefault("chunksize", IO_CONFIG.chunksize)

	return pd.read_csv(path, **kwargs)


# Leitura do cabeçalho
def read_header(path, sep=None, encoding=None):
	sep = sep or IO_CONFIG.sep_in
	encoding = encoding or IO_CONFIG.encoding_in

	with open(path, "r", encoding=encoding) as f:
		return f.readline().rstrip("\n").split(sep)


# Escrita CSV
def write_csv(df: pd.DataFrame, path, **kwargs):
	path = Path(path)
	path.parent.mkdir(parents=True, exist_ok=True)

	kwargs.setdefault("index", False)
	kwargs.setdefault("sep", IO_CONFIG.sep_out)
	kwargs.setdefault("encoding", IO_CONFIG.encoding_out)

	df.to_csv(path, **kwargs)
