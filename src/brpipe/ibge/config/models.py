from dataclasses import dataclass
from typing import List, Optional

from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.tipos import TipoAgregacao, TipoDado

@dataclass(frozen=True)
class ColunaIBGEConfig:
	nome: str
	tipo_dado: TipoDado
	tipo_agregacao: TipoAgregacao
	tipo_visualizacao: ResultadoTipo
	coluna_peso: str | None = None

@dataclass(frozen=True)
class MergeColunasConfig:
	destino: str
	fontes: list[str]
	metodo: str
	coluna_peso: str | None = None
	peso_merge: list[float] | None = None

@dataclass(frozen=True)
class SheetIBGEConfig:
	sheet_id: Optional[str]
	descricao: str
	arquivo: str
	colunas_especificas: List[ColunaIBGEConfig]
	merges_colunas: Optional[List[MergeColunasConfig]] = None
	remover_colunas: Optional[List[str]] = None

@dataclass(frozen=True)
class TabelaIBGEConfig:
    tabela_id: str
    descricao: str
    arquivo_xls: str

    sheets: List[SheetIBGEConfig]
