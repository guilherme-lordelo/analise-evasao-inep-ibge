import pandas as pd
from brpipe.utils.io import read_csv
from brpipe.utils.paths import arquivo_estadual
from brpipe.viz.mapas.config import VARIAVEIS, ANOS
from brpipe.viz.mapas.dados.normalizar import normalizar_metrica_long

def carregar_metrica_uf() -> pd.DataFrame:
	df = read_csv(arquivo_estadual)

	return normalizar_metrica_long(
		df,
		coluna_territorio=VARIAVEIS.territoriais["uf"],
		coluna_uf=None,
		coluna_ano=VARIAVEIS.coluna_ano,
		anos=ANOS,
	)

