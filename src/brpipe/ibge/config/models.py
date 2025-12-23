from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class TransformacaoColunaConfig:
    fonte: str                 # coluna original (ex: PERC_HOMEM)
    destino: str               # novo nome (ex: SEXO_LOGIT)
    tipo: str
    escala_origem: Optional[str] = None

@dataclass(frozen=True)
class MergeColunasConfig:
    destino: str
    fontes: List[str]
    metodo: str  # "soma", "media", etc.


@dataclass(frozen=True)
class SheetIBGEConfig:
    sheet_id: Optional[str]
    descricao: str
    arquivo: str

    colunas_especificas: List[str]

    merges_colunas: Optional[List[MergeColunasConfig]] = None
    transformacoes_colunas: Optional[List[TransformacaoColunaConfig]] = None
    remover_colunas: Optional[List[str]] = None

@dataclass(frozen=True)
class TabelaIBGEConfig:
    tabela_id: str
    descricao: str
    arquivo_xls: str

    sheets: List[SheetIBGEConfig]
