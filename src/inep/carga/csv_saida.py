from inep.config import IO


def csv_kwargs_saida(df):
	kwargs = {
		"sep": IO.sep_out,
		"encoding": IO.encoding_out,
		"index": False,
	}

	if IO.ordem_colunas:
		cols = [c for c in IO.ordem_colunas if c in df.columns]
		df = df[cols]

	if IO.compress:
		kwargs["compression"] = "gzip"

	return df, kwargs
