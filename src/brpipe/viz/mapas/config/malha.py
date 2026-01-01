from dataclasses import dataclass

@dataclass(frozen=True)
class MalhaConfig:
    municipio: str
    uf: str
