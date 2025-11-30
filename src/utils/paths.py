from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"

# Fontes originais
RAW_INEP = DATA_DIR / "raw" / "inep_micros"      # arquivos CSV originais
RAW_IBGE = DATA_DIR / "raw" / "ibge_xls"         # xls originais

# Resultados intermediários
INTERIM_INEP = DATA_DIR / "interim" / "inep_reduzido"    # INEP pós extração
INTERIM_IBGE = DATA_DIR / "interim" / "ibge_csv"         # IBGE convertido p/ CSV

# Resultados processados
PROCESSED_INEP = DATA_DIR / "processed" / "inep_evasao"
PROCESSED_IBGE = DATA_DIR / "processed" / "ibge_limpo"

# Agregações finais
AGREGACOES = DATA_DIR / "processed" / "aggregations"

# Shapefiles
DATA_SHAPEFILES = DATA_DIR / "shapefiles"
