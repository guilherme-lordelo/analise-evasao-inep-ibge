from inep.config import IO_CONFIG


def csv_kwargs_saida(df):
	kwargs = {
		"sep": IO_CONFIG.sep_out,
		"encoding": IO_CONFIG.encoding_out,
		"index": False,
	}

	if IO_CONFIG.ordem_colunas:
		cols = [c for c in IO_CONFIG.ordem_colunas if c in df.columns]
		df = df[cols]

	if IO_CONFIG.compress:
		kwargs["compression"] = "gzip"

	return df, kwargs
