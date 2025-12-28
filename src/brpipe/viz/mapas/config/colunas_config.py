from dataclasses import dataclass

@dataclass(frozen=True)
class MunicipioColunasConfig:
    malha: str
    tabela: str
    uf: str

@dataclass(frozen=True)
class TerritoriaisConfig:
    municipio: MunicipioColunasConfig

@dataclass(frozen=True)
class ColunasConfig:
    territoriais: TerritoriaisConfig
