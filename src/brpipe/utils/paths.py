from pathlib import Path

from brpipe.inep.config import ARQUIVOS, ANOS
from brpipe.ibge.config import NOME_FINAL_MUNICIPIOS, NOME_FINAL_ESTADOS, NOME_FINAL_NACIONAL


ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data"


# Fontes originais
RAW_INEP = DATA_DIR / "RAW" / "INEP"
RAW_IBGE = DATA_DIR / "RAW" / "IBGE"


# Resultados intermediários
INEP_REDUZIDO = DATA_DIR / "INTERIM" / "INEP"
IBGE_REDUZIDO = DATA_DIR / "INTERIM" / "IBGE"


# Resultados processados
INEP_TRANSFORMACOES = DATA_DIR / "PROCESSED" / "INEP"
PROCESSED_IBGE = DATA_DIR / "PROCESSED" / "IBGE"


# Shapefiles
DATA_SHAPEFILES = DATA_DIR / "SHAPEFILES"


_NOME_MUNICIPAL = ARQUIVOS.transformacao_niveis[0]
_NOME_ESTADUAL = ARQUIVOS.transformacao_niveis[1]
_NOME_NACIONAL = ARQUIVOS.transformacao_niveis[2]


_ano_ini = min(ANOS)
_ano_fim = max(ANOS)


# Resultados INEP
inep_municipal = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS.transformacao_prefixo_out}"
	  f"{_NOME_MUNICIPAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS.transformacao_ext_out}"
)

inep_estadual = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS.transformacao_prefixo_out}"
	  f"{_NOME_ESTADUAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS.transformacao_ext_out}"
)

inep_nacional = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS.transformacao_prefixo_out}"
	  f"{_NOME_NACIONAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS.transformacao_ext_out}"
)

# Resultado IBGE
ibge_municipio = PROCESSED_IBGE / NOME_FINAL_MUNICIPIOS
ibge_estadual = PROCESSED_IBGE / NOME_FINAL_ESTADOS
ibge_nacional = PROCESSED_IBGE / NOME_FINAL_NACIONAL

# Visualizações
MAPAS_RENDER = DATA_DIR / "rendered" / "mapas"
CHARTS_RENDER = DATA_DIR / "rendered" / "charts"