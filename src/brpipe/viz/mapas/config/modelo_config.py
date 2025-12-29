# src/brpipe/viz/mapas/modelo/dado_config.py
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class FiltroConfig:
    tipo: str
    valores: Any  # auto | lista | range

    @classmethod
    def from_dict(cls, d: dict) -> "FiltroConfig":
        return cls(
            tipo=d["tipo"],
            valores=d.get("valores", "auto"),
        )

@dataclass(frozen=True)
class FiltrosConfig:
    filtros: Dict[str, FiltroConfig]

    @classmethod
    def from_dict(cls, d: dict) -> "FiltrosConfig":
        filtros = {
            nome: FiltroConfig.from_dict(cfg)
            for nome, cfg in d.items()
        }
        return cls(filtros=filtros)

@dataclass(frozen=True)
class VisaoTerritorialConfig:
    chave_merge: str

    @classmethod
    def from_dict(cls, d: dict) -> "VisaoTerritorialConfig":
        return cls(
            chave_merge=d["chave_merge"]
        )

@dataclass(frozen=True)
class VisoesConfig:
    territoriais: Dict[str, VisaoTerritorialConfig]

    @classmethod
    def from_dict(cls, d: dict) -> "VisoesConfig":
        territoriais = {
            nome: VisaoTerritorialConfig.from_dict(cfg)
            for nome, cfg in d.get("territoriais", {}).items()
        }
        return cls(territoriais=territoriais)

@dataclass(frozen=True)
class DadosConfig:
    granularidade: str
    dimensoes: List[str]
    coluna_valor: str
    agregacao_padrao: str

    @classmethod
    def from_dict(cls, d: dict) -> "DadosConfig":
        return cls(
            granularidade=d["granularidade"],
            dimensoes=list(d.get("dimensoes", [])),
            coluna_valor=d["coluna_valor"],
            agregacao_padrao=d.get("agregacao_padrao", "mean"),
        )

@dataclass(frozen=True)
class ModeloConfig:
    dados: Dict[str, DadosConfig]
    visoes: Optional[VisoesConfig]
    filtros: Optional[FiltrosConfig]

    @classmethod
    def from_dict(cls, d: dict) -> "ModeloConfig":
        dados = {
            nome: DadosConfig.from_dict(cfg)
            for nome, cfg in d.get("dados", {}).items()
        }

        visoes = None
        if "visoes" in d:
            visoes = VisoesConfig.from_dict(d["visoes"])

        filtros = None
        if "filtros" in d:
            filtros = FiltrosConfig.from_dict(d["filtros"])

        return cls(
            dados=dados,
            visoes=visoes,
            filtros=filtros,
        )
