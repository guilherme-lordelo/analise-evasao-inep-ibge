import pandas as pd
from brpipe.utils.paths import INEP_TRANSFORMACOES
from brpipe.viz.mapas.config import DADOS
from brpipe.viz.mapas.config import VARIAVEIS
from brpipe.viz.mapas.dados.normalizar import normalizar_metrica_long

def carregar_municipios_raw() -> pd.DataFrame:
	path = INEP_TRANSFORMACOES / DADOS.arquivos.municipio
	return pd.read_csv(path, sep=DADOS.separador)


def carregar_metrica_municipios() -> pd.DataFrame:
	df = carregar_municipios_raw()

	if DADOS.formato == "long":
		cfg = DADOS.metrica_principal.long

		return normalizar_metrica_long(
			df,
			coluna_territorio=VARIAVEIS.territoriais["municipio"],
			coluna_uf=VARIAVEIS.territoriais["uf"],
			coluna_ano=VARIAVEIS.coluna_ano,
			anos=cfg.anos,
		)

	raise NotImplementedError("Formato wide não implementado")
