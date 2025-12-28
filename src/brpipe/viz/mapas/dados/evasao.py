import pandas as pd
from brpipe.utils.paths import INEP_TRANSFORMACOES
from brpipe.viz.mapas.config.config import arquivo_evasao

def carregar_evasao_municipios() -> pd.DataFrame:
    path = INEP_TRANSFORMACOES / arquivo_evasao()
    return pd.read_csv(path, sep=";")
