from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class MergeColunasConfig:
    destino: str
    fontes: List[str]
    metodo: str  # "soma", "media", etc.

@dataclass(frozen=True)
class SheetIBGEConfig:
    sheet_id: str
    descricao: str
    arquivo: str

    colunas_especificas: List[str]

    merges_colunas: Optional[List[MergeColunasConfig]] = None

@dataclass(frozen=True)
class TabelaIBGEConfig:
    tabela_id: str
    descricao: str
    arquivo_xls: str

    sheets: List[SheetIBGEConfig]

def carregar_tabelas_ibge(_cfg: dict) -> dict[str, TabelaIBGEConfig]:

    tabelas = {}

    for tabela_id, info in _cfg.get("tabelas", {}).items():

        sheets = []

        for sheet in info.get("sheets", []):

            merges = None
            if "merges_colunas" in sheet:
                merges = [
                    MergeColunasConfig(
                        destino=m["destino"],
                        fontes=m["fontes"],
                        metodo=m.get("metodo", "soma")
                    )
                    for m in sheet["merges_colunas"]
                ]

            sheets.append(
                SheetIBGEConfig(
                    sheet_id=sheet.get("sheet_id", ""),
                    descricao=sheet.get("descricao_sheet", ""),
                    arquivo=sheet["arquivo"],
                    colunas_especificas=sheet.get("colunas", []),
                    merges_colunas=merges
                )
            )

        tabelas[tabela_id] = TabelaIBGEConfig(
            tabela_id=tabela_id,
            descricao=info.get("descricao_tabela", ""),
            arquivo_xls=f"{tabela_id}.xls",
            sheets=sheets
        )

    return tabelas
