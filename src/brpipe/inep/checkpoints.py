# src/inep/checkpoints.py

from pathlib import Path
import pandas as pd

from brpipe.utils.io import write_csv
from brpipe.inep.config import IO


def salvar_checkpoint(
	df: pd.DataFrame,
	*,
	output_path: Path,
) -> None:
	"""
	Persiste um dataframe intermediário.
	"""

	write_csv(
		df,
		output_path,
		encoding=IO.encoding_out,
		sep=IO.sep_out,
		compression=IO.compress,
	)

def carregar_checkpoint(
    input_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        input_path,
        encoding=IO.encoding_out,
        sep=IO.sep_out,
        low_memory=False,
    )