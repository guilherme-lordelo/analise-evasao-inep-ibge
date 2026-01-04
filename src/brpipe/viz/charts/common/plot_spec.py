from dataclasses import dataclass

@dataclass(frozen=True)
class PlotSpecBase:
	nome: str
	nivel: str
