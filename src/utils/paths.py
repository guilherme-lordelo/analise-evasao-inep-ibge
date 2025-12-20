from pathlib import Path

from inep.config import ARQUIVOS_CONFIG, ANOS


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


# Fontes originais
RAW_INEP = DATA_DIR / "raw" / "inep_micros"
RAW_IBGE = DATA_DIR / "raw" / "ibge_xls"


# Resultados intermediários
INEP_REDUZIDO = DATA_DIR / "interim" / "inep_reduzido"
IBGE_REDUZIDO = DATA_DIR / "interim" / "ibge_csv"


# Resultados processados
INEP_TRANSFORMACOES = DATA_DIR / "processed" / "inep_integracoes"
PROCESSED_IBGE = DATA_DIR / "processed" / "ibge_limpo"


# Shapefiles
DATA_SHAPEFILES = DATA_DIR / "shapefiles"


_NOME_MUNICIPAL = ARQUIVOS_CONFIG.transformacao_niveis[0]
_NOME_ESTADUAL = ARQUIVOS_CONFIG.transformacao_niveis[1]
_NOME_NACIONAL = ARQUIVOS_CONFIG.transformacao_niveis[2]


_ano_ini = min(ANOS)
_ano_fim = max(ANOS)


# Resultados
arquivo_municipal = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS_CONFIG.transformacao_prefixo_out}"
	  f"{_NOME_MUNICIPAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS_CONFIG.transformacao_ext_out}"
)

arquivo_estadual = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS_CONFIG.transformacao_prefixo_out}"
	  f"{_NOME_ESTADUAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS_CONFIG.transformacao_ext_out}"
)

arquivo_nacional = (
	INEP_TRANSFORMACOES
	/ f"{ARQUIVOS_CONFIG.transformacao_prefixo_out}"
	  f"{_NOME_NACIONAL}{_ano_ini}_{_ano_fim}"
	  f"{ARQUIVOS_CONFIG.transformacao_ext_out}"
)
