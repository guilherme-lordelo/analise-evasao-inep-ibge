# src/inep/checkpoints.py

from pathlib import Path
import pandas as pd

from utils.io import write_csv
from inep.config import IO


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
