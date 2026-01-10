from enum import Enum
from dataclasses import dataclass

class FormaColuna(Enum):
	CRUA = "crua"
	SIMPLES = "simples"
	COMPLETA = "completa"


@dataclass
class ColunaEditavel:
	nome: str
	formato: str = "CONTAGEM"
	coluna_peso: str | None = None
	forma: FormaColuna = FormaColuna.CRUA
