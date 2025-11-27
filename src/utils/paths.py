from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Diretório geral de dados
DATA_DIR = ROOT / "data"

# Subpastas
DATA_RAW = DATA_DIR / "raw"
DATA_INTERIM = DATA_DIR / "interim"
DATA_PROCESSED = DATA_DIR / "processed"
DATA_SHAPEFILES = DATA_DIR / "shapefiles"

# Caminhos específicos usados anteriormente
RAW_IBGE_XLS = DATA_RAW / "ibge_xls"
OUT_IBGE_CSV = DATA_INTERIM / "ibge_csv"
