from brpipe.inep.config import IO


def csv_kwargs_saida(df):
	kwargs = {
		"sep": IO.sep_out,
		"encoding": IO.encoding_out,
		"index": False,
	}

	return df, kwargs
