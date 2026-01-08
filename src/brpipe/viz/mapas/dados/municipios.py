import pandas as pd
from brpipe.utils.io import read_csv
from brpipe.utils.paths import inep_municipal
from brpipe.viz.mapas.config import VARIAVEIS, ANOS
from brpipe.viz.mapas.dados.normalizar import normalizar_metrica_long

def carregar_metrica_municipios() -> pd.DataFrame:
	df = read_csv(inep_municipal)

	return normalizar_metrica_long(
		df,
		coluna_territorio=VARIAVEIS.territoriais["municipio"],
		coluna_uf=VARIAVEIS.territoriais["uf"],
		coluna_ano=VARIAVEIS.coluna_ano,
		anos=ANOS,
	)
