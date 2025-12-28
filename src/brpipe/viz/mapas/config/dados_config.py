# src/brpipe/viz/mapas/config/dados_config.py

from dataclasses import dataclass
from typing import Optional, Literal

@dataclass(frozen=True)
class MetricaLongConfig:
    coluna_ano: str
    coluna_valor: str
    agregacao: str = "mean"
    anos: Optional[list[int]] = None

@dataclass(frozen=True)
class MetricaWideConfig:
    coluna_valor: str

@dataclass(frozen=True)
class MetricaConfig:
    coluna_mapa: str
    wide: Optional[MetricaWideConfig] = None
    long: Optional[MetricaLongConfig] = None

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ArquivosDadosConfig:
    municipio: str
    uf: str
    nacional: Optional[str] = None

from typing import Literal

@dataclass(frozen=True)
class DadosConfig:
    formato: Literal["wide", "long"]
    separador: str
    arquivos: ArquivosDadosConfig
    metrica_principal: MetricaConfig
