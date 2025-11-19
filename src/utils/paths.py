from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"

RAW_IBGE_XLS = "data/raw/ibge_xls"
OUT_IBGE_CSV = "data/interim/ibge_csv"