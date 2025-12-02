# src/ibge/config.py

from utils.config import load_config
from utils.colunas_base import get_colunas_municipio

_cfg = load_config("ibge")

# ====================================================================
# COLUNAS BASE DO IBGE
# ====================================================================
COLUNAS_BASE_IBGE = get_colunas_municipio(include_nome=True)

# ====================================================================
# CARREGA TABELAS + SHEETS A PARTIR DO YAML
# ====================================================================

SHEETS_IBGE = {}   # { "tab1": {arquivo_xls, sheets:[...]}, ... }

tabelas_cfg = _cfg.get("tabelas", {})

for tabela_id, tabela_info in tabelas_cfg.items():

    tabela_expandida = {
        "arquivo_xls": f"{tabela_id}.xls",     # RAW IBGE file
        "sheets": []                           # lista de dicts
    }

    for sheet in tabela_info.get("sheets", []):
        tabela_expandida["sheets"].append({
            "sheet_id": sheet.get("sheet_id"),
            "arquivo": sheet["arquivo"],
            "colunas": sheet.get("colunas", []),
        })

    SHEETS_IBGE[tabela_id] = tabela_expandida


# ====================================================================
# Funções utilitárias
# ====================================================================

def get_colunas_base():
    return COLUNAS_BASE_IBGE

def get_tabela_info(tabela_id):
    return SHEETS_IBGE[tabela_id]

def get_sheets(tabela_id):
    return SHEETS_IBGE[tabela_id]["sheets"]

def get_arquivo_xls(tabela_id):
    return SHEETS_IBGE[tabela_id]["arquivo_xls"]
