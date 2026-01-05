from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class PlotSpecBase(ABC):
	nome: str
	nivel: str
	coluna_territorial: str | None
	valor_territorial: str | None

	@property
	@abstractmethod
	def variaveis(self) -> list[str]:
		...