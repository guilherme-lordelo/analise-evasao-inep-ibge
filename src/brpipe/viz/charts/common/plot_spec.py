from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class PlotSpecBase(ABC):
	nome: str
	nivel: str

	@property
	@abstractmethod
	def variaveis(self) -> list[str]:
		...