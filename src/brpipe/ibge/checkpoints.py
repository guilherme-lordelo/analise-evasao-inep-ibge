# src/inep/checkpoints.py

from pathlib import Path
import pandas as pd

from brpipe.utils.io import write_csv
from brpipe.ibge.config import SAIDA_IBGE

ENCODING = SAIDA_IBGE.get("encoding", "utf-8")
SEP_OUT = SAIDA_IBGE.get("sep", ";")

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
		encoding=ENCODING,
		sep=SEP_OUT,
	)

def carregar_checkpoint(
    input_path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        input_path,
        encoding=ENCODING,
        sep=SEP_OUT,
        low_memory=False,
    )