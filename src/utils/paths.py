from pathlib import Path
from inep.config import (TRANSFORMACAO_EXT_OUT, TRANSFORMACAO_PREFIXO_OUT, TRANSFORMACAO_NIVEIS, ANOS)

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"

# Fontes originais
RAW_INEP = DATA_DIR / "raw" / "inep_micros"      # arquivos CSV originais
RAW_IBGE = DATA_DIR / "raw" / "ibge_xls"         # xls originais

# Resultados intermediários
INEP_REDUZIDO = DATA_DIR / "interim" / "inep_reduzido"    # INEP pós extração
IBGE_REDUZIDO = DATA_DIR / "interim" / "ibge_csv"         # IBGE convertido p/ CSV

# Resultados processados
INEP_TRANSFORMACOES = DATA_DIR / "processed" / "inep_integracoes"
PROCESSED_IBGE = DATA_DIR / "processed" / "ibge_limpo"

# Shapefiles
DATA_SHAPEFILES = DATA_DIR / "shapefiles"

_NOME_MUNICIPAL = TRANSFORMACAO_NIVEIS[0]
_NOME_ESTADUAL = TRANSFORMACAO_NIVEIS[1]
_NOME_NACIONAL = TRANSFORMACAO_NIVEIS[2]

# Resultados
arquivo_municipal = INEP_TRANSFORMACOES / f"{TRANSFORMACAO_PREFIXO_OUT}{_NOME_MUNICIPAL}{min(ANOS)}_{max(ANOS)}{TRANSFORMACAO_EXT_OUT}"
arquivo_estadual = INEP_TRANSFORMACOES / f"{TRANSFORMACAO_PREFIXO_OUT}{_NOME_ESTADUAL}{min(ANOS)}_{max(ANOS)}{TRANSFORMACAO_EXT_OUT}"
arquivo_nacional = INEP_TRANSFORMACOES / f"{TRANSFORMACAO_PREFIXO_OUT}{_NOME_NACIONAL}{min(ANOS)}_{max(ANOS)}{TRANSFORMACAO_EXT_OUT}"