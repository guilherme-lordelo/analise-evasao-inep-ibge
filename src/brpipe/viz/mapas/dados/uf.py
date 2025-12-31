import pandas as pd
from brpipe.viz.mapas.config import VARIAVEIS
from brpipe.utils.paths import INEP_TRANSFORMACOES
from brpipe.viz.mapas.config import DADOS
from brpipe.viz.mapas.dados.normalizar import normalizar_metrica_long


def carregar_uf_raw() -> pd.DataFrame:
	path = INEP_TRANSFORMACOES / DADOS.arquivos.uf
	return pd.read_csv(path, sep=DADOS.separador)

def normalizar_uf(df: pd.DataFrame):
	return df.rename(columns={
		VARIAVEIS.territoriais["uf"]: "uf",
		VARIAVEIS.coluna_ano: "ano",
	})

def carregar_metrica_uf() -> pd.DataFrame:
	df = carregar_uf_raw()

	if DADOS.formato == "long":
		cfg = DADOS.metrica_principal.long

		return normalizar_metrica_long(
			df,
			coluna_territorio=VARIAVEIS.territoriais["uf"],
			coluna_uf=None,
			coluna_ano=VARIAVEIS.coluna_ano,
			anos=cfg.anos,
		)

	raise NotImplementedError("Formato wide não implementado")
