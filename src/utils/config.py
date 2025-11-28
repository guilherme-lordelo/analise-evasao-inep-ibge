# src/utils/config.py
import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"

def load_config(name: str):
    """Carrega um arquivo YML qualquer, ex: load_config('inep')"""
    path = CONFIG_DIR / f"{name}.yml"
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
